#!/usr/bin/python3
# -*- coding : utf-8 -*-
class Test() :
    def __init__(self, co_svc, sh_svc, manag_clt) :
        self.connexion = co_svc
        self.shortcut = sh_svc
        self.manager = manag_clt

        self.message_alert = {'type' : "alert",
                              'sender' : "username",
                              'message' : "Alerte : Je suis en danger ! Venez m'aider !"}
        self.message_read = {'type' : "alert_read",
                             'reader' : "Jean Dupont"}
        self.message_error = {'type' : "alert_error",
                              'message' : "Erreur, le message d'alerte ne doit finallement pas être pris en compte..."}

    def send_alert(self) :
        self.manager.output_processing("i_am_in_alert")

    def send_read(self) :
        self.manager.output_processing("alert_is_readed:root")

    def send_error(self) :
        self.manager.output_processing("alert_is_an_error")

    def recv_alert(self) :
        self.connexion.input_message_list.append(self.message_alert)

    def recv_read(self) :
        self.connexion.input_message_list.append(self.message_read)

    def recv_error(self) :
        self.connexion.input_message_list.append(self.message_error)

    def make_shortcut(self) :
        self.shortcut.alert = True

if __name__ == "__main__" :
    import client_connection
    cotosrv = client_connection.NetworkClient("HOST", "PORT")
    import shortcut_alert
    shortcut= shortcut_alert.ListenShortcut("F1")
    import client_manager
    manager = client_manager.ManagerClient(cotosrv, shortcut)

    t = Test(cotosrv, shortcut, manager)
    t.send_alert()
    t.send_read()
    t.send_error()
    t.recv_alert()
    t.recv_read()
    t.recv_read()
    t.recv_error()
    t.make_shortcut()
