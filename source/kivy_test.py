from typing import Text
import kivy
from kivy.uix.widget import Widget

kivy.require("2.0.0")  # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout


class HomePage(GridLayout):
    def __init__(self, **kwargs):
        super(HomePage, self).__init__(**kwargs)

        self.cols = 2

        self.add_widget(Label(text="Hello, what's your name?"))
        self.add_widget(TextInput(multiline=False))


class MyApp(App):
    def build(self):
        return HomePage()


if __name__ == "__main__":
    MyApp().run()