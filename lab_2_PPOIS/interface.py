import tkinter as tk
from tkcalendar import DateEntry
from tkinter import messagebox as mb, BOTH, END, VERTICAL
import logic as lg
from tkinter import ttk
from tkinter import filedialog as fd
import table as tb

current_page = 1
current_num_of_pages = 0

def read_file():
    filepath = fd.askopenfilename()
    if filepath != "":
        lg.read_xml(filepath)
        global current_page
        global current_num_of_pages
        current_page = 0
        current_num_of_pages = len(lg.list_of_players)//10 + 1
        renew_table(1)


def add_batton_cleaked():
    dial_window = tk.Toplevel(window)  # Use Toplevel instead of Tk for a new window
    lab_name = tk.Label(dial_window, text='Имя')
    lab_name.grid(column=0, row=1)
    enter_name = tk.Entry(dial_window, width=10)
    enter_name.grid(column=1, row=1)
    lab_sname = tk.Label(dial_window, text='Отчество')
    lab_sname.grid(column=0, row=2)
    enter_sname = tk.Entry(dial_window, width=10)
    enter_sname.grid(column=1, row=2)
    lab_lname = tk.Label(dial_window, text='Фамилия')
    lab_lname.grid(column=0, row=0)
    enter_lname = tk.Entry(dial_window, width=10)
    enter_lname.grid(column=1, row=0)
    lab_bdate = tk.Label(dial_window, text='Дата \n рождения')
    lab_bdate.grid(column=0, row=3)
    bdate = DateEntry(dial_window, width=12, background="darkblue", foreground="white", borderwidth=2)
    bdate.grid(column=1, row=3)
    lab_team = tk.Label(dial_window, text='Футбольная \n команда')
    lab_team.grid(column=0, row=4)
    enter_team = tk.Entry(dial_window, width=10)
    enter_team.grid(column=1, row=4)
    lab_city = tk.Label(dial_window, text='Домашний  \n город')
    lab_city.grid(column=0, row=5)
    enter_city = tk.Entry(dial_window, width=10)
    enter_city.grid(column=1, row=5)
    lab_sost = tk.Label(dial_window, text='Состав')
    lab_sost.grid(column=0, row=6)
    sost = tk.StringVar()
    sost.set('основной')
    drop_sost = tk.OptionMenu(dial_window, sost, 'основной', 'запасной')
    drop_sost.grid(column=1, row=6)
    lab_position = tk.Label(dial_window, text='Позиия')
    lab_position.grid(column=0, row=7)
    pos_list = ['форвард', 'оттянутый нападающий', 'крайний нападающий', 'полусредний нападающий',
                'центральный опорный полузащитник', 'центральный полузащитник',
                'центральный атакующий полузащитник','фланговый полузащитник', 'центральный защитник',
                'свободный защитник(либеро)', 'фланговый защитник', 'вратарь']
    pos = tk.StringVar()
    pos.set('форвард')
    drop_pos = tk.OptionMenu(dial_window, pos, 'форвард', 'оттянутый нападающий', 'крайний нападающий', 'полусредний нападающий',
                'центральный опорный полузащитник', 'центральный полузащитник',
                'центральный атакующий полузащитник','фланговый полузащитник', 'центральный защитник',
                'свободный защитник(либеро)', 'фланговый защитник', 'вратарь')
    drop_pos.grid(column=1, row=7)
    def add_clicked():
        if(enter_name.get() == '' or enter_lname.get() == '' or enter_sname.get() == '' or enter_city.get() == ''
           or enter_team.get() == ''):
            mb.showwarning('Предупреждение','Не все поля заполнены')
        else:
            lg.add_to_list(enter_name.get(), enter_sname.get(), enter_lname.get(), bdate.get_date(),
                           enter_team.get(), enter_city.get(), sost.get(), pos.get())
            global current_page
            global current_num_of_pages
            if (len(lg.list_of_players) % 10 == 1):
                current_num_of_pages += 1
            renew_table(current_page)
            dial_window.destroy()

    but = tk.Button(dial_window, text='добавить', command=add_clicked)
    but.grid(column=0, row=8)


def find_full_name():
    dial_window = tk.Toplevel(window)  # Use Toplevel instead of Tk for a new window
    lab_name = tk.Label(dial_window, text='Имя')
    lab_name.grid(column=0, row=1)
    enter_name = tk.Entry(dial_window, width=10)
    enter_name.grid(column=1, row=1)
    lab_sname = tk.Label(dial_window, text='Отчество')
    lab_sname.grid(column=0, row=2)
    enter_sname = tk.Entry(dial_window, width=10)
    enter_sname.grid(column=1, row=2)
    lab_lname = tk.Label(dial_window, text='Фамилия')
    lab_lname.grid(column=0, row=0)
    enter_lname = tk.Entry(dial_window, width=10)
    enter_lname.grid(column=1, row=0)
    def add_clicked():
        name = enter_name.get()
        lname = enter_lname.get()
        sname = enter_sname.get()
        if name == '' and lname == '' and sname == '':
            mb.showwarning('Предупреждение','Хотя бы  одно поле должно быть заполнено')
        else:
            dial_window.destroy()
            print_founded(lg.find_players(name, sname, lname, '', '', '', '', '')[0])

    but = tk.Button(dial_window, text='найти', command=add_clicked)
    but.grid(column=0, row=8)

def find_birth_date():
    dial_window = tk.Toplevel(window)
    lab_bdate = tk.Label(dial_window, text='Дата \n рождения')
    lab_bdate.grid(column=0, row=3)
    bdate = DateEntry(dial_window, width=12, background="darkblue", foreground="white", borderwidth=2)
    bdate.grid(column=1, row=3)

    def add_clicked():
        birth_date = bdate.get_date()
        dial_window.destroy()
        print_founded(lg.find_players('', '', '', birth_date, '', '', '', '')[0])

    but = tk.Button(dial_window, text='найти', command=add_clicked)
    but.grid(column=0, row=8)


def find_position():
    dial_window = tk.Toplevel(window)
    lab_position = tk.Label(dial_window, text='Позиия')
    lab_position.grid(column=0, row=7)
    pos_list = ['форвард', 'оттянутый нападающий', 'крайний нападающий', 'полусредний нападающий',
                'центральный опорный полузащитник', 'центральный полузащитник',
                'центральный атакующий полузащитник', 'фланговый полузащитник', 'центральный защитник',
                'свободный защитник(либеро)', 'фланговый защитник', 'вратарь']
    pos = tk.StringVar()
    pos.set('форвард')
    drop_pos = tk.OptionMenu(dial_window, pos, 'форвард', 'оттянутый нападающий', 'крайний нападающий',
                             'полусредний нападающий',
                             'центральный опорный полузащитник', 'центральный полузащитник',
                             'центральный атакующий полузащитник', 'фланговый полузащитник', 'центральный защитник',
                             'свободный защитник(либеро)', 'фланговый защитник', 'вратарь')
    drop_pos.grid(column=1, row=7)
    def add_clicked():
        print_founded(lg.find_players('', '', '', '', '', '', '', pos.get())[0])
        dial_window.destroy()
    but = tk.Button(dial_window, text='найти', command=add_clicked)
    but.grid(column=0, row=8)

def find_sost():
    dial_window = tk.Toplevel(window)
    lab_sost = tk.Label(dial_window, text='Состав')
    lab_sost.grid(column=0, row=6)
    sost = tk.StringVar()
    sost.set('основной')
    drop_sost = tk.OptionMenu(dial_window, sost, 'основной', 'запасной')
    drop_sost.grid(column=1, row=6)
    def add_clicked():
        print_founded(lg.find_players('', '', '', '', '', '', sost.get(), '')[0])
        dial_window.destroy()

    but = tk.Button(dial_window, text='найти', command=add_clicked)
    but.grid(column=0, row=8)
def find_city():
    dial_window = tk.Toplevel(window)
    lab_city = tk.Label(dial_window, text='Домашний  \n город')
    lab_city.grid(column=0, row=5)
    enter_city = tk.Entry(dial_window, width=10)
    enter_city.grid(column=1, row=5)
    def add_clicked():
        if(enter_city.get() == ''):
            mb.showwarning('Предупреждение','Поле не заполнено')
        else:
            print_founded(lg.find_players('', '', '', '', '', enter_city.get(), '', '')[0])
            dial_window.destroy()

    but = tk.Button(dial_window, text='найти', command=add_clicked)
    but.grid(column=0, row=8)
def find_team():
    dial_window = tk.Toplevel(window)
    lab_team = tk.Label(dial_window, text='Футбольная \n команда')
    lab_team.grid(column=0, row=4)
    enter_team = tk.Entry(dial_window, width=10)
    enter_team.grid(column=1, row=4)
    def add_clicked():
        if(enter_team.get() == ''):
            mb.showwarning('Предупреждение','Поле не заполнено')
        else:
            #dial_window.destroy()
            print_founded(lg.find_players('', '', '', '', enter_team.get(), '', '', '')[0])
            dial_window.destroy()


    but = tk.Button(dial_window, text='найти', command=add_clicked)
    but.grid(column=0, row=8)

def del_full_name():
    dial_window = tk.Toplevel(window)  # Use Toplevel instead of Tk for a new window
    lab_name = tk.Label(dial_window, text='Имя')
    lab_name.grid(column=0, row=1)
    enter_name = tk.Entry(dial_window, width=10)
    enter_name.grid(column=1, row=1)
    lab_sname = tk.Label(dial_window, text='Отчество')
    lab_sname.grid(column=0, row=2)
    enter_sname = tk.Entry(dial_window, width=10)
    enter_sname.grid(column=1, row=2)
    lab_lname = tk.Label(dial_window, text='Фамилия')
    lab_lname.grid(column=0, row=0)
    enter_lname = tk.Entry(dial_window, width=10)
    enter_lname.grid(column=1, row=0)

    def add_clicked():
        if (enter_name.get() == '' and enter_lname == '' and enter_sname == ''):
            mb.showwarning('Предупреждение', 'Хотя бы одно поле должно быть заполнено')
        else:
            #dial_window.destroy()
            founded = lg.find_players(enter_name.get(), enter_sname.get(), enter_lname.get(), '', '', '', '', '')
            print_founded(founded[0])
            mb.showinfo(str(len(founded[0])),'элементов удалено')
            lg.delete_info(founded[1])
            dial_window.destroy()
            global current_page
            current_page = 1
            global current_num_of_pages
            count_lab = len(lg.list_of_players) % 10
            renew_table(1)



    but = tk.Button(dial_window, text='удалить', command=add_clicked)
    but.grid(column=0, row=8)

def del_birth_date():
    dial_window = tk.Toplevel(window)
    lab_bdate = tk.Label(dial_window, text='Дата \n рождения')
    lab_bdate.grid(column=0, row=3)
    bdate = DateEntry(dial_window, width=12, background="darkblue", foreground="white", borderwidth=2)
    bdate.grid(column=1, row=3)

    def add_clicked():
        founded = lg.find_players('', '', '', bdate.get_date(), '', '', '', '')
        dial_window.destroy()
        print_founded(founded[0])
        mb.showinfo(str(len(founded[0])), 'элементов удалено')
        lg.delete_info(founded[1])
        dial_window.destroy()
        global current_page
        current_page = 1
        global current_num_of_pages
        current_num_of_pages = len(lg.list_of_players) // 10 + 1
        renew_table(1)

    but = tk.Button(dial_window, text='найти', command=add_clicked)
    but.grid(column=0, row=8)


def del_pos():
    dial_window = tk.Toplevel(window)
    lab_position = tk.Label(dial_window, text='Позиия')
    lab_position.grid(column=0, row=7)
    pos_list = ['форвард', 'оттянутый нападающий', 'крайний нападающий', 'полусредний нападающий',
                'центральный опорный полузащитник', 'центральный полузащитник',
                'центральный атакующий полузащитник', 'фланговый полузащитник', 'центральный защитник',
                'свободный защитник(либеро)', 'фланговый защитник', 'вратарь']
    pos = tk.StringVar()
    pos.set('форвард')
    drop_pos = tk.OptionMenu(dial_window, pos, 'форвард', 'оттянутый нападающий', 'крайний нападающий',
                             'полусредний нападающий',
                             'центральный опорный полузащитник', 'центральный полузащитник',
                             'центральный атакующий полузащитник', 'фланговый полузащитник', 'центральный защитник',
                             'свободный защитник(либеро)', 'фланговый защитник', 'вратарь')
    drop_pos.grid(column=1, row=7)
    def add_clicked():
        founded = lg.find_players('', '', '', '', '', '', '', pos.get())
        print_founded(founded[0])
        dial_window.destroy()
        mb.showinfo(str(len(founded[0])), 'элементов удалено')
        lg.delete_info(founded[1])
        dial_window.destroy()
        global current_page
        current_page = 1
        global current_num_of_pages
        current_num_of_pages = len(lg.list_of_players) // 10 + 1
        renew_table(1)


    but = tk.Button(dial_window, text='найти', command=add_clicked)
    but.grid(column=0, row=8)


def del_sost():
    dial_window = tk.Toplevel(window)
    lab_sost = tk.Label(dial_window, text='Состав')
    lab_sost.grid(column=0, row=6)
    sost = tk.StringVar()
    sost.set('основной')
    drop_sost = tk.OptionMenu(dial_window, sost, 'основной', 'запасной')
    drop_sost.grid(column=1, row=6)

    def add_clicked():
        founded = lg.find_players('', '', '', '', '', '', sost.get(), '')
        print_founded(founded)
        dial_window.destroy()
        mb.showinfo(str(len(founded[0])), 'элементов удалено')
        lg.delete_info(founded[1])
        dial_window.destroy()
        global current_page
        current_page = 1
        global current_num_of_pages
        current_num_of_pages = len(lg.list_of_players) // 10 + 1
        renew_table(1)

    but = tk.Button(dial_window, text='найти', command=add_clicked)
    but.grid(column=0, row=8)

def del_team():
    dial_window = tk.Toplevel(window)
    lab_team = tk.Label(dial_window, text='Футбольная \n команда')
    lab_team.grid(column=0, row=4)
    enter_team = tk.Entry(dial_window, width=10)
    enter_team.grid(column=1, row=4)

    def add_clicked():
        if (enter_team.get() == ''):
            mb.showwarning('Предупреждение', 'Поле не заполнено')
        else:
            # dial_window.destroy()
            founded = lg.find_players('', '', '', '', enter_team.get(), '', '', '')
            print_founded(founded[0])
            mb.showinfo(str(len(founded[0])), 'элементов удалено')
            lg.delete_info(founded[1])
            dial_window.destroy()
            global current_page
            current_page = 1
            global current_num_of_pages
            current_num_of_pages = len(lg.list_of_players) // 10 + 1
            renew_table(1)

    #dial_window.destroy()

    but = tk.Button(dial_window, text='удалить', command=add_clicked)
    but.grid(column=0, row=8)

def del_city():
    dial_window = tk.Toplevel(window)
    #dial_window = tk.Toplevel(window)
    lab_city = tk.Label(dial_window, text='Домашний  \n город')
    lab_city.grid(column=0, row=5)
    enter_city = tk.Entry(dial_window, width=10)
    enter_city.grid(column=1, row=5)

    def add_clicked():
        if (enter_city.get() == ''):
            mb.showwarning('Предупреждение', 'Поле не заполнено')
        else:
            founded = lg.find_players('', '', '', '', '', enter_city.get(), '', '')
            print_founded(founded)
            dial_window.destroy()
            mb.showinfo(str(len(founded[0])), 'элементов удалено')
            lg.delete_info(founded[1])
            dial_window.destroy()
            global current_page
            current_page = 1
            global current_num_of_pages
            current_num_of_pages = len(lg.list_of_players) // 10 + 1
            renew_table(1)

    but = tk.Button(dial_window, text='найти', command=add_clicked)
    but.grid(column=0, row=8)


def print_founded(list_of_players):
    w = tb.Window(list_of_players)
    #dial_window = tk.Tk()
    #columns = ("name", "birth_date", "team", "town", "sost", "pos")
    #frame_tree = tk.Frame(dial_window)
    #tree = ttk.Treeview(frame_tree,columns=columns, show="headings")
    #tree.pack(fill=BOTH, expand=1)

    # определяем заголовки
    #tree.heading("name", text="ФИО игрока")
    #tree.heading("birth_date", text="Дата рождения")
    #tree.heading("team", text="Футбольная команда")
    #tree.heading("town", text="Домашний город")
    #tree.heading("sost", text="Состав")
    #tree.heading("pos", text="Позиция")

    #for person in list_of_players:
     #   tree.insert("", END, values=person)
    #dial_window=tree
    #scrollbar = ttk.Scrollbar(orient=VERTICAL, command=tree.yview)
    #tree.pack(fill=BOTH, expand=1)
    #scrollbar.pack()


list_of_items = []
def renew_table(page_num):
    people = lg.get_players(page_num)
    for element in list_of_items:
        tree.delete(element)
    list_of_items.clear()
    for person in people:
        list_of_items.append(tree.insert("", END, values=person))
        #tree.pack()
    global current_num_of_pages
    count_lab.config(text= str(page_num) + '/' + str(current_num_of_pages))

def to_beggining():
    global current_page
    global current_num_of_pages
    renew_table(1)
    current_page = 1

def to_end():
    global current_page
    global current_num_of_pages
    renew_table(current_num_of_pages)
    current_page = current_num_of_pages

def prev():
    global current_page
    if(current_page != 1):
        current_page -= 1
        renew_table(current_page)

def next_():
    global current_page
    global current_num_of_pages
    if(current_page != current_num_of_pages):
        current_page+=1
        renew_table(current_page)


window = tk.Tk()
window.geometry("1200x600")
window.title("lab_2")

# Create a Date Entry widget
menu = tk.Menu(window)# определяем столбцы

file_menu = tk.Menu(menu, tearoff=0)

file_menu.add_command(label="Открыть", command=read_file)
#file_menu.add_separator()
#file_menu.add_command(label="Сохранить")
file_menu.add_command(label="Сохранить как...", command=lg.save_file)

find_player_menu = tk.Menu(menu, tearoff=0)
find_player_menu.add_command(label="по ФИО", command=find_full_name)
find_player_menu.add_command(label="по дате рождения", command=find_birth_date)
find_player_menu.add_command(label="по позиции", command=find_position)
find_player_menu.add_command(label="по составу",command= find_sost)
find_player_menu.add_command(label="по футбольной команде",command= find_team)
find_player_menu.add_command(label="по домашенему городу", command= find_city)

delete_player_menu = tk.Menu(menu, tearoff=0)
delete_player_menu.add_command(label="по ФИО", command=del_full_name)
delete_player_menu.add_command(label="по дате рождения", command=del_birth_date)
delete_player_menu.add_command(label="по позиции", command=del_pos)
delete_player_menu.add_command(label="по составу",command= del_sost)
delete_player_menu.add_command(label="по футбольной команде", command=del_team)
delete_player_menu.add_command(label="по домашенему городу", command=del_city)

function_menu = tk.Menu(menu, tearoff=0)
function_menu.add_command(label="Добавить игрока", command=add_batton_cleaked)
function_menu.add_cascade(label="Найти игроков", menu=find_player_menu)
function_menu.add_cascade(label="Удалить игроков", menu=delete_player_menu)


menu.add_cascade(label="Файл", menu=file_menu)
menu.add_cascade(label="Редактирование", menu=function_menu)
menu.add_command(label="Выйти", command=window.destroy)
window.config(menu=menu)

# определяем столбцы
columns = ("name", "birth_date", "team", "town", "sost", "pos")

tree = ttk.Treeview(columns=columns, show="headings")
tree.pack(fill=BOTH, expand=1)

# определяем заголовки
tree.heading("name", text="ФИО игрока")
tree.heading("birth_date", text="Дата рождения")
tree.heading("team", text="Футбольная команда")
tree.heading("town", text="Домашний город")
tree.heading("sost", text="Состав")
tree.heading("pos", text="Позиция")

# добавляем данные

to_begining_but = tk.Button(text="|ᐊᐊ", command= to_beggining)
to_begining_but.pack(fill=BOTH, expand=1)
prev_but = tk.Button(text="ᐊ", command=prev)
prev_but.pack(fill=BOTH, expand=1)
count_lab = tk.Label(text="0/0")
count_lab.pack(fill=BOTH, expand=1)
next_but = tk.Button(text="ᐅ", command=next_)
next_but.pack(fill=BOTH, expand=1)
to_end_but = tk.Button(text="ᐅᐅ|", command=to_end)
to_end_but.pack(fill=BOTH, expand=1)
#add_batton_cleaked()

window.mainloop()
