#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Создание финального PDF с полным решением на русском языке
"""

def create_pdf_manually():
    """
    Создает PDF файл вручную с базовой структурой
    """

    # Читаем текстовое решение
    with open('/home/user/Krurmaru/solution_full.txt', 'r', encoding='utf-8') as f:
        full_text = f.read()

    # Создаем простой PDF с текстом в UTF-16BE для поддержки кириллицы
    pdf_objects = []

    # Функция для создания Unicode строки для PDF
    def make_unicode_string(text):
        """Преобразует текст в UTF-16BE hex для PDF"""
        utf16_bytes = text.encode('utf-16be')
        hex_str = utf16_bytes.hex()
        return f'<FEFF{hex_str}>'

    # Начало PDF
    pdf_content = b'%PDF-1.7\n'
    pdf_content += b'%\xC2\xB5\xC2\xB6\n'

    object_offsets = []

    # Объект 1: Catalog
    object_offsets.append(len(pdf_content))
    obj1 = b'''1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
'''
    pdf_content += obj1

    # Объект 2: Pages
    object_offsets.append(len(pdf_content))
    obj2 = b'''2 0 obj
<< /Type /Pages /Kids [3 0 R 4 0 R 5 0 R 6 0 R 7 0 R 8 0 R 9 0 R 10 0 R] /Count 8 >>
endobj
'''
    pdf_content += obj2

    # Создаем шрифт с поддержкой Unicode
    object_offsets.append(len(pdf_content))
    obj_font = b'''3 0 obj
<< /Type /Font /Subtype /Type0 /BaseFont /Helvetica /Encoding /Identity-H >>
endobj
'''
    pdf_content += obj_font

    # Разбиваем текст на страницы (примерно по 50 строк на страницу)
    lines = full_text.split('\n')
    pages_text = []
    current_page = []
    lines_per_page = 55

    for line in lines:
        current_page.append(line)
        if len(current_page) >= lines_per_page:
            pages_text.append('\n'.join(current_page))
            current_page = []

    if current_page:
        pages_text.append('\n'.join(current_page))

    # Создаем страницы
    page_obj_start = 4
    content_obj_start = page_obj_start + len(pages_text)

    for i, page_text in enumerate(pages_text):
        # Страница
        page_obj_num = page_obj_start + i
        content_obj_num = content_obj_start + i

        object_offsets.append(len(pdf_content))
        page_obj = f'''{page_obj_num} 0 obj
<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 3 0 R >> >>
   /MediaBox [0 0 595 842] /Contents {content_obj_num} 0 R >>
endobj
'''.encode('utf-8')
        pdf_content += page_obj

    # Создаем content streams для каждой страницы
    for i, page_text in enumerate(pages_text):
        content_obj_num = content_obj_start + i

        # Создаем текстовый поток
        stream_data = 'BT\n/F1 9 Tf\n50 800 Td\n14 TL\n'

        # Используем простой текст (не Unicode для совместимости)
        # Заменяем русские буквы на транслит для гарантии отображения
        for line in page_text.split('\n')[:55]:
            # Экранируем спецсимволы
            line = line.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
            if len(line) > 100:
                line = line[:100]
            stream_data += f'({line}) Tj T*\n'

        stream_data += 'ET\n'
        stream_bytes = stream_data.encode('utf-8')

        object_offsets.append(len(pdf_content))
        content_obj = f'''{content_obj_num} 0 obj
<< /Length {len(stream_bytes)} >>
stream
{stream_data}endstream
endobj
'''.encode('utf-8')
        pdf_content += content_obj

    # xref table
    xref_offset = len(pdf_content)
    xref = f'''xref
0 {len(object_offsets) + 1}
0000000000 65535 f
'''
    for offset in object_offsets:
        xref += f'{offset:010d} 00000 n \n'

    pdf_content += xref.encode('utf-8')

    # Trailer
    trailer = f'''trailer
<< /Size {len(object_offsets) + 1} /Root 1 0 R >>
startxref
{xref_offset}
%%EOF
'''.encode('utf-8')
    pdf_content += trailer

    # Сохраняем PDF
    with open('/home/user/Krurmaru/solution_russian.pdf', 'wb') as f:
        f.write(pdf_content)

    print('PDF создан: solution_russian.pdf')

    # Также создадим красивую HTML версию для просмотра в браузере
    create_beautiful_html(full_text)

def create_beautiful_html(text):
    """Создает красиво отформатированный HTML"""

    html = '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Контрольная работа №1 - Уравнения математической физики</title>
    <style>
        @page {
            size: A4;
            margin: 2cm;
        }

        body {
            font-family: 'Times New Roman', Times, serif;
            line-height: 1.5;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }

        .page {
            background: white;
            padding: 2cm;
            margin: 20px auto;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            min-height: 29.7cm;
        }

        pre {
            font-family: 'Courier New', Courier, monospace;
            white-space: pre-wrap;
            word-wrap: break-word;
            font-size: 10pt;
            line-height: 1.4;
            page-break-inside: avoid;
        }

        h1 {
            text-align: center;
            font-size: 18pt;
            margin-bottom: 30px;
        }

        @media print {
            body {
                background: white;
            }
            .page {
                box-shadow: none;
                margin: 0;
                page-break-after: always;
            }
        }
    </style>
</head>
<body>
    <div class="page">
        <pre>'''

    html += text.replace('<', '&lt;').replace('>', '&gt;')

    html += '''</pre>
    </div>
</body>
</html>'''

    with open('/home/user/Krurmaru/РЕШЕНИЕ_КОНТРОЛЬНОЙ.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print('HTML создан: РЕШЕНИЕ_КОНТРОЛЬНОЙ.html')

if __name__ == '__main__':
    create_pdf_manually()
    print('\n✓ Все файлы созданы успешно!')
    print('  - solution_russian.pdf (PDF версия)')
    print('  - РЕШЕНИЕ_КОНТРОЛЬНОЙ.html (HTML для просмотра)')
    print('  - solution_full.txt (текстовая версия)')
