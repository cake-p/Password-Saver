from os import system
from os.path import exists
from json import loads
from sys import exit
from src.AESCipher import AESCipher
from msvcrt import getch
from src import lib


def main():
    title = 'Password Saver v1.3'
    system('title ' + title)
    system('cls')
    print(title + '\n\nЗагрузка данных...')
    if exists('data'):
        if exists('data.key'):
            with open('data.key', 'rb') as f:
                crypto = AESCipher(f.read())
        else:
            print('Введите пароль: ', end='')
            crypto = AESCipher(lib.getpass().encode('utf8'))
    else:
        crypto = lib.create_data()
        if not crypto:
            exit()
        
    with open("data", "rb") as f:
        try:
            data = loads(crypto.decrypt(f.read()))
            if isinstance(data, list):
                for i, value in enumerate(data):
                    data[i]['login'] = False
                lib.data_save(crypto, data)
            else:
                data = data['data']
        except:
            print('Неверный пароль!')
            exit()

    system('cls')
    while True:
        system('cls')
        print('Главное меню\n\n1. Генерация нового пароля\n2. Добавление существующего пароля в список\n'
              '3. Список паролей\n4. Создать резервную копию данных\n5. Настройки\n0. Выход')
        get = getch()
        if get == b'1':
            lib.passwd_generate(crypto, data)
        elif get == b'2':
            lib.passwd_add(crypto, data)
        elif get == b'3':
            lib.passwd_list(crypto, data)
        elif get == b'4':
            lib.passwd_backup(crypto, data)
        elif get == b'5':
            lib.passwd_settings(data)
        elif get == b'0':
            with open("data", "rb") as fr:
                with open("data.last.backup", "wb") as fw:
                    fw.write(fr.read())
            exit()
