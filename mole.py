from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.clock import Clock
from random import randint


class MoleGame(BoxLayout):
    def __init__(self, **kwargs):
        super(MoleGame, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.score = 0
        self.score_label = Label(text="Score: 0", font_size=20)
        self.add_widget(self.score_label)

        self.mole_buttons = []
        for i in range(3):
            row_box = BoxLayout(spacing=10)
            for j in range(3):
                mole_button = ToggleButton(text='Mole {}'.format(i * 3 + j + 1), on_press=self.whack_mole)
                self.mole_buttons.append(mole_button)
                row_box.add_widget(mole_button)
            self.add_widget(row_box)

        self.start_button = Button(text='Start Game', on_press=self.start_game)
        self.add_widget(self.start_button)
        self.game_active = False
        self.correct_mole = None
        self.clock_event = None

    def start_game(self, instance):
        self.score = 0
        self.update_score_label()
        self.game_active = True
        self.start_button.disabled = True
        self.clock_event = Clock.schedule_interval(self.show_random_mole, 2.0)

    def whack_mole(self, instance):
        if instance.state == 'down' and self.game_active and instance == self.correct_mole:
            self.score += 1
            self.update_score_label()

    def show_random_mole(self, dt):
        for mole_button in self.mole_buttons:
            mole_button.state = 'normal'

        random_mole = randint(0, 8)
        self.correct_mole = self.mole_buttons[random_mole]
        self.correct_mole.state = 'down'

    def update_score_label(self):
        self.score_label.text = "Score: {} out of 10".format(self.score)
        if self.score == 10:
            self.end_game()

    def end_game(self):
        self.game_active = False
        self.start_button.disabled = False
        Clock.unschedule(self.show_random_mole)
        self.correct_mole = None


class WhackAMoleApp(App):
    def build(self):
        return MoleGame()


if __name__ == '__main__':
    WhackAMoleApp().run()