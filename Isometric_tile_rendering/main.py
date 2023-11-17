import pygame 
import os
from tile import Tile

# Setup display

WIDTH = 1200
HEIGHT = 800
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Isometric")

def main():
	run = True 
	clock = pygame.time.Clock()
	FPS = 60
	tiles = []
	TILE_WIDTH,TILE_HEIGHT = 120,60 # !ratio 1/2
	COLS = 25
	ROWS = 25
	Y_OFFSET = -WIDTH/4
	mouseX,mouseY = 0,0
	selected_tile = None

	# Create tiles 
	for i in range(ROWS):
		for j in range(COLS):
			x = WIDTH/2 - TILE_WIDTH/2 + (j-i)*TILE_WIDTH/2
			y = Y_OFFSET + (j+i)*TILE_HEIGHT/2
			tile = Tile(x,y,TILE_WIDTH,TILE_HEIGHT)
			tiles.append(tile)

	def update():
		nonlocal selected_tile 
		selected_tile = None
		mouseX,mouseY = pygame.mouse.get_pos()
		for tile in tiles:
			if not selected_tile and mouseX > tile.pos.x and mouseX < tile.pos.x + tile.width and mouseY > tile.pos.y and mouseY < tile.pos.y + tile.height:
				x_offset = int(mouseX - tile.pos.x)
				y_offset = int(mouseY - tile.pos.y)
				if tile.mask.get_at((x_offset,y_offset))[3] == 255:
					tile.select = True
					selected_tile = tile
				else:
					tile.select = False
			else:
				tile.select = False
	def draw():
		# clear background
		WIN.fill((255,255,255))

		# Draw tiles
		for tile in tiles:
			tile.draw(WIN)

		pygame.display.update()
		update()

	while run:

		clock.tick(FPS)

		draw()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				selected_tile.img_state += 1

main()