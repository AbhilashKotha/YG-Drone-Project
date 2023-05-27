# YG-Drone-Project

## Introduction
Drones provide an excellent learning opportunity for science and technology educators, students, kids, and drone enthusiasts. They provide a hands-on learning experience about the principles of flight and electronics, among other topics. The current cost of a full drone setup, however, can quickly exceed one’s budget. One potential solution to expand the availability of classroom drone projects is to replace the drone’s standalone remote controller with a mobile app that allows the users to control the drones indoors or within a closed range.

The project intends to develop a mobile application that provides some of the basic functionalities of a drone’s standalone remote controller. 

As part of the project, we want to build an application that
* Is easy to use.
* Allows pairing between the drone’s onboard receiver with the drone pilot’s mobile device (iOS or Android) via Bluetooth.
* Sends requests to the drone’s receiver to control the throttle, aileron, elevator, and rudder.
* Allows users to configure settings particular to their particular drones (i.e., degrees of movement for each control surface).
* Gets the current status of the drone (i.e., the current position of the control surfaces).

A Major portion of this project already has been implemented as part of the software engineering class. During this class, we aim to resolve some of the issues that we were facing during the development of the application. One of the major issues that has been already identified is Bluetooth connectivity. As part of this project, we will set up meetings with the stakeholders and decide the action plan on whether to move with another protocol or find a supporting framework that supports Bluetooth.

The application that we build will have the following features to start with.

* Arm the plane
* Set the sensitivity of the buttons
* Control the plane with two control wheels which are used to alter parameters yaw, pitch, roll, and Throttle
* Disarm the plane

## Process diagram

The image shown below shows how our mobile application works at the basic level. Everything outside the dotted rectangular box is external to the system that we are going to build.

The app requires the user to have their mobile device's Bluetooth and the drone's Bluetooth turned on. The first step involves pairing the mobile device with the drone's receiver. If the pairing is unsuccessful, the user is informed and prompted to retry the process until it is successful.

Once the pairing is successful, the user will be shown drone controls like throttle, aileron, rudder, and elevator along with a close button that disconnects the drone from phone

The user controls the drone using the controls displayed on the mobile device's screen. The app validates the user's commands to ensure that they are valid for the drone. If the command is valid, the app sends the respective signal to the drone's receiver, and the drone executes the command. If the command is invalid, the user receives an error message, and they can attempt to control the drone again.

Finally, If the user wants to disconnect the app from the drone, they can do so by clicking the close button displayed, and the drone will be unpaired from the mobile device and the user can exit the app.

![image](https://github.com/AbhilashKotha/YG-Drone-Project/blob/main/ProcessDiagram.png)

Below are a few sample UI design screenshots

![image](https://github.com/AbhilashKotha/YG-Drone-Project/assets/113061137/a63fee31-8d3d-422e-acde-94b48e38da52)
![image](https://github.com/AbhilashKotha/YG-Drone-Project/assets/113061137/56c7b66c-3c92-4f59-a8c2-19d0d92887d1)
![image](https://github.com/AbhilashKotha/YG-Drone-Project/assets/113061137/6d00ff67-635c-47c2-8033-3f9c26c6f6c7)

## Architecture


Below diagram shows the basic architecture diagram of the application

![image](https://github.com/AbhilashKotha/YG-Drone-Project/assets/113061137/92311d57-3057-4176-b8b5-31f730eb1c1a)



