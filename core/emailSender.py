#!/usr/bin/python

import smtplib

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("sispaiunb@gmail.com", "dinossauro")


def sendMessage():
	print "Gussssss"
<<<<<<< HEAD
	msg = "\n Ocorreu um erro com os sensores de sua Piscina!"
=======
	msg = "\n Ocorreu um erro com os sensores de sua Piscina!" # The /n separates the message from the headers
>>>>>>> 45db55c4f48a6cfed58ade5d2018e8f1ff866558
	server.sendmail("sispaiunb@gmail.com", "correia.gustavol@gmail.com", msg)