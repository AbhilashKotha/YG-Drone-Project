from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

class InstructorScreen(Screen):
    def __init__(self, **kwargs):
        super(InstructorScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        heading_label = Label(text='Instructor View')
        layout.add_widget(heading_label)

        display_button = Button(text='Display Logs', size_hint=(0.5, 0.1))
        display_button.bind(on_press=self.display_logs)
        layout.add_widget(display_button)

        scroll_view = ScrollView(size_hint=(1, 0.9))
        self.logs_label = Label(text='', size_hint=(None, None))
        self.logs_label.bind(size=self.logs_label.setter('text_size'))
        scroll_view.add_widget(self.logs_label)
        layout.add_widget(scroll_view)

        self.add_widget(layout)

    def display_logs(self, *args):
        log_file_path = 'backend/flight_path.txt'  # Replace with the actual file path

        try:
            with open(log_file_path, 'r') as file:
                logs = file.read()
                self.logs_label.text = logs
        except FileNotFoundError:
            self.logs_label.text = 'Logs file not found.'
