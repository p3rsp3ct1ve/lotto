import io
import codecs
import kivy
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRaisedButton
from kivy.graphics import Instruction, InstructionGroup, Color, Line, Rectangle
from kivy.uix.label import Label, CoreLabel
from kivy.uix.screenmanager import Screen
from kivy.core.text import LabelBase
from kivymd.toast.kivytoast.kivytoast import toast
from kivy.core.window import Window
import random
Window.size = (300, 100)

class CanvasWindow(Screen):
    def __init__(self, **kwargs):
        super(CanvasWindow, self).__init__(**kwargs)

    def render(self, parts, *args):

        LabelBase.register(name='CG', fn_regular='CenturyGothic.ttf')

        with self.canvas:
            Color(0,0,0,1)

            # Базовые размеры
            w = 595
            h = 842

            # Начало
            x = 94
            y = 94

            # Отступ
            margin = 70

            # Фон
            Color(1,1,1,1) #white
            self.canvas.add(Rectangle(size=[w,h], pos=[0, 0]))

            # Лото

            for i in range(len(parts)):
                j = 1
                j += int(i/6)
                name = CoreLabel(font_name='CG', text=parts[i], font_size=45)
                name.refresh()
                name = name.texture
                Color(1,0,0,1)
                self.canvas.add(Line(circle=(x*(i - (j - 1)*6) + margin, y*j, 47), width=1))
                Color(1,166/255,0,1)
                self.canvas.add(Rectangle(size=name.size, pos=[(x*(i - (j - 1)*6)+margin)-(name.size[0]/2), y*j-name.size[1]/2], texture=name))

    def createTickets(self, parts):

        LabelBase.register(name='CG', fn_regular='CenturyGothic.ttf')

        with self.canvas:
            Color(0,0,0,1)

            # Базовые размеры
            w = 595
            h = 842

            # Начало
            x = 94
            y = 94

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

            print(tickets)

            trigger = 0

            for i in range(len(tickets)):
                Color(0,0,0,1)
                self.canvas.add(Line(rectangle=(0, marginY*trigger, w, ticketY), width=1))
                for num in range(len(tickets[i])):
                    j = 1
                    j += int(num/4)
                    name = CoreLabel(font_name='CG', text=str(tickets[i][num]), font_size=45)
                    name.refresh()
                    name = name.texture
                    Color(50/255,139/255,184/255,1)
                    self.canvas.add(Line(rectangle=(margin + (cell+middleX)*(num - (j-1)*4), margin + (cell+middleY)*(j-1) + marginY*trigger, cell, cell), width=3))
                    Color(0,0,0,1)
                    self.canvas.add(Rectangle(size=name.size, pos=(margin + (cell+middleX)*(num - (j-1)*4) + cell/2 - name.size[0]/2, margin + (cell+middleY)*(j-1) + cell/2 - name.size[1]/2 + marginY*trigger), texture=name))
                trigger = 1



class MainApp(MDApp):

    def __init__(self, **kwargs):
        self.title = "Lotto"
        super().__init__(**kwargs)

    def build(self):
        box = BoxLayout(orientation='vertical', size=(300,100))
        box.bind(minimum_height=box.setter('height'))
        self.can = CanvasWindow(size=[595,842])
        button = MDRaisedButton(text='Создать', pos_hint={'center_x': 0.5, 'center_y': 0.5}, on_press=self.hnh)
        box.add_widget(Label())
        box.add_widget(button)
        box.add_widget(Label())
        return box

    def hnh(self, *args):
        handle = codecs.open('Lotto.txt', 'r', 'cp1251')
        parts = handle.read()
        handle.close()
        parts = parts.split(', ')
        lists = len(parts) / 48
        if lists != int(lists):
            lists = int(lists) + 1
        for i in range(lists):
            if i == lists:
                self.can.render(parts[48*i:])
            else:
                self.can.render(parts[48*i:48*(i+1)])
            self.can.export_to_png('List' + str(i+1) + '.png')
        self.createTickets(parts)
        toast('Лото создано')

    def createTickets(self, parts):
        random.shuffle(parts)
        lists = len(parts) / 16
        if lists != int(lists):
            lists = int(lists) + 1
        else:
            lists = int(lists)
        for i in range(lists):
            if i == lists:
                self.can.createTickets(parts[16*i:])
            else:
                self.can.createTickets(parts[16*i:16*(i+1)])
            self.can.export_to_png('Ticket' + str(i+1) + '.png')

if __name__ == "__main__":
    MainApp().run()