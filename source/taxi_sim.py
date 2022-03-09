import argparse
import collections
import queue
import random

DEFAULT_NUMBER_OF_TAXIS = 3
DEFAULT_END_TIME = 180
SEARCH_DURATION = 5
TRIP_DURATION = 20
DEPARTURE_INTERVAL = 5

Event = collections.namedtuple('Event', 'time proc action')


# BEGIN TAXI_PROCESS
def taxi_process(ident, trips, start_time=0):
    """
    Отдает модели события при каждом изменении состояния
    * taxi_process -- вызывается один раз для каждого такси и
      создаёт объект-генератор, представляющий его действия.
    * ident -- это номер такси.
    * trips -- сколько поездок должен совершить такси перед
      тем как вернуться в гараж.
    * start_time -- когда такси выезжает из гаража.
    """
    time = yield Event(start_time, ident, 'leave garage')
    """
    Первый отданный объект Event -- 'leave garage'
    Выполнение сопрограммы приостанавливается, так что главный
    цикл моделирования может перейти к следующему запланированному
    событию. Когда настанет время возобновить процесс, главный цикл
    отправит (методом send) текущее модельное время, которое будет
    присвоено переменной time.
    """
    for i in range(trips):
        # этот блок повторяется по одному разу для каждой поездки.
        time = yield Event(time, ident, 'pick up passenger')
        """
        Отдает событие посадки пассажира. Здесь сопрограмма 
        приостанавливается. Когда настанет время возобновить этот
        процесс, главный цикл снова отправит текущее время.        
        """
        time = yield Event(time, ident, 'drop off passenger')
        """
        Отдает событие высадки пассажира. Сопрограмма снова 
        приостанавливается и ждёт, когда главный цикл отправит 
        ее время возобновления.
        """

    yield Event(time, ident, 'going home')
    """
    Цикл for заканчивается после заданного числа поездок и отдает
    последнее событие 'going home'. Сопрограмма приостанавливается
    в последний раз. При возобновлении она получит от главного цикла
    модельное время, но я не присваиваю его никакой переменной, 
    потому что оно не будет использоваться.
    """
# END TAXI_PROCESS


# BEGIN TAXI_SIMULATOR
class Simulator:

    def __init__(self, proc_map):
        """
        Очередь PriorityQueue для хранения запланированных событий,
        упорядоченная по возрастанию времени.

        :param proc_map: словарь, для построения локальной копии,
        потому что по ходу моделирования каждое такси, возвращающееся
        в гараж, удаляется из self.procs, а мы не хотим изменять объект,
        переданный пользователем
        """
        self.events = queue.PriorityQueue()
        self.procs = dict(proc_map)

    def run(self, end_time):
        """
        Планирует и отображает события, пока не истечёт время.
        :param: end_time: окончание модельного времени -- единственный
        обязательный аргумент run.
        """
        # планируем первое событие для каждой машины
        for _, proc in sorted(self.procs.items()):
            """
            Используя функцию sorted для выборки элементов self.proc,
            упорядоченных по ключу; сам ключ нам не важен, поэтому
            присваиваем его переменной _.
            """
            first_event = next(proc)
            """
            Данный вызов инициализирует каждую сопрограмму, заставляя
            её дойти до первого предложения yield, после чего ей можно
            посылать данные. Отдаётся объект event.
            """
            self.events.put(first_event)
            """
            Помещаем каждое событие в очередь с приоритетами self.events.
            Первым событием для каждого такси является `leave garage`.  
            """

        sim_time = 0                # обнуляем часы модельного времени
        while sim_time < end_time:
            # Главный цикл моделирования: выполнять, пока sim_time меньше end_time.
            if self.events.empty():
                print('*** end of events ***')
                # Выход из цикла по окончанию событий в очереди.
                break

            current_event = self.events.get()
            # Получаем из очереди объект Event с наименьшим значением time.

            sim_time, proc_id, previous_action = current_event
            # Распаковываем кортеж Event.

            print('taxi: ', proc_id, proc_id * ' ', current_event)
            # Распечатываем объект Event.

            active_proc = self.procs[proc_id]
            # Извлекаем сопрограмму для активного такси из словаря self.procs.

            next_time = sim_time + compute_duration(previous_action)
            # Вычисляем время следующего возобновления, складывая sim_time и
            # результат вызова функции compute_duration(...) для предыдущего действия.

            try:
                next_event = active_proc.send(next_time)
                # Отправляем time сопрограмме такси. Сопрограмма отдаст
                # next_event или возбудит исключение
            except StopIteration:
                del self.procs[proc_id]
                # Удаляем событие из словаря, если возникло исключение.
            else:
                self.events.put(next_event)
                # В противном случае помещаем next_event в очередь.
        else:
            msg = '*** end of simulation time: {} events pending ***'
            print(msg.format(self.events.qsize()))
            # Если произошел выход из цикла в связи с истечением времени,
            # печатаем количество оставшихся в очереди событий.
# END TAXI_SIMULATOR


def compute_duration(previous_action):
    """Вычисляет длительность действия, пользуясь экспоненциальным распределением"""
    if previous_action in ['leave garage', 'drop off passenger']:
        # новое состояние -> поиск пассажира
        interval = SEARCH_DURATION
    elif previous_action == 'pick up passenger':
        # новое состояние -> поездка
        interval = TRIP_DURATION
    elif previous_action == 'going home':
        interval = 1
    else:
        raise ValueError(f'Unknown previous_action: {previous_action}')
    return int(random.expovariate(1/interval))


def main(end_time=DEFAULT_END_TIME, num_taxis=DEFAULT_NUMBER_OF_TAXIS, seed=None):
    """Инициализирует генератор случайных чисел, строит proc-объекты и запускает моделирование"""
    if seed is not None:
        random.seed(seed)   # чтобы получать воспроизводимые результаты

    taxis = {i: taxi_process(i, (i+1)*2, i*DEPARTURE_INTERVAL) for i in range(num_taxis)}

    sim = Simulator(taxis)
    sim.run(end_time)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Taxi fleet simulator.')
    parser.add_argument('-e', '--end-time', type=int, default=DEFAULT_END_TIME,
                        help=f'simulation end time; default = {DEFAULT_END_TIME}')
    parser.add_argument('-t', '--taxis', type=int, default=DEFAULT_NUMBER_OF_TAXIS,
                        help=f'number of taxis running; default = {DEFAULT_NUMBER_OF_TAXIS}')
    parser.add_argument('-s', '--seed', type=int, default=None, help='random generator seed (for testing)')
    args = parser.parse_args()
    main(args.end_time, args.taxis, args.seed)


"""
$ python3 taxi_sim.py -s 3 -e 120
taxi:  0  Event(time=0, proc=0, action='leave garage')
taxi:  0  Event(time=1, proc=0, action='pick up passenger')
taxi:  1   Event(time=5, proc=1, action='leave garage')
taxi:  1   Event(time=7, proc=1, action='pick up passenger')
taxi:  2    Event(time=10, proc=2, action='leave garage')
taxi:  2    Event(time=14, proc=2, action='pick up passenger')
taxi:  2    Event(time=15, proc=2, action='drop off passenger')
taxi:  2    Event(time=15, proc=2, action='pick up passenger')
taxi:  0  Event(time=16, proc=0, action='drop off passenger')
taxi:  0  Event(time=17, proc=0, action='pick up passenger')
taxi:  0  Event(time=22, proc=0, action='drop off passenger')
taxi:  1   Event(time=25, proc=1, action='drop off passenger')
taxi:  1   Event(time=28, proc=1, action='pick up passenger')
taxi:  0  Event(time=49, proc=0, action='going home')
taxi:  2    Event(time=51, proc=2, action='drop off passenger')
taxi:  2    Event(time=56, proc=2, action='pick up passenger')
taxi:  2    Event(time=59, proc=2, action='drop off passenger')
taxi:  1   Event(time=64, proc=1, action='drop off passenger')
taxi:  2    Event(time=64, proc=2, action='pick up passenger')
taxi:  1   Event(time=74, proc=1, action='pick up passenger')
taxi:  2    Event(time=78, proc=2, action='drop off passenger')
taxi:  2    Event(time=83, proc=2, action='pick up passenger')
taxi:  2    Event(time=84, proc=2, action='drop off passenger')
taxi:  2    Event(time=91, proc=2, action='pick up passenger')
taxi:  1   Event(time=101, proc=1, action='drop off passenger')
taxi:  1   Event(time=102, proc=1, action='pick up passenger')
taxi:  1   Event(time=102, proc=1, action='drop off passenger')
taxi:  2    Event(time=108, proc=2, action='drop off passenger')
taxi:  2    Event(time=111, proc=2, action='going home')
taxi:  1   Event(time=112, proc=1, action='going home')
*** end of events ***
"""