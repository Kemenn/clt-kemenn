#! /usr/bin/env python3
#coding: utf-8
from os import name, environ

"""Les différents paramètres configurable sont :
 - HOST : l'adresse ip du serveur d'alerte
 - PORT : le port pour se connecter au serveur d'alerte
 - NBR_TRY : le nombe de tentative de connexion au serveur avant abandon
 - TIME_TRY : le temps qui sépare chaque tentative (en seconde)
 - MAINTENANCE_TIME : correspond au temps d'attente (en minute) en cas
                      de demande de redémarrage des clients en mode
                      maintenance.
 - ALERT_SHORTCUT : touche pour laquelle un double appuie déclenchera l'alerte.
 - ICON : Le chemin vers l'icone utilisé pour les notifications.
 # OUT_LOG : Chemin du fichier dans lequel seront écrit les logs.
 # ERR_LOG : Pareil que précédemment mais pour les messages d'erreurs.
 - NOTIFY_TTL : dictionnaire des titres affichés lors d'une notification.
 - NOTIFY_TXT : dictionnaire des messages affichés lors d'une notification.
"""

HOST="srv-kemenn.domain.local"
PORT=4700
NBR_TRY = 11           #number of tries to connect to server before shutdown client
TIME_TRY = 70          #time between tries (in seconds)
MAINTENANCE_TIME = 5   #time before retries to connect in minutes
ALERT_SHORTCUT = 'F12' #key use for send alert

if name == "posix" :
    ICON = "/usr/share/icons/alert_icon.png"
#    OUT_LOG = "{}/.cache/alert/out.log".format(environ['HOME'])
#    ERR_LOG = "{}/.cache/alert/err.log".format(environ['HOME'])
else :
    ICON = "C:\\Program Files\\alert\\icons\\alert_icon.ico"
#    OUT_LOG = "{}\\AppData\\Local\\alert\\out.log".format(environ['USERPROFILE'])
#    ERR_LOG = "{}\\AppData\\Local\\alert\\err.log".format(environ['USERPROFILE'])

NOTIFY_TTL = {
    'unavailable' : "Serveur d'alerte non disponible...",
    'nonetwork' : "Réseaux non disponible...",
    'unreachable' : "Serveur d'alerte injoignable...",
    'started' : "Alerte est démarré...",
    'shutdown' : "Arrêt du logiciel d'alerte...",
    'maintenance' : "Arrêt du logiciel d'alerte...",
    'error' : "Arrêt du logiciel d'alerte..."
}
NOTIFY_TXT = {
    'unavailable' : "Le logiciel d'alerte retente une connexion\ndans quelques instants...",
    'nonetwork' : "Le logiciel d'alerte n'a pas accès au réseaux.\nNouvelle tentative dans quelques instants...",
    'unreachable' : "Le logiciel d'alerte va s'arrêter et ne sera pas actif durant votre session.\nVeuillez contacter votre administrateur réseaux !",
    'started' : "Le logiciel d'alerte est correctement démarré !",
    'shutdown' : "Le logiciel d'alerte va s'arrêter suite à la demande de l'administrateur.\nL'envoie d'alerte n'est plus possible durant votre session !",
    'maintenance' : "Le logiciel d'alerte est déconnecté suite à la demande de l'administrateur.\nL'envoie d'alerte n'est plus possible temporairement !\nLe client se reconnectera dans {} minutes.".format(MAINTENANCE_TIME),
    'error' : "Le logiciel d'alerte s'est arrêté pour une raison inconnue.\nL'envoie d'alerte n'est plus possible temporairement !\nLe client tente de se reconnecter."
}
