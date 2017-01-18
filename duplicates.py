#!/usr/bin/python3
import os
import sys
from argparse import ArgumentParser
from collections import defaultdict


def get_file_size(file_path):
    '''
    Функция возвращает размер файла в байтах
    '''
    try:
        filesize = os.path.getsize(file_path)
        return filesize
    except FileNotFoundError as err:
        if os.name == 'nt':  # Костыль для обработки длинных имён в Windows
            externalpath = '\\\\?\\{}'.format(file_path)
            filesize = os.path.getsize(externalpath)
            return filesize
        else:
            raise  #todo: Проверить на ubuntu


def list_dir(dir_path):
    '''
    Функция для получения списка всех полных путей файлов из каталога
    '''
    files = []
    for root, dirname, filenames in os.walk(dir_path):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            real_filepath = os.path.abspath(os.path.realpath(filepath))
            files.append(real_filepath)
    return files


def make_dict_of_files(files_list):
    '''
    Функция составляет словарь из списка файлов
    Ключи словаря - имя файла
    Значения по ключам - набор полных путей каталогов,
        в котором найден этот файл
    '''
    file_dict = defaultdict(set)
    for filepath in files_list:
        file_dir, file_name = os.path.split(filepath)
        file_size = get_file_size(filepath)
        dict_key = (file_name, file_size)
        file_dict[dict_key].add(file_dir)
    return file_dict


def find_duplicates(files_list):
    '''
    Функция поиска дубликатов в списке файлов
    Возвращает словарь {filename: {fullpath,}
    '''
    keys_to_remove = []
    file_dict = make_dict_of_files(files_list)
    keys_to_remove = [f for f, s in file_dict.items() if len(s) == 1]
    for key in keys_to_remove:
        del file_dict[key]
    return file_dict


def print_duplicates(duplicates):
    '''
    Функция для вывода дубликатов на экран
    '''
    for filename, dirpath_list in duplicates.items():
        print('Идентичный файл [{}] в каталогах:'.format(filename[0]))
        for dirpath in dirpath_list:
            print('>> {}'.format(dirpath))
        print('--')


def main(dir_path):
    all_files_in_dir = list_dir(dir_path)
    print('Найдено {} файлов. Обрабатываем...'.format(len(all_files_in_dir)))
    duplicates = find_duplicates(all_files_in_dir)
    print_duplicates(duplicates)
    print('====')
    print('Всего найдено {} пар одинаковых файлов'.format(len(duplicates)))


if __name__ == '__main__':
    parser = ArgumentParser(description='Finds duplicates in folder')
    parser.add_argument('path_to_dir', help='an integer for the accumulator')
    args = parser.parse_args()

    dir_path = os.path.abspath(os.path.realpath(args.path_to_dir))
    if not os.path.isdir(dir_path):
        print('Такой папки не существует: {}. Попробуй ещё раз'.format(dir_path))
        sys.exit(-1)

    main(dir_path)
