import itertools
import os
import sys
from optparse import OptionParser


def are_files_duplicates(file_path1, file_path2):
    '''
    Функция проверяет, являются ли два файла идентичными
    Сравнение основывается на имени файла и его размере в байтах
    '''
    try:
        if os.path.getsize(file_path1) == os.path.getsize(file_path2):
            return True
    except FileNotFoundError as err:
        if os.name == 'nt':  # Костыль для обработки длинных имён в Windows
            externalpath1 = '\\\\?\\{}'.format(file_path1)
            externalpath2 = '\\\\?\\{}'.format(file_path2)
            if os.path.getsize(externalpath1) == \
               os.path.getsize(externalpath2):
                return True
        else:
            print(u'По каким-то причинам не удалось открыть файл. Ошибка: {}'
                  .format(err))


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
    Значения по ключам - список полных путей каталогов,
        в котором найден этот файл
    '''
    file_dict = {}  # filename: [fullpath,]
    for filepath in files_list:
        filename_split = os.path.split(filepath)
        if filename_split[1] not in file_dict:
            file_dict[filename_split[1]] = [filename_split[0]]
        else:
            file_dict[filename_split[1]].append(filename_split[0])
    return file_dict


def find_duplicates(files_list):
    '''
    Функция поиска дубликатов в списке файлов
    Возвращает кортеж из (имя_файла, путь_к_каталогу_1, путь_к_каталогу_2)
    '''
    duplicates = []
    file_dict = make_dict_of_files(files_list)

    for file in file_dict:
        if len(file_dict[file]) > 1:
            for couple_of_pathes in itertools.combinations(file_dict[file], 2):
                if are_files_duplicates(os.path.join(couple_of_pathes[0], file),
                                        os.path.join(couple_of_pathes[1], file)):
                    duplicates.append((file, couple_of_pathes[0],
                                      couple_of_pathes[1]))
    return duplicates


def print_duplicates(duplicates):
    '''
    Функция для вывода дубликатов на экран
    '''
    for dup in duplicates:
        print(u'Идентичный файл [{}] в каталогах:'.format(dup[0]))
        print(u'>> {}'.format(dup[1]))
        print(u'>> {}\n'.format(dup[2]))


def main(dir_path):
    all_files_in_dir = list_dir(dir_path)
    print(u'Найдено {} файлов. Обрабатываем...'.format(len(all_files_in_dir)))
    duplicates = find_duplicates(all_files_in_dir)
    print_duplicates(duplicates)
    print(u'====')
    print(u'Всего найдено {} пар одинаковых файлов'.format(len(duplicates)))


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
