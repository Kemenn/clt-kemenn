#!/usr/bin/env python3
#coding: utf-8

import os
import sys
import client_window
from time import sleep
from ast import literal_eval
from threading import Thread
from tkinter.messagebox import showinfo, showerror

class ManagerClient(Thread) :
    """ Gère les messages reçus par l'objet de connection au serveur, et les
    messages devant être affichés dans les fenêtres. Il gère aussi les messages
    provenant des fenêtres pour envoyer un message au serveur (confirmation de
    lecture ou erreur d'alerte)."""
    def __init__(self, connection_srvc, shortcut_srvc) :
        Thread.__init__(self)
        self.network_service = connection_srvc
        self.shortcut_service = shortcut_srvc
        self.userid = self.getuserid()
        self.window = None
        self.client_life = True
        self.new_message_for_server_list = []

    def run(self) :
        """ Initialise la connexion au serveur. Attent les messages venant du
        serveur pour les envoyer à traiter. Attend également que des messages
        soit à envoyer au serveur pour les pousser au gestionnaire de connexion."""
        sys.stdout.write("[started] client manager !\n")
        sys.stdout.flush()
        while self.client_life is True :
            # Msg from server
            for msg in self.network_service.input_message_list :
                self.input_processing(msg)
                self.network_service.delmsg(msg)
            # Manage window
            if self.window is not None :
                for msg in self.window.output_message :
                    self.output_processing(msg)
                    self.window.output_message.remove(msg)
                if self.window.exists :
                    self.window.update()
                else :
                    self.window = None
            # Msg from keyboard
            if self.shortcut_service.alert :
                self.output_processing("i_am_in_alert")
                self.shortcut_service.alert = False
            # Msg to server
            for msg in self.new_message_for_server_list :
                self.network_service.addmsg(msg)
                self.new_message_for_server_list.remove(msg)
            sleep(0.1)

    def input_processing(self, msg) :
        """ Fonction qui traite les messages du serveur et créer les évènements
        qui y sont associés selon leurs types :
        - alert : affiche une fenêtre avec le message d'alerte venant d'être
        reçus.
        - read : confirmation de lecture, ajoute le nom de l'expéditeur dans le
        message de la fenêtre de confirmation.
        - spvs : message de la supervision, affiche la fenêtre avec le message
        venant d'être reçus.
        - alert_sending : confirme l'envoie de l'alerte aux autres utilisateurs."""
        if msg['type'] == "alert_sending" :
            if self.window is not None and self.window.exists :
                self.window.addmessage(msg['message'])
            else :
                self.window = client_window.showconfirm(msg['message'])
        elif msg['type'] == "alert" :
            if self.window is not None and self.window.exists :
                self.window.addmessage(msg['message'])
            else :
                self.window = client_window.showalert(msg['message'], msg['sender'])
        elif msg['type'] == "alert_read" :#Don't open confirm window : is create by "alert_sending", just add os.name's reader
            if self.window is not None :
                self.window.addreader(msg['reader'])
        elif msg['type'] == "alert_error" :
            showinfo("Erreur", msg['message'])
        elif msg['type'] == "asklocation" :
            default = "" if not 'location' in msg else msg['location']
            location = client_window.asklocation(msg['message'], default) #Attention : arrêt du client durant le temps de l'entrée
            while location == "" :
                #showerror("Erreur", "Vous devez impérativement entrez une localisation !")
                location = client_window.asklocation(msg['message'], default)
            self.output_processing("location={}".format(location))

        elif msg['type'] == "command" :
            self.stop(option=msg['cmd'])


    def output_processing(self, message) :
        """ Construit le message qui sera envoyé au serveur selon son type :
        - i_am_in_alert : envoie une alerte, le raccourcis clavier a été pressé.
        - alert_is_readed : l'utilisateur à lu un message d'alerte en cours.
        - alert_is_en_error : l'utilisateur a envoyé une alerte par erreur."""
        if message == "i_am_in_alert" :
            self.new_message_for_server_list.append(
                {'type' : "alert",
                 'sender' : self.userid})
        elif "alert_is_readed" in message :
            self.new_message_for_server_list.append(
                {'type' : "alert_read",
                 'sender' : self.userid,
                 'receiver' : message.split(":")[1]})#the id of user in alert
        elif message == "alert_is_an_error" :
            self.new_message_for_server_list.append(
                {'type' : "alert_error",
                 'sender' : self.userid})
        elif "location=" in message :
            self.new_message_for_server_list.append(
                {'type' : "config_location",
                 'sender' : self.userid,
                 'location' : message[9:]})

    def stop(self, option="stopped") :
        """ Stop the thread"""
        self.client_life = option
        sys.stdout.write("[stopped] client manager : {}\n".format(option))
        sys.stdout.flush()

    def getuserid(self) :
        if os.name == "posix" :
            return os.environ["USER"].lower()
        else :
            return os.environ["USERNAME"].lower()   



if __name__ == "__main__" :
    import client_connection
    import shortcut_alert
    co = client_connection("localhost", 4700)
    co.start()
    shrtcut = shortcut_alert.ListenShortcut('F1')
    shrtcut.start()
    client = ManagerClient(co, shrtcut)
    client.start()

    commande = ""
    while client.client_life != "finish" :
        commande = str(input(">>> "))
        if commande == "alert" :
            client.output_processing("i_am_in_alert")
        elif commande == "stop" :
            client.stop()
    sys.exit()
