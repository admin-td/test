import subprocess
from datetime import datetime


def ACES_2065_1():
    not_mov_files.sort()
    first_file = not_mov_files[0]
    match = re.search(r'(.*?)(\d+)\.(dpx|exr)$', first_file)
    prefix = match.group(1)
    number_str = match.group(2)
    suffix = match.group(3)
    num_digits = len(number_str)
    format_specifier = f"%0{num_digits}d"
    sequence_path = os.path.join(retrieved_item['path'], f"{prefix}{format_specifier}.{suffix}")
    sequence_path = sequence_path.replace('\\', '/')
    fps_number = re.search(r'\((.*?)\)', fps_value).group(1)

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

    temp_folder_path = os.path.join(retrieved_item['path'], 'temp')
    temp_folder_path = temp_folder_path.replace('\\', '/')
    if not os.path.exists(temp_folder_path):
        os.makedirs(temp_folder_path)
        subprocess.call(['attrib', '+h', temp_folder_path])
    prefix = prefix[:-1]
    new_output_path = os.path.join(temp_folder_path, f'{prefix}.mov')
    new_output_path = new_output_path.replace('\\', '/')

    if os.path.isfile(new_output_path):
        print(f'This file({new_output_path}) is already exists.')
    else:
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

def ACEScg():
    not_mov_files.sort()
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
    root['monitorLut'].setValue('Rec.709')

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

    temp_folder_path = os.path.join(retrieved_item['path'], 'temp')
    temp_folder_path = temp_folder_path.replace('\\', '/')
    if not os.path.exists(temp_folder_path):
        os.makedirs(temp_folder_path)
        subprocess.call(['attrib', '+h', temp_folder_path])
    prefix = prefix[:-1]
    new_output_path = os.path.join(temp_folder_path, f'{prefix}.mov')
    new_output_path = new_output_path.replace('\\', '/')

    if os.path.isfile(new_output_path):
        print(f'This file({new_output_path}) is already exists.')
    else:
        write_node = nuke.createNode('Write')
        write_node['file_type'].setValue('mov')
        write_node['file'].setValue(new_output_path)
        write_node['mov64_fps'].setValue(float(fps_number))
        write_node['raw'].setValue(True)
        write_node['mov64_codec'].setValue('H.264')
        write_node['mov64_quality'].setValue('Custom')
        write_node.setInput(0, ocio_node)

        nuke.execute(write_node, first_frame, last_frame)

        print(f"Read node created for sequence: {sequence_path}")
        print(f"Original range set to: {first_frame} - {last_frame}")


def AlexaV3():
    not_mov_files.sort()
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

    temp_folder_path = os.path.join(retrieved_item['path'], 'temp')
    temp_folder_path = temp_folder_path.replace('\\', '/')
    if not os.path.exists(temp_folder_path):
        os.makedirs(temp_folder_path)
        subprocess.call(['attrib', '+h', temp_folder_path])
    prefix = prefix[:-1]
    new_output_path = os.path.join(temp_folder_path, f'{prefix}.mov')
    new_output_path = new_output_path.replace('\\', '/')

    if os.path.isfile(new_output_path):
        print(f'This file({new_output_path}) is already exists.')
    else:
        write_node = nuke.createNode('Write')
        write_node['file_type'].setValue('mov')
        write_node['file'].setValue(new_output_path)
        write_node['colorspace'].setValue('rec709')
        write_node.setInput(0, ocio_node)

        nuke.execute(write_node, first_frame, last_frame)

        print(f"Read node created for sequence: {sequence_path}")
        print(f"Original range set to: {first_frame} - {last_frame}")

def rec709():
    not_mov_files.sort()
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

    temp_folder_path = os.path.join(retrieved_item['path'], 'temp')
    temp_folder_path = temp_folder_path.replace('\\', '/')
    if not os.path.exists(temp_folder_path):
        os.makedirs(temp_folder_path)
        subprocess.call(['attrib', '+h', temp_folder_path])
    prefix = prefix[:-1]
    new_output_path = os.path.join(temp_folder_path, f'{prefix}.mov')
    new_output_path = new_output_path.replace('\\', '/')

    if os.path.isfile(new_output_path):
        print(f'This file({new_output_path}) is already exists.')
    else:
        write_node = nuke.createNode('Write')
        write_node['file_type'].setValue('mov')
        write_node['file'].setValue(new_output_path)
        write_node['colorspace'].setValue('rec709')
        write_node.setInput(0, read_node)

        nuke.execute(write_node, first_frame, last_frame)

        print(f"Read node created for sequence: {sequence_path}")
        print(f"Original range set to: {first_frame} - {last_frame}")


def sRGB():
    not_mov_files.sort()
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

    temp_folder_path = os.path.join(retrieved_item['path'], 'temp')
    temp_folder_path = temp_folder_path.replace('\\', '/')
    if not os.path.exists(temp_folder_path):
        os.makedirs(temp_folder_path)
        subprocess.call(['attrib', '+h', temp_folder_path])
    prefix = prefix[:-1]
    new_output_path = os.path.join(temp_folder_path, f'{prefix}.mov')
    new_output_path = new_output_path.replace('\\', '/')

    if os.path.isfile(new_output_path):
        print(f'This file({new_output_path}) is already exists.')
    else:
        write_node = nuke.createNode('Write')
        write_node['file_type'].setValue('mov')
        write_node['file'].setValue(new_output_path)
        write_node['colorspace'].setValue('sRGB')
        write_node.setInput(0, read_node)

        nuke.execute(write_node, first_frame, last_frame)

        print(f"Read node created for sequence: {sequence_path}")
        print(f"Original range set to: {first_frame} - {last_frame}")


if __name__ == '__main__':

    import os
    import nuke
    import json
    import re

    retrieved_list = json.loads(os.getenv('TEMP_PATH', ''))

    for retrieved_item in retrieved_list:

        file_list = os.listdir(retrieved_item['path'])
        not_mov_files = [f for f in file_list if f.endswith('.exr') or f.endswith('dpx')]
        root = nuke.root()
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        if not_mov_files:
            if retrieved_item['metadata']['type'] == 'exr':
                width = retrieved_item['metadata']['width']
                height = retrieved_item['metadata']['height']
                fps_value = retrieved_item['metadata']['fps']
                fps_number = re.search(r'\((.*?)\)', fps_value).group(1)
                new_format = nuke.addFormat(f"{width} {height} 1 1 HD_{retrieved_item['path']}_{timestamp}")
                if retrieved_item['colorspace'] == 'ACES - ACES2065-1':
                    ACES_2065_1()
                elif retrieved_item['colorspace'] == 'ACES - ACEScg':
                    ACEScg()
                elif retrieved_item['colorspace'] == 'AlexaV3LogC':
                    AlexaV3()
                elif retrieved_item['colorspace'] == 'rec709':
                    rec709()
                elif retrieved_item['colorspace'] == 'sRGB':
                    sRGB()

            elif retrieved_item['metadata']['type'] == 'dpx':
                width = retrieved_item['metadata']['width']
                height = retrieved_item['metadata']['height']
                fps_number = retrieved_item['metadata']['fps']
                new_format = nuke.addFormat(f"{width} {height} 1 1 HD_{retrieved_item['path']}_{timestamp}")
                if retrieved_item['colorspace'] == 'ACES - ACES2065-1':
                    ACES_2065_1()
                elif retrieved_item['colorspace'] == 'ACES - ACEScg':
                    ACEScg()
                elif retrieved_item['colorspace'] == 'AlexaV3LogC':
                    AlexaV3()
                elif retrieved_item['colorspace'] == 'rec709':
                    rec709()
                elif retrieved_item['colorspace'] == 'sRGB':
                    sRGB()