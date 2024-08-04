# Список всіх операцій, та їх пріоритет
import math

config = {
    '(': 0,
    ')': 0,
    '-': 1,
    '+': 1,
    'g': 2,  # GCD
    'l': 2,  # LCD
    'a': 2,  # MAX
    'i': 2,  # MIN
    's': 2,  # SIN
    'c': 2,  # COS
    't': 2,  # TAN
    'p': 2,  # TAN
    '*': 3,
    '/': 3,
    '%': 3,
    '^': 4,
    '!': 5,
    '~': 6,  # Унарний мінус
}

constants = {
    '@p': 3.141592,
    '@e': 2.718281,
    '@c': 299792458
}


def isValid(expression):
    expression = validate(expression)
    for entry in expression:
        if not (entry in config.keys() or entry.isdigit() or entry == '.'):
            return False
    if any(char in expression for char in config.keys()):
        return expression
    else:
        return False


def validate(expression):
    expression = expression.replace(' ', '')
    expression = expression.replace(',', '.')
    expression = expression.replace('gcd', 'g')
    expression = expression.replace('lcd', 'l')
    expression = expression.replace('max', 'a')
    expression = expression.replace('min', 'i')
    expression = expression.replace('sin', 's')
    expression = expression.replace('cos', 'c')
    expression = expression.replace('tg', 't')
    expression = expression.replace('tan', 't')
    expression = expression.replace('phi', 'p')
    for constant in constants.keys():
        expression = expression.replace(constant, str(constants[constant]))
    bracketLoop = 0
    for i in expression:
        if i == '(':
            bracketLoop += 1
        elif i == ')':
            bracketLoop -= 1
    if bracketLoop > 0:
        expression += ')' * bracketLoop
    elif bracketLoop < 0:
        expression = "(" * abs(bracketLoop) + expression
    return expression


def toPostfix(expression):
    result = ""  # Коміркка для постфіксного запису
    operations = []  # Стек операцій
    currentNumber = ''
    for i in range(0, len(expression)):
        if expression[i] in config.keys():
            if currentNumber != ' ':  # Перевірка щоб не пушити два пустих числа, тобто зайві пробели
                result += currentNumber
                currentNumber = ' '
            # Це операція
            if expression[i] == '(':
                operations.append('(')
            elif expression[i] == ')':
                # Заносимо до віхдної строки все що було до першої дужки
                while len(operations) > 0 and operations[len(operations) - 1] != '(':
                    result += f' {operations.pop()}'
                operations.pop()
            else:
                op = expression[i]
                if expression[i] == '-' and (i == 0 or expression[i - 1] in config.keys()):
                    op = '~'
                while len(operations) > 0 and config[operations[len(operations) - 1]] >= config[op]:
                    result += f' {operations.pop()}'  # Занесення в вихідну строку всіх операцій з вищим пріоритетом
                operations.append(op)
        else:
            # Додавання числа в вихідну строку
            if expression[i] != ')':
                currentNumber += expression[i]
    result += currentNumber
    operations.reverse()
    for op in operations:
        if op != '(':
            result += f' {op}'
    return result


def calculateRPN(expression):
    operators = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y,
        '%': lambda x, y: x % y,
        '^': lambda x, y: x ** y,
        'g': lambda x, y: gcd(x, y),
        'l': lambda x, y: lcd(x, y),
        'a': lambda x, y: max(x, y),
        'i': lambda x, y: min(x, y),
        's': lambda x: math.sin(x),
        'c': lambda x: math.cos(x),
        't': lambda x: math.tan(x),
        'p': lambda x: euler_phi(x),
        '~': lambda x: -x,
        '!': lambda x: FactTree(x),
    }
    stack = []

    unary = ['~', '!', 's', 'c', 't', 'p']

    for token in expression.split():
        if token.replace('.', '').isdigit():
            stack.append(float(token))
        elif token in operators:
            if token in unary:
                operand1 = stack.pop()
                result = operators[token](operand1)
            else:
                operand2 = stack.pop()
                operand1 = stack.pop()
                result = operators[token](operand1, operand2)
            stack.append(result)
    if int(stack[0]) == stack[0]:
        return int(stack[0])
    return stack[0]  # Результат знаходиться у вершині стеку


def gcd(a, b):
    limiter = 0
    a, b = abs(a), abs(b)
    a, b = max(a, b), min(a, b)
    while b != 0 and limiter < 100:
        a = a % b
        a, b = b, a
        limiter += 1
    return a


def lcd(a, b):
    return int((a / gcd(a, b)) * b)


def ProdTree(l, r):
    if l > r:
        return 1
    if l == r:
        return l
    if r - l == 1:
        return l * r
    m = (l + r) // 2
    return ProdTree(l, m) * ProdTree(m + 1, r)


def FactTree(n):
    if n > 1558:
        return 1
    if n < 0:
        return 0
    if n == 0:
        return 1
    if n == 1 or n == 2:
        return n
    return ProdTree(2, n)


def euler_phi(n):
    result = n  # Початкове значення - n

    # Знаходимо прості множники числа n
    i = 2
    while i * i <= n:
        if n % i == 0:
            while n % i == 0:
                n //= i
            result *= (1.0 - (1.0 / i))
        i += 1

    # Якщо n є простим числом більшим за 1
    if n > 1:
        result *= (1.0 - (1.0 / n))

    return int(result)
