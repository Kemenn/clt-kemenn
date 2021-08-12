# Kemenn Client

The client for Kemenn project.

This client allows a user in danger to warn his colleagues by using a simple keyboard shortcut. Colleagues will then have a simple graphical window displayed with a message indicating the person in danger, and the location.

You can found more technical details on documentation : https://github.com/Kemenn/documentation.git

- [DESCRIPTION](#description)
- [INSTALLATION](#installation)
- [CONFIGURATION](#configuration)
- [OPTIONS](#options)
- [TODO TASKS](#todo-tasks)



## Description

### Sending messages

**Sending an alert**

A double press on the F12 key is enough to send an alert.

It is possible to send a counter-indication in case of error, and thus a false alarm, in order to avoid panicking colleagues ;)

**Confirmation of reading an alert**

A user who receives an alert can click on a "Read" button. This has the effect of immediately notifying the person in danger that the alert has been read by such and such a person.

This is intended to reassure, although it is not a necessity.

**Canceling an alert**

A user who has sent an alert by mistake can warn other users that it is a false alert. To do this, the user who sent the alert simply presses the "Cancel" button.

This is to avoid the displacement of co-workers!


### User group :

To determine who should receive the alert from which user, user groups are created. Thus a user of a group sends the alert to the other users of his group.
The user can be part of several groups. In this case the recipients are all the other users of all the groups to which the user in danger belongs.
A special group called "global group" allows users in this group to receive alerts from everyone!

[Groups can be configured from the web interface.](#groups-management)


### Location :

To determine the location of a device, we use its mac address. So there is a correspondence between the mac address and a humanly understandable name that is made.

It is possible to configure this in the web interface. But if a client connects with a given device for the first time, the kemenn server detects it and automatically asks for a comprehensible location name in order to register it.



## Installation

**Python dependancy :**
`ast, datetime, keyboard, netifaces, os, plyer (just linux), random, select, socket, sys, threading, time, tkinter, win10toast (just windows)`


### Windows :

The installation is done in two parts: The creation of the executable, then the installation itself (by copying the files).

*Note*: Python does not need to be installed on the targeted computers, but only on the computer that will create the executable.

**1 - Create the executable** :

- *Installing python* : <https://www.python.org/downloads/>
- *Installing the dependencies requires* :
  `python -m pip install keyboard, netifaces, tkinter, win10toast`
- *Installing pyinstaller* :
  `python -m pip install pyinstaller`
- *Downloading the sources* from the github repository.
    * you can just download the archive directly from github. Then extract the files.
    * or use this command :
    `git clone https://github.com/Kemenn/clt-kemenn.git`
- Open powershell and move through the previously downloaded sources to the `clt-kemenn/` folder with the `cd` command.
- *Create the executable* with the command: `pyinstaller --onefile --noconsole ./main.py`

If the dependencies are correctly satisfied, the executable should be in the "dist" folder.

**2 - Install the software in users computer** :

 - Create a "kemenn" folder.
 - Copy the previously created executable to it.
 - Copy the "icons" folder from source to it *(clt-kemenn/icons)*.
 - Copy this "kemenn" folder in "C:\Program Files\"
 - To launch kemenn at startup, create a shortcut from "C:\Program Files\kemenn\main.exe" to the special folder `shell:common startup`.


#### Linux (debian based) :

A completer



## Configuration

The file "configuration.py" contain all configuration for client. You must to modify this file before create the .exe file.

In order, you can set :

| Variable name | Fonction |
| :-----------: | :------- |
| HOST          | The ip or hostname of kemenn server |
| PORT          | The listened port configure in kemenn server |
| NBR_TRY       | The number of times the client tries to connect to the kemenn server before stopping. |
| TIME_TRY      | Waiting time between two connection attempts. |
| MAINTENANCE_TIME | Time to wait for a new connection attempt when the alert server is in maintenance. (See the srv-kemenn documentation) |
| ALERT_SHORTCUT | The key on the keyboard that must be pressed twice to send an alert. |
|               |  |
| ICON          | The path to the icon use in notification. |
| NOTIFY_TTL    | The title of notification (you can modify just value at right of ":" between quotation marks). |
| NOTIFY_TXT    | The content of notification (you can modify just value at right of ":" between quotation marks). |



## Todo Tasks

 - Create a configuration file other than in python to allow changing the configuration without having to recreate the executable.
 
 - Change the grapic windows by windows in Gtk... or other...
 
 - Complete the documentation for linux installation.