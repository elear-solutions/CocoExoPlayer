import os
from pprint import pprint

source_folder = os.path.abspath('./ExoPlayer')
target_folder = os.path.abspath('./')


def get_target_file_path(source_file_path):
    source_file_replacer = 'com{0}google{0}android{0}exoplayer2'.format(os.path.sep)
    target_file_replacer = 'buzz{0}getcoco{0}exoplayer2'.format(os.path.sep)

    target_file_path = source_file_path
    target_file_path = target_file_path.replace(source_folder, target_folder)
    target_file_path = target_file_path.replace(source_file_replacer, target_file_replacer)

    return target_file_path


def write_to_file(file_path, lines):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, mode='w+', newline='', encoding='iso-8859-1') as file:
        file.writelines(lines)


def modify_lines(lines, file_name):
    modified_lines = []

    for line in lines:
        modified_line = line

        if '_com_google_android_exoplayer2_' in modified_line:
            raise Exception('.c or .h file not excluded')

        if 'settings.gradle' == file_name \
                and ('demo' in modified_line
                     or 'playbacktests' in modified_line):
            modified_line = '// ' + modified_line

        if ('core_settings.gradle' == file_name
            or 'build.gradle' == file_name) \
                and 'extension-' in modified_line:
            modified_line = '// ' + modified_line

        # package names in java & xml
        modified_line = modified_line.replace('com.google.android.exoplayer2', 'buzz.getcoco.exoplayer2')

        modified_lines.append(modified_line)

    return modified_lines


def read_from_file(file_path):
    print('editing file: {}'.format(file_path))

    with open(file_path, newline='', encoding='iso-8859-1') as file:
        return file.readlines()


def copy_contents(source_file_path, target_file_path):
    print('copying file: {}'.format(source_file_path))

    with open(source_file_path, mode='rb') as source:
        os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
        with open(target_file_path, mode='wb+') as destination:
            destination.write(source.read())


extensions = set([])
files_per_extension = {}

file_excludes = {'.git'}
folder_excludes = {'.git', '.github', 'demos', 'docs', 'extensions'}

# import shutil
# shutil.rmtree(target_folder, ignore_errors=True)

for root, dirs, files in os.walk(source_folder):
    dirs[:] = [d for d in dirs if d not in folder_excludes]
    files[:] = [f for f in files if f not in file_excludes]

    print('in directory: {}'.format(root))
    print('subdirectories: {}'.format(dirs))

    for file_name in files:

        # source files which need editing
        source_file_path = os.path.abspath(os.path.join(root, file_name))
        target_file_path = os.path.abspath(get_target_file_path(source_file_path))

        ignored_file_name, extension = os.path.splitext(file_name)
        extensions.add(extension)

        if files_per_extension.get(extension, None) is None:
            files_per_extension[extension] = []

        files_per_extension[extension].append(source_file_path)

        if '.java' == extension \
                or '.md' == extension \
                or '.glsl' == extension \
                or '.json' == extension \
                or '.txt' == extension \
                or '.gradle' == extension \
                or '.kt' == extension \
                or '.html' == extension \
                or '.js' == extension \
                or '.css' == extension \
                or '.scss' == extension \
                or '.xml' == extension \
                or '.yml' == extension \
                or '.html' == extension \
                or '.cpp' == extension \
                or '.cc' == extension \
                or '.h' == extension \
                or '.c' == extension:

            # reading the lines into a list
            lines = read_from_file(source_file_path)

            # getting the modified file path and modified lines
            lines = modify_lines(lines, file_name)

            # writing everything back
            write_to_file(target_file_path, lines)

        # binary files which just need copying
        else:
            copy_contents(source_file_path, target_file_path)

pprint('available extensions: {}'.format(extensions))
pprint('files per extension: {}'.format(files_per_extension))
