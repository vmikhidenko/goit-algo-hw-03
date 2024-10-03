import turtle

def koch_curve(t, order, size):
    """
    Рекурсивно малює криву Коха.
    
    :param t: Об'єкт turtle.
    :param order: Рекурсивний порядок кривої.
    :param size: Довжина сторони кривої.
    """
    if order == 0:
        t.forward(size)
    else:
        koch_curve(t, order-1, size/3)
        t.left(60)
        koch_curve(t, order-1, size/3)
        t.right(120)
        koch_curve(t, order-1, size/3)
        t.left(60)
        koch_curve(t, order-1, size/3)

def draw_koch_snowflake(order, size=300):
    """
    Малює сніжинку Коха, яка складається з трьох кривих Коха.
    
    :param order: Рекурсивний порядок сніжинки.
    :param size: Довжина сторони трикутника-сніжинки.
    """
    # Налаштування екрану
    window = turtle.Screen()
    window.bgcolor("white")
    window.title("Сніжинка Коха")

    # Налаштування черепашки
    t = turtle.Turtle()
    t.speed(0)  # Максимальна швидкість малювання
    t.color("blue")
    t.penup()
    # Розраховуємо початкову позицію для центрування сніжинки
    t.goto(-size / 2, size / (2 * 3**0.5))
    t.pendown()

    # Малюємо три криві Коха, утворюючи трикутник
    for _ in range(3):
        koch_curve(t, order, size)
        t.right(120)  # Поворот на 120 градусів для наступної кривої

    # Завершуємо малювання
    t.hideturtle()
    window.mainloop()

# Виклик функції для малювання сніжинки Коха з порядком 3
draw_koch_snowflake(3)
