#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Создание SVG графиков для задачи 3 - профиль струны
"""

def create_svg_header(width, height):
    """Создать заголовок SVG"""
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
<defs>
    <style>
        text {{ font-family: Arial, sans-serif; }}
        .title {{ font-size: 16px; font-weight: bold; }}
        .label {{ font-size: 14px; }}
        .small {{ font-size: 12px; }}
    </style>
</defs>
'''

def create_svg_footer():
    """Закрыть SVG"""
    return '</svg>'

def draw_axes(x_min, x_max, y_max, scale_x, scale_y, origin_x, origin_y):
    """Нарисовать оси координат"""
    svg = ''

    # Ось X
    svg += f'<line x1="{origin_x + scale_x * (x_min - 0.5)}" y1="{origin_y}" '
    svg += f'x2="{origin_x + scale_x * (x_max + 0.5)}" y2="{origin_y}" '
    svg += 'stroke="black" stroke-width="2" marker-end="url(#arrowX)"/>\n'

    # Ось Y
    svg += f'<line x1="{origin_x}" y1="{origin_y + 20}" '
    svg += f'x2="{origin_x}" y2="{origin_y - scale_y * (y_max + 0.3)}" '
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

    return svg

def triangular_profile(x, h=100, l=100):
    """Треугольный профиль φ(x) = h(1 - |x|/l)"""
    if abs(x) <= l:
        return h * (1 - abs(x) / l)
    else:
        return 0

def create_profile_at_t0():
    """График при t = 0"""
    width, height = 800, 400
    svg = create_svg_header(width, height)

    # Параметры
    h = 150  # высота
    l = 200  # полуоснование
    scale_x = 1.5
    scale_y = 1.0
    origin_x = width // 2
    origin_y = height - 80

    # Оси
    svg += draw_axes(-l*1.3, l*1.3, h*1.2, scale_x, scale_y, origin_x, origin_y)

    # Треугольник
    points = []
    for x in range(-l, l+1, 5):
        y = triangular_profile(x, h, l)
        px = origin_x + scale_x * x
        py = origin_y - scale_y * y
        points.append(f"{px},{py}")

    svg += f'<polyline points="{" ".join(points)}" fill="none" stroke="blue" stroke-width="3"/>\n'

    # Отметки на оси X
    for x_val, label in [(-l, '-l'), (0, '0'), (l, 'l')]:
        px = origin_x + scale_x * x_val
        svg += f'<line x1="{px}" y1="{origin_y-5}" x2="{px}" y2="{origin_y+5}" stroke="black" stroke-width="2"/>\n'
        svg += f'<text x="{px}" y="{origin_y+25}" text-anchor="middle" class="label">{label}</text>\n'

    # Отметка высоты
    svg += f'<line x1="{origin_x}" y1="{origin_y}" x2="{origin_x}" y2="{origin_y - scale_y*h}" stroke="gray" stroke-width="1" stroke-dasharray="5,5"/>\n'
    svg += f'<text x="{origin_x+10}" y="{origin_y - scale_y*h}" class="label">h</text>\n'

    # Заголовок
    svg += f'<text x="{width//2}" y="30" text-anchor="middle" class="title">t = 0 (начальный профиль)</text>\n'

    svg += create_svg_footer()
    return svg

def create_profile_at_t_quarter():
    """График при t = l/(4c)"""
    width, height = 900, 400
    svg = create_svg_header(width, height)

    # Параметры
    h = 150
    l = 180
    ct = l / 4  # центр волн
    scale_x = 1.5
    scale_y = 1.0
    origin_x = width // 2
    origin_y = height - 80

    # Оси
    svg += draw_axes(-l*1.5, l*1.5, h*0.8, scale_x, scale_y, origin_x, origin_y)

    # Правая волна (красная пунктирная)
    points_r = []
    for x in range(int(ct-l), int(ct+l)+1, 5):
        y = 0.5 * triangular_profile(x - ct, h, l)
        px = origin_x + scale_x * x
        py = origin_y - scale_y * y
        points_r.append(f"{px},{py}")
    svg += f'<polyline points="{" ".join(points_r)}" fill="none" stroke="red" stroke-width="2" stroke-dasharray="8,4"/>\n'

    # Левая волна (синяя пунктирная)
    points_l = []
    for x in range(int(-ct-l), int(-ct+l)+1, 5):
        y = 0.5 * triangular_profile(x + ct, h, l)
        px = origin_x + scale_x * x
        py = origin_y - scale_y * y
        points_l.append(f"{px},{py}")
    svg += f'<polyline points="{" ".join(points_l)}" fill="none" stroke="blue" stroke-width="2" stroke-dasharray="8,4"/>\n'

    # Суммарный профиль (фиолетовый жирный)
    points_sum = []
    for x in range(int(-ct-l), int(ct+l)+1, 5):
        y = 0.5 * triangular_profile(x - ct, h, l) + 0.5 * triangular_profile(x + ct, h, l)
        px = origin_x + scale_x * x
        py = origin_y - scale_y * y
        points_sum.append(f"{px},{py}")
    svg += f'<polyline points="{" ".join(points_sum)}" fill="none" stroke="purple" stroke-width="4"/>\n'

    # Отметки
    for x_val, label in [(-ct, '-l/4'), (0, '0'), (ct, 'l/4')]:
        px = origin_x + scale_x * x_val
        svg += f'<line x1="{px}" y1="{origin_y-5}" x2="{px}" y2="{origin_y+5}" stroke="black" stroke-width="2"/>\n'
        svg += f'<text x="{px}" y="{origin_y+25}" text-anchor="middle" class="label">{label}</text>\n'

    # Отметка высоты в центре
    h_center = 0.75 * h  # 3h/4
    svg += f'<text x="{origin_x+15}" y="{origin_y - scale_y*h_center}" class="small">3h/4</text>\n'

    # Легенда
    svg += f'<line x1="50" y1="60" x2="100" y2="60" stroke="red" stroke-width="2" stroke-dasharray="8,4"/>\n'
    svg += f'<text x="110" y="65" class="small">правая волна h/2</text>\n'

    svg += f'<line x1="50" y1="80" x2="100" y2="80" stroke="blue" stroke-width="2" stroke-dasharray="8,4"/>\n'
    svg += f'<text x="110" y="85" class="small">левая волна h/2</text>\n'

    svg += f'<line x1="50" y1="100" x2="100" y2="100" stroke="purple" stroke-width="4"/>\n'
    svg += f'<text x="110" y="105" class="small">суммарный профиль</text>\n'

    # Заголовок
    svg += f'<text x="{width//2}" y="30" text-anchor="middle" class="title">t = l/(4c) (волны перекрываются)</text>\n'

    svg += create_svg_footer()
    return svg

def create_profile_at_t_critical():
    """График при t = l/c (критический момент)"""
    width, height = 900, 400
    svg = create_svg_header(width, height)

    # Параметры
    h = 150
    l = 150
    ct = l  # центр волн
    scale_x = 1.2
    scale_y = 1.0
    origin_x = width // 2
    origin_y = height - 80

    # Оси
    svg += draw_axes(-l*1.8, l*1.8, h*0.7, scale_x, scale_y, origin_x, origin_y)

    # Левая волна (синяя)
    points_l = []
    for x in range(int(-ct-l), 1, 5):
        y = 0.5 * triangular_profile(x + ct, h, l)
        px = origin_x + scale_x * x
        py = origin_y - scale_y * y
        points_l.append(f"{px},{py}")
    svg += f'<polyline points="{" ".join(points_l)}" fill="none" stroke="blue" stroke-width="4"/>\n'

    # Правая волна (красная)
    points_r = []
    for x in range(0, int(ct+l)+1, 5):
        y = 0.5 * triangular_profile(x - ct, h, l)
        px = origin_x + scale_x * x
        py = origin_y - scale_y * y
        points_r.append(f"{px},{py}")
    svg += f'<polyline points="{" ".join(points_r)}" fill="none" stroke="red" stroke-width="4"/>\n'

    # Точка касания
    svg += f'<circle cx="{origin_x}" cy="{origin_y}" r="6" fill="black"/>\n'
    svg += f'<text x="{origin_x}" y="{origin_y+30}" text-anchor="middle" class="small">точка касания</text>\n'

    # Отметки
    for x_val, label in [(-2*l, '-2l'), (-l, '-l'), (0, '0'), (l, 'l'), (2*l, '2l')]:
        px = origin_x + scale_x * x_val
        svg += f'<line x1="{px}" y1="{origin_y-5}" x2="{px}" y2="{origin_y+5}" stroke="black" stroke-width="2"/>\n'
        svg += f'<text x="{px}" y="{origin_y+50}" text-anchor="middle" class="small">{label}</text>\n'

    # Отметки высоты полуволн
    h_half = 0.5 * h
    svg += f'<text x="{origin_x - scale_x*l+15}" y="{origin_y - scale_y*h_half}" class="small">h/2</text>\n'
    svg += f'<text x="{origin_x + scale_x*l+15}" y="{origin_y - scale_y*h_half}" class="small">h/2</text>\n'

    # Заголовок
    svg += f'<text x="{width//2}" y="30" text-anchor="middle" class="title">t = l/c (критический момент - волны касаются)</text>\n'

    svg += create_svg_footer()
    return svg

def create_profile_separated():
    """График при t > l/c (волны разошлись)"""
    width, height = 900, 400
    svg = create_svg_header(width, height)

    # Параметры
    h = 150
    l = 120
    ct = 1.5 * l  # центр волн
    scale_x = 1.2
    scale_y = 1.0
    origin_x = width // 2
    origin_y = height - 80

    # Оси
    svg += draw_axes(-ct*1.3, ct*1.3, h*0.7, scale_x, scale_y, origin_x, origin_y)

    # Левая волна
    points_l = []
    for x in range(int(-ct-l), int(-ct+l)+1, 5):
        y = 0.5 * triangular_profile(x + ct, h, l)
        px = origin_x + scale_x * x
        py = origin_y - scale_y * y
        points_l.append(f"{px},{py}")
    svg += f'<polyline points="{" ".join(points_l)}" fill="none" stroke="blue" stroke-width="4"/>\n'

    # Правая волна
    points_r = []
    for x in range(int(ct-l), int(ct+l)+1, 5):
        y = 0.5 * triangular_profile(x - ct, h, l)
        px = origin_x + scale_x * x
        py = origin_y - scale_y * y
        points_r.append(f"{px},{py}")
    svg += f'<polyline points="{" ".join(points_r)}" fill="none" stroke="red" stroke-width="4"/>\n'

    # Зазор (жирная линия по оси X)
    x_gap_left = -ct + l
    x_gap_right = ct - l
    svg += f'<line x1="{origin_x + scale_x*x_gap_left}" y1="{origin_y}" '
    svg += f'x2="{origin_x + scale_x*x_gap_right}" y2="{origin_y}" stroke="green" stroke-width="4"/>\n'

    # Стрелка для зазора
    gap_mid_x = origin_x
    svg += f'<line x1="{origin_x + scale_x*x_gap_left}" y1="{origin_y+30}" '
    svg += f'x2="{origin_x + scale_x*x_gap_right}" y2="{origin_y+30}" stroke="green" stroke-width="2" '
    svg += 'marker-start="url(#arrowLeft)" marker-end="url(#arrowRight)"/>\n'
    svg += f'<text x="{gap_mid_x}" y="{origin_y+50}" text-anchor="middle" class="small" fill="green" font-weight="bold">зазор: u = 0</text>\n'

    svg += '''<defs>
    <marker id="arrowLeft" markerWidth="10" markerHeight="10" refX="0" refY="3" orient="auto">
        <path d="M9,0 L9,6 L0,3 z" fill="green" />
    </marker>
    <marker id="arrowRight" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
        <path d="M0,0 L0,6 L9,3 z" fill="green" />
    </marker>
</defs>
'''

    # Отметки
    for x_val, label in [(-ct, '-3l/2'), (0, '0'), (ct, '3l/2')]:
        px = origin_x + scale_x * x_val
        svg += f'<line x1="{px}" y1="{origin_y-5}" x2="{px}" y2="{origin_y+5}" stroke="black" stroke-width="2"/>\n'
        svg += f'<text x="{px}" y="{origin_y-15}" text-anchor="middle" class="small">{label}</text>\n'

    # Заголовок
    svg += f'<text x="{width//2}" y="30" text-anchor="middle" class="title">t = 3l/(2c) (волны полностью разошлись)</text>\n'

    svg += create_svg_footer()
    return svg

def create_all_graphs():
    """Создать все графики"""

    # График 1: t = 0
    svg1 = create_profile_at_t0()
    with open('/home/user/Krurmaru/график_t0.svg', 'w', encoding='utf-8') as f:
        f.write(svg1)
    print("✓ График t=0 создан: график_t0.svg")

    # График 2: t = l/(4c)
    svg2 = create_profile_at_t_quarter()
    with open('/home/user/Krurmaru/график_t_quarter.svg', 'w', encoding='utf-8') as f:
        f.write(svg2)
    print("✓ График t=l/(4c) создан: график_t_quarter.svg")

    # График 3: t = l/c
    svg3 = create_profile_at_t_critical()
    with open('/home/user/Krurmaru/график_t_critical.svg', 'w', encoding='utf-8') as f:
        f.write(svg3)
    print("✓ График t=l/c создан: график_t_critical.svg")

    # График 4: t > l/c
    svg4 = create_profile_separated()
    with open('/home/user/Krurmaru/график_t_separated.svg', 'w', encoding='utf-8') as f:
        f.write(svg4)
    print("✓ График t>l/c создан: график_t_separated.svg")

    print("\n✅ Все 4 графика успешно созданы!")
    print("\nФайлы:")
    print("  1. график_t0.svg - начальный профиль")
    print("  2. график_t_quarter.svg - волны перекрываются")
    print("  3. график_t_critical.svg - критический момент")
    print("  4. график_t_separated.svg - волны разошлись")

if __name__ == '__main__':
    create_all_graphs()
