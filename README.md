# Kemenn Client

The client for Kemenn project.

This client allows a user in danger to warn his colleagues by using a simple keyboard shortcut. Colleagues will then have a simple graphical window displayed with a message indicating the person in danger, and the location.

This is the technical documentation. You can find the users documentation here : https://github.com/Kemenn/presentation.git

- [DESCRIPTION](#description)
- [INSTALLATION](#installation)
- [CONFIGURATION](#configuration)
- [OPTIONS](#options)
- [TODO TASKS](#todo-tasks)



## Description

The client is made in 4 parts :

 - There is a service that **manages the connection** to the alert server. It works in parallel in a completely autonomous way.

 - There is the **shortcut detector**. It listens to the keyboard to detect the double press of the F12 key (by default). When the key has been pressed twice in a row, an alert is sent.

 - There is the **message manager**. As soon as a message is received, it processes it (answer to the server, display a window with a message, send an alert).

 - There is the **displayer**. It is responsible for displaying a window in a non-blocking way.


### Deployement diagram
![The deployement diagram](./docs/french_deployment_diagram.png)


### Use case diagram
![The use case diagram](./docs/french_use_case_diagram.png)



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

The file "configuration.py" contain all configuration for client.

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