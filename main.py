from kivy.config import Config
Config.set('graphics', 'width', '300')
Config.set('graphics', 'height', '400')
Config.set('graphics', 'multisamples', '0')

import io
import os, sys
import codecs
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.graphics import Instruction, InstructionGroup, Color, Line, Rectangle, BorderImage
from kivy.uix.button import Button
from kivy.uix.label import Label, CoreLabel
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.core.audio import SoundLoader
from kivy.resources import resource_add_path, resource_find
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
import random

# Пути к файлам
paths = {
    'logo': 'Logo.png',
    'font': 'CenturyGothic.ttf',
    'kv': 'main2.kv',
    'bg': 'bg.png',
    'mp3': 'finish.mp3'
}

class CanvasWindow(Screen):
    def __init__(self, **kwargs):
        super(CanvasWindow, self).__init__(**kwargs)

    def createCoins(self, parts, shape, color):

        # Шрифт
        LabelBase.register(name='CG', fn_regular=paths['font'])

        with self.canvas:

            Color(0,0,0,1) #black

            # Базовые размеры
            w = 595
            h = 842

            # Размеры жетона
            x = 94
            y = 94

            # Отступ от края листа
            margin = 70

            # Фон
            Color(1,1,1,1) #white
            self.canvas.add(Rectangle(size=[w,h], pos=[0, 0]))

            # Жетоны

            for i in range(len(parts)):
                # Ряд жетонов на листе
                row = 1
                row += int(i/6)
                # Надпись на жетоне
                name = CoreLabel(font_name='CG', text=parts[i], font_size=45)
                name.refresh()
                name = name.texture
                Color(0,0,0,1) #black
                if shape == 'round':
                    self.canvas.add(Line(circle=(x*(i - (row - 1)*6) + margin, y*row, 47), width=1))
                if shape == 'square':
                    self.canvas.add(Line(rectangle=(x*(i - (row - 1)*6) + margin - x/2, y*row - y/2, 94, 94), width=1))
                Color(rgba=color)
                self.canvas.add(Rectangle(size=name.size, pos=[(x*(i - (row - 1)*6)+margin)-(name.size[0]/2), y*row-name.size[1]/2], texture=name))

    def createTickets(self, parts, font_color, border_color):

        # Шрифт
        LabelBase.register(name='CG', fn_regular=paths['font'])

        with self.canvas:
            Color(0,0,0,1) #black

            # Базовые размеры
            w = 595
            h = 842

            # Отступ
            margin = 28
            marginY = 369

            # Промежуток
            middleX = 9
            middleY = 65

            # Размеры билета
            ticketX = 567
            ticketY = 369

            # Размеры ячейки
            cell = 128

            # Фон
            Color(1,1,1,1) #white
            self.canvas.add(Rectangle(size=[w,h], pos=[0, 0]))

            # Изображение
            imageX = 111
            imageY = 45

            # Билеты

            tickets = [None] * int(len(parts)/8)
            for i in range(len(tickets)):
                tickets[i] = [None] * 8

            num = 0
            for i in range(len(parts)):
                if (num/8 == 1):
                    num = 0
                tickets[int(i/8)][num] = parts[i]
                num += 1

            # trigger запускает отрисовку второго билета на листе
            trigger = 0

            for i in range(len(tickets)):
                Color(0,0,0,1) #black
                self.canvas.add(Line(rectangle=(0, marginY*trigger, w, ticketY), width=1))
                for num in range(len(tickets[i])):
                    # Ряд в билете
                    j = 1
                    j += int(num/4)

                    # Формирование содержимого ячейки
                    name = CoreLabel(font_name='CG', text=str(tickets[i][num]), font_size=45)
                    name.refresh()
                    name = name.texture

                    Color(rgba=border_color)
                    self.canvas.add(Line(rectangle=(margin + (cell+middleX)*(num - (j-1)*4), margin + (cell+middleY)*(j-1) + marginY*trigger, cell, cell), width=3))
                    Color(rgba=font_color)
                    self.canvas.add(Rectangle(size=name.size, pos=(margin + (cell+middleX)*(num - (j-1)*4) + cell/2 - name.size[0]/2, margin + (cell+middleY)*(j-1) + cell/2 - name.size[1]/2 + marginY*trigger), texture=name))
                # Добавление логотипов на билет
                self.canvas.add(Rectangle(source=paths['logo'], size=(imageX, imageY), pos=(ticketX/3-imageX/2, margin + cell + middleY/2 - imageY/2 + marginY*trigger)))
                self.canvas.add(Rectangle(source=paths['logo'], size=(imageX, imageY), pos=((ticketX/3)*2-imageX/2, margin + cell + middleY/2 - imageY/2 + marginY*trigger)))
                trigger = 1

class BL(BoxLayout):
    def __init__(self, **kwargs):
        super(BL, self).__init__(**kwargs)

class MainApp(MDApp):

    def __init__(self, **kwargs):
        self.title = "Lotto"

        self.colors = {
            'Чёрный': (0,0,0,1),
            'Красный': (1,0,0,1),
            'Зелёный': (0,1,0,1),
            'Синий': (50/255,139/255,184/255,1),
            'Жёлтый': (1,251/255,3/255,1),
            'Оранжевый': (1,166/255,0,1),
            'Фиолетовый': (158/255,3/255,1,1),
        }

        # переменные для хранения выбранных цветов, изначально везде чёрный
        self.coin_font = self.colors['Чёрный']
        self.ticket_font = self.colors['Чёрный']
        self.ticket_border = self.colors['Чёрный']

        # переменная для хранения выбранной формы жетоов, изначально круг
        self.shape = 'round'

        super().__init__(**kwargs)

    def build(self):
        with open(paths['kv'], encoding='utf-8', errors='ignore') as f:
            Builder.load_string(f.read())
        self.box = BL()
        Clock.schedule_once(self.fillColors)
        self.can = CanvasWindow(size=[595,842])
        return self.box

    # Изменение формы жетона
    def changeShape(self, shape):
        self.shape = shape
        if shape == 'round':
            self.box.ids.button_round.background_color = (107/255, 235/255, 33/255, 1)
            self.box.ids.button_square.background_color = (179/255, 181/255, 177/255, 1)
        else:
            self.box.ids.button_round.background_color = (179/255, 181/255, 177/255, 1)
            self.box.ids.button_square.background_color = (107/255, 235/255, 33/255, 1)

    # Формирование кнопок с цветовой палитрой
    def fillColors(self, *args):

        self.box.ids.image_logo.source = paths['logo']

        coinFontButtons = self.box.ids.coin_font_color
        ticketFontButtons = self.box.ids.ticket_font_color
        ticketBorderButtons = self.box.ids.ticket_border_color

        for i in self.colors.keys():
            coinFontButtons.add_widget(Button(background_normal=paths['bg'], background_color=self.colors[i], pos_hint={'center_y': 0.5}, on_press= lambda event, color=self.colors[i]: self.applyColor(color, 1)))
            ticketFontButtons.add_widget(Button(background_normal=paths['bg'], background_color=self.colors[i], pos_hint={'center_y': 0.5}, on_press= lambda event, color=self.colors[i]: self.applyColor(color, 2)))
            ticketBorderButtons.add_widget(Button(background_normal=paths['bg'], background_color=self.colors[i], pos_hint={'center_y': 0.5}, on_press= lambda event, color=self.colors[i]: self.applyColor(color, 3)))

    # Применяем цвет принажатии на кнопку пользователем
    def applyColor(self, color, mode):

        if mode == 1:
            self.box.ids.coin_font_label.color = color
            self.coin_font = color
        if mode == 2:
            self.box.ids.ticket_font_label.color = color
            self.ticket_font = color
        if mode == 3:
            self.box.ids.ticket_border_label.color = color
            self.ticket_border = color

    # Подготовка данных для создания жетонов
    def create(self, *args):

        try:
            handle = codecs.open('Lotto.txt', 'r', 'cp1251')
        except:
            handle = codecs.open('Lotto.txt', 'r', 'utf8')
        parts = handle.read()
        handle.close()

        # Берём разделитель из поля ввода и формируем список из файла
        separator = self.box.ids.separator.text
        parts = parts.split(separator)

        # Если количество элементов не кратно восьми - отбрасываем лишнее
        parts = parts[0:len(parts) - len(parts)%8]

        # Количество страниц
        lists = len(parts) / 48
        if lists != int(lists):
            lists = int(lists) + 1

        for i in range(lists):
            if i == lists:
                self.can.createCoins(parts[48*i:], self.shape, self.coin_font)
            else:
                self.can.createCoins(parts[48*i:48*(i+1)], self.shape, self.coin_font)
            self.can.export_to_png('List' + str(i+1) + '.png')
        self.createTickets(parts)

    # Подготовка данных для билетов
    def createTickets(self, parts):

        # Перемешиваем список
        random.shuffle(parts)

        # Количество страниц
        lists = len(parts) / 16
        if lists != int(lists):
            lists = int(lists) + 1
        else:
            lists = int(lists)

        for i in range(lists):
            if i == lists:
                self.can.createTickets(parts[16*i:], self.ticket_font, self.ticket_border)
            else:
                self.can.createTickets(parts[16*i:16*(i+1)], self.ticket_font, self.ticket_border)
            self.can.export_to_png('Ticket' + str(i+1) + '.png')

        # По завершении проигрываем звук
        sound = SoundLoader.load(paths['mp3'])
        if sound:
            sound.play()


if __name__ == "__main__":
    if hasattr(sys, '_MEIPASS'):
        for key in paths.keys():
            paths[key] = sys._MEIPASS + '/' + paths[key]
        resource_add_path(os.path.join(sys._MEIPASS))
    MainApp().run()