import os
import re
import pymem
import keyboard
import pymem.process
from colorama import Fore, init

# Initialization Colorama
init()

statusWallHack = False

# Keyboard Key
key1 = 'f1'
key2 = 'f10'

def exit():
    print(Fore.RED + "Exit...")
    os.abort()

def wallhack():
    try:
        processCS = pymem.Pymem('csgo.exe')
        client = pymem.process.module_from_name(processCS.process_handle,'client.dll')
        clientModule = processCS.read_bytes(client.lpBaseOfDll, client.SizeOfImage)
        addr = client.lpBaseOfDll + re.search(rb'\x33\xC0\x83\xFA.\xB9\x20',clientModule).start() + 4
        processCS.write_uchar(addr, 2 if processCS.read_uchar(addr) == 1 else 1)
        processCS.close_process()
    except pymem.exception.ProcessNotFound:
        print(Fore.RED + 'csgo.exe не запущен!')
    except pymem.exception.ProcessError:
        print(Fore.RED + 'Ошибка доступа к процессу csgo.exe')
    except pymem.exception.ModuleNotFound:
        print(Fore.RED + 'Модуль не найден')
    except pymem.exception.MemoryReadError:
        print(Fore.RED + 'Ошибка Чтение Памяти')
    except pymem.exception.MemoryWriteError:
        print(Fore.RED + 'Ошибка записи в Память')
    except AttributeError:
        print(Fore.RED + 'Шаблон байта не найден')
    else:
        global statusWallHack
        statusWallHack = not statusWallHack
        print(Fore.GREEN + "WH ON" if statusWallHack else Fore.RED + "WH OFF")

if __name__ == '__main__':
    print(Fore.LIGHTMAGENTA_EX + f'''
        [{key1}] WH [{key2}] Exit
    ''')
    keyboard.add_hotkey(key1, wallhack)
    keyboard.add_hotkey(key2, exit)
    keyboard.wait()