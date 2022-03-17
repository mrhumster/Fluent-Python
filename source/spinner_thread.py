import itertools
import sys
import threading
import time


class Signal:
    go = True


def spin(msg, signal):
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))
        # \x08 -- символ забоя, возвращает курсор назад
        time.sleep(.1)
        if not signal.go:
            break
    write(' ' * len(status) + '\x08' * len(status))


def slow_function():
    # имитируем длительную операцию ввода-вывода
    time.sleep(5)
    """
    Данный вызов блокирует главный поток, но GIL
    освобождается,  так  что  второй поток может 
    работать далее. 
    """
    return 42


def supervisor():
    signal = Signal()

    spinner = threading.Thread(
        target=spin,
        args=('Thinking!', signal)
    )
    print('spinner object:', spinner)
    spinner.start()     # Запускаем второй поток
    result = slow_function()
    signal.go = False   # Сигналим для остановки
    spinner.join()      # Ожидаем завершения 2-го потока
    return result


def main():
    result = supervisor()
    print('Answer:', result)


if __name__ == '__main__':
    main()