#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# AmigaNG Workbench 3.1
# Version 0.2
# (c) 2014 - 2024
# by Wolfgang Schuster

import os
import time
import pygame
import psutil

from pygame.locals import (
	K_UP,
	K_DOWN,
	K_LEFT,
	K_RIGHT,
	K_ESCAPE,
	K_RETURN,
	KEYDOWN,
	QUIT,
)

pygame.init()
pygame.joystick.init()

width = 800
height = 600

if not pygame.font: print('Fehler pygame.font Modul konnte nicht geladen werden!')
menuefont = pygame.font.Font("fonts/AmigaTopaz.ttf", 15)
iconfont = pygame.font.Font("fonts/AmigaTopaz.ttf", 15)
font = pygame.font.Font("fonts/AmigaTopaz.ttf", 15)
	
class appicon:
	def __init__(self, screen, name ,typ, pos, befehl):
		self.screen = screen
		self.name = name
		self.typ = typ		
		self.pos = pos
		self.befehl = befehl
		self.rect = pygame.Rect(0,0,0,0)
		self.clicked = False
		self.image = pygame.image.load("images/fd1.png")
		self.cimage = pygame.image.load("images/fd2.png")
		
		if self.typ=="hd":		
			self.image = pygame.image.load("images/hd1.png")
			self.cimage = pygame.image.load("images/hd2.png")
		elif self.typ=="cli":
			self.image = pygame.image.load("images/cli1.png")
			self.cimage = pygame.image.load("images/cli2.png")

	def ausgabe(self,screen, font):
			if self.clicked:
				self.rect = screen.blit(self.cimage,self.pos)
				pygame.draw.line(screen, (0,0,0), [self.rect.x-1, self.rect.y-2], [self.rect.x-1, self.rect.y+self.rect.h+2], 1)	
				pygame.draw.line(screen, (0,0,0), [self.rect.x-1, self.rect.y-2], [self.rect.x+self.rect.w+1, self.rect.y-2], 2)	
				pygame.draw.line(screen, (255,255,255), [self.rect.x+self.rect.w+1, self.rect.y-2], [self.rect.x+self.rect.w+1, self.rect.y+self.rect.h+1], 1)	
				pygame.draw.line(screen, (255,255,255), [self.rect.x, self.rect.y+self.rect.h+2], [self.rect.x+self.rect.w+1, self.rect.y+self.rect.h+2], 2)
				icontext = font.render(self.name, True, (0, 0, 0))
				screen.blit(icontext,(self.rect.x+self.rect.w/2-icontext.get_rect().w/2,self.rect.y+self.rect.h+6))
			else:
				self.rect = screen.blit(self.image,self.pos)
				pygame.draw.line(screen, (255,255,255), [self.rect.x-1, self.rect.y-2], [self.rect.x-1, self.rect.y+self.rect.h+2], 1)	
				pygame.draw.line(screen, (255,255,255), [self.rect.x-1, self.rect.y-2], [self.rect.x+self.rect.w+1, self.rect.y-2], 2)	
				pygame.draw.line(screen, (0,0,0), [self.rect.x+self.rect.w+1, self.rect.y-2], [self.rect.x+self.rect.w+1, self.rect.y+self.rect.h+1], 1)	
				pygame.draw.line(screen, (0,0,0), [self.rect.x, self.rect.y+self.rect.h+2], [self.rect.x+self.rect.w+1, self.rect.y+self.rect.h+2], 2)
				icontext = font.render(self.name, True, (0, 0, 0))
				screen.blit(icontext,(self.rect.x+self.rect.w/2-icontext.get_rect().w/2,self.rect.y+self.rect.h+6))
				
			return
		
	
class fenster:
	def __init__(self, typ, fenstername, fensterrect):
		self.typ = typ		
		self.fensterrect = fensterrect
		self.savefensterrect = pygame.Rect(0,0,0,0)
		self.savefensterrect.x = self.fensterrect.x
		self.savefensterrect.y = self.fensterrect.y
		self.savefensterrect.w = self.fensterrect.w
		self.savefensterrect.h = self.fensterrect.h						
		self.outfensterrect = pygame.Rect(self.fensterrect.x-4,self.fensterrect.y-22,self.fensterrect.w+21,self.fensterrect.h+25)
		self.fenstername = fenstername
		self.aktiv = True
		self.farbe = (0,0,0)
		self.hinweistext = []
		self.icons = []
		self.verschieben = False
		self.fenstercloserect = (0,0,0,0)	
		self.fenstertoprect = (0,0,0,0)	
		self.fenstervollrect = (0,0,0,0)	
		self.fensterfrontrect = (0,0,0,0)	
		self.fenstersizerect = (0,0,0,0)	
		self.fensterokrect = (0,0,0,0)	
		self.fenstercancelrect = (0,0,0,0)	

	def ausgabe(self, screen):
		if self.aktiv:
			self.farbe = (102,136,187)
		else:
			self.farbe = (170,170,170)		

		pygame.draw.rect(screen, (170, 170, 170), self.fensterrect, 0)	
		
		# Top	
		pygame.draw.rect(screen, self.farbe, (self.fensterrect.x-4,self.fensterrect.y-20,self.fensterrect.w+22,18), 0)			
		pygame.draw.rect(screen, (0,0,0), (self.fensterrect.x-3,self.fensterrect.y-2,self.fensterrect.w+21,2), 0)			
		pygame.draw.rect(screen, (255,255,255), (self.fensterrect.x-4,self.fensterrect.y-22,self.fensterrect.w+22,2), 0)
		pygame.draw.rect(screen, (0,0,0), (self.fensterrect.x-3,self.fensterrect.y-2,self.fensterrect.w+21,2), 0)			

		if self.typ != "hinweis" and self.typ != "janein":
			pygame.draw.line(screen, (0,0,0), [self.fensterrect.x+16, self.fensterrect.y-20], [self.fensterrect.x+16, self.fensterrect.y-3], 1)
			pygame.draw.line(screen, (255,255,255), [self.fensterrect.x+17, self.fensterrect.y-20], [self.fensterrect.x+17, self.fensterrect.y-3], 1)
			pygame.draw.line(screen, (0,0,0), [self.fensterrect.x+self.fensterrect.w-33, self.fensterrect.y-20], [self.fensterrect.x+self.fensterrect.w-33, self.fensterrect.y-3], 1)
			pygame.draw.line(screen, (255,255,255), [self.fensterrect.x+self.fensterrect.w-32, self.fensterrect.y-20], [self.fensterrect.x+self.fensterrect.w-32, self.fensterrect.y-3], 1)
			pygame.draw.rect(screen, (0,0,0), (self.fensterrect.x+3,self.fensterrect.y-15,7,9), 0)			
			pygame.draw.rect(screen, (255,255,255), (self.fensterrect.x+5,self.fensterrect.y-13,3,5), 0)					
			pygame.draw.rect(screen, (0,0,0), (self.fensterrect.x+self.fensterrect.w-27,self.fensterrect.y-18,15,14), 0)			
			pygame.draw.rect(screen, self.farbe, (self.fensterrect.x+self.fensterrect.w-26,self.fensterrect.y-16,13,10), 0)			
			pygame.draw.rect(screen, (0,0,0), (self.fensterrect.x+self.fensterrect.w-27,self.fensterrect.y-17,8,7), 0)			
			pygame.draw.rect(screen, (255,255,255), (self.fensterrect.x+self.fensterrect.w-25,self.fensterrect.y-16,4,4), 0)			
			self.fenstercloserect = (self.fensterrect.x-2,self.fensterrect.y-20,18,18)	
			self.fenstervollrect = (self.fensterrect.x+self.fensterrect.w-31,self.fensterrect.y-20,23,18)	
			self.fenstersizerect = (self.fensterrect.x+self.fensterrect.w,self.fensterrect.y+self.fensterrect.h-14,17,15)	
		
		pygame.draw.line(screen, (0,0,0), [self.fensterrect.x+self.fensterrect.w-8, self.fensterrect.y-20], [self.fensterrect.x+self.fensterrect.w-8, self.fensterrect.y-3], 1)
		pygame.draw.line(screen, (255,255,255), [self.fensterrect.x+self.fensterrect.w-7, self.fensterrect.y-20], [self.fensterrect.x+self.fensterrect.w-7, self.fensterrect.y-3], 1)		
		pygame.draw.rect(screen, (0,0,0), (self.fensterrect.x+self.fensterrect.w-4,self.fensterrect.y-18,13,10), 0)			
		pygame.draw.rect(screen, (170,170,170), (self.fensterrect.x+self.fensterrect.w-3,self.fensterrect.y-16,11,6), 0)			
		pygame.draw.rect(screen, (0,0,0), (self.fensterrect.x+self.fensterrect.w+1,self.fensterrect.y-14,13,10), 0)			
		pygame.draw.rect(screen, (255,255,255), (self.fensterrect.x+self.fensterrect.w+2,self.fensterrect.y-12,11,6), 0)			
		self.fenstertoprect = (self.fensterrect.x+18,self.fensterrect.y-20,self.fensterrect.w-51,18)	
		self.fensterfrontrect = (self.fensterrect.x+self.fensterrect.w-7,self.fensterrect.y-20,23,18)	

		# Left
		pygame.draw.rect(screen, self.farbe, (self.fensterrect.x-3,self.fensterrect.y,3,self.fensterrect.h+2), 0)			
		pygame.draw.rect(screen, (255,255,255), (self.fensterrect.x-4,self.fensterrect.y-22,1,self.fensterrect.h+24), 0)			
		pygame.draw.rect(screen, (0,0,0), (self.fensterrect.x-1,self.fensterrect.y,1,self.fensterrect.h), 0)			

		# Bottom
		pygame.draw.rect(screen, (255,255,255), (self.fensterrect.x,self.fensterrect.y+self.fensterrect.h,self.fensterrect.w+17,2), 0)			
		pygame.draw.rect(screen, (0,0,0), (self.fensterrect.x-4,self.fensterrect.y+self.fensterrect.h+2,self.fensterrect.w+21,2), 0)			
							
		# Right
		if self.typ == "hinweis" or self.typ == "janein":
			pygame.draw.rect(screen, self.farbe, (self.fensterrect.x+self.fensterrect.w+15,self.fensterrect.y,2,self.fensterrect.h+2), 0)			
			pygame.draw.rect(screen, (255,255,255), (self.fensterrect.x+14+self.fensterrect.w,self.fensterrect.y,1,self.fensterrect.h+2), 0)			
			pygame.draw.rect(screen, (0,0,0), (self.fensterrect.x+self.fensterrect.w+17,self.fensterrect.y-20,1,self.fensterrect.h+24), 0)			

		else:
			pygame.draw.rect(screen, self.farbe, (self.fensterrect.x+self.fensterrect.w+1,self.fensterrect.y,16,self.fensterrect.h+2), 0)			
			pygame.draw.rect(screen, (255,255,255), (self.fensterrect.x+self.fensterrect.w,self.fensterrect.y,1,self.fensterrect.h+2), 0)			
			pygame.draw.rect(screen, (0,0,0), (self.fensterrect.x+self.fensterrect.w+17,self.fensterrect.y-20,1,self.fensterrect.h+24), 0)			
			pygame.draw.rect(screen, (255,255,255), (self.fensterrect.x+self.fensterrect.w,self.fensterrect.y+self.fensterrect.h-15,17,2), 0)			
	
			pygame.draw.rect(screen, (0,0,0), (self.fensterrect.x+self.fensterrect.w+4,self.fensterrect.y+self.fensterrect.h-10,10,10), 0)			
			pygame.draw.rect(screen, (255,255,255), (self.fensterrect.x+self.fensterrect.w+5,self.fensterrect.y+self.fensterrect.h-9,8,7), 0)			
			pygame.draw.line(screen, (0,0,0), [self.fensterrect.x+self.fensterrect.w+4, self.fensterrect.y+self.fensterrect.h-2], [self.fensterrect.x+self.fensterrect.w+12, self.fensterrect.y+self.fensterrect.h-10], 2)
			pygame.draw.line(screen, self.farbe, [self.fensterrect.x+self.fensterrect.w+3, self.fensterrect.y+self.fensterrect.h-3], [self.fensterrect.x+self.fensterrect.w+12, self.fensterrect.y+self.fensterrect.h-12], 4)
			pygame.draw.rect(screen, self.farbe, (self.fensterrect.x+self.fensterrect.w+4,self.fensterrect.y+self.fensterrect.h-10,5,5), 0)			


		tmptext = self.fenstername
		fenstertext = font.render(tmptext, True, (0, 0, 0))
		if self.typ == "hinweis" or self.typ == "janein":
			screen.blit(fenstertext,(self.fensterrect.x,self.fensterrect.y-19))
		else:
			screen.blit(fenstertext,(self.fensterrect.x+22,self.fensterrect.y-19))
					

		if self.typ == "hinweis" or self.typ == "janein":
			pygame.draw.rect(screen, (225,225,225), (self.fensterrect.x,self.fensterrect.y,self.fensterrect.w+14,self.fensterrect.h), 0)			
			pygame.draw.rect(screen, (170,170,170), (self.fensterrect.x+5,self.fensterrect.y+5,self.fensterrect.w+4,self.fensterrect.h-44), 0)			
			pygame.draw.line(screen, (0,0,0), [self.fensterrect.x+6, self.fensterrect.y+5], [self.fensterrect.x+6, self.fensterrect.y+self.fensterrect.h-40], 1)
			pygame.draw.line(screen, (255,255,255), [self.fensterrect.x+self.fensterrect.w+8, self.fensterrect.y+5], [self.fensterrect.x+self.fensterrect.w+8, self.fensterrect.y+self.fensterrect.h-40], 1)		
			pygame.draw.line(screen, (0,0,0), [self.fensterrect.x+6, self.fensterrect.y+5], [self.fensterrect.x+self.fensterrect.w+8, self.fensterrect.y+5], 1)
			pygame.draw.line(screen, (255,255,255), [self.fensterrect.x+6, self.fensterrect.y+self.fensterrect.h-40], [self.fensterrect.x+self.fensterrect.w+8, self.fensterrect.y+self.fensterrect.h-40], 1)

		if self.typ == "hinweis" or self.typ == "janein":
			# OK-Button
			tmptext = "OK"
			buttonwidth = 30
			buttonheight = 20
			if self.typ == "hinweis":
				buttonposx = self.fensterrect.x+(self.fensterrect.w+14)/2-buttonwidth/2
			elif self.typ == "janein":
				buttonposx = self.fensterrect.x+6
			buttonposy = self.fensterrect.y+self.fensterrect.h-30				
			pygame.draw.rect(screen, (255,255,255), (buttonposx-1,buttonposy-1,buttonwidth+2,buttonheight+2), 0)			
			pygame.draw.rect(screen, (0,0,0), (buttonposx,buttonposy,buttonwidth+1,buttonheight+1), 0)			
			self.fensterokrect = pygame.draw.rect(screen, (170,170,170), (buttonposx,buttonposy,buttonwidth,buttonheight), 0)			
			buttontext = font.render(tmptext, True, (0, 0, 0))
			screen.blit(buttontext,((buttonposx+buttonwidth/2-buttontext.get_width()/2,buttonposy+buttonheight/2-buttontext.get_height()/2)))
			
				
			i = 0
			for htext in self.hinweistext:	
				tmptext = htext
				hinweistext = font.render(tmptext, True, (0, 0, 0))
				if self.typ == "janein":
					screen.blit(hinweistext,(self.fensterrect.x+(self.fensterrect.w+14)/2-hinweistext.get_width()/2,self.fensterrect.y+10+i*(hinweistext.get_height()+2)))
				elif self.typ == "hinweis":
					screen.blit(hinweistext,(self.fensterrect.x+24,self.fensterrect.y+16+i*(hinweistext.get_height()+2)))
				i = i + 1

		if self.typ == "janein":
			# Cancle-Button
			tmptext = "ABBRECHEN"
			buttonwidth = 80
			buttonheight = 20
			buttonposx = self.fensterrect.x+self.fensterrect.w+14-buttonwidth-6
			buttonposy = self.fensterrect.y+self.fensterrect.h-30
			pygame.draw.rect(screen, (255,255,255), (buttonposx-1,buttonposy-1,buttonwidth+2,buttonheight+2), 0)			
			pygame.draw.rect(screen, (0,0,0), (buttonposx,buttonposy,buttonwidth+1,buttonheight+1), 0)			
			self.fenstercancelrect = pygame.draw.rect(screen, (170,170,170), (buttonposx,buttonposy,buttonwidth,buttonheight), 0)			
			buttontext = font.render(tmptext, True, (0, 0, 0))
			screen.blit(buttontext,((buttonposx+buttonwidth/2-buttontext.get_width()/2,buttonposy+buttonheight/2-buttontext.get_height()/2)))
			
		if self.verschieben==True:			
			pygame.draw.rect(screen, (255, 0, 0), self.outfensterrect, 2)

		return
		
	def closerect(self):
		return(self.fenstercloserect)
	
	def okrect(self):
		return(self.fensterokrect)
	
	def cancelrect(self):
		return(self.fenstercancelrect)
	
	def vollrect(self):
		return(self.fenstervollrect)

	def frontrect(self):
		return(self.fensterfrontrect)
	
	def toprect(self):
		return(self.fenstertoprect)

	def outrect(self):
		return(self.outfensterrect)
	
def main():

	menueaktion = ""
	meldung = "Amigang Workbench (c)2014-2024 Wolfgang Schuster"

	screen = pygame.display.set_mode([width, height])
	
	pygame.display.set_caption("AmigangOS")
	pygame.mouse.set_visible(1)
	#pygame.key.set_repeat(1,30)

	anzahljoy = pygame.joystick.get_count()
	print("Anzahl Joysticks: ", anzahljoy)
	if anzahljoy > 0:
		for i in range(anzahljoy):
			joystick = pygame.joystick.Joystick(i)
			joystick.init()	
			print("Name: ",joystick.get_name())
			numaxes = joystick.get_numaxes()
			print("Axes: ",numaxes)
			for i in range(numaxes):
				print(joystick.get_axis(i))
			numhats = joystick.get_numhats()
			print("Hats: ", numhats)
			
			print("Buttons: ",joystick.get_numbuttons())

# Icons Workbench
	wbicons = []
	wbicons.append(appicon(screen,"Ram Disk" ,"ramdisk", (40,30), "dir:/home/wolf"))
	wbicons.append(appicon(screen,"DH0" ,"hd", (20,100), "dir:/home/wolf/dh0"))
	wbicons.append(appicon(screen,"DH1" ,"hd", (20,170), "dir:/home/wolf/dh0"))
	wbicons.append(appicon(screen,"Shell" ,"cli", (30,240), "starte:Shell"))
		
	#Menue Images
	menuerechtsoben = pygame.image.load("images/menuerechtsoben.png")
	
	# Menueliste [Name, Menutyp (menue, submenue, subsubmenue),Obermenue,befehl, rect , anzahlsubmenues, id, aktiv]
	menue = [["Workbench", "menue", "", "", pygame.Rect(0,0,0,0), 0, 0, True]]
	menue.append(["Fenster", "menue", "", "", pygame.Rect(0,0,0,0), 0, 0, True])
	menue.append(["Piktogramm", "menue", "", "", pygame.Rect(0,0,0,0), 0, 0, True])
	menue.append(["Hilfsmittel", "menue", "", "", pygame.Rect(0,0,0,0), 0, 0, True])
	menue.append(["* Workbench als Hintergrund", "submenue", "Workbench", "Workbench als Hintergrun", pygame.Rect(0,0,0,0), 0, 0, True])
	menue.append(["Befehl ausführen ...", "submenue", "Workbench", "Befehl ausführen", pygame.Rect(0,0,0,0), 0, 0, True])
	menue.append(["Bild neu aufbauen", "submenue", "Workbench", "Bild neu aufbauen", pygame.Rect(0,0,0,0), 0, 0, True])
	menue.append(["Alles aktualisieren", "submenue", "Workbench", "Alles aktualisieren", pygame.Rect(0,0,0,0), 0, 0, True])
	menue.append(["Letzte Meldung anzeigen", "submenue", "Workbench", "Letzte Meldung anzeigen", pygame.Rect(0,0,0,0), 0, 0, True])
	menue.append(["Version Copyright", "submenue", "Workbench", "Version Copyright", pygame.Rect(0,0,0,0), 0, 0, True])
	menue.append(["Workbench verlassen ...", "submenue", "Workbench", "Workbench verlassen", pygame.Rect(0,0,0,0), 0, 0, True])
	menue.append(["neue Schublade", "submenue", "Fenster", "Fenster:neue Schublade", pygame.Rect(0,0,0,0), 0, 0, True])
	menue.append(["übergeordete Schublade", "submenue", "Fenster", "Fenster:übergeordete Schublade", pygame.Rect(0,0,0,0), 0, 0, True])
	menue.append(["schließen", "submenue", "Fenster", "Fenster:schließen", pygame.Rect(0,0,0,0), 0, 0, True])
	menue.append(["aktualisieren", "submenue", "Fenster", "Fenster:aktualisieren", pygame.Rect(0,0,0,0), 0, 0, True])
	menue.append(["alles auswählen", "submenue", "Fenster", "Fenster:alles auswählen", pygame.Rect(0,0,0,0), 0, 0, True])
	menue.append(["Inhalt aufräumen", "submenue", "Fenster", "Fenster:Inhalt aufräumen", pygame.Rect(0,0,0,0), 0, 0, True])
	menue.append(["fixieren                >>", "submenue", "Fenster:fixieren", "", pygame.Rect(0,0,0,0), 0, 0, True])
	menue.append(["Inhalt anzeigen         >>", "submenue", "Fenster:anzeigen", "", pygame.Rect(0,0,0,0), 0, 0, True])
	menue.append(["Inhalt auflisten        >>", "submenue", "Fenster:auflisten", "", pygame.Rect(0,0,0,0), 0, 0, True])
	menue.append(["öffnen", "submenue", "Piktogramm", "Piktogramm:öffnen", pygame.Rect(0,0,0,0), 0, 0, True])
	menue.append(["kopieren", "submenue", "Piktogramm", "Piktogramm:kopieren", pygame.Rect(0,0,0,0), 0, 0, True])
	menue.append(["umbenennen ...", "submenue", "Piktogramm", "Piktogramm:umbenennen", pygame.Rect(0,0,0,0), 0, 0, True])
	menue.append(["Informationen", "submenue", "Piktogramm", "Piktogramm:Informationen", pygame.Rect(0,0,0,0), 0, 0, True])
	menue.append(["fixieren", "submenue", "Piktogramm", "Piktogramm:fixieren", pygame.Rect(0,0,0,0), 0, 0, True])
	menue.append(["Position freigeben", "submenue", "Piktogramm", "Piktogramm:Position freigeben", pygame.Rect(0,0,0,0), 0, 0, True])
	menue.append(["auslagern", "submenue", "Piktogramm", "Piktogramm:auslagern", pygame.Rect(0,0,0,0), 0, 0, True])
	menue.append(["zurücklegen", "submenue", "Piktogramm", "Piktogramm:zurücklegen", pygame.Rect(0,0,0,0), 0, 0, True])
	menue.append(["-------------------------", "submenue", "Piktogramm", "", pygame.Rect(0,0,0,0), 0, 0, False])
	menue.append(["löschen ...", "submenue", "Piktogramm", "Piktogramm:löschen", pygame.Rect(0,0,0,0), 0, 0, True])
	menue.append(["Disk formatieren ...", "submenue", "Piktogramm", "disk:Disk formatieren", pygame.Rect(0,0,0,0), 0, 0, True])
	menue.append(["Papierkorb leeren", "submenue", "Piktogramm", "Papierkorb leeren", pygame.Rect(0,0,0,0), 0, 0, True])
	menue.append(["WB zurücksetzen", "submenue", "Hilfsmittel", "WB zurücksetzen", pygame.Rect(0,0,0,0), 0, 0, True])
	menue.append(["des Fensters", "subsubmenue", "fixieren                >>", "fixieren des Fensters", pygame.Rect(0,0,0,0), 0, 0, True])
	menue.append(["alles", "subsubmenue", "fixieren                >>", "alles fixieren", pygame.Rect(0,0,0,0), 0, 0, True])
	menue.append(["* Nur Dateien mit Piktogr.", "subsubmenue", "Inhalt anzeigen         >>", "Folder:Inhalt Dateien mit Piktogr.", pygame.Rect(0,0,0,0), 0, 0, True])
	menue.append(["alle Dateien", "subsubmenue", "Inhalt anzeigen         >>", "Folder:Inhalt alles", pygame.Rect(0,0,0,0), 0, 0, True])
	menue.append(["als Piktogramm", "subsubmenue", "Inhalt auflisten        >>", "Folder:auflisten Piktogramm", pygame.Rect(0,0,0,0), 0, 0, True])
	menue.append(["nach Namen", "subsubmenue", "Inhalt auflisten        >>", "Folder:auflisten Namen", pygame.Rect(0,0,0,0), 0, 0, True])
	menue.append(["nach Datum", "subsubmenue", "Inhalt auflisten        >>", "Folder:auflisten Datum", pygame.Rect(0,0,0,0), 0, 0, True])
	menue.append(["nach Größe", "subsubmenue", "Inhalt auflisten        >>", "Folder:auflisten Größe", pygame.Rect(0,0,0,0), 0, 0, True])


	menueid = 1
	for menueeintrag in menue:
		menueeintrag[6] = menueid
		menueid = menueid + 1
		for submenueeintrag in menue:
			if submenueeintrag[2] == menueeintrag[0]:
				menueeintrag[5] = menueeintrag[5] + 1

#	for menueeintrag in menue:
#		print(menueeintrag)

	menuemode = 0
	aktivmenue = 0
	aktivuntermenuerect = pygame.Rect(0,0,0,0)
	aktivuntermenue = 0
	aktivsubuntermenuerect = pygame.Rect(0,0,0,0)
	aktivsubuntermenue = 0
	menueposx = 0
	menueposy = 0
	
	befehl = ""
	
	freemem = 0
	memtimer = 0
	
	leftclick = False
	rightclick = False
	leftclickpos = (0,0)
	rightclickpos = (0,0)
	lastleftclick = time.time()
	leftdoppelclick = False

	aktivicon = 0
	
	aktivfolder = 0
	
	aktivshell = False

	aktivfenster = []
	
	fensterlastpos = (0,0)
	
	running = True
	while running:

		mousepos = pygame.mouse.get_pos()
	
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

# Tastatur
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					menueaktion = "ESC"
				elif event.key == K_RIGHT:
					menueaktion = "RIGHT"
				elif event.key == K_LEFT:
					menueaktion = "LEFT"
				elif event.key == K_DOWN:
					menueaktion = "DOWN"
				elif event.key == K_UP:
					menueaktion = "UP"
				elif event.key == K_RETURN:
					menueaktion = "RETURN"

# Maus
			elif event.type == pygame.MOUSEBUTTONUP:
				if event.button==1:
					leftclick = False
				if event.button==3:
					rightclick = False
					menuemode=1
					befehl=""
					if aktivsubuntermenue>0:
						if menue[aktivsubuntermenue-1][2]==menue[aktivuntermenue-1][0]:
							befehl = menue[aktivsubuntermenue-1][3]
					elif aktivuntermenue>0:
						if menue[aktivuntermenue-1][2]==menue[aktivmenue-1][0]:
							befehl = menue[aktivuntermenue-1][3]
					print(aktivmenue,aktivuntermenue,aktivsubuntermenue)
					
				if event.button==1:
					menuemode=1
				menuemode=1
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button==1:
					leftclick = True
					leftclickpos = mousepos
					if time.time()-lastleftclick < 0.2:
						leftdoppelclick=True
					else:
						leftdoppelclick=False
					lastleftclick = time.time()
				if event.button==3:
					rightclick = True
					rightclickpos = mousepos
					menuemode=2
					aktivmenue=0
					aktivuntermenue=0
					aktivsubuntermenue=0
														
# Joystick
			elif event.type == pygame.JOYAXISMOTION:
				if event.axis == 0:
					if event.value > 0.9:
						menueaktion = "RIGHT"
					elif event.value < -0.9:
						menueaktion = "LEFT"
				elif event.axis == 1:
					if event.value > 0.9:
						menueaktion = "DOWN"
					elif event.value < -0.9:
						menueaktion = "UP"
			elif event.type == pygame.JOYBUTTONDOWN:
				if event.button == 0:
					menueaktion = "RETURN"
				elif event.button == 1:
					menueaktion = "ESC"
								
# Aktionen ausführen

		if menueaktion != "":
			if menueaktion == "ESC":
				running = False
			menueaktion = ""
						
		screen.fill((170, 170, 170))



#		Desktopicons anzeigen

		for wbicon in wbicons:
			wbicon.ausgabe(screen, iconfont)
			if leftclick:
				if wbicon.rect.collidepoint(mousepos):
					wbicon.clicked = True
				else:
					wbicon.clicked = False


			if leftdoppelclick:
				if wbicon.rect.collidepoint(mousepos):
					befehl = wbicon.befehl	
					leftdoppelclick = False	

#		Fenster anzeigen

		if len(aktivfenster)>0:
			for afenster in aktivfenster:
				afenster.ausgabe(screen)
				if leftclick:
					if pygame.Rect(afenster.outrect()).collidepoint(leftclickpos) or afenster.verschieben:
							afenster.aktiv=True	
							fensteraktiv = afenster						
					else:
							afenster.aktiv=False
					if afenster.aktiv:
						if pygame.Rect(afenster.closerect()).collidepoint(leftclickpos):
							aktivfenster.remove(afenster)
							leftclick=False				
						elif pygame.Rect(afenster.okrect()).collidepoint(leftclickpos):
							if afenster.typ=="janein":
								running=False
							aktivfenster.remove(afenster)
							leftclick=False				
						elif pygame.Rect(afenster.cancelrect()).collidepoint(leftclickpos):
							aktivfenster.remove(afenster)				
							leftclick=False				
						elif pygame.Rect(afenster.vollrect()).collidepoint(leftclickpos):
							if afenster.fensterrect==afenster.savefensterrect:
								afenster.savefensterrect.x = afenster.fensterrect.x
								afenster.savefensterrect.y = afenster.fensterrect.y
								afenster.savefensterrect.w = afenster.fensterrect.w
								afenster.savefensterrect.h = afenster.fensterrect.h						
								afenster.fensterrect.x = 4
								afenster.fensterrect.y = 44
								afenster.fensterrect.w = width-22
								afenster.fensterrect.h = height-64
							else:
								afenster.fensterrect.x = afenster.savefensterrect.x
								afenster.fensterrect.y = afenster.savefensterrect.y
								afenster.fensterrect.w = afenster.savefensterrect.w
								afenster.fensterrect.h = afenster.savefensterrect.h						
							leftclick=False				
						elif pygame.Rect(afenster.frontrect()).collidepoint(leftclickpos):
							print("To Front")
							leftclick=False				
						elif pygame.Rect(afenster.toprect()).collidepoint(leftclickpos):
							afenster.verschieben=True
							afenster.outfensterrect.x = mousepos[0]-leftclickpos[0]+afenster.fensterrect.x-4
							afenster.outfensterrect.y = mousepos[1]-leftclickpos[1]+afenster.fensterrect.y-22
								
				else:
					if afenster.verschieben:					
						afenster.fensterrect.x = afenster.outfensterrect.x+4
						afenster.fensterrect.y = afenster.outfensterrect.y+22
						afenster.verschieben=False
						leftclick=False				
					
			
#		Menue anzeige

		untermenue=0;
		
		if memtimer==0:
			freemem = psutil.virtual_memory()[1]
			memtimer = 500
		memtimer = memtimer -1

		if menuemode == 0:
			menuetext = menuefont.render(str(meldung), True, (0, 0, 0))
		elif menuemode == 1:
			tmptext = "Amiga Workbench  " + str(freemem) + " Free RAM"
			menuetext = menuefont.render(tmptext, True, (0, 0, 0))
			

		pygame.draw.rect(screen, (255,255,255), [0, 0, width, 20], 0)		
		pygame.draw.line(screen, (0,0,0), [0, 20], [width, 20], 2)	
		if menuemode==1:
			pygame.draw.line(screen, (0,0,0), [width-1, 2], [width-1, 21], 1)	
			screen.blit(menuerechtsoben,(width-22,2))


		if menuemode == 2:
			for menueeintrag in menue:
				if menueeintrag[3].split(":")[0] == "Piktogramm":
					if aktivicon == 0:
						menueeintrag[7] = False
					else:
						menueeintrag[7] = True
				if menueeintrag[3].split(":")[0] == "Fenster":
					if aktivfolder == 0:
						menueeintrag[7] = False
					else:
						menueeintrag[7] = True
				if menueeintrag[3].split(":")[0] == "disk" :
					if aktivicon == 0:
						menueeintrag[7] = False
					elif icons[aktivicon-1][1]=="disk":
						menueeintrag[7] = True
				if menueeintrag[3] == "Papierkorb leeren":
					if aktivicon == 0:
						menueeintrag[7] = False
					elif icons[aktivicon-1][1]=="trash":
						menueeintrag[7] = True





			menueposx = 4
									
			# Menue
			for menueeintrag in menue:
							
				menueposy = 2

				if menueeintrag[1] == "menue":

					menueeintragtext = menuefont.render(menueeintrag[0], True, (0, 0, 0))
					menueeintrag[4] = screen.blit(menueeintragtext,(menueposx,menueposy))
					
					if menueeintrag[4].collidepoint(mousepos):
						aktivmenue = menueeintrag[6]
						
					if aktivmenue == menueeintrag[6]:
						pygame.draw.rect(screen, (0,0,0), (menueeintrag[4].x-2,menueeintrag[4].y-2,menueeintrag[4].w+4,menueeintrag[4].h+4), 0)		
						menueeintragtext = menuefont.render(menueeintrag[0], True, (255, 255, 255))
						menueeintrag[4] = screen.blit(menueeintragtext,(menueposx,menueposy))

						aktivuntermenuerect.x = menueeintrag[4].x-2
						aktivuntermenuerect.y = menueeintrag[4].y + menueeintrag[4].h
						aktivuntermenuerect.w = 240
						aktivuntermenuerect.h = menueeintrag[5]*18+8

						# Submenue
						pygame.draw.rect(screen, (255,255,255), (aktivuntermenuerect), 0)		
						pygame.draw.rect(screen, (0,0,0), (aktivuntermenuerect), 2)		

						for submenueeintrag in menue:
							if submenueeintrag[2] == menueeintrag[0]:
								menueposy = menueposy + menueeintrag[4].h + 2
								if submenueeintrag[7]:
									menueeintragtext = menuefont.render(submenueeintrag[0], True, (0, 0, 0))
								else:
									menueeintragtext = menuefont.render(submenueeintrag[0], True, (150, 150, 150))
								submenueeintrag[4] = screen.blit(menueeintragtext,(menueposx+4,menueposy+2))
								submenueeintrag[4].w = aktivuntermenuerect.w-8

								if submenueeintrag[4].collidepoint(mousepos):
									aktivuntermenue = submenueeintrag[6]
									
								if aktivuntermenue == submenueeintrag[6] and submenueeintrag[7]:
									pygame.draw.rect(screen, (0,0,0), (submenueeintrag[4].x-2,submenueeintrag[4].y-2,submenueeintrag[4].w,submenueeintrag[4].h+4), 0)		
									menueeintragtext = menuefont.render(submenueeintrag[0], True, (255, 255, 255))
									submenueeintrag[4] = screen.blit(menueeintragtext,(menueposx+3,menueposy+1))

									if submenueeintrag[5]	 > 0:	
										aktivsubuntermenuerect.x = submenueeintrag[4].x+submenueeintrag[4].w
										aktivsubuntermenuerect.y = submenueeintrag[4].y + menueeintrag[4].h - 20
										aktivsubuntermenuerect.w = 240
										aktivsubuntermenuerect.h = submenueeintrag[5]*18+8

										# SubSubmenue
										pygame.draw.rect(screen, (255,255,255), (aktivsubuntermenuerect), 0)		
										pygame.draw.rect(screen, (0,0,0), (aktivsubuntermenuerect), 2)		

										submenueposy = aktivsubuntermenuerect.y + 4
										submenueposx = aktivsubuntermenuerect.x + 2

										for subsubmenueeintrag in menue:
											if subsubmenueeintrag[2] == submenueeintrag[0]:
												menueeintragtext = menuefont.render(subsubmenueeintrag[0], True, (0, 0, 0))
												subsubmenueeintrag[4] = screen.blit(menueeintragtext,(submenueposx+4,submenueposy+2))
												subsubmenueeintrag[4].w = aktivuntermenuerect.w-8

												if subsubmenueeintrag[4].collidepoint(mousepos):
													aktivsubuntermenue = subsubmenueeintrag[6]
													
												if aktivsubuntermenue == subsubmenueeintrag[6]:
													pygame.draw.rect(screen, (0,0,0), (subsubmenueeintrag[4].x,subsubmenueeintrag[4].y-2,subsubmenueeintrag[4].w,subsubmenueeintrag[4].h+4), 0)		
													menueeintragtext = menuefont.render(subsubmenueeintrag[0], True, (255, 255, 255))
													submenueeintrag[4] = screen.blit(menueeintragtext,(submenueposx+3,submenueposy+1))
				
												submenueposy = submenueposy + subsubmenueeintrag[4].h + 2
				
						

					menueposx = menueposx + menueeintrag[4].w + 8



			
		else:
			screen.blit(menuetext,(4,2)) 		

# Befehlsverarbeitung
		if befehl != "":
			print ("Befehl:", befehl)	
			if befehl=="Workbench verlassen":
				aktivfenster.append(fenster("janein","Workbench",pygame.Rect(5,43,200,100)))
				aktivfenster[len(aktivfenster)-1].hinweistext = ["Wollen Sie wirklich die"]				
				aktivfenster[len(aktivfenster)-1].hinweistext.append("Workbench verlassen?")
#				running=False
			elif befehl=="Letzte Meldung anzeigen":
				menuemode=0
			elif befehl=="starte:Shell":
				aktivfenster.append(fenster("shell","AmigaShell",pygame.Rect(4,120,width-22,280)))
			elif befehl=="Version Copyright":
				aktivfenster.append(fenster("hinweis","Version",pygame.Rect(10,50,200,160)))
				aktivfenster[len(aktivfenster)-1].hinweistext = ["Amigang Workbench 3.1"]
				aktivfenster[len(aktivfenster)-1].hinweistext.append("Version 0.3")
				aktivfenster[len(aktivfenster)-1].hinweistext.append("(c) 2014-2024")
				aktivfenster[len(aktivfenster)-1].hinweistext.append("by Wolfgang Schuster")



			befehl = ""
		
		pygame.display.flip()
	
	pygame.quit()
	
main()