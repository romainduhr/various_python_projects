import pygame
import os
import random

# Load image
SPRITE_SHEET = pygame.image.load(os.path.join("assets", "Tiles.png"))
ALPHA_MODEL = pygame.image.load(os.path.join("assets", "alpha.png"))
MASK = pygame.image.load(os.path.join("assets", "tile_mask.png"))

class Tile():
	def __init__(self,x,y,width,height):
		self.width = width
		self.height = height
		self.pos = pygame.math.Vector2(x,y)
		self.imgs = []
		self.img_state = 3
		self.select = False
		self.mask = pygame.transform.scale(MASK, (self.width,self.height))

		self.init_img()
		self.select_img = self.imgs[0]
		self.imgs.pop(3)
		self.imgs.pop(1)
		self.imgs.pop(0)

	def init_img(self):

		SPRITE_COLUMNS = int(SPRITE_SHEET.get_width() // 40)
		SPRITE_ROWS = int(SPRITE_SHEET.get_height() // 30)
		for i in range(SPRITE_ROWS):
			for j in range(SPRITE_COLUMNS):

				x = j * 40
				y = i * 40
				sprite = ALPHA_MODEL.copy()
				sprite.blit(SPRITE_SHEET,(-x,-y + 20))
				sprite = pygame.transform.scale(sprite,(self.width,self.height*2))
				self.imgs.append(sprite) 
				
	def draw(self,window):
		img = self.imgs[self.img_state % len(self.imgs)]
		window.blit(img,(self.pos.x,self.pos.y - self.height))
		if self.select:
			img = self.select_img
			window.blit(img,(self.pos.x,self.pos.y - self.height))




