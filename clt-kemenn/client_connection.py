#! /usr/bin/env python3
#coding: utf-8

import os
import sys
import socket
import select
import netifaces
from os import name, environ
from ast import literal_eval
from threading import Thread
from time import sleep, time
from datetime import datetime

class NetworkClient(Thread) :
    """ Il s'agit de l'objet principale qui gère la connexion
    du client avec le serveur et qui exécute l'affichage des
    fenêtres d'alerte ou de remplissage d'informations."""

    def __init__(self, host, port) :
        Thread.__init__(self)
        if name == "posix" :
            self.userid = environ["USER"].lower()
        else :
            self.userid = environ["USERNAME"].lower()
        self.input_message_list = [] #msg from server
        self.output_message_list = [] #msg for server
        self.live_connection = True
        self.mac = self.getmac()
        self.connection_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection_to_server.connect((host, port))
        sys.stdout.write("Client is running on {}:{}\n".format(host, port))
        sys.stdout.flush()

    def run(self) :
        """ Fonction qui lance le serveur principal et écoute
        l'arrivé des clients, des messages, etc..."""
        sys.stdout.write("[started] server connection !\n")
        sys.stdout.flush()
        self.connection_to_server.send(self.code(
            {'type' : "asklife", 'sender' : self.userid, 'macaddr' : self.getmac()}))
        message = self.code(self.connection_to_server.recv(1024))
        self.input_message_list.append(literal_eval(message))
        sys.stdout.write("[{}]r {}\n".format(str(datetime.now()), message))
        sys.stdout.flush()
        while self.live_connection :
            read_server = []
            read_server, wlist, xlist = select.select(
                [self.connection_to_server], [], [], 0.05)
            if read_server != [] :
                try : message = self.code(self.connection_to_server.recv(1024))
                except : message = "{'type' : 'commande', 'cmd' : 'restart'}"
                sys.stdout.write("[{}]r {}\n".format(str(datetime.now()), message))
                sys.stdout.flush()
                if message != "" :
                    self.input_message_list.append(literal_eval(message))

            if len(self.output_message_list) > 0 :
                for msg in self.output_message_list :
                    self.connection_to_server.send(self.code(msg))
                    sys.stdout.write("[{}]s {}\n".format(str(datetime.now()), msg))
                    sys.stdout.flush()
                    self.output_message_list.remove(msg)
            sleep(0.47)

        self.live_connection = "stopped"

    def stop(self) :
        """ Fonction qui stop la connection du clients avec
        le server, ou la redémarre"""
        self.live_connection = False
        while self.live_connection != "stopped" : sleep(0.1)
        self.connection_to_server.close()
        sys.stdout.write("[stopped] server connection !\n")
        sys.stdout.flush()

    def code(self, *args) :
        """ Fonction qui prend un/des arguments. Si il y en
        a un seul et de type 'byte' on le décode et on le
        renvoie en type 'str'. Sinon on assemble les arguments
        (si plusieurs) et on retourne une chaine de caractère
        encodé en 'byte'"""
        if len(args) == 1 and type(args[0]) == bytes :
            return args[0].decode()
        return "".join([str(i) for i in args]).encode()

    def addmsg(self, msg) :
        """ Ajoute un message à la liste"""
        msg['macaddr'] = self.mac
        self.output_message_list.append(msg)

    def delmsg(self, msg) :
        """ Enlève un message de la liste des messages reçus"""
        self.input_message_list.remove(msg)

    def read(self) :
        """ Lis les messages entrant """
        messages = self.input_message_list
        self.input_message_list = []
        return messages

    def getmac(self) :
        EXCLUDED_INTERFACE = ['lo']
        EXCLUDED_MAC = ['', '00:00:00:00:00:00:00:e0']
        addr_mac = []
        for i in netifaces.interfaces() :
            if not i in EXCLUDED_INTERFACE :
                mac = netifaces.ifaddresses(i)[netifaces.AF_LINK][0]['addr']
                if not mac in EXCLUDED_MAC :
                    addr_mac.append(mac.replace(":", "").lower())
        return addr_mac[0]

if __name__ == "__main__" :
    import configuration
    co = None
    while co is None :
        try :
            co = NetworkClient(configuration.HOST, configuration.PORT)
        except ConnectionRefusedError:
            print("Erreur lors de la connection")
            sleep(2)
            if connection_valid < 7 : connection_valid += 1
            else : sys.exit(1)
    co.start()
    sleep(2)
    co.stop()
    co.join()
