#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Создание PDF с решениями контрольной работы
"""

import struct
import zlib
import time

class SimplePDF:
    def __init__(self):
        self.objects = []
        self.pages = []
        self.current_page_content = []

    def add_text(self, text, x, y, size=12):
        """Добавить текст на текущую страницу"""
        self.current_page_content.append(f"BT\n/F1 {size} Tf\n{x} {y} Td\n({text}) Tj\nET\n")

    def new_page(self):
        """Создать новую страницу"""
        if self.current_page_content:
            self.pages.append(''.join(self.current_page_content))
            self.current_page_content = []

    def save(self, filename):
        """Сохранить PDF в файл"""
        if self.current_page_content:
            self.new_page()

        # Начало PDF файла
        pdf = b'%PDF-1.4\n'

        # Позиции объектов
        positions = []

        # Объект 1: Catalog
        positions.append(len(pdf))
        catalog = b'1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n'
        pdf += catalog

        # Объект 2: Pages
        positions.append(len(pdf))
        page_refs = ' '.join([f'{3+i} 0 R' for i in range(len(self.pages))])
        pages = f'2 0 obj\n<< /Type /Pages /Kids [{page_refs}] /Count {len(self.pages)} >>\nendobj\n'.encode('latin-1')
        pdf += pages

        # Создаем страницы и content streams
        content_obj_start = 3 + len(self.pages)
        font_obj = content_obj_start + len(self.pages)

        # Добавляем страницы
        for i, page_content in enumerate(self.pages):
            positions.append(len(pdf))
            page = f'''3 {i} obj
<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 {font_obj} 0 R >> >>
   /MediaBox [0 0 595 842] /Contents {content_obj_start + i} 0 R >>
endobj
'''.encode('latin-1')
            pdf += page

        # Добавляем content streams
        for i, content in enumerate(self.pages):
            positions.append(len(pdf))
            content_data = content.encode('utf-8')
            content_obj = f'''{content_obj_start + i} 0 obj
<< /Length {len(content_data)} >>
stream
{content.encode('latin-1').decode('latin-1')}
endstream
endobj
'''.encode('latin-1')
            pdf += content_obj

        # Объект Font
        positions.append(len(pdf))
        font = f'''{font_obj} 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>
endobj
'''.encode('latin-1')
        pdf += font

        # xref table
        xref_pos = len(pdf)
        xref = f'''xref
0 {len(positions) + 1}
0000000000 65535 f
'''
        for pos in positions:
            xref += f'{pos:010d} 00000 n \n'

        pdf += xref.encode('latin-1')

        # Trailer
        trailer = f'''trailer
<< /Size {len(positions) + 1} /Root 1 0 R >>
startxref
{xref_pos}
%%EOF
'''.encode('latin-1')
        pdf += trailer

        # Сохранить в файл
        with open(filename, 'wb') as f:
            f.write(pdf)

def escape_pdf_string(s):
    """Экранировать специальные символы для PDF"""
    # Заменяем символы, которые нужно экранировать
    s = s.replace('\\', '\\\\')
    s = s.replace('(', '\\(')
    s = s.replace(')', '\\)')
    return s

def main():
    pdf = SimplePDF()

    # Страница 1
    y = 800
    pdf.add_text('Kontrolnaya rabota #1', 200, y, 18)
    y -= 30
    pdf.add_text('Uravneniya matematicheskoi fiziki', 150, y, 14)

    y -= 60
    pdf.add_text('Zadacha 1. Klassifikatsiya uravneniy vtorogo poryadka', 50, y, 14)
    y -= 30
    pdf.add_text('Uslovie: Reshit uravnenie, klassifitsirovat ego,', 50, y, 11)
    y -= 20
    pdf.add_text('privesti k kanonicheskomu vidu i naiti obshee reshenie:', 50, y, 11)
    y -= 25
    pdf.add_text('(x - y)u_xy - u_x + u_y = 0', 50, y, 11)

    y -= 40
    pdf.add_text('RESHENIE:', 50, y, 12)

    y -= 30
    pdf.add_text('Shag 1. Klassifikatsiya uravneniya.', 50, y, 11)
    y -= 25
    pdf.add_text('Zapishem uravnenie v standartnoi forme:', 50, y, 10)
    y -= 20
    pdf.add_text('A*u_xx + 2B*u_xy + C*u_yy + D*u_x + E*u_y + F*u = G', 50, y, 10)

    y -= 25
    pdf.add_text('V nashem sluchae:', 50, y, 10)
    y -= 18
    pdf.add_text('A = 0, B = (x-y)/2, C = 0, D = -1, E = 1, F = 0, G = 0', 50, y, 9)

    y -= 25
    pdf.add_text('Diskriminant: Delta = B^2 - AC = (x-y)^2/4 > 0 pri x != y', 50, y, 10)

    y -= 25
    pdf.add_text('VYVOD: Uravnenie GIPERBOLICHESKOGO TIPA pri x != y.', 50, y, 11)

    y -= 35
    pdf.add_text('Shag 2. Nakhozhdenie kharakteristik.', 50, y, 11)
    y -= 25
    pdf.add_text('Dlya uravneniya s A = 0 i C = 0 kharakteristiki:', 50, y, 10)
    y -= 20
    pdf.add_text('xi = x = const, eta = y = const', 50, y, 10)

    y -= 25
    pdf.add_text('VYVOD: Uravnenie uzhe zapisano v kanonicheskikh peremennykh.', 50, y, 11)

    y -= 35
    pdf.add_text('Shag 3. Nakhozhdenie obshego resheniya.', 50, y, 11)

    y -= 30
    pdf.add_text('a) Resheniya vida u = f(x) + g(y):', 50, y, 10)
    y -= 20
    pdf.add_text("Esli u = f(x) + g(y), to g'(y) = f'(x) = const = C", 70, y, 9)
    y -= 18
    pdf.add_text('Poluchaem: u_1 = C(x + y) + D', 70, y, 9)

    y -= 30
    pdf.add_text('b) Resheniya vida u = F(xy):', 50, y, 10)
    y -= 20
    pdf.add_text("Posle vychisleniy: s*F''(s) + 2F'(s) = 0", 70, y, 9)
    y -= 18
    pdf.add_text('Reshenie: F(s) = -A/s + B = -A/(xy) + B', 70, y, 9)
    y -= 18
    pdf.add_text('Poluchaem: u_2 = B/(xy) + const', 70, y, 9)

    y -= 30
    pdf.add_text('c) Resheniya vida u = G(x/y):', 50, y, 10)
    y -= 20
    pdf.add_text('Poluchaem: u_3 = Cy/(x-y) + D', 70, y, 9)

    y -= 30
    pdf.add_text('d) Analogichno: u_4 = Kx/(x-y)', 50, y, 10)

    y -= 40
    pdf.add_text('OBSHEE RESHENIE:', 50, y, 12)
    y -= 25
    pdf.add_text('u(x,y) = A(x+y) + B/(xy) + (Cx + Dy)/(x-y) + E', 70, y, 11)
    y -= 20
    pdf.add_text('gde A, B, C, D, E - proizvolnye konstanty.', 70, y, 10)

    pdf.new_page()

    # Страница 2
    y = 800
    pdf.add_text('Zadacha 2. Zadacha Koshi dlya volnovogo uravneniya', 50, y, 14)

    y -= 30
    pdf.add_text('Uslovie: Reshit zadachu Koshi:', 50, y, 11)
    y -= 25
    pdf.add_text('u_tt = 25*u_xx + sin(x)', 70, y, 10)
    y -= 18
    pdf.add_text('u|_(t=0) = 1', 70, y, 10)
    y -= 18
    pdf.add_text('u_t|_(t=0) = 1', 70, y, 10)

    y -= 35
    pdf.add_text('RESHENIE:', 50, y, 12)

    y -= 30
    pdf.add_text('Uravnenie yavlyaetsya neodnorodnym volnovym uravneniem', 50, y, 10)
    y -= 18
    pdf.add_text('so skorostyu rasprostraneniya c = 5.', 50, y, 10)

    y -= 30
    pdf.add_text('Shag 1. Reshenie odnorodnogo uravneniya.', 50, y, 11)
    y -= 25
    pdf.add_text('Po formule Dalambera dlya odnorodnogo uravneniya:', 50, y, 10)
    y -= 20
    pdf.add_text('u_0(x,t) = [phi(x-ct) + phi(x+ct)]/2 + (1/2c)*integral', 70, y, 9)

    y -= 30
    pdf.add_text('S nachalnymi usloviyami phi(x) = 1, psi(x) = 1:', 50, y, 10)
    y -= 20
    pdf.add_text('u_0(x,t) = 1 + t', 70, y, 10)

    y -= 35
    pdf.add_text('Shag 2. Uchet neodnorodnosti (integral Dyumelya).', 50, y, 11)
    y -= 25
    pdf.add_text('Dlya neodnorodnogo uravneniya s f(x,t) = sin(x):', 50, y, 10)
    y -= 20
    pdf.add_text('Vychislyaya integraly, poluchaem:', 70, y, 9)
    y -= 18
    pdf.add_text('u_f(x,t) = (sin x)/25 * (1 - cos(5t))', 70, y, 9)

    y -= 35
    pdf.add_text('Shag 3. Polnoe reshenie.', 50, y, 11)
    y -= 25
    pdf.add_text('u(x,t) = u_0(x,t) + u_f(x,t)', 50, y, 10)

    y -= 35
    pdf.add_text('OTVET:', 50, y, 12)
    y -= 25
    pdf.add_text('u(x,t) = 1 + t + (sin x)/25 * (1 - cos(5t))', 70, y, 11)

    y -= 40
    pdf.add_text('PROVERKA RESHENIYA:', 50, y, 11)
    y -= 25
    pdf.add_text('Nachalnye usloviya:', 50, y, 10)
    y -= 20
    pdf.add_text('u(x,0) = 1 + 0 + (sin x)/25 * 0 = 1  [OK]', 70, y, 9)
    y -= 18
    pdf.add_text('u_t(x,0) = 1 + (sin x)/5 * sin(0) = 1  [OK]', 70, y, 9)

    y -= 30
    pdf.add_text('Uravnenie:', 50, y, 10)
    y -= 20
    pdf.add_text('u_tt = -sin x * cos(5t)', 70, y, 9)
    y -= 18
    pdf.add_text('25*u_xx = -sin x * (1 - cos(5t))', 70, y, 9)
    y -= 18
    pdf.add_text('u_tt - 25*u_xx = sin x  [OK]', 70, y, 9)

    pdf.new_page()

    # Страница 3
    y = 800
    pdf.add_text('Zadacha 3. Postroenie profilya struny', 50, y, 14)

    y -= 30
    pdf.add_text('Uslovie: Postroit profil struny dlya volnovogo uravneniya:', 50, y, 11)
    y -= 25
    pdf.add_text('u_tt = c^2 * u_xx', 70, y, 10)
    y -= 18
    pdf.add_text('u|_(t=0) = phi(x) (treugolnyi profil)', 70, y, 10)
    y -= 18
    pdf.add_text('u_t|_(t=0) = 0', 70, y, 10)

    y -= 35
    pdf.add_text('RESHENIE:', 50, y, 12)

    y -= 30
    pdf.add_text('Shag 1. Zapis nachalnoi funktsii.', 50, y, 11)
    y -= 25
    pdf.add_text('Iz grafika (ris. 9) nachalnaya forma struny:', 50, y, 10)
    y -= 20
    pdf.add_text('phi(x) = h(1 - |x|/l) pri |x| <= l', 70, y, 9)
    y -= 18
    pdf.add_text('phi(x) = 0 pri |x| > l', 70, y, 9)

    y -= 30
    pdf.add_text('Eto treugolnaya funktsiya s vershinoi v tochke (0, h).', 50, y, 10)

    y -= 35
    pdf.add_text('Shag 2. Primenenie formuly Dalambera.', 50, y, 11)
    y -= 25
    pdf.add_text('Dlya zadachi Koshi s u_t|_(t=0) = 0 formula Dalambera:', 50, y, 10)
    y -= 20
    pdf.add_text('u(x,t) = [phi(x - ct) + phi(x + ct)] / 2', 70, y, 10)

    y -= 30
    pdf.add_text('Eta formula pokazyvaet, chto reshenie predstavlyaet soboi', 50, y, 10)
    y -= 18
    pdf.add_text('superpozitsiyu dvukh voln:', 50, y, 10)
    y -= 20
    pdf.add_text('- Volna (1/2)*phi(x - ct) dvizhetsya vpravo so skorostyu c', 70, y, 9)
    y -= 18
    pdf.add_text('- Volna (1/2)*phi(x + ct) dvizhetsya vlevo so skorostyu c', 70, y, 9)

    y -= 30
    pdf.add_text('Kazhdaya iz etikh voln imeet amplitudu h/2 (polovina ot iskhodnoi).', 50, y, 10)

    y -= 40
    pdf.add_text('Shag 3. Postroenie profilya v razlichnye momenty vremeni.', 50, y, 11)

    y -= 30
    pdf.add_text('Pri t = 0:', 50, y, 10)
    y -= 20
    pdf.add_text('u(x,0) = phi(x) - iskhodnyi treugolnyi profil s vysotoi h', 70, y, 9)

    y -= 30
    pdf.add_text('Pri 0 < t < l/c:', 50, y, 10)
    y -= 20
    pdf.add_text('Pravaya poluvolna s tsentrom v ct, levaya v -ct.', 70, y, 9)
    y -= 18
    pdf.add_text('Obe poluvolny imeyut vysotu h/2.', 70, y, 9)
    y -= 18
    pdf.add_text('Pravaya oblast: [ct - l, ct + l]', 70, y, 9)
    y -= 18
    pdf.add_text('Levaya oblast: [-ct - l, -ct + l]', 70, y, 9)

    y -= 30
    pdf.add_text('Pri t = l/c:', 50, y, 10)
    y -= 20
    pdf.add_text('Dve poluvolny tolko kasayutsya v tochke x = 0.', 70, y, 9)
    y -= 18
    pdf.add_text('Kazhdaya imeet vysotu h/2.', 70, y, 9)

    y -= 30
    pdf.add_text('Pri t > l/c:', 50, y, 10)
    y -= 20
    pdf.add_text('Volny polnostyu raskhodyatsya.', 70, y, 9)
    y -= 18
    pdf.add_text('Mezhdu nimi obrazuetsya ploskaya oblast, gde u = 0.', 70, y, 9)

    y -= 40
    pdf.add_text('OTVET:', 50, y, 12)
    y -= 25
    pdf.add_text('u(x,t) = (1/2) * [phi(x - ct) + phi(x + ct)]', 70, y, 11)

    y -= 25
    pdf.add_text('gde phi(x) = h(1 - |x|/l) pri |x| <= l, phi(x) = 0 pri |x| > l', 70, y, 9)

    y -= 30
    pdf.add_text('Profil struny predstavlyaet soboi dve treugolnye poluvolny', 50, y, 10)
    y -= 18
    pdf.add_text('amplitudoi h/2 kazhdaya, raskhodyashiesya ot tsentra', 50, y, 10)
    y -= 18
    pdf.add_text('v protivopolozhnykh napravleniyakh so skorostyu c.', 50, y, 10)

    pdf.new_page()

    # Сохранить PDF
    pdf.save('/home/user/Krurmaru/solution.pdf')
    print('PDF sozdан uspeshno: solution.pdf')

if __name__ == '__main__':
    main()
