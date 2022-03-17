from concurrent import futures

from flags_threadpool import download_one, main


def download_many(cc_list):
    cc_list = cc_list[:5]
    # Для этой демонстрации мы ограничимся только пятью странами
    # с самым большим населением
    with futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Устанавливаем значение max_workers равным 3, чтобы
        # можно было следить за ожидающими будущими объектами
        # в распечатке.
        to_do = []
        for cc in sorted(cc_list):
            # Обходим коды стран в алфавитном порядке, чтобы
            # было понятно, что результат поступает не по порядку.
            future = executor.submit(download_one, cc)
            # Данный метод планирует выполнение вызываемого объекта
            # и возвращает будущий объект, представляющий ожидающую
            # операцию.
            to_do.append(future)
            # Сохраняем каждый будущий объект, чтобы впоследствии
            # его можно было извлечь с помощью as_completed()
            msg = 'Scheduled for {}: {}'
            print(msg.format(cc, future))
            # Делаем вывод с кодом страны и будущим объектом.

        results = []
        for future in futures.as_completed(to_do):
            # as_completed() отдаст будущие объекты по мере их завершения.
            res = future.result()
            # Получаем результат этого объекта futures.
            msg = '{} result: {!r}'
            print(msg.format(future, res))
            # Отображаем объект future и результат его выполнения.
            results.append(res)
    return len(results)


if __name__ == '__main__':
    main(download_many)
