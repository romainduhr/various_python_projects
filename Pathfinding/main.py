import pygame
import math
from cell import Cell

pygame.font.init()

WIDTH,HEIGHT = 1000,1000
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Path Finding")

def main():

	run = True
	FPS = 60
	clock = pygame.time.Clock()
	cells = []
	main_font = pygame.font.SysFont("comicsans",35)
	play = False

	# create grid

	CELL_LEN = 50
	COL,ROWS = int(WIDTH/CELL_LEN), int(HEIGHT/CELL_LEN)

	for i in range(ROWS):
		for j in range(COL):

			x = j*CELL_LEN
			y = i*CELL_LEN

			cell = Cell(x,y,CELL_LEN)
			cells.append(cell)

	# create source,target,barrier,void_cell

	source = cells[52]
	source.owner = "source"
	target = cells[14]
	target.owner = "target"
	barriers = []
	void_cells = []
	for barrier in barriers: 
		barrier.owner = "barrier"

	for cell in cells:
		if not cell == source and not cell == target and not cell in barriers:
			void_cells.append(cell)

	# define every h_cost

	for void_cell in void_cells:
		dist = (abs(void_cell.pos.x-target.pos.x)/CELL_LEN, abs(void_cell.pos.y-target.pos.y)/CELL_LEN)
		g_cost = int(dist[0]+dist[1])
		void_cell.g_cost = g_cost

	# dictionnary of all cost

	to_visits = {source : 0}
	to_visits_sorted = [[source,0]]
	successfull_cell = None

	def mouse_pos(pos):
		return pos[0] // CELL_LEN, pos[1] // CELL_LEN

	def update():
		nonlocal to_visits
		nonlocal to_visits_sorted
		nonlocal successfull_cell
		for cell in to_visits_sorted:
			to_visits[cell[0]] = cell[1]
		# visit source
		if len(to_visits_sorted) > 0:
			to_visit = to_visits_sorted[0]
			del to_visits[to_visit[0]]
			to_visit[0].visit(cells,to_visits)
			if target in to_visits.keys():
				to_visits.clear()
				successfull_cell = to_visit[0]
			to_visits_sorted = sorted(to_visits.items(), key=lambda t: t[1])
		else : 
			successfull_cell.set_in_path()

	def draw():

		# draw cell

		for cell in cells:
			cell.draw(WIN,main_font)

		pygame.display.update()

	while run:

		clock.tick(FPS)

		draw()
		if play:
			update()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouseX,mouseY = mouse_pos(pygame.mouse.get_pos())
				index = mouseX+mouseY*COL
				barriers.append(cells[index])
				cells[index].set_owner("barrier")
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and not play:
					play = True

main()