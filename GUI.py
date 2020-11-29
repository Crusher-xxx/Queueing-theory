import tkinter as tk
import graph
import program


def calculate():  # Выполнить необходимые расчеты и построить графики
    # Задать конфигурацию на основе ввода пользователя
    m = [int(n) for n in configuration.field_input_configuration.get().split()]
    graph.Vertex.max_requests = m
    graph.Vertex.number_of_processors = len(graph.Vertex.max_requests)

    # Основные параметры для расчета производительности
    N = program.N = graph.Vertex.number_of_processors  # Количество процессоров разных типов
    TO = program.TO = [float(n) for n in configuration.field_TO.get().split()]  # Время выполнения операций
    τ = program.τ = [float(n) for n in configuration.field_τ.get().split()]  # Время цикла оперативной памяти
    ξ = program.ξ = float(configuration.field_ξ.get())  # Коэффициент связности

    # Дополнительные параметры для расчета производительности (вычисляются из основных)
    ν = program.ν = [ξ / (TO + ξ * τ) for TO, τ in zip(TO, τ)]  # Параметр интенсивности
    μ = program.μ = [1 / τ for τ in τ]  # Параметр обслуживания
    ρ = program.ρ = [ν / μ for ν, μ in zip(ν, μ)]

    # Построить граф
    graph.plot_graph(m)
    # Построить график зависимости производительности от количества процессоров
    plt_data = program.plot_graph_for(m, int(plot_data.field_input_plot_for.get()) - 1, int(plot_data.field_plot_up_to.get()))

    # Вывести статистику в окно
    txt = ''
    for m, q, p in zip(plt_data[0], plt_data[1], plt_data[2]):
        txt += ('{:<10} {:<34} {:<30}\n'.format(m, q, p))
    output_window.text.config(state='normal')
    output_window.text.delete(1.0, 'end')
    output_window.text.insert('end', txt)
    output_window.text.config(state='disabled')


root = tk.Tk()  # Создать окно
root.title('РППМВС')  # Заголовок окна
# root.geometry('1800x1000')  # Задать ширину и высоту окна
title = tk.Label(root, text='Расчет параметров производительности многопроцессорной вычислительной системы', font=(None, 18))
title.grid(row=0, column=0, columnspan=2)
label_length = 250


class Configuration:  # Область ввода конфигурации
    def __init__(self):
        self.frame = tk.Frame(root)
        self.frame.grid(row=1, column=0, sticky='W')
        self.title = tk.Label(self.frame, text='\nКонфигурация системы:', font=(None, 14))
        self.title.grid(row=0, column=0, columnspan=2)

        # Поле, чтобы ввести количество типов процессоров
        self.prompt_N = tk.Label(self.frame, text='Количество типов процессоров, N',
                                 wraplength=label_length, justify='left')
        self.prompt_N.grid(row=1, column=0, sticky='W')
        self.field_N = tk.Entry(self.frame)
        self.field_N.grid(row=1, column=1, sticky='W')

        # Поле, чтобы ввести конфигурацию системы
        self.prompt_input_configuration = tk.Label(self.frame, text='Количество процессоров каждого типа, m[i]',
                                                   wraplength=label_length, justify='left')
        self.prompt_input_configuration.grid(row=2, column=0, sticky='W')
        self.field_input_configuration = tk.Entry(self.frame)
        self.field_input_configuration.grid(row=2, column=1, sticky='W')

        # Поле для ввода коэффициента связности
        self.prompt_ξ = tk.Label(self.frame, text='Коэффициент связности, ξ', wraplength=label_length, justify='left')
        self.prompt_ξ.grid(row=3, column=0, sticky='W')
        self.field_ξ = tk.Entry(self.frame)
        self.field_ξ.grid(row=3, column=1, sticky='W')
        self.field_ξ.insert('end', 0.35)

        # Поле для ввода времени выполнения операций
        self.prompt_TO = tk.Label(self.frame, text='Время выполнения операций процессорами каждого типа, TO',
                                  wraplength=label_length, justify='left')
        self.prompt_TO.grid(row=4, column=0, sticky='W')
        self.field_TO = tk.Entry(self.frame)
        self.field_TO.grid(row=4, column=1, sticky='W')
        self.field_TO.insert('end', '0.66 8 57')

        # Поле для ввода времени цикла оперативной памяти
        self.prompt_τ = tk.Label(self.frame, text='Время цикла оперативной памяти для процессоров, τ',
                                 wraplength=label_length, justify='left')
        self.prompt_τ.grid(row=5, column=0, sticky='W')
        self.field_τ = tk.Entry(self.frame)
        self.field_τ.grid(row=5, column=1, sticky='W')
        self.field_τ.insert('end', '1.2 1.2 1.2')


class PlotData:  # Область ввода данных для построения графика
    def __init__(self):
        self.frame = tk.Frame(root)
        self.frame.grid(row=2, column=0, sticky='W')

        # Заголовок данных для графика
        self.title = tk.Label(self.frame, text='\nПостроение графика производительности:', font=(None, 14))
        self.title.grid(row=0, column=0, columnspan=2)

        # Поле, чтобы выбрать тип процессора, для которого будет построен график
        self.prompt_input_plot_for = tk.Label(self.frame, text='Изменяем количество процессоров типа',
                                              wraplength=label_length, justify='left')
        self.prompt_input_plot_for.grid(row=1, column=0, sticky='W')
        self.field_input_plot_for = tk.Entry(self.frame)
        self.field_input_plot_for.grid(row=1, column=1, sticky='W')

        # Поле, чтобы задать максимальное число процессоров для оси X графика
        self.prompt_plot_up_to = tk.Label(self.frame, text='от 0 до', wraplength=label_length, justify='left')
        self.prompt_plot_up_to.grid(row=2, column=0, sticky='W')
        self.field_plot_up_to = tk.Entry(self.frame)
        self.field_plot_up_to.grid(row=2, column=1, sticky='W')


class OutputWindow:  # Область вывода статистики
    def __init__(self):
        self.frame = tk.Frame(root)
        self.frame.grid(row=1, column=1, rowspan=70)

        self.number = tk.Label(self.frame, text='№:', font=(None, 14))
        self.number.grid(row=0, column=0, sticky='W')
        self.queue = tk.Label(self.frame, text='Средняя длина очереди:', font=(None, 14))
        self.queue.grid(row=0, column=1, sticky='W')
        self.perf = tk.Label(self.frame, text='Производительность:', font=(None, 14))
        self.perf.grid(row=0, column=2, sticky='W')

        self.horiz_scroll = tk.Scrollbar(self.frame, orient='horizontal')
        self.horiz_scroll.grid(row=2, column=0, sticky='NSEW', columnspan=3)
        self.vert_scroll = tk.Scrollbar(self.frame, orient='vertical')
        self.vert_scroll.grid(row=1, column=3, sticky='NSEW')
        self.text = tk.Text(self.frame, height=35, width=75, wrap='word',
                            xscrollcommand=self.horiz_scroll.set, yscrollcommand=self.vert_scroll.set)
        self.text.grid(row=1, column=0, columnspan=3)
        self.text.config(state='disabled')
        self.horiz_scroll.config(command=self.text.xview)
        self.vert_scroll.config(command=self.text.yview)


# Кнопка — начать вычисления
button_calculate = tk.Button(root, text='Пуск', command=calculate, font=(None, 14))
button_calculate.grid(row=3, column=0, sticky='S')


configuration = Configuration()
output_window = OutputWindow()
plot_data = PlotData()


root.mainloop()
