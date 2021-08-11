#!/usr/bin/python3
# -*- coding : utf-8 -*-

from os import name
from tkinter import *

class WindowClient(Tk) :
    """ Affiche une fenêtre simple avec une icone, un message
    et deux boutons. Cette fenêtre n'est pas bloquante. Mais il
    faut penser à faire un update régulier, sinon les widgets
    sont inactifs."""
    def __init__ (self, message, userinalert=None, **options) :
        Tk.__init__(self)
        self.exists = True
        self.userinalert = userinalert
        self.output_message = []

        self.window_type = options['window_type']
        self.message = message
        self._title = options['title']
        self.icon = options['icon']
        self.image = PhotoImage(file=self.icon)
        self.button = "  {}  ".format(options['button'])
        self.title(self._title)
        self.wm_attributes("-topmost", 1)
        self.protocol("WM_DELETE_WINDOW", self.exit)
        self.geometry("500x170")
        self.iconphoto(False, self.image)
        self.w_icon = Label(self, image=self.image)
        self.w_icon.image = self.image
        self.w_icon.pack(side=LEFT, padx=4, pady=4)
        self.w_text = Label(self, width=47, wraplength=400, text=self.message,
            justify="left", font='Verdana 15 bold')
        self.w_text.pack(fill=Y, padx=7, pady=7)
        self.buttonspace = Label(self)
        if self.window_type == "alert" :
            self.w_button = Button(self.buttonspace, text=self.button, command=self.send_read)
        elif self.window_type == "confirm" :
            self.w_button = Button(self.buttonspace, text=self.button, command=self.send_error)
        self.w_button.pack(side=LEFT, padx=70, pady=4, fill=X)
        self.w_close = Button(self.buttonspace, text="  Fermer  ", command=self.exit)
        self.w_close.pack(side=RIGHT, padx=40, pady=4, fill=X)
        self.buttonspace.pack(side=BOTTOM)
        self.update()

    def exit(self) :
        self.exists = False
        self.destroy()

    def send_read(self) :
        """ Envoie un signal qui déclenchera l'envoi de la
        confirmation de lecture"""
        self.output_message.append("alert_is_readed:{}".format(self.userinalert))
        self.w_button['state'] = DISABLED

    def send_error(self) :
        """ Envoie un signal qui déclenchera l'envoi de
        l'erreur d'alerte"""
        self.output_message.append("alert_is_an_error")
        self.w_button['state'] = DISABLED

    def textupdate(self) :
        """ Met à jour le widget de texte"""
        self.w_text.config(text=self.message)
        self.w_text.update()

    def addmessage(self, message, separator="\n") :
        """ Ajoute un message complet à celui déjà présent
        dans la fenêtre"""
        self.message = "{}{}{}".format(self.message, separator, message)
        self.textupdate()

    def addreader(self, readername) :
        """ Ajoute le nom prénom d'un utilisateur
        qui a lu l'alerte"""
        if not " : personne" in self.message :
            self.addmessage(readername, separator=", ")
        else :
            self.message = self.message.replace("personne", readername)
            self.textupdate()

def showalert(message, useralert, **options) :
    if options.get('icon') : icon = options['icon']
    elif name == "posix" : icon = "icons/alert_icon.png"
    else : icon = "icons\\alert_icon.png"
    if options.get('title') : title = options['title']
    else : title = "! Alerte : Personne en danger !"
    if options.get('button') : button = options['button']
    else : button = "↩ Lu"
    return WindowClient(message,
        useralert,
        window_type = "alert",
        title = title,
        icon = icon,
        button = button)

def showconfirm(message, **options) :
    if options.get('icon') : icon = options['icon']
    elif name == "posix" : icon = "icons/infos_icon.png"
    else : icon = "icons\\infos_icon.png"
    if options.get('title') : title = options['title']
    else : title = "Kemenn : confirmation d'envoi !"
    if options.get('button') : button = options['button']
    else : button = "Annuler"
    return WindowClient(message,
        window_type = "confirm",
        title = title,
        icon = icon,
        button = button)

def asklocation(message, location="") :
    """ Affiche une fenêtre simple qui demande la
    localisation du bureaux et retourne sa valeur"""
    from time import sleep
    window = Tk()
    window.title("Kemenn - Demande de localisation")
    window.resizable(False, False)
    #Affichage de texte explicatif
    Label(window, text="Veuillez entrer la localisation de l'ordinateur pour le logiciel d'alerte.",
        font='Verdana 12').pack(padx=11, pady=11)
    Label(window, text="En cas d'alerte, le message affiché sera le suivant :",
        font='Verdana 11').pack(padx=11, pady=4)
    Label(window, text=message, font='Verdana 11 bold').pack(padx=11, pady=4)
    #Zone d'entrée de texte
    location_entry = Entry(window, width=len(message)-11, font='Verdana 12')
    location_entry.pack(fill=X, expand=True, padx=11, pady=7)
    location_entry.insert(0, location)
    #Affichage d'un texte informatif
    infos = "Veillez à mettre une localisation claire, sans ambiguïté qui\n"
    infos += "permette à n'importe qui de comprendre où vous vous trouvez."
    Label(window, text=infos, font='Verdana 10 italic', justify='left'
        ).pack(padx=11, pady=4)
    #Affichage du bouton valider
    valid = Button(window, text="Valider", command=window.destroy)
    valid.pack(pady=7)
    while True :
        try :
            window.update()
            location_text = location_entry.get()
        except :
            return location_text
        sleep(0.1)

if __name__ == "__main__" :
    from sys import exit
    from time import sleep

    localisation = asklocation("Alerte, Jean Dupont est en danger à [votre localisation] !",
        location="votre localisation")
    print(localisation)
    exit()

    App = showconfirm("Je confirme que l'alerte a été prise en compte !")
    App.update()
    sleep(0.7)
    App.addmessage("C'est pour ça que je l'affiche...")
    App.update()
    sleep(0.7)
    App.addreader("Cliques sur le bouton !")
    while App.exists :
        App.update()
        sleep(0.5)
