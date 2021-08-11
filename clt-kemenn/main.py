#!/usr/bin/python3
# -*- coding : utf-8 -*-

""" C'est la partie cliente qui gère le lancement et l'arrêt
ou redémarrage des différents services. Il existe trois services
principaux : l'écoute du réseaux, l'écoute du clavier, la gestion
des entrées/sorties qui se chargeras en autre d'ouvrir les fenêtres.

Le client à donc 12 minutes (par défaut) pour réussir à entrer
en contact avec le serveur.
Le client entre en attente de maintenance si le serveur d'alerte
le demande explicitement. ATTENTION : le mode maintenance n'est
pas exactement pareil qu'un redémarrage simple. Il y a un temps
de maintenance en plus pour laisser le temps aux informaticiens
de mettre à jour le serveur par exemple.
Un temps aléatoire entre 0 et 5 secondes est ajouté au moment de
la connexion au serveur pour éviter que trop de clients tentent
de se connecter en même temps au serveur."""

import os
import sys
import socket
import client_connection
import shortcut_alert
import client_manager
from time import sleep
from random import uniform
if os.name == "posix" : from plyer import notification
else : from win10toast import ToastNotifier
#import all configuration variables
from configuration import *

#stdout = open(OUT_LOG, 'w')
#stderr = open(ERR_LOG, 'w')

CONNECTION=True
SHORTCUT_RUNNING=False

def notify(textes) :
    """ Créer une notification. Le paramètre doit être un tuple
    (titre, texte) """
    if os.name == "posix" : notification.notify(
        title=textes[0], message=textes[1], app_name="alert",
            app_icon=ICON)
    else :
        notif = ToastNotifier()
        notif.show_toast(textes[0], textes[1], icon_path=ICON,
            duration=470, threaded=True)

def try_connect() :
    sleep(uniform(0, 5))
    connect_not_valid = 1
    while connect_not_valid :
        try :
            co = client_connection.NetworkClient(HOST, PORT)
            connect_not_valid = 0 #equivalent to False : stop while loop
            return co
        except ConnectionRefusedError :
            sys.stdout.write("connection attempt to the server failed ({}).\n".format(connect_not_valid))
            sys.stdout.flush()
            if connect_not_valid < NBR_TRY : connect_not_valid += 1
            else : return None
            notify((NOTIFY_TTL['unavailable'], NOTIFY_TXT['unavailable']))
        except socket.gaierror :
            sys.stdout.write("no access to network ({}).\n".format(connect_not_valid))
            sys.stdout.flush()
            if connect_not_valid < NBR_TRY : connect_not_valid += 1
            else : return None
            notify((NOTIFY_TTL['nonetwork'], NOTIFY_TXT['nonetwork']))
        sleep(TIME_TRY)
    notify((NOTIFY_TTL['unreachable'], NOTIFY_TXT['unreachable']))
    sys.exit(1)

def client_accepted(network) :
    while len(network.input_message_list) == 0 : sleep(0.4)
    msg = network.input_message_list[0]
    network.input_message_list.remove(msg)
    if msg['type'] == "command" :
        if msg['cmd'] == "shutdown" :
            return False
        return True
    return None


while CONNECTION :
    network_client = try_connect()
    if network_client is not None :
        network_client.start()
        response = client_accepted(network_client)
    else : response = None

    if response == True :
        sys.stdout.write("[starting] all others client's components...\n")
        sys.stdout.flush()
        #Service d'écoute du raccourcis clavier
        if not SHORTCUT_RUNNING :
            shortcut_thread = shortcut_alert.ListenShortcut(ALERT_SHORTCUT)
            shortcut_thread.start()
            SHORTCUT_RUNNING = True
        #Gestionnaire des messages
        client = client_manager.ManagerClient(network_client, shortcut_thread)
        client.start()
        sys.stdout.write("[started] all client's components...\n")
        sys.stdout.flush()
        notify((NOTIFY_TTL['started'], NOTIFY_TXT['started']))


        #Pour faire des test, dé-commenter la ligne, sinon la laisser tel quel.
        #make_test()

        #Attente d'arrêt du coeur du client
        client.join()

        #Arrêt du service réseaux
        network_client.stop()
        network_client.join()
        #Vérifie si le client doit être redémarré ou définitivement arrêté
        if client.client_life == "shutdown" :
            notify((NOTIFY_TTL['shutdown'], NOTIFY_TXT['shutdown']))
            #Arrêt du service clavier
            shortcut_thread.stop()
            shortcut_thread.join() #doit attendre l'appuie sur F1 pour s'arrêter
            SHORTCUT_RUNNING = False
            CONNECTION = False
        elif client.client_life == "maintenance" :
            notify((NOTIFY_TTL['maintenance'], NOTIFY_TXT['maintenance']))
            sleep(MAINTENANCE_TIME*60)
            shortcut_thread.alert = False
        else :
            notify((NOTIFY_TTL['error'], NOTIFY_TXT['error']))
            shortcut_thread.alert = False

    elif response == False :
        network_client.stop()
        network_client.join()
        CONNECTION = False

sys.exit(0)