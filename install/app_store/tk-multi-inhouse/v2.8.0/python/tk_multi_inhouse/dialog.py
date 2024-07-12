# Copyright (c) 2017 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.
import os
import traceback
import re

import sgtk
from sgtk.platform.qt import QtCore, QtGui
from tank_vendor import six
import sys

from .api import PublishManager, PublishItem, PublishTask
from .ui.dialog import Ui_Dialog
from .progress import ProgressHandler
from .summary_overlay import SummaryOverlay
from .publish_tree_widget import TreeNodeItem, TreeNodeTask, TopLevelTreeNodeItem

# import frameworks
settings = sgtk.platform.import_framework("tk-framework-shotgunutils", "settings")
help_screen = sgtk.platform.import_framework("tk-framework-qtwidgets", "help_screen")
task_manager = sgtk.platform.import_framework(
    "tk-framework-shotgunutils", "task_manager"
)
shotgun_model = sgtk.platform.import_framework(
    "tk-framework-shotgunutils", "shotgun_model"
)
shotgun_globals = sgtk.platform.import_framework(
    "tk-framework-shotgunutils", "shotgun_globals"
)

logger = sgtk.platform.get_logger(__name__)


class CheckableItem(QtGui.QStandardItem):
    def __init__(self, text=''):
        super().__init__(text)
        self.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        self.setData(QtCore.Qt.Checked, QtCore.Qt.CheckStateRole)


class AppDialog(QtGui.QWidget):
    """
    Main dialog window for the App
    """

    # main drag and drop areas
    (DRAG_SCREEN, PUBLISH_SCREEN) = range(2)

    # details ui panes
    (
        ITEM_DETAILS,
        TASK_DETAILS,
        PLEASE_SELECT_DETAILS,
        MULTI_EDIT_NOT_SUPPORTED,
    ) = range(4)

    def __init__(self, parent=None):
        """
        :param parent: The parent QWidget for this control
        """
        icon_path = (r"X:\ShotGrid_Test_jw\Project\config_test\install\app_store\tk-multi-inhouse\v2.8.0\resources"
                     r"\browse.png")
        venv_path = r'X:\Inhouse\Python\.venv\Lib\site-packages'
        sys.path.append(venv_path)

        QtGui.QWidget.__init__(self, parent)

        # create a settings manager where we can pull and push prefs later
        # prefs in this manager are shared
        self._settings_manager = settings.UserSettings(sgtk.platform.current_bundle())

        # create a background task manager
        self._task_manager = task_manager.BackgroundTaskManager(
            self, start_processing=True, max_threads=2
        )

        # register the data fetcher with the global schema manager
        shotgun_globals.register_bg_task_manager(self._task_manager)

        self._bundle = sgtk.platform.current_bundle()
        self._validation_run = False
        self._default_directory_path = "X:/ShotGrid_Test_jw/Project/" + self._bundle.context.project.get("name", "Undefined") + '/scan'

        # set up the UI
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # set up the Model
        self.model = QtGui.QStandardItemModel()
        self.ui.listView.setModel(self.model)

        self.ui.browse_button.clicked.connect(lambda: self._on_browse(folders=True))
        self.ui.excel_save_button.clicked.connect(self._save_checked_items_to_excel)
        self.ui.check_button.clicked.connect(self._check_all_items)
        self.ui.uncheck_button.clicked.connect(self._uncheck_all_items)
        self.ui.excel_open_button.clicked.connect(self._on_excel_browse)

        self.ui.browse_button.setIcon(QtGui.QIcon(icon_path))

    def _on_browse(self, folders=False):
        """Opens a file dialog to browse to files for publishing."""

        # Redundant with disabling UI controls but short circuiting this method
        # further ensure that a user won't be able to browse for any file even
        # if a minor UI bug allows a way to do it.

        # if not self.manual_load_enabled:
        #     return

        # options for either browse type
        options = [
            QtGui.QFileDialog.DontResolveSymlinks,
            QtGui.QFileDialog.DontUseNativeDialog,
        ]

        if folders:
            # browse folders specifics
            caption = "Browse folders to publish image sequences"
            file_mode = QtGui.QFileDialog.Directory
            options.append(QtGui.QFileDialog.ShowDirsOnly)
        else:
            # browse files specifics
            caption = "Browse files to publish"
            file_mode = QtGui.QFileDialog.ExistingFiles

        # create the dialog
        file_dialog = QtGui.QFileDialog(parent=self, caption=caption)
        file_dialog.setLabelText(QtGui.QFileDialog.Accept, "Select")
        file_dialog.setLabelText(QtGui.QFileDialog.Reject, "Cancel")
        file_dialog.setFileMode(file_mode)
        file_dialog.setDirectory(self._default_directory_path)

        # set the appropriate options
        for option in options:
            file_dialog.setOption(option)

        # browse!
        if not file_dialog.exec_():
            return

        # process the browsed files/folders for publishing
        paths = file_dialog.selectedFiles()
        if paths:
            # simulate dropping the files into the dialog
            self.ui.lineEdit.setText(str(paths[0]))
            for path in paths:
                self._add_folder_to_list(path)

    def _add_folder_to_list(self, folder_path):
        for root, _, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file).replace("\\", "/")
                self._add_file_to_list(full_path)

    def _add_file_to_list(self, file_path):
        item = CheckableItem(file_path)
        self.model.appendRow(item)

    def _save_checked_items_to_excel(self):
        from openpyxl import Workbook
        checked_items = []
        for row in range(self.model.rowCount()):
            item = self.model.item(row)
            if item.checkState() == QtCore.Qt.Checked:
                checked_items.append(item.text())

        checked_items = []
        for row in range(self.model.rowCount()):
            item = self.model.item(row)
            if item.checkState() == QtCore.Qt.Checked:
                checked_items.append(item.text())

        if checked_items:
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Checked Items"

            for idx, item in enumerate(checked_items, start=1):
                sheet[f'A{idx}'] = item

            save_path = self._get_save_path(self._default_directory_path)
            default_directory = os.path.dirname(save_path)
            default_file_name = os.path.basename(save_path)
            options = QtGui.QFileDialog.Options()

            file_path, _ = QtGui.QFileDialog.getSaveFileName(
                self,
                "Save File",
                os.path.join(default_directory, default_file_name),
                "Excel Files (*.xlsx);;All Files (*)",
                options=options
            )

            if file_path:
                workbook.save(save_path)
                logger.info(f"Checked items saved to {save_path}")

    @staticmethod
    def _get_save_path(folder_path):
        base_name = "scan_list_"
        ext = ".xlsx"
        existing_files = [f for f in os.listdir(folder_path) if f.startswith(base_name) and f.endswith(ext)]

        if not existing_files:
            return os.path.join(folder_path, f"{base_name}01{ext}")

        numbers = [int(re.findall(r'\d+', f[len(base_name):])[0]) for f in existing_files if
                   re.findall(r'\d+', f[len(base_name):])]
        next_number = max(numbers) + 1 if numbers else 1
        next_file_name = f"{base_name}{next_number:02d}{ext}"
        return os.path.join(folder_path, next_file_name)

    def _on_excel_browse(self):
        project_name = "%s" % self._bundle.context.project.get("name", "Undefined")
        default_open_path = "X:/ShotGrid_Test_jw/Project/" + project_name + '/scan'
        options = QtGui.QFileDialog.Options()
        file_path, _ = QtGui.QFileDialog.getOpenFileName(
            self,
            "Select Excel File",
            default_open_path,
            "Excel Files (*.xlsx);;All Files (*)",
            options=options
        )

        if file_path:
            self._open_excel_file(file_path)

    @staticmethod
    def _open_excel_file(file_path):
        try:
            os.startfile(file_path)
        except Exception as e:
            logger.info(f'An error occurred while opening the file: {e}')

    def _check_all_items(self):
        for row in range(self.model.rowCount()):
            item = self.model.item(row)
            item.setCheckState(QtCore.Qt.Checked)

    def _uncheck_all_items(self):
        for row in range(self.model.rowCount()):
            item = self.model.item(row)
            item.setCheckState(QtCore.Qt.Unchecked)
