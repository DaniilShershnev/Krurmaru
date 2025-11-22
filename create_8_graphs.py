#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Создание 8 графиков профиля струны для i = 1,2,3,4,5,6,7,8
"""

def create_svg_header(width, height):
    """Создать заголовок SVG"""
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
<defs>
    <style>
        text {{ font-family: Arial, sans-serif; }}
        .title {{ font-size: 18px; font-weight: bold; }}
        .label {{ font-size: 14px; }}
    </style>
</defs>
'''

def create_svg_footer():
    """Закрыть SVG"""
    return '</svg>'

def triangular_profile(x, h=100, l=100):
    """Треугольный профиль φ(x) = h(1 - |x|/l)"""
    if abs(x) <= l:
        return h * (1 - abs(x) / l)
    else:
        return 0

def create_profile_graph(i, total_graphs=8):
    """
    Создать график профиля для момента времени i
    i = 1,2,3,4,5,6,7,8
    Время: t = (i-1) * l/(4c), чтобы покрыть от 0 до почти 2*l/c
    """

    width, height = 900, 450
    svg = create_svg_header(width, height)

    # Параметры
    h = 150  # высота треугольника
    l = 150  # полуоснование

    # Определяем время для каждого i
    # i=1: t=0
    # i=2: t=l/(4c)
    # i=3: t=l/(2c)
    # i=4: t=3l/(4c)
    # i=5: t=l/c (критический момент)
    # i=6: t=5l/(4c)
    # i=7: t=3l/(2c)
    # i=8: t=7l/(4c)

    t_factor = (i - 1) / 4.0  # это будет коэффициент для t/l в единицах c
    ct = t_factor * l  # ct = центр волны

    scale_x = 1.3
    scale_y = 1.1
    origin_x = width // 2
    origin_y = height - 80

    # Определяем диапазон оси X
    if i == 1:
        x_range = 1.5 * l
    else:
        x_range = max(1.5 * l, 1.2 * (ct + l))

    # Оси
    svg += f'<line x1="{origin_x - scale_x * x_range}" y1="{origin_y}" '
    svg += f'x2="{origin_x + scale_x * x_range}" y2="{origin_y}" '
    svg += 'stroke="black" stroke-width="2" marker-end="url(#arrowX)"/>\n'

    svg += f'<line x1="{origin_x}" y1="{origin_y + 20}" '
    svg += f'x2="{origin_x}" y2="{origin_y - scale_y * h * 1.2}" '
    svg += 'stroke="black" stroke-width="2" marker-end="url(#arrowY)"/>\n'

    # Стрелки
    svg += '''<defs>
    <marker id="arrowX" markerWidth="10" markerHeight="10" refX="5" refY="3" orient="auto" markerUnits="strokeWidth">
        <path d="M0,0 L0,6 L9,3 z" fill="black" />
    </marker>
    <marker id="arrowY" markerWidth="10" markerHeight="10" refX="5" refY="3" orient="auto" markerUnits="strokeWidth">
        <path d="M0,0 L0,6 L9,3 z" fill="black" />
    </marker>
</defs>
'''

    # Рисуем профиль струны
    if i == 1:
        # t = 0: исходный треугольник
        points = []
        for x in range(-l, l+1, 3):
            y = triangular_profile(x, h, l)
            px = origin_x + scale_x * x
            py = origin_y - scale_y * y
            points.append(f"{px},{py}")
        svg += f'<polyline points="{" ".join(points)}" fill="none" stroke="blue" stroke-width="4"/>\n'

        # Отметка высоты
        svg += f'<line x1="{origin_x}" y1="{origin_y}" x2="{origin_x}" y2="{origin_y - scale_y*h}" '
        svg += 'stroke="gray" stroke-width="1" stroke-dasharray="5,5"/>\n'
        svg += f'<text x="{origin_x+15}" y="{origin_y - scale_y*h}" class="label">h</text>\n'

        time_label = "t = 0"

    else:
        # t > 0: две волны
        # Правая волна (движется вправо)
        points_r = []
        x_start_r = int(ct - l)
        x_end_r = int(ct + l)
        for x in range(x_start_r, x_end_r + 1, 3):
            y = 0.5 * triangular_profile(x - ct, h, l)
            px = origin_x + scale_x * x
            py = origin_y - scale_y * y
            points_r.append(f"{px},{py}")

        if len(points_r) > 0:
            svg += f'<polyline points="{" ".join(points_r)}" fill="none" stroke="red" stroke-width="4"/>\n'

        # Левая волна (движется влево)
        points_l = []
        x_start_l = int(-ct - l)
        x_end_l = int(-ct + l)
        for x in range(x_start_l, x_end_l + 1, 3):
            y = 0.5 * triangular_profile(x + ct, h, l)
            px = origin_x + scale_x * x
            py = origin_y - scale_y * y
            points_l.append(f"{px},{py}")

        if len(points_l) > 0:
            svg += f'<polyline points="{" ".join(points_l)}" fill="none" stroke="blue" stroke-width="4"/>\n'

        # Зазор между волнами (если есть)
        if ct > l:
            gap_left = -ct + l
            gap_right = ct - l
            svg += f'<line x1="{origin_x + scale_x * gap_left}" y1="{origin_y}" '
            svg += f'x2="{origin_x + scale_x * gap_right}" y2="{origin_y}" '
            svg += 'stroke="green" stroke-width="4"/>\n'

        # Отметки высоты полуволн
        h_half = 0.5 * h
        if ct >= l/4:
            svg += f'<text x="{origin_x + scale_x*ct + 10}" y="{origin_y - scale_y*h_half}" class="label" fill="red">h/2</text>\n'
            svg += f'<text x="{origin_x - scale_x*ct - 40}" y="{origin_y - scale_y*h_half}" class="label" fill="blue">h/2</text>\n'

        # Вычисляем время в читаемом формате
        if t_factor == 0.25:
            time_label = "t = l/(4c)"
        elif t_factor == 0.5:
            time_label = "t = l/(2c)"
        elif t_factor == 0.75:
            time_label = "t = 3l/(4c)"
        elif t_factor == 1.0:
            time_label = "t = l/c"
        elif t_factor == 1.25:
            time_label = "t = 5l/(4c)"
        elif t_factor == 1.5:
            time_label = "t = 3l/(2c)"
        elif t_factor == 1.75:
            time_label = "t = 7l/(4c)"
        else:
            time_label = f"t = {t_factor}l/c"

    # Отметки на оси X
    x_marks = []
    if i == 1:
        x_marks = [(-l, '-l'), (0, '0'), (l, 'l')]
    elif i <= 4:
        x_marks = [(-ct, f'-{t_factor}l'), (0, '0'), (ct, f'{t_factor}l')]
    else:
        # Для больших t показываем границы волн
        x_marks = [
            (-ct-l, f'-{t_factor+1}l'),
            (-ct, f'-{t_factor}l'),
            (0, '0'),
            (ct, f'{t_factor}l'),
            (ct+l, f'{t_factor+1}l')
        ]

    for x_val, label in x_marks:
        px = origin_x + scale_x * x_val
        if abs(px - origin_x) < scale_x * x_range:  # Проверяем, что точка в пределах графика
            svg += f'<line x1="{px}" y1="{origin_y-5}" x2="{px}" y2="{origin_y+5}" stroke="black" stroke-width="2"/>\n'
            svg += f'<text x="{px}" y="{origin_y+25}" text-anchor="middle" class="label">{label}</text>\n'

    # Заголовок
    svg += f'<text x="{width//2}" y="35" text-anchor="middle" class="title">{time_label} (график {i})</text>\n'

    # Добавляем информацию о состоянии
    if i == 1:
        status = "Начальный профиль"
    elif i <= 4:
        status = "Волны перекрываются"
    elif i == 5:
        status = "Критический момент - волны касаются"
    else:
        status = "Волны полностью разошлись"

    svg += f'<text x="{width//2}" y="60" text-anchor="middle" font-size="14px" fill="#666">{status}</text>\n'

    svg += create_svg_footer()
    return svg

def create_all_8_graphs():
    """Создать все 8 графиков"""

    for i in range(1, 9):
        svg = create_profile_graph(i)
        filename = f'/home/user/Krurmaru/график_{i}.svg'

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(svg)

        print(f"✓ График {i} создан: график_{i}.svg")

    print("\n✅ Все 8 графиков успешно созданы!")
    print("\nСписок файлов:")
    for i in range(1, 9):
        if i == 1:
            desc = "t = 0 (начальный профиль)"
        elif i == 2:
            desc = "t = l/(4c)"
        elif i == 3:
            desc = "t = l/(2c)"
        elif i == 4:
            desc = "t = 3l/(4c)"
        elif i == 5:
            desc = "t = l/c (критический момент)"
        elif i == 6:
            desc = "t = 5l/(4c)"
        elif i == 7:
            desc = "t = 3l/(2c)"
        elif i == 8:
            desc = "t = 7l/(4c)"

        print(f"  {i}. график_{i}.svg - {desc}")

if __name__ == '__main__':
    create_all_8_graphs()
