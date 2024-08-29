import shutil
import subprocess
from datetime import datetime
import os


def convert_to_copy_path(path):
    """
    Copy the scanned files according to the toolkit folder structure.
    """
    parts = path.split('/')
    target_folder = None
    if os.path.isdir(path):
        parts = parts[-1].split('_')
    else:
        parts = parts[-2].split('_')

    # Extract the necessary parts
    project_code = parts[0]
    seq_code = parts[1]
    shot_code = parts[1] + '_' + parts[2] + '_' + parts[3]
    category = parts[4]
    version = parts[5]

    # Extract version information from source path
    target_folder = os.path.join(
        r'X:\ShotGrid_Test_jw\Project',
        project_code,
        '04_SEQ',
        seq_code,
        shot_code,
        'Plates',
        category,
        version
    )

    return target_folder
            # # If the route already exists
            # if os.path.isdir(target_folder):
            #     logger.info(f'target_folder already exists: {target_folder}')
            # else:
            #     # Copy files to target folder
            #     self._copy_files(checked_item_path, target_folder, temp_folder_name, origin_directory_path)

def ACES_2065_1_Seq():
    not_mov_files.sort()
    parts = retrieved_item['path'].split('/')
    origin_directory_path = parts[-1]

    first_file = not_mov_files[0]
    match = re.search(r'(.*?)(\d+)\.(dpx|exr)$', first_file)
    prefix = match.group(1)
    number_str = match.group(2)
    suffix = match.group(3)
    num_digits = len(number_str)
    format_specifier = f"%0{num_digits}d"
    sequence_path = os.path.join(retrieved_item['path'], f"{prefix}{format_specifier}.{suffix}")
    sequence_path = sequence_path.replace('\\', '/')

    first_frame = int(number_str)
    last_frame = first_frame + len(not_mov_files) - 1

    root['first_frame'].setValue(first_frame)
    root['last_frame'].setValue(last_frame)
    root['fps'].setValue(float(fps_number))
    root['format'].setValue(new_format)
    root['colorManagement'].setValue('OCIO')
    root['OCIO_config'].setValue('custom')
    root['customOCIOConfigPath'].setValue('X:/FAM/from_mthd/240411_spec/OCIO/config.ocio')

    read_node = nuke.createNode('Read')
    read_node['file'].setValue(sequence_path)
    read_node['first'].setValue(first_frame)
    read_node['last'].setValue(last_frame)
    read_node['origfirst'].setValue(first_frame)
    read_node['origlast'].setValue(last_frame)
    read_node['format'].setValue(new_format)
    read_node['colorspace'].setValue('ACES - ACES2065-1')

    ocio_node = nuke.createNode('OCIODisplay')
    ocio_node['colorspace'].setValue('ACES - ACES2065-1')
    ocio_node.setInput(0, read_node)

    copy_path = convert_to_copy_path(retrieved_item["path"])
    temp_folder_path = os.path.join(copy_path, 'temp')
    temp_folder_path = temp_folder_path.replace('\\', '/')

    if not os.path.exists(temp_folder_path):
        os.makedirs(temp_folder_path)
        subprocess.call(['attrib', '+h', temp_folder_path])

    new_output_path = os.path.join(temp_folder_path, f'{origin_directory_path}.mov')
    new_output_path = new_output_path.replace('\\', '/')

    # if os.path.isfile(new_output_path):
    #     print(f'This file({new_output_path}) is already exists.')
    # else:
    write_node = nuke.createNode('Write')
    write_node['file_type'].setValue('mov')
    write_node['file'].setValue(new_output_path)
    write_node['mov64_fps'].setValue(float(fps_number))
    write_node['colorspace'].setValue('ACES - ACES2065-1')
    write_node['raw'].setValue(True)
    write_node.setInput(0, ocio_node)

    nuke.execute(write_node, first_frame, last_frame)

    print(f"Read node created for sequence: {sequence_path}")
    print(f"Original range set to: {first_frame} - {last_frame}")


def ACES_2065_1_Mov():
    parts = retrieved_item['path'].split('/')
    origin_directory_path = parts[-2]

    root['first_frame'].setValue(first_frame)
    root['last_frame'].setValue(last_frame)
    root['fps'].setValue(float(fps_number))
    root['format'].setValue(new_format)
    root['colorManagement'].setValue('OCIO')
    root['OCIO_config'].setValue('custom')
    root['customOCIOConfigPath'].setValue('X:/FAM/from_mthd/240411_spec/OCIO/config.ocio')

    read_node = nuke.createNode('Read')
    read_node['file'].setValue(retrieved_item['path'])
    read_node['first'].setValue(first_frame)
    read_node['last'].setValue(last_frame)
    read_node['origfirst'].setValue(first_frame)
    read_node['origlast'].setValue(last_frame)
    read_node['format'].setValue(new_format)
    read_node['colorspace'].setValue('ACES - ACES2065-1')

    ocio_node = nuke.createNode('OCIODisplay')
    ocio_node['colorspace'].setValue('ACES - ACES2065-1')
    ocio_node.setInput(0, read_node)

    copy_path = convert_to_copy_path(retrieved_item["path"])
    temp_folder_path = os.path.join(copy_path, 'temp')
    temp_folder_path = temp_folder_path.replace('\\', '/')

    if not os.path.exists(temp_folder_path):
        os.makedirs(temp_folder_path)
        subprocess.call(['attrib', '+h', temp_folder_path])

    new_output_path = os.path.join(temp_folder_path, f'{origin_directory_path}.mov')
    new_output_path = new_output_path.replace('\\', '/')

    # if os.path.isfile(new_output_path):
    #     print(f'This file({new_output_path}) is already exists.')
    # else:
    write_node = nuke.createNode('Write')
    write_node['file_type'].setValue('mov')
    write_node['file'].setValue(new_output_path)
    write_node['mov64_fps'].setValue(float(fps_number))
    write_node['colorspace'].setValue('ACES - ACES2065-1')
    write_node['raw'].setValue(True)
    write_node.setInput(0, ocio_node)

    nuke.execute(write_node, first_frame, last_frame)

    print(f"Read node created for mov: {retrieved_item['path']}")
    print(f"Original range set to: {first_frame} - {last_frame}")


def ACEScg_Seq():
    not_mov_files.sort()
    parts = retrieved_item['path'].split('/')
    origin_directory_path = parts[-1]

    first_file = not_mov_files[0]
    match = re.search(r'(.*?)(\d+)\.(dpx|exr)$', first_file)
    prefix = match.group(1)
    number_str = match.group(2)
    suffix = match.group(3)
    num_digits = len(number_str)
    format_specifier = f"%0{num_digits}d"
    sequence_path = os.path.join(retrieved_item['path'], f"{prefix}{format_specifier}.{suffix}")
    sequence_path = sequence_path.replace('\\', '/')
    first_frame = int(number_str)
    last_frame = first_frame + len(not_mov_files) - 1

    root['first_frame'].setValue(first_frame)
    root['last_frame'].setValue(last_frame)
    root['fps'].setValue(float(fps_number))
    root['format'].setValue(new_format)
    root['colorManagement'].setValue('OCIO')
    root['OCIO_config'].setValue('custom')
    root['customOCIOConfigPath'].setValue('X:/2D_In_find_of_the_king/6_spec/OCIO/config.ocio')
    root['monitorLut'].setValue('Rec.709 (ACES)')

    read_node = nuke.createNode('Read')
    read_node['file'].setValue(sequence_path)
    read_node['first'].setValue(first_frame)
    read_node['last'].setValue(last_frame)
    read_node['origfirst'].setValue(first_frame)
    read_node['origlast'].setValue(last_frame)
    read_node['format'].setValue(new_format)
    read_node['colorspace'].setValue('ACES - ACEScg')

    ocio_node = nuke.createNode('OCIODisplay')
    ocio_node['colorspace'].setValue('ACES - ACEScg')
    ocio_node.setInput(0, read_node)

    copy_path = convert_to_copy_path(retrieved_item["path"])
    temp_folder_path = os.path.join(copy_path, 'temp')
    temp_folder_path = temp_folder_path.replace('\\', '/')

    if not os.path.exists(temp_folder_path):
        os.makedirs(temp_folder_path)
        subprocess.call(['attrib', '+h', temp_folder_path])

    prefix = prefix[:-1]
    new_output_path = os.path.join(temp_folder_path, f'{origin_directory_path}.mov')
    new_output_path = new_output_path.replace('\\', '/')

    # if os.path.isfile(new_output_path):
    #     print(f'This file({new_output_path}) is already exists.')
    # else:
    write_node = nuke.createNode('Write')
    write_node['file_type'].setValue('mov')
    write_node['file'].setValue(new_output_path)
    write_node['mov64_fps'].setValue(float(fps_number))
    write_node['raw'].setValue(True)
    write_node['mov64_codec'].setValue(r'h264\tH.264')
    write_node['mov64_quality'].setValue('Custom')
    write_node['colorspace'].setValue('Output - Rec.709')
    write_node.setInput(0, ocio_node)

    nuke.execute(write_node, first_frame, last_frame)

    print(f"Read node created for sequence: {sequence_path}")
    print(f"Original range set to: {first_frame} - {last_frame}")


def ACEScg_Mov():
    parts = retrieved_item['path'].split('/')
    origin_directory_path = parts[-2]

    root['first_frame'].setValue(first_frame)
    root['last_frame'].setValue(last_frame)
    root['fps'].setValue(float(fps_number))
    root['format'].setValue(new_format)
    root['colorManagement'].setValue('OCIO')
    root['OCIO_config'].setValue('custom')
    root['customOCIOConfigPath'].setValue('X:/2D_In_find_of_the_king/6_spec/OCIO/config.ocio')
    root['monitorLut'].setValue('Rec.709 (ACES)')

    read_node = nuke.createNode('Read')
    read_node['file'].setValue(retrieved_item['path'])
    read_node['first'].setValue(first_frame)
    read_node['last'].setValue(last_frame)
    read_node['origfirst'].setValue(first_frame)
    read_node['origlast'].setValue(last_frame)
    read_node['format'].setValue(new_format)
    read_node['colorspace'].setValue('ACES - ACEScg')

    ocio_node = nuke.createNode('OCIODisplay')
    ocio_node['colorspace'].setValue('ACES - ACEScg')
    ocio_node.setInput(0, read_node)

    copy_path = convert_to_copy_path(retrieved_item["path"])
    temp_folder_path = os.path.join(copy_path, 'temp')
    temp_folder_path = temp_folder_path.replace('\\', '/')

    if not os.path.exists(temp_folder_path):
        os.makedirs(temp_folder_path)
        subprocess.call(['attrib', '+h', temp_folder_path])

    new_output_path = os.path.join(temp_folder_path, f'{origin_directory_path}.mov')
    new_output_path = new_output_path.replace('\\', '/')

    # if os.path.isfile(new_output_path):
    #     print(f'This file({new_output_path}) is already exists.')
    # else:
    write_node = nuke.createNode('Write')
    write_node['file_type'].setValue('mov')
    write_node['file'].setValue(new_output_path)
    write_node['mov64_fps'].setValue(float(fps_number))
    write_node['raw'].setValue(True)
    write_node['mov64_codec'].setValue(r'h264\tH.264')
    write_node['mov64_quality'].setValue('Custom')
    write_node['colorspace'].setValue('Output - Rec.709')
    write_node.setInput(0, ocio_node)

    nuke.execute(write_node, first_frame, last_frame)

    print(f"Read node created for mov: {retrieved_item['path']}")
    print(f"Original range set to: {first_frame} - {last_frame}")


def AlexaV3_Mov():
    parts = retrieved_item['path'].split('/')
    origin_directory_path = parts[-2]

    default_directory = os.path.dirname(retrieved_item['path'])
    default_file_name = os.path.basename(retrieved_item['path'])

    root['first_frame'].setValue(first_frame)
    root['last_frame'].setValue(last_frame)
    root['fps'].setValue(float(fps_number))
    root['format'].setValue(new_format)

    read_node = nuke.createNode('Read')
    read_node['file'].setValue(retrieved_item['path'])
    read_node['first'].setValue(first_frame)
    read_node['last'].setValue(last_frame)
    read_node['origfirst'].setValue(first_frame)
    read_node['origlast'].setValue(last_frame)
    read_node['format'].setValue(new_format)

    ocio_node = nuke.createNode('JUNG_OCIO')
    ocio_node.setInput(0, read_node)

    copy_path = convert_to_copy_path(retrieved_item["path"])
    temp_folder_path = os.path.join(copy_path, 'temp')
    temp_folder_path = temp_folder_path.replace('\\', '/')

    if not os.path.exists(temp_folder_path):
        os.makedirs(temp_folder_path)
        subprocess.call(['attrib', '+h', temp_folder_path])

    new_output_path = os.path.join(temp_folder_path, f'{origin_directory_path}.mov')
    new_output_path = new_output_path.replace('\\', '/')

    # if os.path.isfile(new_output_path):
    #     print(f'This file({new_output_path}) is already exists.')
    # else:
    write_node = nuke.createNode('Write')
    write_node['file_type'].setValue('mov')
    write_node['file'].setValue(new_output_path)
    write_node['colorspace'].setValue('rec709')
    write_node.setInput(0, ocio_node)

    nuke.execute(write_node, first_frame, last_frame)

    print(f"Read node created for mov: {retrieved_item['path']}")
    print(f"Original range set to: {first_frame} - {last_frame}")


def AlexaV3_Seq():
    not_mov_files.sort()
    parts = retrieved_item['path'].split('/')
    origin_directory_path = parts[-1]

    first_file = not_mov_files[0]
    match = re.search(r'(.*?)(\d+)\.(dpx|exr)$', first_file)
    prefix = match.group(1)
    number_str = match.group(2)
    suffix = match.group(3)
    num_digits = len(number_str)
    format_specifier = f"%0{num_digits}d"
    sequence_path = os.path.join(retrieved_item['path'], f"{prefix}{format_specifier}.{suffix}")
    sequence_path = sequence_path.replace('\\', '/')

    first_frame = int(number_str)
    last_frame = first_frame + len(not_mov_files) - 1

    root['first_frame'].setValue(first_frame)
    root['last_frame'].setValue(last_frame)
    root['fps'].setValue(float(fps_number))
    root['format'].setValue(new_format)

    read_node = nuke.createNode('Read')
    read_node['file'].setValue(sequence_path)
    read_node['first'].setValue(first_frame)
    read_node['last'].setValue(last_frame)
    read_node['origfirst'].setValue(first_frame)
    read_node['origlast'].setValue(last_frame)
    read_node['format'].setValue(new_format)

    ocio_node = nuke.createNode('JUNG_OCIO')
    ocio_node.setInput(0, read_node)

    copy_path = convert_to_copy_path(retrieved_item["path"])
    temp_folder_path = os.path.join(copy_path, 'temp')
    temp_folder_path = temp_folder_path.replace('\\', '/')

    if not os.path.exists(temp_folder_path):
        os.makedirs(temp_folder_path)
        subprocess.call(['attrib', '+h', temp_folder_path])

    prefix = prefix[:-1]
    new_output_path = os.path.join(temp_folder_path, f'{origin_directory_path}.mov')
    new_output_path = new_output_path.replace('\\', '/')

    # if os.path.isfile(new_output_path):
    #     print(f'This file({new_output_path}) is already exists.')
    # else:
    write_node = nuke.createNode('Write')
    write_node['file_type'].setValue('mov')
    write_node['file'].setValue(new_output_path)
    write_node['colorspace'].setValue('rec709')
    write_node.setInput(0, ocio_node)

    nuke.execute(write_node, first_frame, last_frame)

    print(f"Read node created for sequence: {sequence_path}")
    print(f"Original range set to: {first_frame} - {last_frame}")


def rec709_Mov():
    parts = retrieved_item['path'].split('/')
    origin_directory_path = parts[-2]
    default_directory = os.path.dirname(retrieved_item['path'])
    default_file_name = os.path.basename(retrieved_item['path'])

    root['first_frame'].setValue(first_frame)
    root['last_frame'].setValue(last_frame)
    root['fps'].setValue(float(fps_number))
    root['format'].setValue(new_format)

    read_node = nuke.createNode('Read')
    read_node['file'].setValue(retrieved_item['path'])
    read_node['first'].setValue(first_frame)
    read_node['last'].setValue(last_frame)
    read_node['origfirst'].setValue(first_frame)
    read_node['origlast'].setValue(last_frame)
    read_node['format'].setValue(new_format)
    read_node['colorspace'].setValue('rec709')

    copy_path = convert_to_copy_path(retrieved_item["path"])
    temp_folder_path = os.path.join(copy_path, 'temp')
    temp_folder_path = temp_folder_path.replace('\\', '/')

    if not os.path.exists(temp_folder_path):
        os.makedirs(temp_folder_path)
        subprocess.call(['attrib', '+h', temp_folder_path])

    new_output_path = os.path.join(temp_folder_path, f'{origin_directory_path}.mov')
    new_output_path = new_output_path.replace('\\', '/')

    # if os.path.isfile(new_output_path):
    #     print(f'This file({new_output_path}) is already exists.')
    # else:
    write_node = nuke.createNode('Write')
    write_node['file_type'].setValue('mov')
    write_node['file'].setValue(new_output_path)
    write_node['colorspace'].setValue('rec709')
    write_node.setInput(0, read_node)

    nuke.execute(write_node, first_frame, last_frame)

    print(f"Read node created for mov: {retrieved_item['path']}")
    print(f"Original range set to: {first_frame} - {last_frame}")


def rec709_Seq():
    not_mov_files.sort()
    parts = retrieved_item['path'].split('/')
    origin_directory_path = parts[-1]
    first_file = not_mov_files[0]
    match = re.search(r'(.*?)(\d+)\.(dpx|exr)$', first_file)
    prefix = match.group(1)
    number_str = match.group(2)
    suffix = match.group(3)
    num_digits = len(number_str)
    format_specifier = f"%0{num_digits}d"
    sequence_path = os.path.join(retrieved_item['path'], f"{prefix}{format_specifier}.{suffix}")
    sequence_path = sequence_path.replace('\\', '/')

    first_frame = int(number_str)
    last_frame = first_frame + len(not_mov_files) - 1

    root['first_frame'].setValue(first_frame)
    root['last_frame'].setValue(last_frame)
    root['fps'].setValue(float(fps_number))
    root['format'].setValue(new_format)

    read_node = nuke.createNode('Read')
    read_node['file'].setValue(sequence_path)
    read_node['first'].setValue(first_frame)
    read_node['last'].setValue(last_frame)
    read_node['origfirst'].setValue(first_frame)
    read_node['origlast'].setValue(last_frame)
    read_node['format'].setValue(new_format)
    read_node['colorspace'].setValue('rec709')

    copy_path = convert_to_copy_path(retrieved_item["path"])
    temp_folder_path = os.path.join(copy_path, 'temp')
    temp_folder_path = temp_folder_path.replace('\\', '/')

    if not os.path.exists(temp_folder_path):
        os.makedirs(temp_folder_path)
        subprocess.call(['attrib', '+h', temp_folder_path])

    prefix = prefix[:-1]
    new_output_path = os.path.join(temp_folder_path, f'{origin_directory_path}.mov')
    new_output_path = new_output_path.replace('\\', '/')

    # if os.path.isfile(new_output_path):
    #     print(f'This file({new_output_path}) is already exists.')
    # else:
    write_node = nuke.createNode('Write')
    write_node['file_type'].setValue('mov')
    write_node['file'].setValue(new_output_path)
    write_node['colorspace'].setValue('rec709')
    write_node.setInput(0, read_node)

    nuke.execute(write_node, first_frame, last_frame)

    print(f"Read node created for sequence: {sequence_path}")
    print(f"Original range set to: {first_frame} - {last_frame}")


def sRGB_Mov():
    parts = retrieved_item['path'].split('/')
    origin_directory_path = parts[-2]

    root['first_frame'].setValue(first_frame)
    root['last_frame'].setValue(last_frame)
    root['fps'].setValue(float(fps_number))
    root['format'].setValue(new_format)

    read_node = nuke.createNode('Read')
    read_node['file'].setValue(retrieved_item['path'])
    read_node['first'].setValue(first_frame)
    read_node['last'].setValue(last_frame)
    read_node['origfirst'].setValue(first_frame)
    read_node['origlast'].setValue(last_frame)
    read_node['format'].setValue(new_format)
    read_node['colorspace'].setValue('sRGB')

    copy_path = convert_to_copy_path(retrieved_item["path"])
    temp_folder_path = os.path.join(copy_path, 'temp')
    temp_folder_path = temp_folder_path.replace('\\', '/')

    if not os.path.exists(temp_folder_path):
        os.makedirs(temp_folder_path)
        subprocess.call(['attrib', '+h', temp_folder_path])

    new_output_path = os.path.join(temp_folder_path, f'{origin_directory_path}.mov')
    new_output_path = new_output_path.replace('\\', '/')

    # if os.path.isfile(new_output_path):
    #     print(f'This file({new_output_path}) is already exists.')
    # else:
    write_node = nuke.createNode('Write')
    write_node['file_type'].setValue('mov')
    write_node['file'].setValue(new_output_path)
    write_node['colorspace'].setValue('sRGB')
    write_node.setInput(0, read_node)

    nuke.execute(write_node, first_frame, last_frame)

    print(f"Read node created for mov: {retrieved_item['path']}")
    print(f"Original range set to: {first_frame} - {last_frame}")

def sRGB_Seq():
    not_mov_files.sort()
    parts = retrieved_item['path'].split('/')
    origin_directory_path = parts[-1]

    first_file = not_mov_files[0]
    match = re.search(r'(.*?)(\d+)\.(dpx|exr)$', first_file)
    prefix = match.group(1)
    number_str = match.group(2)
    suffix = match.group(3)
    num_digits = len(number_str)
    format_specifier = f"%0{num_digits}d"
    sequence_path = os.path.join(retrieved_item['path'], f"{prefix}{format_specifier}.{suffix}")
    sequence_path = sequence_path.replace('\\', '/')

    first_frame = int(number_str)
    last_frame = first_frame + len(not_mov_files) - 1

    root['first_frame'].setValue(first_frame)
    root['last_frame'].setValue(last_frame)
    root['fps'].setValue(float(fps_number))
    root['format'].setValue(new_format)

    read_node = nuke.createNode('Read')
    read_node['file'].setValue(sequence_path)
    read_node['first'].setValue(first_frame)
    read_node['last'].setValue(last_frame)
    read_node['origfirst'].setValue(first_frame)
    read_node['origlast'].setValue(last_frame)
    read_node['format'].setValue(new_format)
    read_node['colorspace'].setValue('sRGB')

    copy_path = convert_to_copy_path(retrieved_item["path"])
    temp_folder_path = os.path.join(copy_path, 'temp')
    temp_folder_path = temp_folder_path.replace('\\', '/')

    if not os.path.exists(temp_folder_path):
        os.makedirs(temp_folder_path)
        subprocess.call(['attrib', '+h', temp_folder_path])

    prefix = prefix[:-1]
    new_output_path = os.path.join(temp_folder_path, f'{origin_directory_path}.mov')
    new_output_path = new_output_path.replace('\\', '/')

    # if os.path.isfile(new_output_path):
    #     print(f'This file({new_output_path}) is already exists.')
    # else:
    write_node = nuke.createNode('Write')
    write_node['file_type'].setValue('mov')
    write_node['file'].setValue(new_output_path)
    write_node['colorspace'].setValue('sRGB')
    write_node.setInput(0, read_node)

    nuke.execute(write_node, first_frame, last_frame)

    print(f"Read node created for sequence: {sequence_path}")
    print(f"Original range set to: {first_frame} - {last_frame}")

def legacy_Seq():
    not_mov_files.sort()
    first_file = not_mov_files[0]
    parts = retrieved_item['path'].split('/')
    origin_directory_path = parts[-1]
    match = re.search(r'(.*?)(\d+)\.(dpx|exr)$', first_file)
    prefix = match.group(1)
    number_str = match.group(2)
    suffix = match.group(3)
    num_digits = len(number_str)
    format_specifier = f"%0{num_digits}d"
    sequence_path = os.path.join(retrieved_item['path'], f"{prefix}{format_specifier}.{suffix}")
    sequence_path = sequence_path.replace('\\', '/')

    first_frame = int(number_str)
    last_frame = first_frame + len(not_mov_files) - 1

    root['first_frame'].setValue(first_frame)
    root['last_frame'].setValue(last_frame)
    root['fps'].setValue(float(fps_number))
    root['format'].setValue(new_format)

    read_node = nuke.createNode('Read')
    read_node['file'].setValue(sequence_path)
    read_node['first'].setValue(first_frame)
    read_node['last'].setValue(last_frame)
    read_node['origfirst'].setValue(first_frame)
    read_node['origlast'].setValue(last_frame)
    read_node['format'].setValue(new_format)

    copy_path = convert_to_copy_path(retrieved_item["path"])
    temp_folder_path = os.path.join(copy_path, 'temp')
    temp_folder_path = temp_folder_path.replace('\\', '/')

    if not os.path.exists(temp_folder_path):
        os.makedirs(temp_folder_path)
        subprocess.call(['attrib', '+h', temp_folder_path])

    new_output_path = os.path.join(temp_folder_path, f'{origin_directory_path}.mov')
    new_output_path = new_output_path.replace('\\', '/')

    # if os.path.isfile(new_output_path):
    #     print(f'This file({new_output_path}) is already exists.')
    # else:
    write_node = nuke.createNode('Write')
    write_node['file_type'].setValue('mov')
    write_node['file'].setValue(new_output_path)
    read_colorspace = read_node['colorspace'].value()
    write_node['colorspace'].setValue(read_colorspace)
    write_node.setInput(0, read_node)

    nuke.execute(write_node, first_frame, last_frame)

    print(f"Read node created for sequence: {sequence_path}")
    print(f"Original range set to: {first_frame} - {last_frame}")


def legacy_Mov():
    parts = retrieved_item['path'].split('/')
    origin_directory_path = parts[-2]

    default_directory = os.path.dirname(retrieved_item['path'])
    default_file_name = os.path.basename(retrieved_item['path'])

    copy_path = convert_to_copy_path(retrieved_item["path"])
    temp_folder_path = os.path.join(copy_path, 'temp')
    temp_folder_path = temp_folder_path.replace('\\', '/')

    if not os.path.exists(temp_folder_path):
        os.makedirs(temp_folder_path)
        subprocess.call(['attrib', '+h', temp_folder_path])

    new_output_path = os.path.join(temp_folder_path, f'{origin_directory_path}_{default_file_name}')
    new_output_path = new_output_path.replace('\\', '/')

    # if os.path.isfile(new_output_path):
    #     print(f'This file({new_output_path}) is already exists.')
    # else:
    shutil.copy2(retrieved_item['path'], new_output_path)
    print(f'Copied {retrieved_item["path"]} to {new_output_path}')


if __name__ == '__main__':

    import os
    import nuke
    import json
    import re

    retrieved_items = json.loads(os.getenv('TEMP_PATH', ''))

    for retrieved_item in retrieved_items:

        parts = retrieved_item['path'].split('/')
        origin_directory_path = parts[-1]
        target_folder = None
        if os.path.isdir(retrieved_item['path']):
            parts = parts[-1].split('_')

        # Extract the necessary parts
        project_code = parts[0]
        seq_code = parts[1]
        shot_code = parts[1] + '_' + parts[2] + '_' + parts[3]
        category = parts[4]
        version = parts[5]

        # Extract version information from source path
        target_folder = os.path.join(
            r'X:\ShotGrid_Test_jw\Project',
            project_code,
            '04_SEQ',
            seq_code,
            shot_code,
            'Plates',
            category,
            version
        )
        temp_folder_path = os.path.join(target_folder, 'temp')
        temp_folder_path = temp_folder_path.replace('\\', '/')
        new_output_path = os.path.join(temp_folder_path, f'{origin_directory_path}.mov')
        new_output_path = new_output_path.replace('\\', '/')

        if not os.path.isfile(new_output_path):
            root = nuke.root()
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

            if retrieved_item['path'].endswith('.mov'):
                width = retrieved_item['metadata']['width']
                height = retrieved_item['metadata']['height']
                fps_value = retrieved_item['metadata']['fps']
                first_frame = retrieved_item['metadata']['first_frame']
                last_frame = retrieved_item['metadata']['last_frame']
                fps_number = retrieved_item['metadata']['fps']
                new_format = nuke.addFormat(f"{width} {height} 1 1 HD_{retrieved_item['path']}_{timestamp}")

                if retrieved_item['colorspace'] == 'ACES - ACES2065-1':
                    ACES_2065_1_Mov()
                elif retrieved_item['colorspace'] == 'ACES - ACEScg':
                    ACEScg_Mov()
                elif retrieved_item['colorspace'] == 'AlexaV3LogC':
                    AlexaV3_Mov()
                elif retrieved_item['colorspace'] == 'rec709':
                    rec709_Mov()
                elif retrieved_item['colorspace'] == 'sRGB':
                    sRGB_Mov()
                elif retrieved_item['colorspace'] == 'legacy':
                    legacy_Mov()

            else:
                file_list = os.listdir(retrieved_item['path'])
                not_mov_files = [f for f in file_list if f.endswith('.exr') or f.endswith('dpx')]

                if retrieved_item['metadata']['type'] == 'exr':
                    width = retrieved_item['metadata']['width']
                    height = retrieved_item['metadata']['height']
                    fps_value = retrieved_item['metadata']['fps']
                    fps_number = re.search(r'\((.*?)\)', fps_value).group(1)
                    new_format = nuke.addFormat(f"{width} {height} 1 1 HD_{retrieved_item['path']}_{timestamp}")
                    if retrieved_item['colorspace'] == 'ACES - ACES2065-1':
                        ACES_2065_1_Seq()
                    elif retrieved_item['colorspace'] == 'ACES - ACEScg':
                        ACEScg_Seq()
                    elif retrieved_item['colorspace'] == 'AlexaV3LogC':
                        AlexaV3_Seq()
                    elif retrieved_item['colorspace'] == 'rec709':
                        rec709_Seq()
                    elif retrieved_item['colorspace'] == 'sRGB':
                        sRGB_Seq()
                    elif retrieved_item['colorspace'] == 'legacy':
                        legacy_Seq()

                elif retrieved_item['metadata']['type'] == 'dpx':
                    width = retrieved_item['metadata']['width']
                    height = retrieved_item['metadata']['height']
                    fps_number = retrieved_item['metadata']['fps']
                    new_format = nuke.addFormat(f"{width} {height} 1 1 HD_{retrieved_item['path']}_{timestamp}")
                    if retrieved_item['colorspace'] == 'ACES - ACES2065-1':
                        ACES_2065_1_Seq()
                    elif retrieved_item['colorspace'] == 'ACES - ACEScg':
                        ACEScg_Seq()
                    elif retrieved_item['colorspace'] == 'AlexaV3LogC':
                        AlexaV3_Seq()
                    elif retrieved_item['colorspace'] == 'rec709':
                        rec709_Seq()
                    elif retrieved_item['colorspace'] == 'sRGB':
                        sRGB_Seq()
                    elif retrieved_item['colorspace'] == 'legacy':
                        legacy_Seq()
