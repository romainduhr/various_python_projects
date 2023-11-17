import pygame 
import math

WIDTH,HEIGHT = 800,800
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("path")

path = [(398, 237), (436, 256), (473, 304), (479, 365), (474, 402), (438, 416), (389, 426), (330, 407), (309, 373), (276, 333), (263, 294), (312, 263), (372, 242), (399, 237)]
current_path = 0

x,y = 0,0
speed = 8
pos = []

def main():
	run = True
	FPS = 60
	clock = pygame.time.Clock()

	def update():
		global current_path
		global x,y
		global speed
		
		pathX,pathY = path[current_path][0],path[current_path][1]
		velX, velY = pathX - x, pathY - y
		vel_len = math.sqrt(velX ** 2 + velY **2)
		if vel_len < 10:
			current_path += 1
			if current_path >= len(path):
				current_path = 0

		if not vel_len == 0:
			velX,velY = velX/vel_len, velY/vel_len
		
		newX,newY = x + velX*speed, y + velY*speed
		x,y = newX,newY

	def draw():
		WIN.fill((255,255,255))

		pygame.draw.rect(WIN, (255,0,0), (x,y,20,20))

		pygame.display.update()
		update()


	while run:
		clock.tick(FPS)

		draw()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouseX,mouseY = pygame.mouse.get_pos()
				pos.append((mouseX,mouseY))

	print(pos)
main()

