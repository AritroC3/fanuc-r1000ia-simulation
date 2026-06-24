import os

def fix_urdf_paths(urdf_file):
    if not os.path.exists(urdf_file):
        print(f"ERROR: Cannot find URDF file at {urdf_file}")
        return

    with open(urdf_file, 'r') as file:
        urdf_content = file.read()

    original_content = urdf_content
    updated = False

    # Fix duplicated mesh folders
    bad_duplicate = '../meshes/r1000ia80f/r1000ia80f/'
    good_path = '../meshes/r1000ia80f/'
    if bad_duplicate in urdf_content:
        urdf_content = urdf_content.replace(bad_duplicate, good_path)
        print("Success: Fixed the duplicated 'r1000ia80f' mesh paths!")
        updated = True

    # Fix standard package string
    search_str = 'package://fanuc_r1000ia_support/meshes/'
    if search_str in urdf_content:
        urdf_content = urdf_content.replace(search_str, '../meshes/')
        print("Success: Mapped standard mesh paths correctly.")
        updated = True

    # Fix alternate package string
    search_str_alt = 'package://fanuc_description/meshes/'
    if search_str_alt in urdf_content:
        urdf_content = urdf_content.replace(search_str_alt, '../meshes/')
        print("Success: Mapped alternate mesh paths correctly.")
        updated = True

    if not updated:
        print("Paths look clean or have already been updated.")
        return

    with open(urdf_file, 'w') as file:
        file.write(urdf_content)

if __name__ == "__main__":
    urdf_path = os.path.join('assets', 'fanuc_r1000ia_support', 'urdf', 'r1000ia80f.urdf')
    fix_urdf_paths(urdf_path)