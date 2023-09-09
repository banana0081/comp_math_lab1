from solver import *
from tkinter import *
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import tkinter.scrolledtext as scrolledtext
import os

HELP_MESSAGE = '''Данная программа решает системы линейных алгебраических уравнений (СЛАУ) используя метод Гаусса.
Программа может работать в двух режимах - пользовательский ввод и чтение данных из файла. Независимо от выбранного метода пользователь увидит треугольный вид матрицы, вектор неизвестных и вектор невязок.

Для использования программы в режиме пользовательского ввода введите количество уравнений/размерность матрицы (от 2 до 20). Затем введите матрицу коэффициентов и вектор свободных членов (можно использовать стрелки и Enter для навигации).

Для использования программы в режиме чтения из файла создайте файл, в файле данные должны храниться в таком формате:
n
a11 a12... a1n
a21 a22... a2n
.
.
.
an1 an2... ann
b1 b2... bn

ВАЖНО! Файл должен быть доступен для чтения, а формат данных должен строго соблюдаться - значения разделены пробелом.
Пример содержимого файла:
3
10 -7 0
-3 2 6
5 -1 5
7 4 6

Автор - Бугаев Сергей Юрьевич
ИТМО, 2023
'''

def select_file():
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir=os.getcwd(),
        filetypes=filetypes)
    """ try: """
    f = open(filename, 'r')
    n = f.readline().split()
    if len(n)!=1:
        raise AttributeError
    n = int(n[0])
    a = []
    for j in range(n):
        line = [float(i.replace(',', '.')) for i in f.readline().split()]
        a.append(line)
    b = [float(i) for i in f.readline().split()]
    packed = solve(a, b, n)
    showResults(packed)
    """ except Exception as e:
        print(f'Ошибка: {e}')
        showResults('''Файл должен быть доступен для чтения, данные в файле должны быть представлены в следующем формате:
n
a11 a12... a1n
a21 a22... a2n
.
.
.
an1 an2... ann
b1 b2... bn


Пример:
3
10 -7 0
-3 2 6
5 -1 5
7 4 6''') """
        
def input_matrix(n):
    global input_vector

    newWindow = Toplevel(root)
    newWindow.resizable(False, False)
    def on_closing():
        newWindow.destroy()
    newWindow.protocol("WM_DELETE_WINDOW", on_closing)
    newWindow.title("Введите матрицу")
    font_size=12 if n<10 else 16
    fields = {}
    matrix = [[0 for j in range(n)] for i in range(n)]
    b = [0 for i in range(n)]
    def ok(args):
        good = True
        for coords in fields.keys():
            field = fields[coords]
            value = field.get()
            i, j = coords[0]-1, coords[1]-1
            try:
                if value == '':
                    raise ValueError
                value = float(value)
                matrix[i][j] = value
                field.config({"background": "#ffffff"})
            except (ValueError, TypeError) as e:
                field.config({"background": "#ffaaaa"})
                good = False
        if not(good):
            return
        newWindow.destroy()
        input_vector(n, matrix, b)
        return
    
    def random():
        m = generate_random_solvable(n)
        matrix = m[0]
        for i in range(n):
            b[i] = m[1][i]
        for i in range(1, n+1):
            for j in range(1, n+1):
                field = fields[(i, j, )]
                value = matrix[i-1][j-1]
                field.delete(0, 'end')
                field.insert(0, str(value))
        return

    def move_entry(x):
        fields[x].focus()

    frame = Frame(
                master=newWindow,
                relief=RAISED
            )
    frame.rowconfigure(0, weight=2)
    frame.columnconfigure(0, weight=2)
    frame.grid(columnspan=n)
    Help_text = Label(master=frame, text='Введите матрицу A', font=f'Monospace {font_size}')
    Help_text.pack()
    mainFrame = Frame(
                master=newWindow,
                borderwidth=25,
                relief=FLAT
            )
    for i in range(1, n+1):
        if n<10:
            mainFrame.columnconfigure(i, weight=1, minsize=30)
        else:
            mainFrame.columnconfigure(i, weight=1, minsize=20)
        for j in range(1, n+1):
            frame = Frame(
                master=mainFrame,
                relief=RAISED,
                borderwidth=1
            )
            frame.grid(row=i, column=j, padx=10, pady=10)
            field = Entry(master=frame, width=10)
            fields[(i, j, )] = field

            if i!=1:
                fields[(i, j, )].bind('<Up>', lambda e, x=i, y=j: move_entry((x-1, y, )))
            if i!=n:
                fields[(i, j, )].bind('<Down>', lambda e, x=i, y=j: move_entry((x+1, y, )))
            if j!=1:
                fields[(i, j, )].bind('<Left>', lambda e, x=i, y=j: move_entry((x, y-1, )))
            if j!=n:
                fields[(i, j, )].bind('<Right>', lambda e, x=i, y=j: move_entry((x, y+1, )))
            field.pack()
    mainFrame.grid(row=2, columnspan=n, sticky="NSEW")
    buttonsFrame = Frame(
                master=newWindow,
                relief=FLAT,
                bg="#adadad",
                height=80
            )
    frame = Frame(
                master=buttonsFrame,
                relief=RAISED,
                borderwidth=1
            )
    frame.place(x=5*n, y=25)
    def ok_click():
        ok('')
    ok_btn = Button(master=frame, text="ОК", width=8, height=1, font='roboto 9', command=ok_click)
    ok_btn.pack()
    newWindow.update_idletasks() 
    newWindow.bind('<Return>', ok)
    frame = Frame(
                master=buttonsFrame,
                relief=RAISED,
                borderwidth=1
            )
    frame.place(x=newWindow.winfo_width()-66-5*n, y=25)
    rnd_btn = Button(master=frame, text="Случайная", width=8, height=1, font='roboto 9', command=random)
    rnd_btn.pack()
    buttonsFrame.grid(row=3, columnspan=n, sticky="NSEW")

def input_vector(n, matrix, b):
    newWindow = Toplevel(root)
    def on_closing():
        newWindow.destroy()
    newWindow.protocol("WM_DELETE_WINDOW", on_closing)
    newWindow.title("Введите вектор свободных членов B")
    fields = {}
    vector = [0 for i in range(n)]
    def fill():
        for i in range(1, n+1):
            fields[i].delete(0, 'end')
            fields[i].insert(0, b[i-1])

    def ok(args):
        good = True
        for i in fields.keys():
            field = fields[i]
            value = field.get()
            try:
                if value == '':
                    raise ValueError
                value = float(value)
                vector[i-1] = value
            except (ValueError, TypeError) as e:
                field.config({"background": "#ffaaaa"})
                good = False
        if not(good):
            return
        newWindow.destroy()
        packed = solve(matrix, vector, n)
        showResults(packed)
        return
    
    def move_entry(x):
        fields[x].focus()

    mainFrame = Frame(
                master=newWindow,
                borderwidth=25,
                relief=FLAT
            )
    for i in range(1, n+1):
        frame = Frame(
            master=mainFrame,
            relief=RAISED,
            borderwidth=1
        )
        frame.grid(row=i, padx=10, pady=10)
        field = Entry(master=frame, width=10)
        fields[i] = field
        if i!=1:
            fields[i].bind('<Up>', lambda e, x=i: move_entry(x-1))
        if i!=n:
            fields[i].bind('<Down>', lambda e, x=i: move_entry(x+1))
        
        field.pack()
    mainFrame.grid(row=2, columnspan=n, sticky="E")
    frame = Frame(
                master=newWindow,
                relief=FLAT,
                height=80,
                bg = '#adadad'
            )
    def ok_click():
        ok('')
    okbtn = Button(master=frame, text="ОК", width=10, height=1, font='roboto 10', command=ok_click)
    okbtn.pack()
    frame.grid(row=3, columnspan=n, sticky="NSEW")
    newWindow.bind('<Return>', ok)
    fill()
class App(Frame):
    
    def __init__(self):
        super().__init__()

        self.initUI()

    

    def initUI(self):
        self.master.title("Решение СЛАУ методом Гаусса")
        self.pack(fill=BOTH, expand=True)
        self.n = 0
        def ok():
            try:
                self.n = int(w.get())
                if self.n>20 or self.n<0:
                    raise TypeError
                input_matrix(self.n)
            except (TypeError, ValueError) as e:
                showLargeMessage('''Размерность матрицы должна быть целым числом от 2 до 20''', "Ошибка")
        l = Label(self,text="Введите размерность матрицы n:", font='roboto 14')
        l.place(relx=.5, rely=.15, anchor = CENTER)

        w = Spinbox(self, from_ = 2, to = 20, width=8, font='roboto 12')
        w.place(relx=.5, rely=.35, anchor = CENTER)

        okbtn = Button(self, text="ОК", width=10, height=1, font='roboto 10', command=ok)
        okbtn.place(relx=.5, rely=.6, anchor = CENTER)
        
        hbtn = Button(self, text="Из файла", width=10, font='roboto 10', command=select_file)
        hbtn.place(relx=.15, rely=.85, anchor = CENTER)
        def showHelp():
            showLargeMessage(HELP_MESSAGE, "Помощь")
            return
        obtn = Button(self, text="Помощь", width=10, font='roboto 10', command=showHelp)
        obtn.place(relx=.85, rely=.85, anchor = CENTER)



def main():
    global root
    root = Tk()
    root.geometry("450x180")
    root.resizable(False, False)
    app = App()
    root.mainloop()

def savefileas(text):    
    try:
        path = fd.asksaveasfile(filetypes = (("Text files", "*.txt"), ("All files", "*.*"))).name
    
    except:
        return   
    
    with open(path, 'w') as f:
        f.write(text)

def showResults(message):
    newWindow = Toplevel(root)
    def on_closing():
        txt.configure(state=NORMAL)
        txt.delete("1.0", END)
        newWindow.destroy()
    newWindow.protocol("WM_DELETE_WINDOW", on_closing)
    newWindow.title("Решение")
    newWindow.geometry("800x600")
    
    txt = scrolledtext.ScrolledText(newWindow, undo=True)
    txt['font'] = ('Courier New, monospace', '12')
    txt.pack(side=TOP, expand=1, fill=BOTH)
    txt.insert(INSERT, message)
    txt.configure(state=DISABLED)
    buttonFrame = Frame(
                master=newWindow,
                relief=FLAT,
                borderwidth=1,
                height=120,
                bg = '#adadad'
            )
    buttonFrame.pack(side=BOTTOM, expand=1, fill=BOTH)
    def save():
        savefileas(message)
        on_closing()
    savebtn = Button(buttonFrame, text="Save to file", width=10, borderwidth=1, height=1, font='roboto 10', command=save)
    savebtn.pack(expand=1)
    okbtn = Button(buttonFrame, text="Close", width=10, height=1, borderwidth=1, font='roboto 10', command=on_closing)
    okbtn.pack(expand=1)
    
    
def showLargeMessage(message, title):
    newWindow = Toplevel(root)
    def on_closing():
        txt.configure(state=NORMAL)
        txt.delete("1.0", END)
        newWindow.destroy()
    newWindow.protocol("WM_DELETE_WINDOW", on_closing)
    newWindow.title(title)
    newWindow.geometry("800x600")
    txt = scrolledtext.ScrolledText(newWindow, undo=True)
    txt['font'] = ('Courier New, monospace', '12')
    txt.pack(expand=True, fill='both')
    txt.insert(INSERT, message)
    txt.configure(state=DISABLED)
    


if __name__ == '__main__':
    main()