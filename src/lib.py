from msvcrt import getch
from os import system
from sys import stdout
from time import time
from json import dumps
from datetime import datetime
from src.AESCipher import AESCipher
from Crypto.Random.random import choice
from Crypto.Random import get_random_bytes


def passwd_change_login(crypto, data, data_id):
    system('cls')
    if data[data_id]['login']:
        print('Старый логин: ' + data[data_id]['login'] + '\n')
    print('Введите новый логин: ', end='')
    stdout.flush()
    data[data_id]['login'] = input()
    data_save(crypto, data)
    system('cls')
    print('Название изменено\n\nНажмите любую клавишу...')
    getch()


def data_save(crypto, data, name='data'):
    with open(name, "wb") as f:
        f.write(crypto.encrypt(dumps({
            'version': 2,
            'data': data,
        })))


def passwd_delete(crypto, data, data_id):
    system('cls')
    print('Для удаления пароля "' + data[data_id]['name'] + '" введите "удалить" без кавычек\n')
    if input().lower() != 'удалить':
        system('cls')
        print('Пароль НЕ удалён\n\nНажмите любую клавишу...')
        getch()
        return False

    del data[data_id]
    data_save(crypto, data)
    system('cls')
    print('Пароль удалён\n\nНажмите любую клавишу...')
    getch()


def passwd_first_in_list(crypto, data, data_id):
    passwd = data[data_id].copy()
    del data[data_id]
    data.insert(0, passwd)
    data_save(crypto, data)
    system('cls')
    print('Пароль перенесён в начало списка\n\nНажмите любую клавишу...')
    getch()


def passwd_change_passwd(crypto, data, data_id):
    system('cls')
    print('Старый пароль: ' + '*' * len(data[data_id]['passwd']) + '\nВведите новый пароль: ', end='')
    stdout.flush()
    passwd = getpass()
    
    system('cls')
    print('Введите его ещё раз: ', end='')
    stdout.flush()
    if passwd != getpass():
        print('Неверный пароль!\n\nНажмите любую клавишу...')
        getch()
        return False
        
    data[data_id]['passwd'] = passwd
    data_save(crypto, data)
    system('cls')
    print('Пароль изменён\n\nНажмите любую клавишу...')
    getch()


def passwd_change_name(crypto, data, data_id):
    system('cls')
    print('Старое название: ' + data[data_id]['name'] + '\nВведите новое название: ', end='')
    stdout.flush()
    data[data_id]['name'] = input()
    data_save(crypto, data)
    system('cls')
    print('Название изменено\n\nНажмите любую клавишу...')
    getch()


def create_data(data=[]):
    auto = False
    system('cls')
    while True:
        print('Вы можете придумать и ввести пароль или\nоставить поле пустым и доступ к паролям будет без пароля: ',
              end='')
        passwd = getpass()
        system('cls')
        if passwd == '':
            auto = True
            passwd = get_random_bytes(512)
            with open('data.key', 'wb') as f:
                f.write(passwd)
            break
        elif len(passwd) > 2:
            break
        else:
            system('cls')
            print('Длина пароля должна быть не меньше 3 символов!\n')
    if auto:
        crypto = AESCipher(passwd)
    else:
        print('Введите его ещё раз: ', end='')
        stdout.flush()
        if passwd != getpass():
            print('Неверный пароль!\n\nНажмите любую клавишу...')
            getch()
            return False
        crypto = AESCipher(passwd.encode('utf8'))
    data_save(crypto, data)
    return crypto


def passwd_settings(data):
    system('cls')
    print('Настройки\n\n1. Изменить пароль/data.key при входе в программу\n0. В главное меню')
    while True:
        get = getch()
        if get == b'1':
            if create_data(data):
                system('cls')
                print('Настройки изменены\n\nНажмите любую клавишу...')
                getch()
            break
        elif get == b'0':
            break


def passwd_backup(crypto, data):
    system('cls')
    try:
        name = 'data.' + str(int(time())) + '.backup'
        data_save(crypto, data, name)
        with open(name, 'rb') as f:
            crypto.decrypt(f.read())
        print('Резервная копия данных сохранена в ' + name)
    except:
        print('Ошибка: Не удалось сохранить резервную копию данных!')
    print('\nНажмите любую клавишу...')
    getch()


def passwd_generate(crypto, data):
    system('cls')
    passwd = {}
    print('Название для пароля: ', end='')
    passwd['name'] = input()
    print('Логин/почта (можно пропустить): ', end='')
    passwd['login'] = input()
    if passwd['login'] == '':
        passwd['login'] = False
    print('Использовать символы в пароле? По умолчанию, нет (y/n): ', end='')
    if input().lower() in ['y', 'yes', 'да', 'д']:
        symbols = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
                   'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
                   'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z',
                   'x', 'c', 'v', 'b', 'n', 'm', 'Q', 'W', 'E', 'R',
                   'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F',
                   'G', 'H', 'J', 'K', 'L', 'Z', 'X', 'C', 'V', 'B',
                   'N', 'M', '~', '!', '@', '#', '$', '%', '^', '&',
                   '*', '(', ')', '_', '+', '|', '`', '-', '=', '\\',
                   '"', '№', ';', ':', '?', '/', '[', ']', '{', '}',
                   '\'', '.', '>', ',', '<']
    else:
        symbols = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
                   'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
                   'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z',
                   'x', 'c', 'v', 'b', 'n', 'm', 'Q', 'W', 'E', 'R',
                   'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F',
                   'G', 'H', 'J', 'K', 'L', 'Z', 'X', 'C', 'V', 'B',
                   'N', 'M']
    print('Длина пароля. По умолчанию, 12: ', end='')
    length = input()
    if length.isdigit():
        length = int(length)
    else:
        length = 12
        
    while True:
        system('cls')
        passwd['passwd'] = ''
        for i in range(length):
            passwd['passwd'] = passwd['passwd'] + choice(symbols)
        print('Пароль: ' + passwd['passwd'] + '\nПересоздать? (y/n) ', end='')
        if input().lower() in ['n', 'no', 'н', 'нет', '']:
            break
    
    passwd['date'] = int(time())
    data.insert(0, passwd)
    data_save(crypto, data)
        
    
def passwd_add(crypto, data):
    system('cls')
    passwd = {}
    print('Добавление пароля\n\nНазвание для пароля: ', end='')
    passwd['name'] = input()
    print('Логин/почта (можно пропустить): ', end='')
    passwd['login'] = input()
    if passwd['login'] == '':
        passwd['login'] = False
    print('Введите пароль: ', end='')
    passwd['passwd'] = getpass()
    print('Введите пароль ещё раз: ', end='')
    if passwd['passwd'] != getpass():
        print('Неверный пароль!')
        getch()
    else:
        passwd['date'] = int(time())
        data.insert(0, passwd)
        data_save(crypto, data)


def passwd_show(crypto, data, data_id, show=False):
    passwd = data[data_id]
    system('cls')
    print('Название: ' + passwd['name'])
    if passwd['login']:
        print('Логин: ' + passwd['login'])
    print('Дата создания: ' + str(datetime.fromtimestamp(passwd['date']).strftime("%d.%m.%y %H:%M")))
    if show:
        print('Пароль: ' + passwd['passwd'])
        print('\n1. Скрыть пароль')
    else:
        print('Пароль: ' + '*' * len(passwd['passwd']))
        print('\n1. Показать пароль')
    print('2. Изменить название\n3. Изменить логин\n4. Изменить пароль\n'
          '5. Изменить дату (не работает)\n6. Поднять в списке\n7. Удалить\n0. В главное меню')
    while True:
        get = getch()
        if get == b'1':
            passwd_show(crypto, data, data_id, not show)
            break
        elif get == b'2':
            passwd_change_name(crypto, data, data_id)
            break
        elif get == b'3':
            passwd_change_login(crypto, data, data_id)
            break
        elif get == b'4':
            passwd_change_passwd(crypto, data, data_id)
            break
        # elif get == b'5':
        #    print('Не работает')
        elif get == b'6':
            passwd_first_in_list(crypto, data, data_id)
            break
        elif get == b'7':
            passwd_delete(crypto, data, data_id)
            break
        elif get == b'0':
            break


def passwd_list(crypto, data, j=0):
    system('cls')
    while True:
        print('Список паролей\n')
        i = 0
        l = len(data)
        # print(data)
        while True:
            if j*7+i > l-1 or i > 6:
                break
                
            print(str((i+1) % 8) + '. ' + data[j*7+i]['name'])
            i = i + 1
        if j > 0:
            print('8. Назад')
        if l > 7+j*7:
            print('9. Далее')
        print('0. В главное меню')
    
        get = getch()
        if get == b'1' and j*7+1 <= l:
            passwd_show(crypto, data, j*7)
            break
        elif get == b'2' and j*7+2 <= l:
            passwd_show(crypto, data, j*7+1)
            break
        elif get == b'3' and j*7+3 <= l:
            passwd_show(crypto, data, j*7+2)
            break
        elif get == b'4' and j*7+4 <= l:
            passwd_show(crypto, data, j*7+3)
            break
        elif get == b'5' and j*7+5 <= l:
            passwd_show(crypto, data, j*7+4)
            break
        elif get == b'6' and j*7+6 <= l:
            passwd_show(crypto, data, j*7+5)
            break
        elif get == b'7' and j*7+7 <= l:
            passwd_show(crypto, data, j*7+6)
            break
        elif get == b'8' and j > 0:
            passwd_list(crypto, data, j-1)
            break
        elif get == b'9' and l > 7+j:
            passwd_list(crypto, data, j+1)
            break
        elif get == b'0':
            return True
        else:
            system('cls')


def getpass(asterisk=True):
    stdout.flush()
    text = ''
    skip = False
    while True:
        get = getch()
        if skip:
            skip = False
            continue
        
        if get == b'\r':
            print()
            return text
        elif get == b'\x08':
            if len(text) > 0:
                text = text[:-1]
                stdout.write('\b \b')
                stdout.flush()
        elif get == b'\xe0' or get == b'\x00':
            skip = True
        elif get == b' ' or get == b'\x1b':
            continue
        else:
            try:
                char = get.decode('ascii')
                text = text + char
                if asterisk:
                    stdout.write('*')
                else:
                    stdout.write(char)
                stdout.flush()
            except:
                pass
