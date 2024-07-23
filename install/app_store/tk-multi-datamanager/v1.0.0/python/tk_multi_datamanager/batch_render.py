import subprocess


def get_exr_format(file_path):
    temp_node = nuke.createNode('Read', inpanel=False)
    temp_node['file'].setValue(file_path)
    width = temp_node.width()
    height = temp_node.height()
    nuke.delete(temp_node)
    return width, height


if __name__ == '__main__':

    import os
    import nuke
    import json
    import re
    retrieved_list = json.loads(os.getenv('TEMP_PATH', ''))

    for folder_path in retrieved_list:

        file_list = os.listdir(folder_path)
        not_mov_files = [f for f in file_list if f.endswith('.exr') or f.endswith('dpx')]
        root = nuke.root()

        if not_mov_files:
            not_mov_files.sort()

            first_file = not_mov_files[0]
            match = re.search(r'(.*?)(\d+)\.(dpx|exr)$', first_file)
            prefix = match.group(1)
            number_str = match.group(2)
            suffix = match.group(3)
            num_digits = len(number_str)
            format_specifier = f"%0{num_digits}d"

            sequence_path = os.path.join(folder_path, f"{prefix}{format_specifier}.{suffix}")
            sequence_path = sequence_path.replace('\\', '/')

            read_node = nuke.createNode('Read')

            read_node['file'].setValue(sequence_path)

            first_frame = int(number_str)
            last_frame = first_frame + len(not_mov_files) - 1

            read_node['first'].setValue(first_frame)
            read_node['last'].setValue(last_frame)
            read_node['origfirst'].setValue(first_frame)
            read_node['origlast'].setValue(last_frame)
            root['first_frame'].setValue(first_frame)
            root['last_frame'].setValue(last_frame)

            write_node = nuke.createNode('Write')

            temp_folder_path = os.path.join(folder_path, 'temp')
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
                write_node['file'].setValue(new_output_path)

                write_node['file_type'].setValue('mov')

                write_node.setInput(0, read_node)
                nuke.execute(write_node, first_frame, last_frame)

                print(f"Read node created for sequence: {sequence_path}")
                print(f"Original range set to: {first_frame} - {last_frame}")

