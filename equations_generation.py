import math
import random

###########################
# вспомогательные функции #
###########################

def sign(number):
    """
    return sign of number like number -1 or 1
    WARNING: if number is zero it returns zero
    """
    if(number > 0):
        return(1)
    elif(number < 0):
        return(-1)
    else:
        return(0)

def simplify_fraction(a, b):
    """
    a/b
    здесь не будет выноситься целая часть из дроби, если она есть
    """
    if(a == 0):
        return(0)
    # наибольший общий делитель
    gcd = math.gcd(a, b)
    a = int(a/gcd)
    b = int(b/gcd)
    sign_frac = sign(a) * sign(b)
    if(b == 1 or b == -1):
        return(str(sign_frac * abs(a)))
    else:
        return(str(sign_frac * abs(a)) + '/' + str(abs(b)))

def multipliers_list(number):
    """
    раскладывает число на множители
    выводит список из простых множителей
    """
    multipliers = [1]
    for i in range(2, int(math.sqrt(number)) + 1):
        if(number == 1):
            return(multipliers)
        while(number % i == 0):
            number = int(number/i)
            multipliers.append(i)
    multipliers.append(number)
    return(multipliers)


def simplify_root(number):
    """
    функция выносит множители, если возможно
    и выдает результат в виде списка, где сначала идет
    вынесенная часть, а потом та, что под корнем
    """
    if(number == 0):
        return(str(0))
    # число, которое в итоге будет под корнем
    with_root = 1
    # число, которое в итоге будет вне корня
    without_root = 1
    # получаем список из множителей числа
    multipliers = multipliers_list(number)
    # ищем уникальные (разные) множители
    uniq_multipliers = set(multipliers[1:])
    # пробегаемся по каждому уникальному множителю
    # и смотрим можно ли вынести
    for i in uniq_multipliers:
        # количество одинаковых множителей
        count = multipliers.count(i)
        # количество множителей, которые можем вынести
        double_mults = count//2
        # осталось ли что-нибудь под корнем
        last = count%2
        # проверяем осталось ли что нибудь под корнем
        # от этого множителя, если остался доумножем то, что под корнем
        if(last == 1):
            with_root *= i
        # проверям есть личто-нибудь вынести из под корня
        # если есть, то доумножаем к тому что вне корня столько
        # раз, сколько можно вынести
        if(double_mults > 0):
            without_root *= i**double_mults
    return([without_root, with_root])

def root_to_text(a, b):
    """
    a*b^(1/2)
    """
    if(b == 1):
        return(str(a))
    elif(a == 1):
        return('\u221a' + str(b))
    else:
        return(str(a) + '\u221a' + str(b))

#################################
# конец вспомогательных функций #
#################################

def first_item(number, variable: str):
    """
    ТОЛЬКО ДЛЯ ПЕРВОЙ ПЕРЕМЕННОЙ
    здесь подразумевается, что первый коэффициент не может
    быть равен нулю, иначе это уже, например, не квадратное уравнение,
    если мы его хотели сдеать, а уже линейное, ответ для которого
    ищется уже по-другому
    """
    if(number == 1):
        return(variable + ' ')
    elif(number == -1):
        return('-' + variable + ' ')
    else:
        return(str(number) + variable + ' ')

def item(number, variable: str):
    """
    ТОЛЬКО ДЛЯ ВНУТРЕННИХ КОЭФФИЦИЕНТОВ
    делает коэффициент перед переменой удобным для нас
    например:
    пробел в конце строки нужен, так как после него ожидается другая
    переменная или пробел
    -4x -> '- 4x '
    -1x -> '- x '
    6x -> '+ 6x '
    """
    if(number == 1):
        if(variable == ''):
            return('+ 1 ')
        else:
            return('+ ' + variable + ' ')
    elif(number == -1):
        if(variable == ''):
            return('- 1 ')
        else:
            return('- ' + variable + ' ')
    elif(number == 0):
        return('')
    elif(number > 0):
        return('+ ' + str(number) + variable + ' ')
    elif(number < 0):
        return('- ' + str(number*(-1)) + variable + ' ')

def linear_eq(a, b):
    """
    'ax + b = 0'
    """
    return(first_item(a, 'x') + item(b, '') + '= 0')

def linear_eq_answer(a, b):
    """
    'ax + b = 0'
    answer:
    -b/a
    """
    return('x = ' + simplify_fraction(-b, a))

def quad_eq(a, b, c):
    """
    'ax^2 + bx + c = 0'
    """
    return(first_item(a, 'x\u00b2') + item(b, 'x') + item(c, '') + '= 0')

def quad_eq_answer(a, b, c):
    """
    'ax^2 + bx + c = 0'
    """
    # discriminant
    discr = b**2 - 4*a*c
    # если дискриминант равен нулю, то ответ простой без корня
    if(discr == 0):
        return('x\u2081 = ' + simplify_fraction(-b, 2*a) + '\n' + 'x\u2082 = ' + simplify_fraction(-b, 2*a))
    elif(discr < 0):
        return('Нет решений.')
    else: # далее остается узнать вынесентся ли корень из дискриминанта полностью или частично
        # получаем упрощенный (если возможно) корень из дискриминанта (в виде списка)
        root_discr = simplify_root(discr)
        if(root_discr[1] == 1): # случай,когда корень раскрылся полностью
            return('x\u2081 = ' + simplify_fraction(-b - root_discr[0], 2*a) + '\n' + 'x\u2082 = ' + simplify_fraction(-b + root_discr[0], 2*a))
        elif(root_discr[0] == 1):
            return('x\u2081 = (' + str(-b) + ' + ' + root_to_text(1, root_discr[1]) + ')/' + str(2*a) + '\n' + 'x\u2082 = (' + str(-b) + ' - ' + root_to_text(1, root_discr[1]) + ')/' + str(2*a))
        else: # сложный случай, когда дробь с корнем еще может сократиться
            # ищем НОД слагаемых числителя
            gcd_1 = math.gcd(b, root_discr[0])
            # ищем НОД числителя и знаменателя
            gcd_2 = math.gcd(gcd_1, 2*a)
            denominator = int(2*a/gcd_2)
            if(denominator == 1 or denominator == -1): # случай сокращения знаменателя дроби
                return('x\u2081 = ' + str(denominator*int(-b/gcd_2)) + ' + ' + root_to_text(int(root_discr[0]/gcd_2), root_discr[1]) + '\n' + 'x\u2082 = ' + str(denominator*int(-b/gcd_2)) + ' - ' + root_to_text(int(root_discr[0]/gcd_2), root_discr[1]))
            else:
                return('x\u2081 = (' + str(int(-b/gcd_2)) + ' + ' + root_to_text(int(root_discr[0]/gcd_2), root_discr[1]) + ')/' + str(denominator) + '\n' + 'x\u2082 = (' + str(int(-b/gcd_2)) + ' - ' + root_to_text(int(root_discr[0]/gcd_2), root_discr[1]) + ')/' + str(denominator))



def sum_expression(a: int, b: int):
    """
    выводит текст суммы двух чисел a и b
    Пример:
    для 5 и 7: '5 + 7 ='
    для -3 и -2: '-3 - 2 ='
    """
    return(str(a) + ' ' + item(b, '') + '=')

def answer_sum_expression(a: int, b: int):
    return(a + b)


def multiply_expression(a: int, b: int):
    '''
    ПРЕДПОЛАГАЕТСЯ, ЧТО a и b > 0
    выводит текст произведения двух чисел a и b
    Пример:
    для 4 и 2: '4 * 2 ='
    '''
    return(str(a) + ' * ' + str(b) + ' =')

def answer_multiply_expression(a: int, b: int):
    return(a * b)


def division_expression(a: int, b: int):
    '''
    ПРЕДПОЛАГАЕТСЯ, ЧТО a и b > 0
    выводит текст деления двух чисел a и b
    Пример:
    для 3 и 5: '3 : 5 ='
    '''
    return(str(a) + ' : ' + str(b) + ' =')

def answer_division_expression(a: int, b: int):
    return(simplify_fraction(a, b))



# далее идет диалог с пользователем
print('Меню:')
print('1) Выражения;')
print('2) Уравнения;')
type_of_equation = input('Введите номер нужного пункта: ')
print()
if(type_of_equation == '1'):
    print('Доступные выражения:')
    print('1) Сложение и разность;')
    print('2) Умножение;')
    print('3) Деление;')
    type_of_equation = input('Введите номер нужного пункта: ')
    amount = int(input("Введите количество: "))
    if(type_of_equation == '1'):
        # диапазон для выбора коэффициентов (не включая ноль)
        list_of_coefs = list(range(-100, 0)) + list(range(1,100))
        for i in range(1, amount + 1):
            print('##### ' + str(i) + ' #####')
            a = random.choice(list_of_coefs)
            b = random.choice(list_of_coefs)
            print(sum_expression(a, b))
            print(answer_sum_expression(a, b))
    elif(type_of_equation == '2'):
        # диапазон для выбора коэффициентов (не включая ноль)
        list_of_coefs = list(range(1, 100))
        for i in range(1, amount + 1):
            print('##### ' + str(i) + ' #####')
            a = random.choice(list_of_coefs)
            b = random.choice(list_of_coefs)
            print(multiply_expression(a, b))
            print(answer_multiply_expression(a, b))
    elif(type_of_equation == '3'):
        # диапазон для выбора коэффициентов (не включая ноль)
        list_of_coefs = list(range(1, 100))
        for i in range(1, amount + 1):
            print('##### ' + str(i) + ' #####')
            a = random.choice(list_of_coefs)
            b = random.choice(list_of_coefs)
            print(division_expression(a*b, b))
            print(a)
    exit(0)

print()
print('1) Линейные уравнения;')
print('2) Квадратные уравнения;')
print('3) Решить свое;')

type_of_equation = input('Введите номер нужного пункта: ')

# здесь будем решать "свое" уравнение

if(type_of_equation == '3'):
    print('Доступные уравнения:')
    print('1) Линейное уравнение;')
    print('2) Квадратное уравнение;')
    type_of_equation = input('Введите номер нужного пункта: ')
    if(type_of_equation == '1'):
        print('Вид уравнения: ax + b = 0')
        a = int(input('a: '))
        b = int(input('b: '))
        print(linear_eq(a, b))
        print(linear_eq_answer(a, b))
    else:
        print('Вид уравнения: ax\u00b2 + bx + c = 0')
        a = int(input('a: '))
        b = int(input('b: '))
        c = int(input('c: '))
        print(quad_eq(a, b, c))
        print(quad_eq_answer(a, b, c))
    exit(0)


# закончили решать "свое" уравнение

quantity_of_equations = int(input('Введите количество уравнений: '))

# диапазон для выбора коэффициентов (не включая ноль)
list_of_coefs = list(range(-20, 0)) + list(range(1,21))

if(type_of_equation == '1'):
    for i in range(quantity_of_equations):
        print('######## ' + str(i + 1) + ' ########')
        a = random.choice(list_of_coefs)
        b = random.choice(list_of_coefs)
        print(linear_eq(a, b))
        print(linear_eq_answer(a, b))
elif(type_of_equation == '2'):
    for i in range(quantity_of_equations):
        print('######## ' + str(i + 1) + ' ########')
        a = random.choice(list_of_coefs)
        b = random.choice(list_of_coefs)
        c = random.choice(list_of_coefs)
        print(quad_eq(a, b, c))
        print(quad_eq_answer(a, b, c))

