from typing import Type
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.core.text import LabelBase
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
import sqlite3

Window.size = (270.9, 558)
LabelBase.register(name = "Nunito", fn_regular= "Nunito-ExtraBold.ttf")

class Salinguahe(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_file('KV files/main.kv')
        self.screen.ids.dialects1.text = "SELECT"
        self.screen.ids.dialects2.text = "SELECT"
        menu_items = [
            {
                "text": f"{i}",
                "font_name":'nunito',
                "font_size":2,
                "viewclass": "OneLineListItem",
                "on_release": lambda x = f"{i}": self.set_item(x),
            } for i in ["Tagalog","Cebuano","Ilocano", "English"]
        ]
        self.menu = MDDropdownMenu(
            caller=self.screen.ids.dialects1,
            items=menu_items,
            radius=[20, 20, 20, 20],
            border_margin=80,
            ver_growth="down",
            hor_growth="right",
            background_color = "4fe3c1",
            width_mult = 2, 
        )
        menu_items1 = [
            {
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x = f"{i}": self.set_item1(x),
            } for i in ["Tagalog","Cebuano","Ilocano","English"]
        ]
        self.menu1 = MDDropdownMenu(
            caller=self.screen.ids.dialects2,
            items=menu_items1,
            radius=[20, 20, 20, 20],
            border_margin=80,
            ver_growth="down",
            hor_growth="left",
            background_color = "4fe3c1",
            width_mult = 2,
            elevation= 16 
        )

    def error_handling(self, message):
        self.dialog = MDDialog(
        title="Error",
        text= message,
        size_hint= (1,1),
        radius=[20, 20, 20, 20],
        md_bg_color= "#4fe3c1")
        self.dialog.open()

    def settings(self):
        print("setting pressed")

    def translate(self):
        con = sqlite3.connect('dialect.db')
        c = con.cursor()
        From = self.screen.ids.dialects1.text
        To = self.screen.ids.dialects2.text
        Word = self.screen.ids.input.text

        try:
            c.execute(f"SELECT {To} FROM dialect where {From} = '{Word.upper()}'")
            con.commit()
            out = c.fetchall()[0][0]
        except:
            pass

        if From == 'SELECT' or To == 'SELECT':
            self.error_handling("Please Specify Dialect/s")
        elif From == To:
            self.error_handling("Same Dialect Selected")
        elif Word == '':
            self.error_handling("Please Input A Word")
        else:
            try:
                self.screen.ids.output.text = out
                if out == '':
                    self.screen.ids.output.text = "None"
            except:
                self.screen.ids.output.text = "None"

        con.close()
        
    def clear(self):
        self.screen.ids.input.text = ""
        self.screen.ids.output.text = "OUTPUT HERE"
        self.screen.ids.dialects1.text = "SELECT"
        self.screen.ids.dialects2.text = "SELECT"
        
    def switch(self):
        d1 = self.screen.ids.dialects1.text 
        d2 = self.screen.ids.dialects2.text 
        self.screen.ids.dialects1.text = d2
        self.screen.ids.dialects2.text = d1

    def set_item1(self, text__item):
        self.screen.ids.dialects2.text = text__item
        self.menu1.dismiss()

    def set_item(self, text__item):
        self.screen.ids.dialects1.text = text__item
        self.menu.dismiss()

    def build(self):
        return self.screen

if __name__ == '__main__':
    Salinguahe().run()
