
import random, copy
import numpy as np

packed = ''''''
DISPLAY_ACC_MATRIX = 3
DISPLAY_ACC_SOLUTION = 15
restoration = []
def print_extended_matrix(a, b, n):
    global packed
    for i in range(n):
        packed+=('\t'.join([f"%.{DISPLAY_ACC_MATRIX}g" % j for j in a[i]]) + '\t|\t' + f"%.{DISPLAY_ACC_MATRIX}g" % b[i] + '\n')

def print_vector(a):
    global packed
    packed+=('\t\t'.join([f"%.{DISPLAY_ACC_SOLUTION}g" % j for j in a])+ '\n')

def prepare_matrix(a, b, k): #меняем k-ую строку дополненной матрицы на любую из строк [k, n] с максимальным по модулю k-ым элементом.

    max_elem = abs(a[k][k])
    max_index = k
    for i in range(k+1, len(a)):
        if abs(a[i][k])>max_elem:
            max_elem = a[i][k]
            max_index = i
    if max_index!=k:
        a[k], a[max_index] = a[max_index], a[k]
        b[k], b[max_index] = b[max_index], b[k]
        restoration.append([k, max_index])

def restore(b):
    a = b.copy()
    for i in reversed(restoration):
        a[i[0]], a[i[1]] = a[i[1]], a[i[0]]
    return a
def solve(a, b, n):
    global packed
    packed = ''''''
    for i in range(n):
        for j in range(n):
            a[i][j]=np.float64(a[i][j])
        b[i]=np.float64(b[i])
    for k in range(n-1): #прямой ход
        prepare_matrix(a, b, k)
        for i in range(k+1, n):
            div = a[i][k]/a[k][k]
            b[i] -= div*b[k]
            for j in range(k, n):
                a[i][j] -= div*a[k][j]
    packed+=('\nТреугольный вид матрицы: \n')
    print_extended_matrix(a, b,n)
    det = 1
    for k in range(n):
        det*=a[k][k]
    if abs(det) < 10**-8: #Т.к. операции с плав. точкой, проверку на нулевой определитель реализуем с точностью до 1e-8
        packed+=('Нулевой определитель, СЛАУ неопределенная или несовместная')
        return packed
    x = [0 for i in range(n)]
    for k in range(n-1, -1, -1): #Обратный ход
        x[k] = (b[k]-sum([a[k][j]*x[j] for j in range(k+1, n)])) / a[k][k]
    packed+=('\nВектор неизвестных: \n')
    print_vector(x)

    r = [0 for i in range(n)] #Вычисляем невязки
    for i in range(n):
        r[i] = sum([np.float64(a[i][j])*np.float64(x[j]) for j in range(n)]) - np.float64(b[i])
    packed+=('\nВектор невязок: \n')
    print_vector(restore(r))
    packed+=('\n')
    return packed

def generate_random_solvable(n):
    a = [[0 for i in range(n)] for i in range(n)]
    b = [0 for i in range(n)]
    for i in range(n):
        for j in range(n):
            a[i][j]=round(random.random()*20-10, 2)
        b[i] = round(random.random()*20-10, 2)
    if 'Нулевой определитель, СЛАУ неопределенная или несовместная' in solve(copy.deepcopy(a), b.copy(), n):
        return(generate_random_solvable())
    else:
        return((a, b))