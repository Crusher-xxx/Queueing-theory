import math
from multipledispatch import dispatch
import matplotlib.pyplot as plt

plt.ion()  # Включить интерактивный режим работы с графиками


@dispatch(list, list, list)
def custom_prod(m, j, ρ):  # Вспомогательная функция
    result = 1
    for i in range(0, N):
        # Количество запросов не может превышать количество процессоров
        result *= math.factorial(m[i]) / math.factorial(m[i] - j[i]) * (ρ[i] ** j[i])
    return result


@dispatch(list)
def custom_prod(j):  # Вспомогательная функция
    result = 1
    for element in j:
        result *= math.factorial(element)
    return result


def probability_specific(j, l, m):  # Вероятность нахождения системы в состоянии j
    def recursive_sum(i, j):
        result = 0

        if i == N:
            # print(j)
            return math.factorial(l) / custom_prod(j) * custom_prod(m, j, ρ)

        for j[i] in range(0, m[i] + 1):
            result += recursive_sum(i + 1, j)

        return result

    # Передать копию списка, чтобы не модифицировать исходный
    return (math.factorial(l) / custom_prod(j) * custom_prod(m, j, ρ)) / recursive_sum(0, j[:])


def probability_specific2(j, m):  # Вероятность нахождения системы в состоянии j
    def product(j):
        result = 1
        for i in range(0, N):
            result *= ρ[i] ** j[i]
        # print(j, result)
        return result

    def recursive_sum(i, j):
        result = 0

        if i == N:
            # print(j, product(j))
            return product(j)

        for j[i] in range(0, m[i] + 1):
            result += recursive_sum(i + 1, j)

        return result

    return product(j) / recursive_sum(0, j[:])  # Передать копию списка, чтобы не модифицировать исходный


def probability_specific3(j, m):  # Вероятность нахождения системы в состоянии j
    def product(j):
        result = 1
        for i in range(0, N):  # Проходимся по каждому типу процессора

            # Вычисляем P0 — решение уравнения
            P0 = 0
            for ii in range(0, m[i] + 1):
                P0 += math.factorial(m[i]) / math.factorial(m[i] - ii) * (ρ[i] ** ii)
                # print(f'P{i} = {P0}')
            P0 = 1 / P0

            # Находим вероятность P(j[i]) через P0
            result *= (ρ[i] ** j[i]) * math.factorial(m[i]) / math.factorial(m[i] - j[i]) * P0
        # print(j, result)
        return result * math.factorial(sum(j)) / custom_prod(j)

    def recursive_sum(i, j):  # Перебрать все возможные комбинации запросов
        result = 0

        if i == N:  # Как только комбинация сформирована, вернуть результат для данной комбинации
            # print(j, product(j))
            return product(j)

        for j[i] in range(0, m[i] + 1):
            result += recursive_sum(i + 1, j)

        return result

    return product(j) / recursive_sum(0, j[:])  # Передать копию списка, чтобы не модифицировать исходный


def probability_general(l, m):  # Вероятность нахождения системы при длине очереди l
    def recursive_sum(i, j):
        result = 0

        if i == N:  # Если список закончился
            if sum(j) == l:  # Сумма запросов в списке должна равняться длине очереди
                # result = probability_specific(j, l, m)                                     # Аналитический метод
                result = probability_specific2(j, m)  # EXCEL
                # result = probability_specific3(j, m)                                       # Терсков
                # print(j)
            return result

        j[i] = 0
        while j[i] <= m[i] and j[i] <= l:  # j[i] стремится к l, но не может превышать m[i]
            result += recursive_sum(i + 1, j)
            j[i] += 1

        return result

    j = [0] * N  # Количество запросов от процессора каждого типа
    return recursive_sum(0, j)


def mean_queue_length(m):
    result = 0
    # for l in range(2, N + 1):     # TERSKOV
    for l in range(1, sum(m) + 1):  # PANFILOV
        result += probability_general(l, m) * (l - 1)
        # result += l
    # return result / sum(m)
    return result


def real_performance(i, mean_queue):  # Реальная производительность процессора типа i
    return 1 / (TO[i] + (1 + mean_queue) * τ[0])


def max_performance(i):  # Предельная производительность процессора типа i
    return 1 / (TO[i] + τ[0])


def relative_loss_factor(i, mean_queue):  # Коэффициент относительных потерь для процессора типа i
    # return max_performance(i) / real_performance(i, mean_queue)
    # return 1 + mean_queue * τ[i] / (TO[i] + τ[0])                                                           # TERSKOV
    return 1 + mean_queue * τ[i] / (TO[i] + τ[i])  # PANFILOV


def relative_performance(m, i, mean_queue):  # Относительная производительность процессора типа i
    # return (min(TO) / TO[i]) * m[i] / relative_loss_factor(i, mean_queue)                                   # TERSKOV
    return m[i] / relative_loss_factor(i, mean_queue)  # PANFILOV


def general_performance(m, mean_queue):  # Общая производительность системы
    result = 0
    for i in range(0, N):
        result += relative_performance(m, i, mean_queue)
    return result


def plot_graph_for(configuration, index, up_to):  # index — для процессоров какого типа строить график
    m = configuration.copy()
    # Контейнеры для хранения
    perf = []  # производительности
    m_index_values = []  # количества процессоров типа m[index]
    queue = []  # средней длины очереди

    P0 = []
    P1 = []

    # Вычисления
    for m[index] in range(0, up_to + 1):
        m_index_values.append(m[index])
        queue.append(mean_queue_length(m))
        perf.append(general_performance(m, queue[-1]))  # performance(queue[-1])   general_performance(m, queue[-1])
        print(f'{m[index]} finished')  # Отслеживать прогресс

        P0.append(probability_general(0, m))
        P1.append(probability_general(1, m))

    # Отрисовка графика
    fig = plt.figure()
    m[index] = 'x'  # Заменить количество подписью, чтобы было видно для какого процессора построен график
    fig.canvas.set_window_title(f'Конфигурация - {m}')
    # plt.title(f'Конфигурация - {m}')
    plt.xlabel(f'Количество процессоров m-{index + 1}')
    plt.ylabel('Производительность')

    plt.plot(m_index_values, perf)
    plt.show()

    # Вывод статистики
    print(
        '{:<4} {:<20} {:<24} {:<24} {:<24}'.format(f'm-{index}', 'Производительность', 'Ср. Длина очереди', 'P0', 'P1'))
    for m_index_values, perf, queue, P0, P1 in zip(m_index_values, perf, queue, P0, P1):
        print('{:<4} {:<20} {:<24} {:<24} {:<24}'.format(m_index_values, perf, queue, P0, P1))


if __name__ == "__main__":
    # Необходимо задать перед вычислениями  <--- ОБЯЗАТЕЛЬНО
    m = [3, 3]  # Количество процессоров каждого типа
    N = len(m)  # Количество процессоров разных типов

    TO = [0.66, 8, 57]  # Время выполнения операций
    τ = [1.2, 1.2, 1.2]  # Время цикла оперативной памяти
    ξ = 0.35  # Коэффициент связности

    # Данные значения будут вычислены на основе введенных выше
    ν = [ξ / (TO + ξ * τ) for TO, τ in zip(TO, τ)]  # Параметр интенсивности
    μ = [1 / τ for τ in τ]  # Параметр обслуживания
    ρ = [ν / μ for ν, μ in zip(ν, μ)]

    # m = [1, 1, 1] # Количество процессоров каждого типа
    # N = len(m) # Количество процессоров разных типов
    # probabilities = []
    # nodes = []
    # for j1 in range(0, m[0] + 1):
    #     for j2 in range(0, m[1] + 1):
    #         for j3 in range(0, m[2] + 1):
    #             # probabilities.append(probability_specific([j1, j2, j3], j1 + j2 + j3, m))
    #             probabilities.append(probability_specific2([j1, j2, j3], m))
    #             nodes.append(str(j1) + str(j2) + str(j3))
    # print('\n'.join([f'{nodes} — {str(probabilities)}' for nodes, probabilities in zip(nodes, probabilities)]))
    # print(f'Сумма вероятностей = {sum(probabilities)}')

    m = [3, 3]  # Количество процессоров каждого типа
    N = len(m)  # Количество процессоров разных типов
    probabilities = []
    nodes = []
    for j1 in range(0, m[0] + 1):
        for j2 in range(0, m[1] + 1):
            # probabilities.append(probability_specific([j1, j2], j1 + j2, m))
            probabilities.append(probability_specific2([j1, j2], m))
            # probabilities.append(probability_specific3([j1, j2], m))
            nodes.append(str(j1) + str(j2))
    print('\n'.join([f'{nodes} — {str(probabilities)}' for nodes, probabilities in zip(nodes, probabilities)]))
    print(f'Сумма вероятностей = {sum(probabilities)}')

    # print(probability_general(3, m)) # формула P-l, где l = 3
    # print(probability_specific2([3, 0], m) + \
    #       probability_specific2([2, 1], m) + \
    #       probability_specific2([1, 2], m) + \
    #       probability_specific2([0, 3], m)) # сложить все значения с очередью 3
    # print(probability_general(0, m))
    # print(probability_specific2([0, 0], m))
    # print(probability_general(6, m))
    # print(probability_specific2([3, 3], m))
    plot_graph_for(m, 0, 15)

    print(mean_queue_length(m))

    P0 = [];
    P1 = []
    P0.append(probability_general(0, m))
    P1.append(probability_general(1, m))
    print(P0, P1)
    for l in range(0, 2):  # PANFILOV
        print(f'P{l}     {probability_general(l, m)}')

    plt.show(block=True)
