"""
Игра-угадайка (бинарный поиск)
"""


def main(targets, value): # функция реализации бинарного поиска
    counter = 1 # счётчик количества сравнений бинарного поиска
    low, high, mid = 0, len(targets) - 1, len(targets) // 2
    while targets[mid] != value and low <= high: # цикл работает, пока искомое число не нашлось
        if value > targets[mid]:
            low = mid + 1
        else:
            high = mid - 1
        mid = (low + high) // 2
        counter += 1 # добавляем 1 к счётчику в конце каждого сравнения

    if low > high:
        return None # число не нашлось
    else:
        return mid, counter # число нашлось


def user_input(): # функция взаимодействия с пользователем
    while True:
        try: # проверка на корректность введённых данных
            l_bord = int(input("Введите начало диапазона: ")) # пользователь задаёт начало списка ждя поиска
            h_bord = int(input("Введите конец диапазона: ")) # пользователь задаёт конец списка ждя поиска
            if l_bord > h_bord: # некорректный список
                print('Некорректный диапазон')
                break
            find_v = list(range(l_bord, h_bord + 1)) # список для нахождения искомого числа
            value = int(input("Загадайте число: ")) # пользователь задаёт искомое число
            if h_bord < value or l_bord > value:
                print(f'Число не внутри диапазона от {l_bord} до {h_bord}') # проверка на принадлежность числа к диапазону
                break
            index, counter = main(find_v, value) # вызов функции main() для реализации бинарного поиска для вводных данных
            if index:
                print(f"Число {find_v[index]}")
                print(f"Количество сравнений: {counter}")
            else:
                print("Число не найдено")
            break
        except ValueError: # проверка на тип данных
            print('Число не является целым')
            break


user_input() # вызов функции для реализации игры-угадайки 


user_input()
