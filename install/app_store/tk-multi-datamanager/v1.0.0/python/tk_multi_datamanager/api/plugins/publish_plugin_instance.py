# Copyright (c) 2018 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

from contextlib import contextmanager
import traceback

try:
    # In Python 3 the interface changed, getargspec is now deprecated.
    # getfullargspec was deprecated in 3.5, but that was reversed in 3.6.
    from inspect import getfullargspec as getargspec
except ImportError:
    # Fallback for Python 2
    from inspect import getargspec

import sgtk
from .instance_base import PluginInstanceBase

logger = sgtk.platform.get_logger(__name__)


class PublishPluginInstance(PluginInstanceBase):
    """
    Class that wraps around a publishing plugin hook

    Each plugin object reflects an instance in the app configuration.
    """

    def __init__(self, name, path, settings, publish_logger=None):
        """
        :param name: Name to be used for this plugin instance
        :param path: Path to publish plugin hook
        :param settings: Dictionary of plugin-specific settings
        :param publish_logger: a logger object that will be used by the hook
        """
        # all plugins need a hook and a name
        self._name = name

        self._icon_pixmap = None

        super(PublishPluginInstance, self).__init__(path, settings, publish_logger)

    def _create_hook_instance(self, path):
        """
        Create the plugin's hook instance.

        Injects the plugin base hook class in order to provide a default
        implementation.
        """
        bundle = sgtk.platform.current_bundle()
        hook = bundle.create_hook_instance(
            path, base_class=bundle.base_hooks.PublishPlugin
        )
        hook.id = path
        return hook

    @property
    def name(self):
        """
        The name of this publish plugin instance
        """
        return self._name

    @property
    def plugin_name(self):
        """
        The name of the publish plugin itself.
        Always a string.
        """
        value = None
        try:
            value = self._hook_instance.name
        except AttributeError:
            pass

        return value or "Untitled Integration."

    @property
    def description(self):
        """
        The description of the publish plugin.
        Always a string.
        """
        value = None
        try:
            value = self._hook_instance.description
        except AttributeError:
            pass

        return value or "No detailed description provided."

    @property
    def icon(self):
        """
        Returns the icon for this plugin instance.

        .. warning:: This property will return ``None`` when run without a UI
            present
        """

        # nothing to do if running without a UI
        if not sgtk.platform.current_engine().has_ui:
            return None

        if not self._icon_pixmap:
            self._icon_pixmap = self._load_plugin_icon()

        return self._icon_pixmap

    @property
    def item_filters(self):
        """
        The item filters defined by this plugin
        or [] if none have been defined.
        """
        try:
            return self._hook_instance.item_filters
        except AttributeError:
            return []

    @property
    def has_custom_ui(self):
        """
        Checks if a plugin has a custom widget.

        :returns: ``True`` if the plugin supports ``create_settings_widget``,
            ``get_ui_settings`` and ``set_ui_settings``,``False`` otherwise.
        """
        return all(
            hasattr(self._hook_instance, attr)
            for attr in ["create_settings_widget", "get_ui_settings", "set_ui_settings"]
        )

    @property
    def settings(self):
        """
        returns a dict of resolved raw settings given the current state
        """
        return self._settings

    def run_accept(self, item):
        """
        Executes the hook accept method for the given item

        :param item: Item to analyze
        :returns: dictionary with boolean keys accepted/visible/enabled/checked
        """

        try:
            return self._hook_instance.accept(self.settings, item)
        except Exception:
            error_msg = traceback.format_exc()
            self._logger.error(
                "Error running accept for %s" % self,
                extra=_get_error_extra_info(error_msg),
            )
            return {"accepted": False}
        finally:
            if sgtk.platform.current_engine().has_ui:
                from sgtk.platform.qt import QtCore

                QtCore.QCoreApplication.processEvents()

    def run_validate(self, settings, item):
        """
        Executes the validation logic for this plugin instance.

        :param settings: Dictionary of settings
        :param item: Item to analyze
        :return: True if validation passed, False otherwise.
        """

        with self._handle_plugin_error(None, "Error Validating: %s"):
            status = self._hook_instance.validate(settings, item)

        # check that we are not trying to publish to a site level context
        if item.context.project is None:
            status = False
            self.logger.error(
                "Please link '%s' to a Flow Production Tracking object and task!"
                % item.name
            )

        if status:
            self.logger.debug("Validation successful!")
        else:
            self.logger.error("Validation failed.")

        return status

    def run_publish(self, settings, item, CheckableItem, colorspace):
        """
        Executes the publish logic for this plugin instance.

        :param settings: Dictionary of settings
        :param item: Item to analyze
        """
        import os
        import re


        with self._handle_plugin_error("Publish complete!", "Error publishing: %s"):
            path = item.properties["path"]
            folder_path = os.path.dirname(path)

            if 'Upload' not in settings:
                checked_item_path = folder_path.replace('\\', '/')
                parts = checked_item_path.split('/')
                project_code = parts[3]
                if os.path.isdir(checked_item_path):
                    parts = parts[-1].split('_')

                # Extract the necessary parts
                seq_code = parts[0]
                shot_code = parts[0] + '_' + parts[1] + '_' + parts[2]
                category = parts[3]
                version = parts[4]

                # Extract version information from source path
                target_folder = os.path.join(
                    r'X:\ShotGrid_Test_jw\Project',
                    project_code,
                    '04_SEQ',
                    seq_code,
                    shot_code,
                    'Plates',
                    category,
                    version,
                )

                for root, _, files in os.walk(target_folder):
                    if files:
                        if files[0].endswith('.exr') or files[0].endswith('.dpx'):
                            match = re.search(r'\.(\d+)\.', files[0])
                            if match:
                                frame_number = match.group(1)
                                padding = len(frame_number)
                                new_filename = files[0].replace(frame_number, f"%0{padding}d")
                                file = new_filename
                        else:
                            if files[0].endswith('.mov'):
                                file = files[0]

                target_folder_file = target_folder + '\\' + file

                config_path = r'X:\ShotGrid_Test_jw\Project\config_test'
                tk = sgtk.sgtk_from_path(config_path)
                sg = tk.shotgun

                current_engine = sgtk.platform.current_engine()
                context = current_engine.context
                project_id = context.project['id']
                user_id = context.user['id']

                sequence = sg.find_one('Sequence', [
                    ['project', 'is', {'type': 'Project', 'id': project_id}],
                    ['code', 'is', seq_code]
                ], ['id'])

                if not sequence:
                    sequence_data = {
                        'project': {'type': 'Project', 'id': project_id},
                        'code': seq_code,
                    }
                    sequence = sg.create('Sequence', sequence_data)
                    logger.info(f"Created Sequence: {sequence}")

                sequence_id = sequence['id']

                existing_shots = sg.find('Shot', [
                    ['project', 'is', {'type': 'Project', 'id': project_id}],
                    ['sg_sequence', 'is', {'type': 'Sequence', 'id': sequence_id}],
                    ['code', 'is', shot_code]
                ])

                check_items = CheckableItem.fetch_checked_items()
                check_item = next(item for item in check_items if item['Shot_Code'] == shot_code)

                # shot_data by excel
                if not existing_shots:
                    shot_data = {
                        'project': {'type': 'Project', 'id': project_id},
                        'sg_sequence': {'type': 'Sequence', 'id': sequence_id},
                        'code': shot_code,
                        'sg_cut_in': check_item['Cut_In'],
                        'sg_cut_out': check_item['Cut_Out'],
                        'sg_cut_duration': check_item['Duration'],
                        'sg_org_clip': check_item['Org_Clip'],
                        'sg_org_resolution': check_item['Resolution'],
                        'sg_fps': check_item['Fps'],
                        'sg_colorspace' : colorspace,
                        "task_template": {"type": "TaskTemplate", "id": 46}
                    }
                    new_shot = sg.create('Shot', shot_data)
                    shot_id = new_shot['id']
                    logger.info(f"Created Shot: {new_shot}")
                else:
                    filters = [
                        ['project', 'is', {'type': 'Project', 'id': project_id}],
                        ['code', 'is', shot_code]
                    ]
                    fields = ['id']
                    shot_id = sg.find_one('Shot', filters, fields)
                    shot_id = shot_id['id']

                    shot_data = {
                        'project': {'type': 'Project', 'id': project_id},
                        'sg_sequence': {'type': 'Sequence', 'id': sequence_id},
                        'code': shot_code,
                        'sg_cut_in': check_item['Cut_In'],
                        'sg_cut_out': check_item['Cut_Out'],
                        'sg_cut_duration': check_item['Duration'],
                        'sg_org_clip': check_item['Org_Clip'],
                        'sg_org_resolution': check_item['Resolution'],
                        'sg_fps': check_item['Fps'],
                        'sg_colorspace': colorspace
                    }
                    sg.update('Shot', shot_id, shot_data)

                upload_movie_path = target_folder + '\\temp\\'

                # Set mov file path and name
                mov_files = [f for f in os.listdir(upload_movie_path) if f.endswith('.mov')]
                upload_movie_path = upload_movie_path + mov_files[0]

                if category == 'org':
                    file_type_id = 166
                elif category == 'edit':
                    file_type_id = 167
                elif category.startswith("src"):
                    file_type_id = 199

                if path.endswith('mov'):
                    movie_file_path = upload_movie_path
                    frames_file_path = ''
                else:
                    movie_file_path = upload_movie_path
                    frames_file_path = target_folder_file

                # MOV file version register
                version_data = {
                    'project': {'type': 'Project', 'id': project_id},
                    'entity': {'type': 'Shot', 'id': shot_id},  # shot or entity
                    'code': shot_code + '_' + category + '_' + version,  # version name
                    'sg_path_to_movie': movie_file_path,
                    'sg_path_to_frames': frames_file_path,
                    'sg_version_type' : category
                }

                # Version create
                new_version = sg.create('Version', version_data)

                # File upload
                sg.upload('Version', new_version['id'], upload_movie_path, field_name='sg_uploaded_movie')
                publish_code = target_folder_file.split('\\')
                logger.info(f"Created Version details: {new_version}")

                thumbnail_path =  item.get_thumbnail_as_path(),
                publish_name = publish_code[-1]
                # Version publish
                publish_data = {
                    'project': {'type': 'Project', 'id': project_id},
                    'entity': {'type': 'Shot', 'id': shot_id},
                    'published_file_type': {'type': 'PublishedFileType', 'id': file_type_id},
                    'path': {
                        'local_path': target_folder_file,
                        'type': 'Path',  # Path type(ex: 'Path', 'Link'..)
                    },
                    'code': publish_name,
                    'version': new_version,
                    'image' : thumbnail_path[0],
                    'description' : item.description,
                    'created_by': {'type': 'HumanUser', 'id': user_id},
                }

                # Publish
                published_file = sg.create('PublishedFile', publish_data)
                logger.info(f"Published file created: {published_file['id']}")


    def run_finalize(self, settings, item):
        """
        Executes the finalize logic for this plugin instance.

        :param settings: Dictionary of settings
        :param item: Item to analyze
        """
        with self._handle_plugin_error("Finalize complete!", "Error finalizing: %s"):
            self._hook_instance.finalize(settings, item)

    ############################################################################
    # ui methods

    def run_create_settings_widget(self, parent, items):
        """
        Creates a custom widget to edit a plugin's settings.

        .. note:: This method is a no-op if running without a UI present

        :param parent: Parent widget
        :type parent: :class:`QtGui.QWidget`
        :param items: A list of PublishItems the selected tasks are parented to.
        """

        # nothing to do if running without a UI
        if not sgtk.platform.current_engine().has_ui:
            return None

        with self._handle_plugin_error(None, "Error laying out widgets: %s"):

            if len(getargspec(self._hook_instance.create_settings_widget).args) == 3:
                return self._hook_instance.create_settings_widget(parent, items)
            else:
                # Items is a newer attribute, which an older version of the hook
                # might not implement, so fallback to passing just the parent.
                return self._hook_instance.create_settings_widget(parent)

    def run_get_ui_settings(self, parent, items):
        """
        Retrieves the settings from the custom UI.

        .. note:: This method is a no-op if running without a UI present

        :param parent: Parent widget
        :type parent: :class:`QtGui.QWidget`
        """

        # nothing to do if running without a UI
        if not sgtk.platform.current_engine().has_ui:
            return None

        with self._handle_plugin_error(None, "Error reading settings from UI: %s"):

            if len(getargspec(self._hook_instance.get_ui_settings).args) == 3:
                return self._hook_instance.get_ui_settings(parent, items)
            else:
                # Items is a newer attribute, which an older version of the hook
                # might not implement, so fallback to passing just the parent.
                return self._hook_instance.get_ui_settings(parent)

    def run_set_ui_settings(self, parent, settings, items):
        """
        Provides a list of settings from the custom UI. It is the responsibility of the UI
        handle different values for the same setting.

        .. note:: This method is a no-op if running without a UI present

        :param parent: Parent widget
        :type parent: :class:`QtGui.QWidget`
        :param settings: List of dictionary of settings as python literals.
        :param items: A list of PublishItems the selected tasks are parented to.
        """

        # nothing to do if running without a UI
        if not sgtk.platform.current_engine().has_ui:
            return None

        with self._handle_plugin_error(None, "Error writing settings to UI: %s"):

            if len(getargspec(self._hook_instance.set_ui_settings).args) == 4:
                self._hook_instance.set_ui_settings(parent, settings, items)
            else:
                # Items is a newer attribute, which an older version of the hook
                # might not implement, so fallback to passing just the parent and settings.
                self._hook_instance.set_ui_settings(parent, settings)

    @contextmanager
    def _handle_plugin_error(self, success_msg, error_msg):
        """
        Creates a scope that will properly handle any error raised by the plugin
        while the scope is executed.

        .. note::
            Any exception raised by the plugin is bubbled up to the caller.

        :param str success_msg: Message to be displayed if there is no error.
        :param str error_msg: Message to be displayed if there is an error.
        """

        try:
            # Execute's the code inside the with statement. Any errors will be
            # caught and logged and the events will be processed
            yield
        except Exception as e:
            exception_msg = traceback.format_exc()
            self._logger.error(
                error_msg % (e,), extra=_get_error_extra_info(exception_msg)
            )
            raise
        else:
            if success_msg:
                self._logger.debug(success_msg)
        finally:
            if sgtk.platform.current_engine().has_ui:
                # If we have a UI process the events so that the UI can update mid operation.
                from sgtk.platform.qt import QtCore

                QtCore.QCoreApplication.processEvents()

    def _load_plugin_icon(self):
        """
        Loads the icon defined by the plugin's hook.

        :returns: QPixmap or None if not found
        """

        # defer import until needed and to avoid issues when running without UI
        from sgtk.platform.qt import QtGui

        # load plugin icon
        pixmap = None
        try:
            icon_path = self._hook_instance.icon
            if icon_path:
                try:
                    pixmap = QtGui.QPixmap(icon_path)
                except Exception as e:
                    self._logger.warning(
                        "%r: Could not load icon '%s': %s" % (self, icon_path, e)
                    )
        except AttributeError:
            # plugin does not have an icon
            pass

        # load default pixmap if hook doesn't define one
        if pixmap is None:
            pixmap = QtGui.QPixmap(":/tk_multi_publish2/task.png")

        return pixmap


def _get_error_extra_info(error_msg):
    """
    A little wrapper to return a dictionary of data to show a button in the
    publisher with the supplied error message.
    :param error_msg: The error message to display.
    :return: An logging "extra" dictionary to show the error message.
    """

    return {
        "action_show_more_info": {
            "label": "Error Details",
            "tooltip": "Show the full error tack trace",
            "text": "<pre>%s</pre>" % (error_msg,),
        }
    }
