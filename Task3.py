def move_disk(from_peg, to_peg, pegs):
    """
    Переміщує диск з однієї вежі на іншу.

    :param from_peg: Вежа, з якої переміщується диск
    :param to_peg: Вежа, на яку переміщується диск
    :param pegs: Словник веж
    """
    if not pegs[from_peg]:
        print(f"Вежа {from_peg} пуста. Неможливо перемістити диск.")
        return
    disk = pegs[from_peg].pop()
    if pegs[to_peg] and pegs[to_peg][-1] < disk:
        print(f"Неможливо помістити диск {disk} на менший диск {pegs[to_peg][-1]}.")
        pegs[from_peg].append(disk)  # Відміна переміщення
    else:
        pegs[to_peg].append(disk)
        print(f"Перемістіть диск {disk} з вежі {from_peg} на вежу {to_peg}.")

def hanoi_recursive(n, source, target, auxiliary, pegs):
    """
    Рекурсивно вирішує задачу Ханойських веж.

    :param n: Кількість дисків
    :param source: Вежа, з якої переміщають диски
    :param target: Вежа, на яку переміщають диски
    :param auxiliary: Допоміжна вежа
    :param pegs: Словник веж
    """
    if n == 0:
        return
    hanoi_recursive(n-1, source, auxiliary, target, pegs)
    move_disk(source, target, pegs)
    hanoi_recursive(n-1, auxiliary, target, source, pegs)

def hanoi_tower_func(n):
    """
    Ініціалізує вежі та запускає рекурсивну функцію для вирішення задачі.

    :param n: Кількість дисків
    """
    # Ініціалізація веж
    pegs = {
        'A': list(range(n, 0, -1)),  # Вежа A містить диски від n до 1
        'B': [],
        'C': []
    }
    print("Початковий стан веж:")
    print(pegs)
    print("\nПослідовність переміщень:")
    hanoi_recursive(n, 'A', 'C', 'B', pegs)
    print("\nФінальний стан веж:")
    print(pegs)

# Виклик функції для 3 дисків 
hanoi_tower_func(3)
