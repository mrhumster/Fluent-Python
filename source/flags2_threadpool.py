import collections
from concurrent import futures
import requests
import tqdm     # Импортируем библиотеку с индикатором хода выполнения

from flags2_common import main, HTTPStatus
from flags2_sequential import download_one

DEFAULT_CONCUR_REQ = 30
# Если  при  запуске не задан параметр -m/--max_req,  то принимаем такое
# максимальное  число одновременных запросов, оно и станет размером пула
# потоков. Фактическое число потоков может быть меньше, если загружается
# меньше флагов.
MAX_CONCUR_REQ = 1000
# Максимальное число одновременных запросов независимо от числа загружае-
# мых флагов и от значения параметра -m/--max_req; это  мера предосторож-
# ности.


def download_many(cc_list, base_url, verbose, concur_req):
    counter = collections.Counter()
    with futures.ThreadPoolExecutor(max_workers=concur_req) as executor:
        # Создаём  объект  executor  с параметром max_workers, равным величине
        # concur_req,   которую   функция   main   вычисляет  как  минимум  из
        # MAX_CONCUR_REQ, длины списка cc_list, и значения параметра командной
        # строки -m/--max_req.  Это позволяет избежать создания большего числа
        # потоков, чем необходимо.
        to_do_map = {}
        # Этот словарь отображает каждый экземпляр Future - представляющий одну
        # загрузку -  на  соответствующий  код страны для показа в сообщении об
        # ошибке
        for cc in sorted(cc_list):
            # Обходим список кодов стран в алфавитном порядке. Порядок результатов
            # зависит,  прежде  всего,  от  времени получения HTTP-ответа, но если
            # размер  пула  (определяемый  величиной  concur_req)  гораздо  меньше
            # len(cc_list),  то  может  оказаться,  что результаты возвращаются по
            # алфавиту.
            future = executor.submit(download_one, cc, base_url, verbose)
            # Каждое обращение к executor.submit планирует выполнение одного вызы-
            # ваемого объекта и возвращает экземпляр Future. Первый аргумент - сам
            # вызываемый объект, остальные - передаваемые ему аргументы.
            to_do_map[future] = cc
            # Сохраняем future и код страны в словаре.
        done_iter = futures.as_completed(to_do_map)
        # future.as_completed возвращает итератор, который отдаёт будущие объекты
        # по мере их завершения.
        if not verbose:
            # Если не установлен режим подробной информации, то обертываем результат
            # as_completed ф-ей tqdm, которая отображет индикатор хода выполнения;
            # поскольку у done_iter нет метода len, то мы должны сообщить tqdm
            # ожидаемое количество элементов в виде аргумента total=, что бы tqdm
            # могла оценить объем оставшейся работы.
            done_iter = tqdm.tqdm(done_iter, total=len(cc_list))
        for future in done_iter:
            # Обходим будущие объекты по мере их завершения.
            try:
                res = future.result()
                # Вызов метода result будущего объекта возвращает значение, полученное
                # от вызываемого объекта, или возбуждает исключение, которое было
                # перехвачено во время выполнения объекта. Этот метод может блокировать
                # программу в ожидании разрешения ситуации, но не в данном примере,
                # потому что as_completed возвращает только уже завершенные будущие
                # объекты.
            except requests.exceptions.HTTPError as exc:
                error_msg = f'HTTP {exc.response.status_code} -- {exc.response.reason}'
            except requests.exceptions.ConnectionError:
                error_msg = 'Connection error'
            else:
                error_msg = ''
                status = res.status

            if error_msg:
                status = HTTPStatus.error

            counter[status] += 1
            if verbose and error_msg:
                cc = to_do_map[future]
                print(f'*** Error for {cc}: {error_msg}')
    return counter


if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
