from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.clock import Clock
from random import randint

# Seznam jmen krtků
krtci = ["Krtek Václav", "Krtek Filip", "Krtek Franta",
         "Krtek Matěj", "Krtek Marek", "Krtek Tomáš",
         "Krtek Nicolas", "Krtek Lukáš", "Krtek Pavel"]

# Třída reprezentující hru s krtky
class MoleGame(BoxLayout):
    def __init__(self, **kwargs):
        super(MoleGame, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.score = 0
        self.score_label = Label(text="Skóre: 0", font_size=20)
        self.add_widget(self.score_label)

        self.mole_buttons = []

        # Vytvoření tlačítek pro krtky v mřížce 3x3
        for i in range(3):
            row_box = BoxLayout(spacing=10)
            for j in range(3):
                mole_button = ToggleButton(text='{}'.format(krtci[i * 3 + j]), on_press=self.whack_mole, background_color=(0.824, 0.706, 0.549, 1))
                self.mole_buttons.append(mole_button)
                row_box.add_widget(mole_button)
            self.add_widget(row_box)

        # Tlačítko pro začátek hry
        self.start_button = Button(text='Začít hru', on_press=self.start_game,
                                   background_color=(0.647, 0.322, 0.176, 1))
        self.add_widget(self.start_button)
        self.game_active = False
        self.correct_mole = None
        self.clock_event = None

    # Metoda pro spuštění hry
    def start_game(self, instance):
        self.score = 0
        self.update_score_label()
        self.game_active = True
        self.start_button.disabled = True
        self.clock_event = Clock.schedule_interval(self.show_random_mole, 2.0)

    # Metoda pro úder krtka
    def whack_mole(self, instance):
        if self.game_active:
            if instance == self.correct_mole:
                self.score += 1
            else:
                self.score -= 1 if self.score > 0 else 0
            self.update_score_label()

    # Metoda pro zobrazení náhodného krtka
    def show_random_mole(self, dt):
        for mole_button in self.mole_buttons:
            mole_button.state = 'normal'

        random_mole = randint(0, 8)
        self.correct_mole = self.mole_buttons[random_mole]
        self.correct_mole.state = 'down'

    # Metoda pro aktualizaci zobrazení skóre
    def update_score_label(self):
        self.score_label.text = "Skóre: {} z 10".format(self.score)
        if self.score == 10:
            self.end_game()

    # Metoda pro ukončení hry
    def end_game(self):
        self.game_active = False
        self.start_button.disabled = False
        Clock.unschedule(self.show_random_mole)
        self.correct_mole = None

# Třída reprezentující Kivy aplikaci
class WhackAMoleApp(App):
    def build(self):
        return MoleGame()

# Spuštění aplikace
if __name__ == '__main__':
    WhackAMoleApp().run()
