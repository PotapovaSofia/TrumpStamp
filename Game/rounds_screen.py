from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
import elections_game
import os
import csv
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.app import runTouchApp
from kivy.uix.widget import Widget

import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

states_csv = os.path.join(SCRIPT_DIR, 'db_states.csv')

class RoundsIcon(Button):
    """Icon class."""

    def __init__(self, **kwargs):
        """Init icon."""
        self.name = None# kwargs['name']
        super(RoundsIcon, self).__init__()

    def late_init(self, **kwargs):
        """Populate icon."""
        self.name = kwargs['name']
        #self.image = kwargs['image']

    def render(self):
        if not self.parent:
            print("Render {}".format(self.name))

    def show(self):
        """Set background image."""
        pass

class StatesScroll(ScrollView):
    
    def __init__(self, **kwargs):
        super(StatesScroll, self).__init__(**kwargs)
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        states_db = []
        with open(states_csv) as states_file:
            reader = csv.DictReader(states_file)
            for row in reader:
                row_ = {k: v for k, v in row.iteritems()}
                states_db.append(row_)

        states = np.unique(np.array([states_db[i]['state'] for i in range(len(states_db))]))
        #states = np.unique(np.array(states_db[[1]]))
        for i in range(len(states)):
            btn = Button(text=str(states[i]), size_hint_y=None, height=40)
            layout.add_widget(btn)
        self.add_widget(layout)

    def late_init(self, **kwargs):
        self.pos_hint = kwargs['pos_hint']
        self.size_hint = kwargs['size_hint']

class DistrictsScroll(ScrollView):
    
    def __init__(self, **kwargs):
        super(DistrictsScroll, self).__init__(**kwargs)
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        for i in range(100):
            btn = Button(text=str(i), size_hint_y=None, height=40)
            layout.add_widget(btn)
        self.add_widget(layout)

    def late_init(self, **kwargs):
        self.pos_hint = kwargs['pos_hint']
        self.size_hint = kwargs['size_hint']

class DescriptionScroll(ScrollView):
    
    def __init__(self, **kwargs):
        super(DescriptionScroll, self).__init__(**kwargs)
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        for i in range(100):
            btn = Button(text=str(i), size_hint_y=None, height=40)
            layout.add_widget(btn)
        self.add_widget(layout)

    def late_init(self, **kwargs):
        self.pos_hint = kwargs['pos_hint']
        self.size_hint = kwargs['size_hint']



class RoundsScreen(Screen):

    POSITIONS_X = {0: 728 / 2048.0}
    POSITIONS_Y = {0: (1536. - 1400) / 1536.0}
    SIZES = {0: (730 / 2048.0, (1536 - 1340) / 1536.0)}

    def __init__(self, sm, **kwargs):
        """Init start screen."""
        super(RoundsScreen, self).__init__(**kwargs)
        self.sm = sm
        self.name = kwargs['name']
        self.menu_screen = kwargs['menu']

        self.back_button = self.ids['Back']

        self.back_button.late_init(**{'name': 'Back', 'image': 'assets/settings/btn_back_active.png'})
        self.back_button.bind(on_press=self.pressed_back)
        self.back_button.pos_hint = {'x': self.POSITIONS_X[0],
                                     'y': self.POSITIONS_Y[0]}
        self.back_button.size_hint = self.SIZES[0]
        self.back_button.render()
        self.back_button.show()

        self.game = None
        states_db = []
        with open(states_csv) as states_file:
            reader = csv.DictReader(states_file)
            for row in reader:
                row_ = {k: v for k, v in row.iteritems()}
                states_db.append(row_)

        self.states_scroll = self.ids['StatesScroll']
        self.dist_scroll = self.ids['DistrictsScroll']
        self.descr_scroll = self.ids['DescriptionScroll']

        #self.states_scroll.late_init(size=(Window.width / 4, Window.height/ 2), pos=(Window.width / 6, Window.height/ 3))
        self.states_scroll.late_init(size_hint=(((2048.0 - 400) / 3) / 2048.0, 1000 / 2048.0), 
                                    pos_hint={'x': 128 / 2048.0, 'y': 300.0 / 1536.0})
        self.dist_scroll.late_init(size_hint=(((2048.0 - 400) / 3) / 2048.0, 1000 / 2048.0), 
                                    pos_hint={'x': (128 + ((2048.0 - 400) / 3) + 70) / 2048.0, 'y': 300.0 / 1536.0})
        self.descr_scroll.late_init(size_hint=(((2048.0 - 400) / 3) / 2048.0, 1000 / 2048.0), 
                                    pos_hint={'x': (128 + 2 * ((2048.0 - 400) / 3) + 140) / 2048.0, 'y': 300.0 / 1536.0})

        self.set_new_game()

    def pressed_back(self, *args):
        #self.sm.add_widget(self.menu_screen)
        self.sm.current = 'startscreen'
        #print "pressed back"
        #self.sm.switch_to(self.menu_screen)

    def set_new_game(self):
        self.game = elections_game.ElectionsGame(self.sm, name="electionsgame")


    def set_bot(self, bot_name):
        self.game.set_bot(bot_name)
        #self.sm.switch_to(self.game)

