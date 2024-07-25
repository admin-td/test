import subprocess


def ACES_2065_1():
    not_mov_files.sort()
    first_file = not_mov_files[0]
    match = re.search(r'(.*?)(\d+)\.(dpx|exr)$', first_file)
    prefix = match.group(1)
    number_str = match.group(2)
    suffix = match.group(3)
    num_digits = len(number_str)
    format_specifier = f"%0{num_digits}d"
    width = retrieved_item['metadata']['width']
    height = retrieved_item['metadata']['height']
    sequence_path = os.path.join(retrieved_item['path'], f"{prefix}{format_specifier}.{suffix}")
    sequence_path = sequence_path.replace('\\', '/')
    fps_value = retrieved_item['metadata']['fps']
    fps_number = re.search(r'\((.*?)\)', fps_value).group(1)
    new_format = nuke.addFormat(f"{width} {height} 1 1 HD")

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
        write_node['raw'].setValue(True)
        write_node.setInput(0, ocio_node)

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

        if not_mov_files:
            if retrieved_item['metadata']['type'] == 'exr':
                # colorspace가 ACES_2065-1 인경우
                ACES_2065_1()

            elif retrieved_item['type'] == 'dpx':
                not_mov_files.sort()

                first_file = not_mov_files[0]
                match = re.search(r'(.*?)(\d+)\.(dpx|exr)$', first_file)
                prefix = match.group(1)
                number_str = match.group(2)
                suffix = match.group(3)
                num_digits = len(number_str)
                format_specifier = f"%0{num_digits}d"
                width = int(retrieved_item['metadata']['width'])
                print(f'test: {width}')
                sequence_path = os.path.join(retrieved_item['path'], f"{prefix}{format_specifier}.{suffix}")
                sequence_path = sequence_path.replace('\\', '/')

                new_format = nuke.addFormat(f"{width} 2160 1 1 HD")

                first_frame = int(number_str)
                last_frame = first_frame + len(not_mov_files) - 1

                root['first_frame'].setValue(first_frame)
                root['last_frame'].setValue(last_frame)
                root['fps'].setValue(23.976)
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
                    write_node['mov64_fps'].setValue(23.976)
                    write_node['raw'].setValue(True)
                    write_node.setInput(0, ocio_node)

                    nuke.execute(write_node, first_frame, last_frame)

                    print(f"@@@@@: {retrieved_item['metadata']}")
                    print(f"Read node created for sequence: {sequence_path}")
                    print(f"Original range set to: {first_frame} - {last_frame}")
