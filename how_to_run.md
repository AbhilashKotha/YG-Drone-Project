# Drone RC Mobile App
This project is a mobile Drone Remote Controller that sends commands to a fixed wing plane using a web server. The mobile app was developed in Python, and all the codes are in the `main.py` file in the `kivi_app/` directory. 

## Run the App on Desktop
After cloning the repository, `cd` into the `kivi_app/` directory and create a `venv` in the directory. Install the `requirements.txt` using `pip`. This `requirements.txt` contains all the dependencies necessary to run the app directly using `Python`. However, the goal is to run the mobile version of the app, thus the next step discusses how to build the mobile android app. If you intend to test the app directly on the desktop, you should leave the address of the web server as it is in the `main.py` file as shown below to use the localhost address.  
```
url = f'http://localhost:8000/{route}' # address of localhost
```

## Run the Mobile App  
### Important Information  
Before attempting to build the mobile app, ensure to change the web server's address in *__line 167__* in the ```main.py``` file to use the alias address of the localhost as shown below:
```
url = f'http://10.0.2.2:8000/{route}' # alias address of localhost
```

## Build for Android
To build the Kivy app for Android and test it on an Android Studio emulator, you will need to use the `Buildozer` tool. Buildozer is a tool for packaging Kivy apps for mobile devices. Buildozer tool is part of the packages in the `requirements.txt` file that was installed earlier so you do not have to install it again. The `kivi_app` directory has already been initialized and the configuration `spec` to build the android app has been created which is the `buildozer.spec` file.  

To build the app for Android, run the following command:  
 
```
buildozer android debug deploy run
```
This will build an APK file, deploy it to a connected Android device or emulator, and run it.  

To run the app on the Android Studio emulator, first start the emulator from Android Studio. Then, after the Buildozer command completes, you can manually install the generated APK on the emulator using the ```adb``` command-line tool:  
```
adb install bin/yourpackagename-debug.apk
```
Replace ```<yourpackagename>``` with the package name generated in the ```bin/``` directory.  

Once the APK is installed, you can find your app in the app drawer of the emulator and run it like any other Android app.  

The app is already configured to be able to connect to the web server through the ```alias``` address of the ```localhost``` address, thus no any other configuration is needed to be done on the emulator side. We tested the mobile app using ***Nexus 5 API 28 emulator*** on Android Studio, hence we recommend testing the app using thesame.

## Build for iOS using Kivy-ios and Run on iOS Simulator

Before you begin, ensure that you have a macOS machine with the latest version of Xcode installed. Also, make sure you have Homebrew installed.

1. Install autoconf, automake and libtool:
    ```bash
    brew install autoconf automake libtool pkg-config
    ```
2. Install Kivy-ios:
    ```bash
    pip install kivy-ios
    ```
3. Create a new directory where you want to place the Kivy-ios build and navigate into it:
    ```bash
    mkdir kivy-ios-build
    cd kivy-ios-build
    ```
4. Use Kivy-ios to create a new Xcode project:
    ```bash
    toolchain create <YourProjectName> <path/to/your/main.py>
    ```
    Replace `<YourProjectName>` with the name you want to give your project and `<path/to/your/main.py>` with the path to your main.py file.

5. Build your Xcode project:
    ```bash
    cd <YourProjectName>
    open <YourProjectName>.xcodeproj
    ```
    This will open your project in Xcode.

6. Ensure that the web server's address in `line 167` in the `main.py` file is set to use the alias address of the localhost as shown below, as iOS simulator doesn't support `10.0.2.2` (alias for Android emulator):
    ```python
    url = f'http://localhost:8000/{route}' # alias address of localhost
    ```

7. In Xcode, select an iOS simulator from the target dropdown and click the 'Run' button. This will launch the iOS simulator and run your app.

Please note that Kivy-ios doesn't support all Kivy modules. If your app uses a module that isn't supported, you'll need to build a recipe for it. A recipe is a set of instructions that tells Kivy-ios how to build a module. This can be a complex process and is beyond the scope of this document.

# Web Server
The web server was implemented using **Flask**. To setup and test the web server use the following steps below after cloning the repo:  
1. Create a Python virtual environment  
```
python3 -m venv venv
```
2. Activate the environment  
```
source venv/bin/activate
```
3. Install the dependecies in the requirements file  
```
pip install -r requirements.txt
```
4. Start the Flask server by running the ```main.py``` file. Note that the Flask server is configured to use ```port 8000```, thus the server would run on ```http://localhost:8000```. You can change it if necessary. To run the web server, use the command below:
```
python3 server.py
```

# How to run the application with the new UI

## Option 1
- Open UIRemote.sln from new_user_interface folder in VS
- Run the application in release or debug mode.
- Select the emulator device
## Option 2
- Open any Android emulator
- Drag the apk file "drone_remote.drone_remote.apk" on to the emulator
- Install the application and use the app

Below are some of the screenshots for your reference.

# How the App Works

<p align="center">
  <img src="https://github.com/SLUSE-Spring2022/sprint4-team1-sprint4/assets/89559173/7d17a4ff-8d48-48b5-9408-ba2f2ede35ba.png" alt="RC_Drone_App">
</p>

1. When the user click the "Arm Drone" button, the application sends a HTTP request to the web server.
2. The server processes the request and sends it to the drone and returns a success or failure response to the app.
3. There is also a ```text label``` at the top of the mobile app that displays messages to the user from the web server.
4. Ensure to click the ```Arm Drone``` button on the mobile app to arm the drone before trying to use any of the ```controls``` button. If a user tries to use the controls without arming the drone, the app informs the user to arm the drone first before attempting to fly the drone.
5. At the top right corner of the app screen, there are buttons to set the ```step-sizes``` for percentage increase/decrease of the individual control surfaces.
6. All the controls such as ```throttle```, ```elevator```, ```rudder```, and ```aileron``` have been implemented.

# Connection To The Drone
The drone used in this project is the ArduPilot simulated drone. The simulator has to be running first and the drone shown on the map, before attempting to arm the drone from the mobile application. Remember to ensure that the web server is also running as it serves as the intermediary between the mobile app and the drone.
 

# The Drone Control Server API

The server provides a simple API for controlling the SITL drone using a web service. The following routes are supported for controlling the drone.

## Routes

### POST /arm_drone

Arms the drone.

#### Response

- status: "success" or "error"
- message: A string describing the result of the operation

### POST /set_aileron

Sets the aileron control surface.

#### Parameters

- aileron: Integer (0-100) representing the percentage of aileron control

#### Response

- status: "success" or "error"
- message: A string describing the result of the operation

### POST /set_elevator

Sets the elevator control surface.

#### Parameters

- elevator: Integer (0-100) representing the percentage of elevator control

#### Response

- status: "success" or "error"
- message: A string describing the result of the operation

### POST /set_throttle

Sets the throttle control.

#### Parameters

- throttle: Integer (0-100) representing the percentage of throttle control

#### Response

- status: "success" or "error"
- message: A string describing the result of the operation

### POST /set_rudder

Sets the rudder control surface.

#### Parameters

- rudder: Integer (0-100) representing the percentage of rudder control

#### Response

- status: "success" or "error"
- message: A string describing the result of the operation

## Parameter Validations

All control surface parameters (aileron, elevator, throttle, and rudder) must be within the range of 0 to 100, inclusive.

## Error Handling

If a control surface parameter is out of range, the server will return an error with a status code of 400 and an error message.

If the drone is not armed, the server will return an error with a status code of 400 and an error message.

For other errors, the server will return an error with a status code of 500 and an error message.

# User Interface Design Analysis of Our Drone RC Mobile App

## 1. Consistency
For our app, the mobile interface basically follows this consistency rule, and the layout is clear and is composed of consistent element. All of the drone control and step size adjustment buttons have the same appearance and functionality. The button press events are handled using the same method structure, making the program predictable for the user.

## 2. Enable frequent users to use shortcuts
For our app, the interface is quite straightforward and simple to use. Basically, this mobile app is not needed to add shortcuts. Each button is focused on single function and is located at index interface. There are no specific keyboard shortcuts or gesture-based shortcuts implemented.

## 3. Feedback
Feedback is provided through the ```response_label``` label. Every time a request is sent to the server (e.g., to ```arm``` the drone, change the ```throttle```, ```rudder```, ```elevator```, or ```aileron```), the response from the server is displayed in the ```response_label``` text field.

## 4. Design dialogs to yield closure
Aside the ```Arming``` the drone first before attempting to fly, our UI does not appear to have any dialogs or sequences of action that need to yield closure. However, we could argue that the 'Arm Drone' button could be seen as initiating a sequence, and the feedback given through the ```response_label``` to ```Arm``` the drone first and the response received when the drone is armed, can be seen to provide closure.

## 5. Offer simple error handling
For error messages, our app provides concise messages to users. The feedback label displays messages returned from the server, which could include error messages like trying to fly the drone without arming it. However, there are no specific UI elements for handling or displaying errors, such as dialogs or pop-ups. Also, there's no much mechanism at the frontend for handling incorrect user input or invalid operations (like trying to decrease the step size below 1 or above 100 evn though this is handled implicitly to not allow the app to crash.

## 6. Permit easy reversal of actions
This principle is supported. For instance, if a user increases the throttle or any of the step-size controls and decides that was a mistake, they can easily decrease it again. 

## 7. Support internal locus of control
The interface supports an internal locus of control by allowing the user to directly manipulate the drone's throttle, rudder, elevator, and ailerons, and to adjust the step sizes for these controls. Users should feel in control of the system.

## 8. Reduce short-term memory load
Our UI is relatively simple with clearly labeled controls, which helps to reduce the short-term memory load. However, a possible improvement could be to display the current settings (like the current throttle, rudder, elevator, and aileron percentages) so the user does not have to remember them.