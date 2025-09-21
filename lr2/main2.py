"""
Игра-угадайка (бинарный поиск)
"""

def main(targets, value) -> tuple[int, int]: # функция реализации бинарного поиска
    counter = 0 # счётчик количества сравнений бинарного поиска
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
    l_bord = int(input("Введите начало списка: ")) # пользователь задаёт начало списка ждя поиска
    h_bord = int(input("Введите конец списка: ")) # пользователь задаёт конец списка ждя поиска
    find_v = list(range(l_bord, h_bord + 1)) # список для нахождения искомого числа
    value = int(input(f"Загадайте число от {l_bord} до {h_bord}: ")) # пользователь задаёт искомое число

    index, counter = main(find_v, value) # вызов функции main() для реализации бинарного поиска для вводных данных

    if index:
        print(f"Число {find_v[index]}")
        print(f"Количество сравнений: {counter}")
    else:
        print("Число не найдено.")


user_input()
