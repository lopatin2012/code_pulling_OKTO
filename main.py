import PySimpleGUI as sg  # pip install pysimplegui
import datetime
import time

# Функции ,
def create_to_code(file_okto, file_ready, gtin, date, time_start, time_end):
    lst = []
    date_time_start = datetime.datetime.strptime(time_start, "%H:%M:%S")
    date_time_end = datetime.datetime.strptime(time_end, "%H:%M:%S")
    second_date_time_start = date_time_start.hour * 3600 + date_time_start.minute * 60 + date_time_start.second
    second_date_time_end = date_time_end.hour * 3600 + date_time_end.minute * 60 + date_time_end.second + 1
    str_date_start = time.strftime("%H-%M-%S", time.gmtime(second_date_time_start))
    str_date_end = time.strftime("%H-%M-%S", time.gmtime(second_date_time_end))
    lst_time = [str(time.strftime("%H:%M:%S", time.gmtime(i)))
                for i in range(second_date_time_start, second_date_time_end)]
    with open(file_okto, "r", encoding="UTF-8") as f_okto:
        for row in f_okto.readlines():
            if gtin in row and date in row and row[11:19] in lst_time:
                lst.append(row[20:])
    with open(f"{file_ready}/{gtin}_{len(lst)}_"
              f"{date}_"
              f"{str_date_start}_"
              f"{str_date_end}_"
              f".txt", "w", encoding="UTF-8") as f_ready:
        for row in lst:
            f_ready.write(row)
    sg.popup_no_titlebar("Готово!")

sg.theme('DarkAmber')   # Тема
# Кнопки и прочее
layout = [
    [sg.Text('Исходный файл:'), sg.Input(key="in"), sg.FileBrowse(file_types=(("Файл с кодами", "*.txt"),))],
    [sg.Text('Новый файл:'), sg.Input(key="out"), sg.FolderBrowse()],
    [sg.Text('Введите GTIN:'), sg.Input(key="gtin")],
    [sg.Text('Введите дату:'), sg.Input(key="date")],
    [sg.Text('Введите время ОТ:'), sg.Input(key="time_start")],
    [sg.Text('Введите время ДО:'), sg.Input(key="time_end")],
    [sg.Button('Преобразовать'), sg.Button('Закрыть')]
]

# Создаём окно
window = sg.Window('Window Title', layout)
# обработка событий и получение значений
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Закрыть': # закрытие окна
        break
    if event == "Преобразовать":
        print(values["in"])
        create_to_code(values["in"], values["out"], values["gtin"],
                       values["date"], values["time_start"], values["time_end"])

window.close()