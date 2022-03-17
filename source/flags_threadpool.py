from concurrent import futures

from flags import save_flag, get_flag, show, main
# используем некоторые функции из flags.py

MAX_WORKERS = 20
# максимальное количество потоков в объекте ThreadPoolExecutor


def download_one(cc):
    # Функция, загружающая одно изображение,
    # её будет исполнять каждый поток.
    image = get_flag(cc)
    show(cc)
    save_flag(image, f'{cc.lower()}.gif')
    return cc


def download_many(cc_list):
    # Устанавливаем количество рабочих потоков:
    # используем минимум из наибольшего допустимого
    # числа потоков и фактического числа подлежащих
    # обработке элементов, что бы не создавать лишних потоков
    workers = min(MAX_WORKERS, len(cc_list))
    with futures.ThreadPoolExecutor(workers) as executor:
        # создаем экземпляр ThreadPoolExecutor с таким числом
        # рабочих потоков; метод executor.__exit__ вызовет
        # executor.shutdown(wait=True), который блокирует
        # выполнение программы до завершения всех потоков.
        res = executor.map(download_one, sorted(cc_list))
        # функция map похож на встроенную map с тем
        # исключением, что функция download_one параллельно
        # вызывается из нескольких потоков; он возвращает
        # генератор, который можно обойти для получения
        # значений, возвращённых каждой функцией.
    return len(list(res))
    # Возвращаем количество полученных результатов.
    # Если функция в каком-то потоке возбудила исключение,
    # то оно возникает в этом месте, когда не явный вызов
    # next() попытается получить соответствующее значение
    # от итератора


if __name__ == '__main__':
    # Вызываем функцию main из модуля flags, передавая
    # ей усовершенствованную функцию download_many.
    main(download_many)
