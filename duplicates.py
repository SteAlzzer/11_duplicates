import os
import sys


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
            print('По каким-то причинам не удалось открыть файл. Ошибка: {}'
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

    !!!
    Коментарий проверяющего:
    >> Алгоритм неоптимален - сравниваешь каждый файл с каждым. Вместо этого используй составной ключ - tuple из имени файла и его размера.
    Делал так сначала, но наличие функции are_files_duplicates() сбивает столку. Ведь она подразумевает, что нужно сравнивать два файла.
    Сравниваем по имени и размеру, как говорится в условии.
    А при использовании составного ключа (filename, size) это как-бы выполняется автоматически.
    !!!
    '''
    file_dict = {}  # tuple(filename, size): {fullpath,}
    for filepath in files_list:
        filename_split = os.path.split(filepath)
        filesize = get_file_size(filepath)
        if (filename_split[1], filesize) not in file_dict:
            file_dict[(filename_split[1], filesize)] = {filename_split[0]}
        else:
            file_dict[(filename_split[1], filesize)].add(filename_split[0])
    return file_dict


def find_duplicates(files_list):
    '''
    Функция поиска дубликатов в списке файлов
    Возвращает словарь {filename: {fullpath,}
    '''
    duplicates = {}
    file_dict = make_dict_of_files(files_list)

    for file, dirpath_list in file_dict.items():
        if len(dirpath_list) > 1:
            if file not in duplicates:
                duplicates[file] = set(dirpath_list)

    return duplicates


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
    if len(sys.argv) != 2:
        print('Необходимо передать путь к директории. Попробуй ещё раз')
        sys.exit(-1)

    dir_path = os.path.abspath(os.path.realpath(sys.argv[1]))
    if not os.path.isdir(dir_path):
        print('Такой папки не существует: {}. Попробуй ещё раз'.format(dir_path))
        sys.exit(-1)

    main(dir_path)
