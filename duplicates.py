import sys
import os
from optparse import OptionParser

def are_files_duplicates(file_path1, file_path2):
    file_path1_name = os.path.split(file_path1)[1]
    file_path2_name = os.path.split(file_path2)[1]
    if file_path1_name == file_path2_name:
        if os.path.getsize(file_path1) == os.path.getsize(file_path2):
            return True
    return False

def list_dirtree(dir_path):
    files = []
    for root, dirname, filenames in os.walk(dir_path):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files

def find_dublicates(files_list):
    counter = 0
    for file_path1 in files_list:
        for file_path2 in files_list:
            if file_path1 == file_path2:
                continue
            elif are_files_duplicates(file_path1, file_path2):
                counter += 1
                file1 = os.path.split(file_path1)
                file2 = os.path.split(file_path2)
                print(u'[!] Найдены одинаковые файлы {} в каталогах:\n {}\n {}\n'.format(file1[1], file1[0], file2[0]))
    return counter


def main(dir_path):
    all_files_in_dir = list_dirtree(dir_path)
    print(u'Найдено {} файлов. Обрабатываем...'.format(len(all_files_in_dir)))
    counter = find_dublicates(all_files_in_dir)
    print(u'====')
    print(u'Всего найдено {} пар одинаковых файлов'.format(counter))


if __name__ == '__main__':
    usage = 'Usage: %prog dir_path'
    parser = OptionParser(usage=usage)

    options, arguments = parser.parse_args()

    if len(arguments) != 1:
        print(u'Необходимо передать путь к директории. Попробуй ещё раз')
        sys.exit(-1)

    dir_path = os.path.abspath(os.path.realpath(arguments[0]))
    if not os.path.isdir(dir_path):
        print(u'Такой папки не существует! Давай по-другому')
        sys.exit(-1)

    main(dir_path)