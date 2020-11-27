import networkx as nx
import matplotlib.pyplot as plt

plt.ion()  # Включить интерактивный режим работы с графиками


class Vertex:
    max_requests = []  # Конфигурация системы (максимум запросов на процессор каждого типа)
    number_of_processors = 0  # Количество разных типов процессоров

    def __init__(self, requests):
        # Верхний индекс
        self.in_process = 1 if sum(requests) > 0 else 0  # Запросов в обработке
        self.in_queue = sum(requests) - self.in_process  # Запросов в очереди
        # Нижний индекс
        self.requests = requests.copy()  # Конфигурация вершины
        # Представление вершины в виде строки для печати
        self.vertex = f'P({self.in_process},{self.in_queue}|{",".join([str(request) for request in requests])})'

        # Найти каналы:
        self.able_to_receive = [None] * Vertex.number_of_processors  # Те, по которым запрос можно принять
        self.able_to_send = [None] * Vertex.number_of_processors  # Те, по которым запрос можно отправить
        for i in range(0, Vertex.number_of_processors):
            self.able_to_receive[i] = True if requests[i] - 1 >= 0 else False
            self.able_to_send[i] = True if requests[i] + 1 <= Vertex.max_requests[i] else False

    def get_equation(self):  # Составить уравнение для вершины
        equation_right = ''  # Правая часть уравнения
        equation_left = '-('  # Левая часть уравнения
        has_first_element = False  # Не ставить плюс перед первым элементом
        for i in range(0, Vertex.number_of_processors):
            if self.able_to_receive[i]:
                equation_left += f' + μ{i + 1}' if has_first_element else f'μ{i + 1}';
                has_first_element = True
                requests = self.requests.copy()
                requests[i] -= 1
                equation_right += f' + ν{i + 1}×{Vertex(requests).vertex}'
            if self.able_to_send[i]:
                equation_left += f' + ν{i + 1}' if has_first_element else f'ν{i + 1}';
                has_first_element = True
                requests = self.requests.copy()
                requests[i] += 1
                equation_right += f' + μ{i + 1}×{Vertex(requests).vertex}'
        equation_left += f')×{self.vertex}'
        equation_right += ' = 0'
        return equation_left + equation_right  # Соединить две части

    def __lt__(self, other):
        return True if (self.in_process + self.in_queue) < (other.in_process + other.in_queue) else False

    def print(self):  # Вывод информации о вершине в консоль
        print(self.vertex)
        print(f'Может принять {self.able_to_receive} Может отправить {self.able_to_send}')
        print(self.get_equation())


def get_equations(config):  # Вернуть систему уравнений для данной конфигурации в виде списка из строк
    def recursion(i):
        if i == Vertex.number_of_processors:
            counter[0] += 1
            equations.append('{:<4} {:<16} {:<20}'.format(counter[0], str(requests), Vertex(requests).get_equation()))
            return

        for requests[i] in range(0, config[i] + 1):
            recursion(i + 1)

    counter = [0]
    requests = [None] * Vertex.number_of_processors
    equations = ['{:<4} {:<16} {:<20}'.format('№', 'Конфигурация', 'Уравнение')]
    recursion(0)
    return equations


def plot_graph(config):  # Построить граф для данной конфигурации
    def recursion(i):
        if i == Vertex.number_of_processors:
            vertices.append(Vertex(requests))
            return

        for requests[i] in range(0, config[i] + 1):
            recursion(i + 1)

    requests = [None] * Vertex.number_of_processors
    vertices = []
    recursion(0)  # Найти все вершины

    # Найти грани
    edges = []
    for vert in vertices:
        for i in range(0, Vertex.number_of_processors):
            if vert.able_to_receive[i]:
                requests = vert.requests.copy()
                requests[i] -= 1
                edges.append((vert.vertex, Vertex(requests).vertex))
            if vert.able_to_send[i]:
                requests = vert.requests.copy()
                requests[i] += 1
                edges.append((vert.vertex, Vertex(requests).vertex))

    # Создать и отрисовать граф
    fig = plt.figure()
    fig.canvas.set_window_title(f'Конфигурация - {config}')
    G = nx.Graph()
    G.add_nodes_from([vert.vertex for vert in vertices])
    G.add_edges_from(edges)
    nx.draw(G, with_labels=True, font_weight='bold', font_size=8)

    # Уменьшить граф, чтобы не срезались подписи
    axis = plt.gca()
    axis.set_xlim([1.1 * x for x in axis.get_xlim()])
    axis.set_ylim([1.0 * y for y in axis.get_ylim()])

    plt.show()


if __name__ == "__main__":
    # Необходимо задать перед вычислениями  <--- ОБЯЗАТЕЛЬНО
    m = [3, 3]  # Задать конфигурацию системы
    # Инициализация класса
    Vertex.max_requests = m
    Vertex.number_of_processors = len(Vertex.max_requests)

    print('\n'.join(get_equations(m)))
    plot_graph(m)
    plt.show(block=True)
