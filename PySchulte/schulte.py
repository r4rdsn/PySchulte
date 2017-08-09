LICENSE = '''
Copyright (C) 2017  alfred richardsn

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import sys
import random
import os.path

from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition

from tinydb import TinyDB
from tinydb import Query

from KivyCalendar import calendar_data


db = TinyDB("db.json")

Config.set("kivy", "exit_on_escape", 0)
Config.set("kivy", "pause_on_minimize", 1)
Config.set("graphics", "width", 450)
Config.set("graphics", "minimum_width", 400)
Config.set("graphics", "height", 590)
Config.set("graphics", "minimum_height", 540)
Config.set("input", "mouse", "mouse, multitouch_on_demand")


def create_table(size):
    row = col = size
    numbers = list(range(1, row * col + 1))
    random.shuffle(numbers)

    return [numbers[i:i + row] for i in range(0, len(numbers), col)]


class MenuScreen(Screen):
    pass


class SettingsScreen(Screen):
    pass


class ScoresScreen(Screen):
    pass


class ImageButton(ButtonBehavior, Image):
    pass


class LicensePopup(Popup):
    def __init__(self, *args, **kwargs):
        super(LicensePopup, self).__init__(*args, **kwargs)
        self.text = LICENSE

        layout = BoxLayout(orientation="vertical")
        layout.add_widget(Label(text=self.text, font_size='13sp'))
        layout.add_widget(Button(text="Close", on_release=self.dismiss, size_hint=(1, .1)))
        self.add_widget(layout)


class AboutScreen(Screen):
    tutorial_text = StringProperty()

    def __init__(self, *args, **kwargs):
        super(AboutScreen, self).__init__(*args, **kwargs)

        self.tutorial_text = "(Labels in [ref=change][b]bold[/b][/ref] are clickable)"

    def show_license(self):
        LicensePopup(title="License").open()

    def change_tutorial(self):
        self.tutorial_text = "(You got it!)"
        Clock.schedule_once(self.hide_tutorial, 1)

    def hide_tutorial(self, *args):
        self.tutorial_text = ""


class TableLayout(GridLayout):
    pass


class SchulteApp(App):
    def build(self):
        self.title = 'PySchulte App'
        self.sm = ScreenManager(transition=NoTransition())

        menu_screen = MenuScreen(name="menu")
        self.sm.add_widget(menu_screen)

        self._size = 5
        settings_screen = SettingsScreen(name="settings")
        self.sm.add_widget(settings_screen)

        scores_screen = ScoresScreen(name="scores")
        self.sm.add_widget(scores_screen)

        about_screen = AboutScreen(name="about")
        self.sm.add_widget(about_screen)

        main_screen = Screen(name="table")
        self.table_ui = BoxLayout(orientation="vertical", padding=[20, 20, 20, 20])
        main_screen.add_widget(self.table_ui)
        self.sm.add_widget(main_screen)

        return self.sm

    def slider_value_change(self, instance, value):
        self._size = self._size_slider.value
        self._size_label.text = str(self._size)
        self._size_label.x = self._size_slider.value_pos[0]

    def goto_main_menu(self, *args):
        self.sm.current = "menu"

    def goto_settings_screen(self, *args):
        self.sm.current = "settings"
        self._size_label.x = self._size_slider.value_pos[0]

    def goto_scores_screen(self, *args):
        self.sm.current = "scores"

    def start_training(self, *args):
        day_tries = db.search(Query().date == calendar_data.today_date_list())

        if len(day_tries) > 10:
            content = BoxLayout(orientation="vertical")
            content.add_widget(Label(text="You have exhausted the limit of day's training (10).\nCome train tomorrow!"))
            close_popup_button = Button(text='Close', size_hint=(1, .2))
            content.add_widget(close_popup_button)
            popup = Popup(title='You cannot start training', size_hint=(.6, .6), content=content)
            close_popup_button.bind(on_release=popup.dismiss)
            popup.open()

        else:
            self.sm.current = "table"
            self.table_ui.clear_widgets()
            self.timer = 0
            self.timer_label = Label(text=str(self.timer), size_hint=(1, .05))
            Clock.unschedule(self.start_timer)
            Clock.schedule_interval(self.start_timer, 0)
            self.table_ui.add_widget(self.timer_label)
            schulte_table = TableLayout(cols=self._size, rows=self._size, size_hint=(1, .75))
            button_grid = create_table(self._size)
            for row in button_grid:
                for n in row:
                    schulte_table.add_widget(Label(text=str(n), font_size='40sp', color=(0, 0, 0, 1)))
            self.table_ui.add_widget(schulte_table)
            self.table_ui.add_widget(Button(text="Generate", size_hint=(1, .1), on_release=self.continue_training))
            self.table_ui.add_widget(Button(text="Back to main menu", size_hint=(1, .1), on_release=self.end_training))

    def start_timer(self, dt):
        self.timer += dt
        self.timer_label.text = "%d" % self.timer

    def continue_training(self, *args):
        Clock.unschedule(self.start_timer)
        db.insert({"date": calendar_data.today_date_list(), "score": self.timer})
        self.start_training()

    def end_training(self, *args):
        Clock.unschedule(self.start_timer)
        self.goto_main_menu()


def main():
    try:
        SchulteApp().run()
    except KeyboardInterrupt:
        sys.exit(0)
