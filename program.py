import matplotlib.pyplot as plt

plt.ion()  # Включить интерактивный режим работы с графиками


def probability_specific(j, m):  # Вероятность нахождения системы в состоянии j
    def product(j):
        result = 1
        for i in range(0, N):
            result *= ρ[i] ** j[i]  # ρ в положительной степени
        return result

    def recursive_sum(j, i=0):
        result = 0

        if i == N:
            return product(j)

        for j[i] in range(0, m[i] + 1):
            result += recursive_sum(j, i + 1)

        return result

    return product(j) / recursive_sum(j[:])  # Передать копию списка, чтобы не модифицировать исходный


def probability_general(l, m):  # Вероятность нахождения системы при длине очереди l
    def recursive_sum(j, i=0):
        result = 0

        if i == N:  # Если список закончился
            if sum(j) == l:  # Сумма запросов в списке должна равняться длине очереди
                result = probability_specific(j, m)
            return result

        j[i] = 0
        while j[i] <= m[i] and j[i] <= l:  # j[i] стремится к l, но не может превышать m[i]
            result += recursive_sum(j, i + 1)
            j[i] += 1

        return result

    j = [0] * N  # Количество запросов от процессора каждого типа
    return recursive_sum(j)


def mean_queue_length(m):  # Новая длина очереди
    result = 0
    l = 0
    for i in range(sum(m) - 1, 0, -1):
        result += probability_general(l, m) * i
        l += 1
    return result


def relative_loss_factor(i, mean_queue):  # Коэффициент относительных потерь для процессора типа i
    return 1 + mean_queue * τ[i] / (TO[i] + τ[i])


def relative_performance(m, i, mean_queue):  # Относительная производительность процессора типа i
    return m[i] / relative_loss_factor(i, mean_queue)


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

    # Вычисления
    for m[index] in range(0, up_to + 1):
        m_index_values.append(m[index])
        queue.append(mean_queue_length(m))
        perf.append(general_performance(m, queue[-1]))  # performance(queue[-1])   general_performance(m, queue[-1])
        print(f'Прогресс: {m[index]}/{up_to}', end="\r")  # Отслеживать прогресс

    # Отрисовка графика
    fig = plt.figure()
    m[index] = 'x'  # Заменить количество подписью, чтобы было видно для какого процессора построен график
    fig.canvas.set_window_title(f'Конфигурация - {m}')
    plt.xlabel(f'Количество процессоров m-{index + 1}')
    plt.ylabel('Производительность')

    plt.plot(m_index_values, perf)
    plt.show()

    return [m_index_values, queue, perf]


if __name__ == "__main__":
    # Необходимо задать перед вычислениями  <--- ОБЯЗАТЕЛЬНО
    m = [5, 3]  # Количество процессоров каждого типа
    N = len(m)  # Количество процессоров разных типов

    TO = [0.66, 8, 57]  # Время выполнения операций
    τ = [1.2, 1.2, 1.2]  # Время цикла оперативной памяти
    ξ = 0.35  # Коэффициент связности

    # Данные значения будут вычислены на основе введенных выше
    ν = [ξ / (TO + ξ * τ) for TO, τ in zip(TO, τ)]  # Параметр интенсивности
    μ = [1 / τ for τ in τ]  # Параметр обслуживания
    ρ = [ν / μ for ν, μ in zip(ν, μ)]

    stats = plot_graph_for(m, 0, 15)
    # Вывод статистики
    print(stats)
    txt = ''
    print('{:<4} {:<20} {:<24}'.format(f'№', 'Производительность', 'Ср. Длина очереди'))
    for i, q, p in zip(stats[0], stats[1], stats[2]):
        txt += ('{:<4} {:<20} {:<24}\n'.format(i, q, p))
    print(txt)

    plt.show(block=True)