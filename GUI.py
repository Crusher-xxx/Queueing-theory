import tkinter as tk
import graph
import program


def calculate(): # Выполнить необходимые расчеты и построить графики
    # Задать конфигурацию на основе ввода пользователя
    m = [int(n) for n in field_input_configuration.get().split()]
    graph.Vertex.max_requests = m
    graph.Vertex.number_of_processors = len(graph.Vertex.max_requests)
    
    
    # Вывести уравнения для системы в окно
    txt = '\n\n'.join(graph.get_equations(m))
    equations.config(state = 'normal')
    equations.delete(1.0, 'end')
    equations.insert('end', txt)
    equations.config(state = 'disabled')
    
    
    # Основные параметры для расчета производительности
    N = program.N = graph.Vertex.number_of_processors            # Количество процессоров разных типов
    TO = program.TO = [float(n) for n in field_TO.get().split()] # Время выполнения операций
    τ = program.τ = [float(n) for n in field_τ.get().split()]    # Время цикла оперативной памяти
    ξ = program.ξ = float(field_ξ.get())                         # Коэффициент связности
    
    # Дополнительные параметры для расчета производительности (вычисляются из основных)
    ν = program.ν = [ξ / (TO + ξ * τ) for TO, τ in zip(TO, τ)] # Параметр интенсивности
    μ = program.μ = [1 / τ for τ in τ]                         # Параметр обслуживания
    ρ = program.ρ = [ν / μ for ν, μ in zip(ν, μ)]
    

    # Построить граф
    graph.plot_graph(m)
    # Построить график зависимости производительности от количества процессоров
    program.plot_graph_for(m, int(field_input_plot_for.get()) - 1, int(field_plot_up_to.get()))
    






root = tk.Tk()                # Создать окно
root.title('СМО')             # Заголовок окна
# root.geometry('1800x1000')  # Задать ширину и высоту окна


# Поле, чтобы ввести конфигурацию системы
prompt_input_configuration = tk.Label(root, text = 'Конфигурация системы — m')
prompt_input_configuration.grid(row = 0, column = 0, sticky = 'w')
field_input_configuration = tk.Entry(root)
field_input_configuration.grid(row = 0, column = 1)


# Поле, чтобы выбрать тип процессора, для которого будет построен график
prompt_input_plot_for = tk.Label(root, text = 'Построить для процессора')
prompt_input_plot_for.grid(row = 1, column = 0, sticky = 'w')
field_input_plot_for = tk.Entry(root)
field_input_plot_for.grid(row = 1, column = 1)


# Поле, чтобы задать максимальное число процессоров для оси X графика
prompt_plot_up_to = tk.Label(root, text = 'Процессоров от 0 до')
prompt_plot_up_to.grid(row = 2, column = 0, sticky = 'w')
field_plot_up_to = tk.Entry(root)
field_plot_up_to.grid(row = 2, column = 1)


# Поле для ввода коэффициента связности
promt_ξ = tk.Label(root, text = 'Коэффициент связности — ξ')
promt_ξ.grid(row = 3, column = 0, sticky = 'w')
field_ξ = tk.Entry(root)
field_ξ.grid(row = 3, column = 1)
field_ξ.insert('end', 0.35)


# Поле для ввода времени выполнения операций
promt_TO = tk.Label(root, text = 'Время выполнения операций — TO')
promt_TO.grid(row = 4, column = 0, sticky = 'w')
field_TO = tk.Entry(root)
field_TO.grid(row = 4, column = 1)
field_TO.insert('end', '0.66 8 57')


# Поле для ввода времени цикла оперативной памяти
promt_τ = tk.Label(root, text = 'Время цикла оперативной памяти — τ')
promt_τ.grid(row = 5, column = 0, sticky = 'w')
field_τ = tk.Entry(root)
field_τ.grid(row = 5, column = 1)
field_τ.insert('end', '1.2 1.2 1.2')


# Кнопка — начать вычисления
button_calculate = tk.Button(root, text = 'Построить', command = calculate)
button_calculate.grid(row = 6, column = 1)


# Окно, куда выводятся уравнения
equations_frame = tk.Frame(root)
equations_frame.grid(row = 0, column = 2, rowspan = 70)
horiz_scroll = tk.Scrollbar(equations_frame, orient = 'horizontal')
horiz_scroll.grid(row = 1, column = 0, sticky = 'N'+'S'+'E'+'W')
vert_scroll = tk.Scrollbar(equations_frame, orient = 'vertical')
vert_scroll.grid(row = 0, column = 1, sticky = 'N'+'S'+'E'+'W')
equations = tk.Text(equations_frame, height = 35, width = 75, wrap = 'word', \
                    xscrollcommand = horiz_scroll.set, yscrollcommand = vert_scroll.set)
equations.grid(row = 0, column = 0)
equations.config(state = 'disabled')
horiz_scroll.config(command = equations.xview)
vert_scroll.config(command = equations.yview)




root.mainloop()