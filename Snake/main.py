import pygame
import os
import random

pygame.font.init()

# Setup display 

WIDTH, HEIGHT = 800,800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

# offset and display variables

OFFSET = 100
CELL_LEN = 40
ROWS = int((WIDTH-OFFSET*2)/CELL_LEN)
COLUMNS = int((HEIGHT-OFFSET*2)/CELL_LEN)

# Load image

BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "BG.png")), (WIDTH,HEIGHT))
SPRITE_SHEET = pygame.image.load(os.path.join("assets", "SpriteSheet.png"))
MODEL_ALPHA = pygame.image.load(os.path.join("assets", "ModelAlpha.png"))
APPLE = pygame.transform.scale(pygame.image.load(os.path.join("assets", "Apple.png")), (CELL_LEN, CELL_LEN))

# class snake

class Snake():
	def __init__(self,x,y,len,dir,sprites):
		self.cells = []
		self.pos = pygame.math.Vector2(x,y)
		self.isGrowing = False
		self.len = len
		self.dir = dir
		self.count = 0
		self.sprites = sprites

		cell = Cell(self.pos.x,self.pos.y,len,self.dir)
		self.cells.append(cell)

	def draw(self,window):
		for i in range(len(self.cells)):
			img = self.choose_sprite(i)
			try: self.cells[i].draw(window,img)
			except: print("lose")

	def update(self):

		if self.count == 10:

			for cell in self.cells :
				if self.pos.x + self.dir.x * self.len == cell.pos.x and self.pos.y + self.dir.y * self.len == cell.pos.y:
					print("lose")
			if self.pos.x + self.dir.x * self.len < WIDTH-OFFSET and self.pos.x + self.dir.x * self.len >= 0 + OFFSET:
				self.pos.x += self.dir.x * self.len
			else:
				print("lose")
			if self.pos.y + self.dir.y * self.len < HEIGHT-OFFSET and self.pos.y + self.dir.y * self.len >= 0 + OFFSET:
				self.pos.y += self.dir.y * self.len
			else:
				print("lose")

			cell = Cell(self.pos.x,self.pos.y,self.len,self.dir)
			self.cells.append(cell)
			if self.isGrowing == False:
				self.cells.pop(0)

			self.count = 0

			self.isGrowing = False

		else:
			self.count += 1

	def control(self, keys):

		if (keys[pygame.K_z] or keys[pygame.K_UP]) and not self.dir == (0,1):
			self.dir = pygame.math.Vector2(0,-1)
		if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and not self.dir == (0,-1):
			self.dir = pygame.math.Vector2(0,1)
		if (keys[pygame.K_q] or keys[pygame.K_LEFT]) and not self.dir == (1,0):
			self.dir = pygame.math.Vector2(-1,0)
		if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and not self.dir == (-1,0):
			self.dir = pygame.math.Vector2(1,0)

	def choose_sprite(self,index):

		# head 

		if index == len(self.cells)-1:
			if self.cells[index].dir == (0,1):
				return self.sprites[9]
			elif self.cells[index].dir == (0,-1):
				return self.sprites[3]
			elif self.cells[index].dir == (1,0):
				return self.sprites[4]
			elif self.cells[index].dir == (-1,0):
				return self.sprites[8]

		# tail

		elif index == 0:
			if self.cells[index].pos.x > self.cells[index+1].pos.x:    # tail go to left
				return self.sprites[18]
			elif self.cells[index].pos.x < self.cells[index+1].pos.x:  # tail go to right
				return self.sprites[14]
			elif self.cells[index].pos.y > self.cells[index+1].pos.y:  # tail go to up
				return self.sprites[13]
			elif self.cells[index].pos.y < self.cells[index+1].pos.y:  # tail go to down
				return self.sprites[19]

		# body right

		elif self.cells[index-1].pos.x == self.cells[index+1].pos.x:
			return self.sprites[7]
		elif self.cells[index-1].pos.y == self.cells[index+1].pos.y:
			return self.sprites[1]

		# body curve

		elif self.cells[index-1].pos.x == self.cells[index].pos.x + CELL_LEN: 	# la case d'avant est à droite 
			if self.cells[index+1].pos.y == self.cells[index].pos.y + CELL_LEN: # la case d'après est en bas
				return self.sprites[0]
			else: 																# la case d'après est en haut
				return self.sprites[5]
		elif self.cells[index-1].pos.x == self.cells[index].pos.x - CELL_LEN: 	# la case d'avant est à gauche
			if self.cells[index+1].pos.y == self.cells[index].pos.y + CELL_LEN: # la case d'après est en bas
				return self.sprites[2]
			else: 																# la case d'après est en haut
				return self.sprites[12]
		elif self.cells[index-1].pos.y == self.cells[index].pos.y - CELL_LEN:	# la case d'avant est en haut
			if self.cells[index+1].pos.x == self.cells[index].pos.x + CELL_LEN: # la case d'après est à droite
				return self.sprites[5]
			else:																# la case d'après est à gauche
				return self.sprites[12]
		elif self.cells[index-1].pos.y == self.cells[index].pos.y + CELL_LEN:	# la case d'avant est en bas
			if self.cells[index+1].pos.x == self.cells[index].pos.x + CELL_LEN: # la case d'après est à droite
				return self.sprites[0]
			else:																# la case d'après est à gauche
				return self.sprites[2]							

# class cell

class Cell():
	def __init__(self,x,y,len,dir):
		self.pos = pygame.math.Vector2(x,y)
		self.len = len
		self.dir = dir

	def draw(self,window,img):
		window.blit(img, (self.pos.x,self.pos.y))

# class apple

class Apple():
	def __init__(self,x,y,len,img):
		self.pos = pygame.math.Vector2(x,y)
		self.len = len
		self.img = img

	def draw(self,window):
		window.blit(self.img, (self.pos.x,self.pos.y))

	def set_pos(self,x,y):
		self.pos = pygame.math.Vector2(x,y)

# Main 

def main():

	# Display variables

	run = True

	# framerate et clock

	FPS = 60
	clock = pygame.time.Clock()

	# game variable

	score = 0
	best = 0

	# create font 

	main_font = pygame.font.SysFont("comicsans", 50)

	# create sprite array

	SPRITE_COLUMNS = int(SPRITE_SHEET.get_width() / 64)
	SPRITE_ROWS = int(SPRITE_SHEET.get_height() / 64)

	snake_sprites = []

	for i in range(SPRITE_COLUMNS+1):
		for j in range(SPRITE_ROWS+1):

			x = j *64
			y = i *64 

			sprite = MODEL_ALPHA.copy()
			sprite.blit(SPRITE_SHEET,(-x,-y))
			sprite = pygame.transform.scale(sprite,(CELL_LEN,CELL_LEN))

			snake_sprites.append(sprite)

	# Create snake

	snake = Snake(int(COLUMNS/2)*CELL_LEN + OFFSET,int(ROWS/2)*CELL_LEN + OFFSET, CELL_LEN, pygame.math.Vector2(0,1), snake_sprites)

	# create apple

	x = random.randint(0,COLUMNS-1) * CELL_LEN + OFFSET
	y = random.randint(0,ROWS-1) * CELL_LEN + OFFSET

	apple = Apple(x,y,CELL_LEN,APPLE)

	# Draw function

	def draw():

		# Draw Background

		WIN.blit(BG,(0,0))

		# Draw chessboard

		for i in range(ROWS):
			for j in range(COLUMNS):

				if (i+j) % 2 == 0:
					cell_color = (20,190,70)
				else:
					cell_color = (130,210,35)

				x = j * CELL_LEN + OFFSET
				y = i * CELL_LEN + OFFSET

				pygame.draw.rect(WIN, cell_color,(x,y,CELL_LEN,CELL_LEN))

		# Draw text

		score_label = main_font.render(f"Score : {score}", 1, (0,0,0))
		best_label = main_font.render(f"Best : {best}", 1, (0,0,0))

		WIN.blit(score_label, (20,20))
		WIN.blit(best_label, (WIDTH-20-best_label.get_width(),20))

		#draw snake

		snake.draw(WIN)

		# draw apple 
			
		apple.draw(WIN)

		pygame.display.update()

	# update function 

	def update():


		nonlocal score
		nonlocal apple
		# update snake

		snake.update()

		if apple.pos.x == snake.pos.x and apple.pos.y == snake.pos.y:
			snake.isGrowing = True
			score += 1

			x = random.randint(0,COLUMNS-1) * CELL_LEN + OFFSET
			y = random.randint(0,ROWS-1) * CELL_LEN + OFFSET

			apple.set_pos(x,y)

	while run:
		clock.tick(FPS)

		draw()
		update()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		keys = pygame.key.get_pressed()
		if keys[pygame.K_ESCAPE]:
			run = False
		snake.control(keys)

# Run main function

main()
