from solver import *
import sys

n = len(sys.argv)
if n>2:
    print('Программа запускается без аргументов в консольном режиме или с одним аргументом для чтения данных из файла.')
elif n==2:
    try:
        f = open(sys.argv[1], 'r')
        n = f.readline().split()
        if len(n)!=1:
            raise AttributeError
        n = int(n[0])
        a = []
        for i in range(n):
            line = [float(i) for i in f.readline().split()]
            a.append(line)
        b = [float(i) for i in f.readline().split()]
        solve(a, b, n)
    except Exception as e:
        print(f'Ошибка: {e}')
        print('''Файл должен быть доступен для чтения, данные в файле должны быть представлены в следующем формате:
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
7 4 6''')
else:
    n = int(input('Введите размерность матрицы n: '))
    print(f'Введите расширенную матрицу - по {n+1} элементов в каждой из {n} строк, разделенных пробелами:')
    m_ext = []
    while len(m_ext)<n:
        line = [float(i) for i in input().split()]
        if len(line)!=n+1:
            print(f'В строке должно быть {n+1} элементов!')
        else:
            m_ext.append(line)
    a = []
    b = []
    for i in m_ext:
        a.append(i[:-1])
        b.append(i[-1])
    solve(a, b, n)