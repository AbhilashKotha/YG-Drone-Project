# Copyright 2023 YG-Drone-Project
"""
Module description: This module contains Python code for the UI.
"""
# Import modules
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.config import Config
import requests

Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')

class DroneApp(App):
    """
    The main app class with all the buttons and layout
    defined.
    """
        
    # Initialize values for the controls and the label
    response_label = None
    throttle_step_size_label = None
    rudder_step_size_label = None
    elevator_step_size_label = None
    aileron_step_size_label = None
    altitude_label = None
    pitch_label = None
    roll_label = None
    yaw_label = None
    throttle_percentage = 0
    throttle_step_size = 1
    rudder_percentage = 0
    rudder_step_size = 1
    elevator_percentage = 0
    elevator_step_size = 1
    aileron_percentage =0
    aileron_step_size = 1
    altitude = 0
    pitch = 0
    roll = 0
    yaw = 0

    def build(self):
        Config.set('graphics', 'orientation', 'landscape')

        layout = BoxLayout(orientation='vertical')

        top_layout = BoxLayout(orientation='horizontal', padding=10)

        left_anchor = AnchorLayout(anchor_x='left', anchor_y='top', size_hint=(0.5, 1))

        # Define a BoxLayout to stack the button and label vertically
        stack_layout = BoxLayout(orientation='vertical', size_hint=(1, None))

        arm_button = Button(text='Arm Drone', size_hint=(1, 0.1))
        arm_button.bind(on_press=self.arm_drone)
        stack_layout.add_widget(arm_button)

        # Add a label to display the armed status
        self.drone_armed_label = Label(text='Drone Status: Unarmed', size_hint=(1, 0.1))
        stack_layout.add_widget(self.drone_armed_label)
        
        left_anchor.add_widget(stack_layout)
        top_layout.add_widget(left_anchor)

        # Right anchor box
        right_anchor = AnchorLayout(anchor_x='right', anchor_y='top', size_hint=(0.8, 1))

        # Layout for step size controls
        step_size_controls = BoxLayout(orientation='vertical', size_hint=(0.8, 1), spacing=10)

        # Throttle controls
        inc_throttle_step_button = Button(text='Increase Throttle step size', size_hint=(1, 0.5))
        inc_throttle_step_button.bind(on_press=self.increase_throttle_step_size)
        step_size_controls.add_widget(inc_throttle_step_button)

        dec_throttle_step_button = Button(text='Decrease Throttle step size', size_hint=(1, 0.5))
        dec_throttle_step_button.bind(on_press=self.decrease_throttle_step_size)
        step_size_controls.add_widget(dec_throttle_step_button)

        self.throttle_step_size_label = Label(
            text=f'Throttle step size: {self.throttle_step_size}', size_hint=(1, 0.5))
        step_size_controls.add_widget(self.throttle_step_size_label)

        # Rudder controls
        inc_rudder_step_button = Button(text='Increase Rudder step size', size_hint=(1, 0.5))
        inc_rudder_step_button.bind(on_press=self.increase_rudder_step_size)
        step_size_controls.add_widget(inc_rudder_step_button)

        dec_rudder_step_button = Button(text='Decrease Rudder step size', size_hint=(1, 0.5))
        dec_rudder_step_button.bind(on_press=self.decrease_rudder_step_size)
        step_size_controls.add_widget(dec_rudder_step_button)

        self.rudder_step_size_label = Label(
            text=f'Rudder step size: {self.rudder_step_size}', size_hint=(1, 0.5))
        step_size_controls.add_widget(self.rudder_step_size_label)

        # Elevator controls
        inc_elevator_step_button = Button(text='Increase Elevator step size', size_hint=(1, 0.5))
        inc_elevator_step_button.bind(on_press=self.increase_elevator_step_size)
        step_size_controls.add_widget(inc_elevator_step_button)

        dec_elevator_step_button = Button(text='Decrease Elevator step size', size_hint=(1, 0.5))
        dec_elevator_step_button.bind(on_press=self.decrease_elevator_step_size)
        step_size_controls.add_widget(dec_elevator_step_button)

        self.elevator_step_size_label = Label(
            text=f'Elevator step size: {self.elevator_step_size}', size_hint=(1, 0.5))
        step_size_controls.add_widget(self.elevator_step_size_label)

        # Aileron controls
        inc_aileron_step_button = Button(text='Increase Aileron step size', size_hint=(1, 0.5))
        inc_aileron_step_button.bind(on_press=self.increase_aileron_step_size)
        step_size_controls.add_widget(inc_aileron_step_button)

        dec_aileron_step_button = Button(text='Decrease Aileron step size', size_hint=(1, 0.5))
        dec_aileron_step_button.bind(on_press=self.decrease_aileron_step_size)
        step_size_controls.add_widget(dec_aileron_step_button)

        self.aileron_step_size_label = Label(text=f'Aileron step size: {self.aileron_step_size}', size_hint=(1, 0.5))
        step_size_controls.add_widget(self.aileron_step_size_label)

        right_anchor.add_widget(step_size_controls)
        top_layout.add_widget(right_anchor)

        self.response_label = Label(text='', halign='center', valign='middle', size_hint=(1, 0.1))
        with self.response_label.canvas.before:
            Color(0.5, 0.5, 0.5, 1)  # Set the RGBA values for the background color
            self.rect = Rectangle(size=self.response_label.size, pos=self.response_label.pos)
        self.response_label.bind(size=self.update_rect, pos=self.update_rect)
        layout.add_widget(self.response_label)

        layout.add_widget(top_layout)

        main_layout = BoxLayout(spacing=40)

        # Layout of the left controls to look like a + button
        left_controls = GridLayout(cols=3, rows=3, size_hint=(0.5, 0.8), spacing=5)
        left_controls.add_widget(Button(text='', background_color=(0, 0, 0, 0)))
        left_controls.add_widget(Button(text='Increase Throttle', on_press=self.increase_throttle))
        left_controls.add_widget(Button(text='', background_color=(0, 0, 0, 0)))
        left_controls.add_widget(Button(text='Left Rudder', on_press=self.left_rudder))
        left_controls.add_widget(Button(text='', background_color=(0, 0, 0, 0)))
        left_controls.add_widget(Button(text='Right Rudder', on_press=self.right_rudder))
        left_controls.add_widget(Button(text='', background_color=(0, 0, 0, 0)))
        left_controls.add_widget(Button(text='Decrease Throttle', on_press=self.decrease_throttle))
        left_controls.add_widget(Button(text='', background_color=(0, 0, 0, 0)))

        # Layout of the right controls to look like a + button
        right_controls = GridLayout(cols=3, rows=3, size_hint=(0.5, 0.8), spacing=5)
        right_controls.add_widget(Button(text='', background_color=(0, 0, 0, 0)))
        right_controls.add_widget(Button(text='Increase Elevator', on_press=self.increase_elevator))
        right_controls.add_widget(Button(text='', background_color=(0, 0, 0, 0)))
        right_controls.add_widget(Button(text='Left Aileron', on_press=self.left_aileron))
        right_controls.add_widget(Button(text='', background_color=(0, 0, 0, 0)))
        right_controls.add_widget(Button(text='Right Aileron', on_press=self.right_aileron))
        right_controls.add_widget(Button(text='', background_color=(0, 0, 0, 0)))
        right_controls.add_widget(Button(text='Decrease Elevator', on_press=self.decrease_elevator))
        right_controls.add_widget(Button(text='', background_color=(0, 0, 0, 0)))

        main_layout.add_widget(left_controls)
        main_layout.add_widget(right_controls)
        layout.add_widget(main_layout)

        info_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))

        self.altitude_label = Label(text=f'Altitude: {self.altitude}')
        info_layout.add_widget(self.altitude_label)

        self.pitch_label = Label(text=f'Pitch: {self.pitch}')
        info_layout.add_widget(self.pitch_label)

        self.roll_label = Label(text=f'Roll: {self.roll}')
        info_layout.add_widget(self.roll_label)

        self.yaw_label = Label(text=f'Yaw: {self.yaw}')
        info_layout.add_widget(self.yaw_label)

        main_layout.add_widget(info_layout)

        return layout
    
    def update_altitude_label(self, instance=None):
        self.altitude_label.text = f'Altitude: {self.altitude}'

    def update_pitch_label(self, instance=None):
        self.pitch_label.text = f'Pitch: {self.pitch}'

    def update_roll_label(self, instance=None):
        self.roll_label.text = f'Roll: {self.roll}'

    def update_yaw_label(self, instance=None):
        self.yaw_label.text = f'Yaw: {self.yaw}'
    
    def update_rect(self, instance, value=None):
        """
        This method contributes to the UI layout
        """
        self.rect.size = instance.size
        self.rect.pos = instance.pos
    
    def send_request(self, route, value=None):
        """
        This method handles all HTTP request to the web server using POST method.
        The mobile uses alias address of the localhost address
        to communicate with the server if you are testing via an 
        emulator 
        """

        url = f'http://localhost:8000/{route}' # alias address of localhost

        data = None
        if value is not None:
            data = {route: value}

        try:
            response = requests.post(url, json=data)
            response_json = response.json()
            if response.status_code == 200:
                message = response_json.get("message", "Error: Invalid server response")
                self.response_label.text = message
                self.altitude = response_json.get("altitude", self.altitude)
                self.pitch = response_json.get("pitch", self.pitch)
                self.roll = response_json.get("roll", self.roll)
                self.yaw = response_json.get("yaw", self.yaw)
                self.update_altitude_label()
                self.update_pitch_label()
                self.update_roll_label()
                self.update_yaw_label()
            else:
                message = response_json.get("message", "Error: Invalid server response")
                self.response_label.text = message
                print(f'Failed request to {route}. Response code:', response.status_code)
        except requests.exceptions.RequestException as exception:
            print('Error connecting to server:', exception)
        except ValueError:
            print('Error decoding server response')

    def arm_drone(self, instance):
        """
        Arm the drone request
        """

        self.send_request('arm_drone')
    
        # Update the armed status label text
        self.drone_armed_label.text = 'Drone Status: Armed'

    def update_throttle_step_size_label(self):
        """
        Label for throttle step size
        """
        self.throttle_step_size_label.text = f'Throttle Step Size: {self.throttle_step_size}%'

    def update_rudder_step_size_label(self):
        """
        Label for rudder step size
        """
        self.rudder_step_size_label.text = f'Rudder Step Size: {self.rudder_step_size}%'

    def update_elevator_step_size_label(self):
        """
        Label for elevator step size
        """
        self.elevator_step_size_label.text = f'Elevator Step Size: {self.elevator_step_size}%'

    def update_aileron_step_size_label(self):
        """
        Label for aileron step size
        """
        self.aileron_step_size_label.text = f'Aileron Step Size: {self.aileron_step_size}%'

    def increase_throttle_step_size(self, instance):
        """
        Increase step size of throttle
        """

        if self.throttle_step_size < 100:
            self.throttle_step_size += 1
            self.update_throttle_step_size_label()

    def decrease_throttle_step_size(self, instance):
        """
        Decrease step size of throttle
        """

        if self.throttle_step_size > 1:
            self.throttle_step_size -= 1
            self.update_throttle_step_size_label()

    def increase_rudder_step_size(self, instance):
        """
        Increase step size of rudder
        """

        if self.rudder_step_size < 100:
            self.rudder_step_size += 1
            self.update_rudder_step_size_label()

    def decrease_rudder_step_size(self, instance):
        """
        Decrease step size of rudder
        """

        if self.rudder_step_size > 1:
            self.rudder_step_size -= 1
            self.update_rudder_step_size_label()

    def increase_elevator_step_size(self, instance):
        """
        Increase step size of elevator
        """

        if self.elevator_step_size < 100:
            self.elevator_step_size += 1
            self.update_elevator_step_size_label()

    def decrease_elevator_step_size(self, instance):
        """
        Decrease step size of elevator
        """

        if self.elevator_step_size > 1:
            self.elevator_step_size -= 1
            self.update_elevator_step_size_label()

    def increase_aileron_step_size(self, instance):
        """
        Increase step size of aileron
        """

        if self.aileron_step_size < 100:
            self.aileron_step_size += 1
            self.update_aileron_step_size_label()

    def decrease_aileron_step_size(self, instance):
        """
        Decrease step size of aileron
        """

        if self.aileron_step_size > 1:
            self.aileron_step_size -= 1
            self.update_aileron_step_size_label()

    def increase_throttle(self, instance):
        """
        This method increases the throttle
        """

        self.throttle_percentage += self.throttle_step_size
        self.throttle_percentage = min(self.throttle_percentage, 100)
        self.send_request('set_throttle', self.throttle_percentage)

    def decrease_throttle(self, instance):
        """
        This method decreases the throttle
        """

        self.throttle_percentage -= self.throttle_step_size
        self.throttle_percentage = max(self.throttle_percentage, 0)
        self.send_request('set_throttle', self.throttle_percentage)

    def left_rudder(self, instance):
        """
        This method decreases the rudder
        """

        self.rudder_percentage -= self.rudder_step_size
        self.rudder_percentage = max(self.rudder_percentage, 0)
        self.send_request('set_rudder', self.rudder_percentage)

    def right_rudder(self, instance):
        """
        This method increases the rudder
        """

        self.rudder_percentage += self.rudder_step_size
        self.rudder_percentage = min(self.rudder_percentage, 100)
        self.send_request('set_rudder', self.rudder_percentage)

    def increase_elevator(self, instance):
        """
        This method increases the elevator
        """

        self.elevator_percentage += self.elevator_step_size
        self.elevator_percentage = min(self.elevator_percentage, 100)
        self.send_request('set_elevator', self.elevator_percentage)

    def decrease_elevator(self, instance):
        """
        This method decreases the elevator
        """

        self.elevator_percentage -= self.elevator_step_size
        self.elevator_percentage = max(self.elevator_percentage, 0)
        self.send_request('set_elevator', self.elevator_percentage)


    def left_aileron(self, instance):
        """
        This method decreases the aileron
        """

        self.aileron_percentage -= self.aileron_step_size
        self.aileron_percentage = max(self.aileron_percentage, 0)
        self.send_request('set_aileron', self.aileron_percentage)

    def right_aileron(self, instance):
        """
        This method increases the aileron
        """

        self.aileron_percentage += self.aileron_step_size
        self.aileron_percentage = min(self.aileron_percentage, 100)
        self.send_request('set_aileron', self.aileron_percentage)


# The Driver code
if __name__ == '__main__':
    DroneApp().run()