#!/usr/bin/env python3
#coding: utf-8

import os
import sys
from keyboard import wait
from time import time, sleep
from threading import Thread

class ListenShortcut(Thread) :
    """ Objet qui se contente d'attendre un double appuie sur une touche.
    Quand le double appuie est effectué, la variable alert passe à True."""
    def __init__(self, key, interval=1) :
        Thread.__init__(self)
        self.listen_keyboard = True
        self.key = key
        self.interval = interval
        self.alert = False
        if os.name == "posix" :
            self.time_file = "/tmp/alert/time_alert_shortcut"
        else :
            self.time_file = "C:\\Users\\{}\\AppData\\Local\\Temp\\alert\\time_alert_shortcut".format(os.environ["USERNAME"])
        self.verify_path()

    def run(self) :
        sys.stdout.write("[started] Shortcut listen service\n")
        sys.stdout.flush()
        if not os.path.exists(self.time_file) : self.write_time("0")
        while self.listen_keyboard :
            wait(self.key)
            self.key_pressed()

    def stop(self) :
        sys.stdout.write("[stopped] Shortcut listen service !\n")
        sys.stdout.flush()
        self.listen_keyboard = False

    def key_pressed(self) :
        """ Quand la touche est appuyé, calcul l'interval
        entre les deux temps d'appuie. Si il est inférieur
        au seuil définit, créé l'alerte."""
        actual_hour = int(time())
        last_pressed_hour = int(self.read_time())
        if actual_hour-last_pressed_hour <= self.interval :
            self.alert = True
        self.write_time(actual_hour)

    def write_time(self, texte) :
        """ Ecrit dans le fichier l'heure à laquelle a
        été dernièrement appuyé la touche définis"""
        open(self.time_file, 'w').write(str(texte))

    def read_time(self) :
        """ Lis le fichier dans lequel est enregistré
        l'heure du dernier appuie sur la touche"""
        return open(self.time_file, 'r').read()

    def verify_path(self) :
        """ Vérifie si les fichier et répertoire existent.
        Sinon il les créer."""
        if not os.path.exists(os.path.dirname(self.time_file)) :
            os.makedirs(os.path.dirname(self.time_file))

if __name__ == "__main__" :
    lstn = ListenShortcut('F1')
    lstn.start()
    lstn.join()
