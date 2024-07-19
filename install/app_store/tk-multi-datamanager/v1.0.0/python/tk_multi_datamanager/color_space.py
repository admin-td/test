

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

    folder_path = r'X:/ShotGrid_Test_jw/Project/test/scan/240715/test_001_0010_org_v001/'
    file_list = os.listdir(folder_path)
    exr_files = [f for f in file_list if f.endswith('.exr')]
    root = nuke.root()


    if exr_files:
        exr_files.sort()

        first_file = exr_files[0]
        first_file_path = os.path.join(folder_path, first_file)

        name_parts = first_file.split('.')
        prefix = '.'.join(name_parts[:-2])
        suffix = name_parts[-1]

        sequence_path = os.path.join(folder_path, f"{prefix}.%04d.{suffix}")
        sequence_path = sequence_path.replace('\\', '/')

        width, height = get_exr_format(first_file_path)
        read_node = nuke.createNode('Read')

        read_node['file'].setValue(sequence_path)

        first_frame = int(name_parts[-2])
        last_frame = first_frame + len(exr_files) - 1

        read_node['first'].setValue(first_frame)
        read_node['last'].setValue(1002)
        read_node['origfirst'].setValue(first_frame)
        read_node['origlast'].setValue(1002)
        # 프레임 범위 설정
        root['first_frame'].setValue(first_frame)
        root['last_frame'].setValue(1002)

        format_string = f"{width} {height} 0 0 {width} {height} 1 HD"
        #    read_node['format'].setValue(format_string)

        write_node = nuke.createNode('Write')
        output_path = r'X:/ShotGrid_Test_jw/Project/test/scan/240715/rendered_output.mov'
        write_node['file'].setValue(output_path)

        write_node['file_type'].setValue('mov')

        write_node.setInput(0, read_node)
        #    update_write_node_paths(write_node)

        #    nuke.execute(write_node, first_frame, last_frame)

        print(f"Read node created for sequence: {sequence_path}")
        print(f"Original range set to: {first_frame} - {last_frame}")
    else:
        print("No EXR files found in the specified folder.")
