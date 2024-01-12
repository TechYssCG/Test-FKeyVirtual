from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.config import Config
from jnius import autoclass, cast

from plyer import window_state

Config.set('graphics', 'width', '300')
Config.set('graphics', 'height', '150')

class FKeyVirtualApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        # Bouton pour mettre l'application en arrière-plan
        overlap_button = Button(text='Overlap', on_press=self.show_overlap_popup)
        self.layout.add_widget(overlap_button)

        # Boutons pour simuler les touches F
        for i in range(1, 13):
            button_text = f'F{i}'
            button = Button(text=button_text, on_press=self.on_button_press)
            self.layout.add_widget(button)

        # Bouton pour activer le clavier personnalisé
        custom_keyboard_button = Button(text='Activer Clavier', on_press=self.enable_custom_keyboard)
        self.layout.add_widget(custom_keyboard_button)

        self.check_orientation()
        Window.bind(on_resize=self.check_orientation)

        return self.layout

    def show_overlap_popup(self, instance):
        content = BoxLayout(orientation='vertical')

        # Logo simple avec un Label
        logo = Label(text='FKey', font_size='48sp', size_hint=(None, None), size=(48, 48))
        content.add_widget(logo)

        # Bouton pour fermer l'application
        exit_button = Button(text='Exit', on_press=self.close_application)
        content.add_widget(exit_button)

        # Popup pour permettre le déplacement du logo
        popup = Popup(content=content, size_hint=(None, None), size=(100, 100))
        popup.open()

    def close_application(self, instance):
        App.get_running_app().stop()

    def on_pause(self):
        # Mettre l'application en arrière-plan
        window_state('iconified')
        return True

    def on_resume(self):
        # Revenir à l'avant-plan
        window_state('normal')

    def on_button_press(self, instance):
        key_to_press = instance.text
        self.simulate_key_press(key_to_press)

    def simulate_key_press(self, key):
        mActivity = autoclass('org.kivy.android.PythonActivity').mActivity
        KeyEvent = autoclass('android.view.KeyEvent')
        action_down = KeyEvent.ACTION_DOWN
        action_up = KeyEvent.ACTION_UP

        code = ord(key[0])
        event_down = KeyEvent(action_down, code)
        event_up = KeyEvent(action_up, code)

        mActivity.dispatchKeyEvent(event_down)
        mActivity.dispatchKeyEvent(event_up)

    def enable_custom_keyboard(self, *args):
        # Ajoutez ici le code pour activer votre clavier personnalisé (non fourni)

    def check_orientation(self, instance=None, width=None, height=None):
        if width is not None and height is not None:
            if width > height:
                self.layout.orientation = 'horizontal'
            else:
                self.layout.orientation = 'vertical'

if __name__ == '__main__':
    FKeyVirtualApp().run() 
