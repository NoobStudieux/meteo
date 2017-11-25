#!/usr/bin/python3.6
#-*-coding:Utf8-*-

import threading, json
from urllib.request import urlopen
from tkinter import *

class ThreadRequete(threading.Thread):
    def __init__(self, canvas):
        threading.Thread.__init__(self)
        self.can = canvas
    def run(self):
        reponse = urlopen("http://www.infoclimat.fr/public-api/gfs/json?_ll=48.85341,2.3488&_auth=U0kAFwV7AyFVeAQzUyUCK1gwUGVeKFN0Uy8HZA9qVCkIY1U0BmYBZ1E%2FBHkGKQA2VntXNAgzBjZUP1AoAXNVNFM5AGwFbgNkVToEYVN8AilYdlAxXn5TdFMzB2cPfFQ2CGxVMQZ7AWJROARgBigANlZgVzIIKAYhVDZQMgFtVTZTOQBtBWIDYlU6BGJTfAIpWG5QYV5hUz1TZgdhD2pUNwhuVTAGYQEyUTYEbwYoADJWYVc0CDQGPlQ%2BUD8BbVUpUy8AHQUVA3xVegQkUzYCcFh2UGVeP1M%2F&_c=51602a5bb6f07ac0369caa115b564ec5")
        reponseJson = json.load(reponse)
        self.can.delete('all')
        x = 20
        y = 400
    # legende 
        self.can.create_text(50,10, text='temperature', fill='red')
        self.can.create_text(50,30, text='pluie', fill='blue')
        self.can.create_text(50,50, text='humidite', fill='light blue')
        self.can.create_text(50,70, text='vent moyen', fill='dark green')
        # créations des 2 axes : 
        self.can.create_line(x,y+200, x, y - 550) # axe y
        self.can.create_line(x,y, x + 850, y)   # axe x
        # graduation sur y : 
        for i in range(-200, 550, 50):
            self.can.create_line(x-5,y-i, x + 5, y-i)
        # traitement des infos : 
        temp_precedente = None
        for r in reponseJson:
            if not re.search("[a-z]{2}", r):
                if x == 20: # si x == 20 il n'ya pas de temperature précedente et donc pas de trace
                    pass
                elif temp_precedente: # sinon dessin si temp_precedente != None
            # temperature
                    temp = reponseJson[r]['temperature']['sol'] - 273.15
                    temp = round(temp,2)
                    self.can.create_line(x-10, y - (temp_precedente * 10) , x, y-(temp*10), fill="red")
            # pluie
                    pluie = reponseJson[r]['pluie']
                    self.can.create_line(x-10, y - (pluie_precedente * 20) , x, y-(pluie*20), fill="blue")
            # humidite
                    humidite = reponseJson[r]['humidite']['2m']
                    self.can.create_line(x-10, y - (humidite_precedente * .2) , x, y-(humidite*.2), fill="light blue")
            # vent moyen
                    vent_moyen = reponseJson[r]['vent_moyen']['10m']
                    self.can.create_line(x-10, y - (vent_moyen_precedent * 3) , x, y-(vent_moyen*3), fill="dark green")
                if re.search("01:00:00", r): # si c'est un nouveau jour je cree le tiret sur x
                    self.can.create_line(x, y+5 , x, y-5)   
                    self.can.create_text(x-5, y+10 , text=r[8:10])
                temp_precedente = reponseJson[r]['temperature']['sol'] - 273.15
                temp_precedente = round(temp_precedente,2)
                pluie_precedente = reponseJson[r]['pluie']
                humidite_precedente = reponseJson[r]['humidite']['2m']
                vent_moyen_precedent = reponseJson[r]['vent_moyen']['10m']
                
                temp = reponseJson[r]['temperature']['sol'] - 273.15
                temp = round(temp,2)
                x += 10
class Fenetre(Frame):
    def __init__(self):
        Frame.__init__(self, bg="red")
        self.can = Canvas(width=800, height=800, bg="green")
        self.can.pack()
        th = ThreadRequete(self.can)
        th.start()

if __name__ == "__main__":
    Fenetre().mainloop()