"""
Загружает флаги стран (с обработкой ошибок)

Sequential version

Sample run:

        $ python3 flags2_sequential.py -s DELAY b
        DELAY site: http://localhost:8002/flags
        Searching for 26 flags: from BA to BZ
        1 concurrent connection will be used.
        --------------------
        17 flags downloaded.
        9 not found.
        Elapsed time: 13.36s

"""
import collections

import requests
import tqdm

from flags2_common import main, save_flag, HTTPStatus, Result

DEFAULT_CONCUR_REQ = 1
MAX_CONCUR_REQ = 1


# BEGIN FLAGS2_BASIC_HTTP_FUNCTION
def get_flag(base_url, cc):
    """
    Функция get_flag не обрабатывает ошибки, она вызывает метод
    requests.Response.raise_for_status для любого кода HTTP,
    кроме 200.
    :param base_url:
    :param cc:
    :return:
    """
    url = f'{base_url}/{cc}/{cc}.gif'
    resp = requests.get(url)
    if resp.status_code != 200:
        resp.raise_for_status()
    return resp.content


def download_one(cc, base_url, verbose=False):
    """
    Функция download_one перехватывает исключение
    requests.exceptions.HTTPError, чтобы обработать
    ошибку с кодом 404 и только ее...
    :param cc: код страны,
    :param base_url: базовый URL для загрузки,
    :param verbose: признак подробного вывода.
    :return: именованый кортеж Result со статусом
    """
    try:
        image = get_flag(base_url, cc)
    except requests.exceptions.HTTPError as exc:
        res = exc.response
        if res.status_code == 404:
            # ...установив локальное состояние HTTPStatus.not_found;
            # HTTPStatus - это перечисление Enum, импортированное из
            # модуля flags2_common.
            status = HTTPStatus.not_found
        else:
            raise
    else:
        # Любое другое исключение типа HTTPError возбуждается повторно,
        # прочие исключения просто распространяются в вызывающую программу.
        save_flag(image, cc.lower() + '.gif')
        status = HTTPStatus.ok
        msg = 'OK'

    if verbose:
        # Если задан параметр -v/--verbose, то отображается сообщение,
        # содержащее код страны и состояние; именно так мы видим индикатор
        # хода выполненния в режиме вывода подробной информации.
        print(cc, msg)

    # Именованный кортеж Result, вохвращенный функцией download_one, включает
    # поле status со значением HTTPStatus.not_found или HTTPStatus.ok.
    return Result(status, cc)
# END FLAGS2_BASIC_HTTP_SEQUENTIAL


# BEGIN FLAGS2_DOWNLOAD_MANU_SEQUENTIAL
def download_many(cc_list, base_url, verbose, max_req):
    # Этот объект Counter подсчитывает количество загрузок с разными исходами:
    # HTTPStatus.ok, HTTPStatus.not_found, HTTPStatus.error.
    counter = collections.Counter()
    # В cc_iter хранится отсортированный по алфавиту список кодов стран,
    # полученных в виде аргументов.
    cc_iter = sorted(cc_list)
    if not verbose:
        # Если не задан режим подробной информации, то cc_iter передается функции
        # tdqm, которая возвращает итератор, отдающий элементы из cc_iter и
        # одновременно отображающий анимированный индикатор хода выполнения.
        cc_iter = tqdm.tqdm(cc_iter)
    for cc in cc_iter:
        # В этом цикле мы обходим cc_iter и...
        try:
            # ...производим загрузку, последовательно обращаясь к download_one/
            res = download_one(cc, base_url, verbose)
        except requests.exceptions.HTTPError as exc:
            # Относящиеся к HTTP исключения, возбуждённые функцией get_flag и не
            # обработанные в download_one, обрабатываются здесь.
            error_msg = f'HTTP error {exc.response.status_code} - {exc.response.reason}'
        except requests.exceptions.ConnectionError as exc:
            # Прочие относящиеся к сети исключения обрабатываются здесь. Все остальные
            # исключения аварийно завершают скрипт, потому что в функции flags2_common.main,
            # из которой вызывается download_many, нет блока try/except.
            error_msg = 'Connection error'
        else:
            # Если исключение не вышло за пределы download_one, то из именованного кортежа
            # HTTPStatus, возвращенного этой функцией, извлекается значение status.
            error_msg = ''
            status = res.status

        if error_msg:
            # Если произошла ошибка, устанавливаем соответствующее значение status.
            status = HTTPStatus.error
        # Увеличиваем счётчик, используя значение из перечисления HTTPStatus в качестве ключа.
        counter[status] += 1
        if verbose and error_msg:
            # При работе в режиме подробной информации отображаем сообщение
            # об ошибке для текущего кода страны, если таковое имеется.
            print(f'*** Error for {cc}: {error_msg}')
    # Возвращаем counter, что бы функция main могла вывести финальный отчёт.
    return counter
# END FLAGS2_DOWNLOAD_MANU_SEQUENTIAL


if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
