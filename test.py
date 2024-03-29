#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pygame
import time

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

width = 800
height = 600

if not pygame.font: print('Fehler pygame.font Modul konnte nicht geladen werden!')
font = pygame.font.Font("fonts/AmigaTopaz.ttf", 15)

class icon:
	def __init__(self, name, typ, surface, befehl, image, image2):
		self.typ = typ		
		self.name = name		
		self.surface = surface		
		self.pos = (0,0) 		
		self.befehl = befehl
		self.image = image 
		self.image2 = image2
		self.clicked = False
		self.rect = pygame.Rect(0,0,0,0)
		
	def ausgabe(self, pos):
		self.pos = pos
		icon = pygame.Surface((self.image.get_width()+10,self.image.get_height()+6))
		icon.fill((170, 170, 170))
		if self.clicked:
			pygame.draw.line(icon, (255,255,255), [icon.get_width()-1,0], [icon.get_width()-1,icon.get_height()-1], 1)
			pygame.draw.line(icon, (255,255,255), [0, icon.get_height()-2], [icon.get_width()-1,icon.get_height()-2], 2)
			pygame.draw.line(icon, (0,0,0), [0, 0], [icon.get_width()-1,0], 2)
			pygame.draw.line(icon, (0,0,0), [0, 0], [0,icon.get_height()-1], 1)
			icon.blit(self.image,(5,5))
		else:		
			pygame.draw.line(icon, (0,0,0), [icon.get_width()-1,0], [icon.get_width()-1,icon.get_height()-1], 1)
			pygame.draw.line(icon, (0,0,0), [0, icon.get_height()-2], [icon.get_width()-1,icon.get_height()-2], 2)
			pygame.draw.line(icon, (255,255,255), [0, 0], [icon.get_width()-1,0], 2)
			pygame.draw.line(icon, (255,255,255), [0, 0], [0,icon.get_height()-1], 1)
			icon.blit(self.image2,(5,3))
			
		self.surface.blit(icon, pos)
		return(icon)
		
	def checkclicked(self,mousepos):
		fensterpos = (100,100)  # Debug
		if self.rect.collidepoint((mousepos[0]-fensterpos[0]-self.pos[0],mousepos[1]-fensterpos[1]-self.pos[1])):
			self.clicked=True
		else:
			self.clicked=False

	
def main():

	menueaktion = ""

	screen = pygame.display.set_mode([width, height])
	
	pygame.display.set_caption("Amigang Workbench 3.1")
	pygame.mouse.set_visible(1)


	fensterpos=(100,100)
	fenster = pygame.Surface((160,200))
	fenster.fill((170, 170, 170))
	pygame.draw.rect(fenster, (0,0,0), (fenster.get_rect()), 1)	
	
	leftclickpos = (0,0)
	leftdoppelclick=False
	lastleftclick = time.time()	

	dh0_icon = icon("DH0:", "hd", fenster, "dir:/home/wolf", pygame.image.load("images/hd2.png"), pygame.image.load("images/hd1.png"))
	dh1_icon = icon("DH1:", "hd", fenster, "dir:/home/wolf", pygame.image.load("images/hd2.png"), pygame.image.load("images/hd1.png"))
		
	running = True
	while running:

		mousepos = pygame.mouse.get_pos()
	
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

# Maus

			elif event.type == pygame.MOUSEBUTTONUP:
				if event.button==1:
					leftclick = False
				if event.button==3:
					rightclick = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button==1:
					leftclick = True
					leftclickpos = mousepos
					if time.time()-lastleftclick < 0.2:
						leftdoppelclick=True
					else:
						leftdoppelclick=False
					lastleftclick = time.time()

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

		if menueaktion != "":
			if menueaktion == "ESC":
				running = False
			menueaktion = ""

						
		screen.fill((170, 170, 170))

		screen.blit(fenster, fensterpos)
				
		dh0_icon.rect = dh0_icon.ausgabe((20,20)).get_rect()
		dh1_icon.rect = dh1_icon.ausgabe((20,100)).get_rect()
		
		dh0_icon.checkclicked(leftclickpos)
		dh1_icon.checkclicked(leftclickpos)

#		if dh0_icon.rect.collidepoint((leftclickpos[0]-dh0_icon.pos[0]-fensterpos[0],leftclickpos[1]-dh0_icon.pos[1]-fensterpos[1])):
#			dh0_icon.clicked=True
#		else:
#			dh0_icon.clicked=False
#
#		if dh1_icon.rect.collidepoint((leftclickpos[0]-dh1_icon.pos[0]-fensterpos[0],leftclickpos[1]-dh1_icon.pos[1]-fensterpos[1])):
#			dh1_icon.clicked=True
#		else:
#			dh1_icon.clicked=False

#		dh0_icon.rect=dh0_icon.ausgabe((20,20))
#		print(dh0_icon.rect.get_rect())
		
		pygame.display.flip()
	
	pygame.quit()
	
main()