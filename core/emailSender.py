#!/usr/bin/python

import smtplib

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("sispaiunb@gmail.com", "dinossauro")


def sendMessage():
	msg = "\n Ocorreu um erro com os sensores de sua Piscina!" 
	server.sendmail("sispaiunb@gmail.com", "correia.gustavol@gmail.com", msg)