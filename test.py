#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pygame

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
		icon = pygame.Surface((self.image.get_width()+10,self.image.get_height()+10))
		icon.fill((170, 170, 170))
		if self.clicked:
			pygame.draw.line(icon, (255,255,255), [icon.get_width()-1,0], [icon.get_width()-1,icon.get_height()-1], 1)
			pygame.draw.line(icon, (255,255,255), [0, icon.get_height()-1], [icon.get_width()-1,icon.get_height()-1], 1)
			pygame.draw.line(icon, (0,0,0), [0, 0], [icon.get_width()-1,0], 1)
			pygame.draw.line(icon, (0,0,0), [0, 0], [0,icon.get_height()-1], 1)
			icon.blit(self.image,(5,5))
		else:		
			pygame.draw.line(icon, (0,0,0), [icon.get_width()-1,0], [icon.get_width()-1,icon.get_height()-1], 1)
			pygame.draw.line(icon, (0,0,0), [0, icon.get_height()-1], [icon.get_width()-1,icon.get_height()-1], 1)
			pygame.draw.line(icon, (255,255,255), [0, 0], [icon.get_width()-1,0], 1)
			pygame.draw.line(icon, (255,255,255), [0, 0], [0,icon.get_height()-1], 1)
			icon.blit(self.image2,(5,5))
			
		self.surface.blit(icon, pos)
		return(icon)

	
hd1_image = pygame.image.load("images/hd1.png")
hd2_image = pygame.image.load("images/hd2.png")

def main():

	menueaktion = ""

	screen = pygame.display.set_mode([width, height])
	
	pygame.display.set_caption("Amigang Workbench 3.1")
	pygame.mouse.set_visible(1)

	dh0_icon = icon("DH0:", "hd", screen, "dir:/home/wolf", hd1_image, hd2_image)	

		
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


		if menueaktion != "":
			if menueaktion == "ESC":
				running = False
			menueaktion = ""
						
		screen.fill((170, 170, 170))

		dh0_icon.ausgabe((20,20))
		
		pygame.display.flip()
	
	pygame.quit()
	
main()