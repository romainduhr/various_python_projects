import pygame

WHITE = 0xFFFFFF
GREY = 0x464745
RED = 0xFF0202
GREEN = 0x27FF00
LIGHT_BLUE = 0x00FFF0
DARK_BLUE = 0x0004FF
YELLOW = 0xFFF700

COLS,ROWS = 20,20

class Cell():
	def __init__(self,x,y,len):
		self.pos = pygame.math.Vector2(x,y)
		self.len = len
		self.owner = None
		self.color = WHITE
		self.h_cost = 0
		self.g_cost = 0
		self.f_cost = 0
		self.is_visited = False
		self.is_check = False
		self.last = None

	def set_color(self):
		if self.owner == "source":
			self.color = GREEN
		elif self.owner == "target":
			self.color = RED
		elif self.is_visited:
			self.color = DARK_BLUE
		elif self.is_check:
			self.color = LIGHT_BLUE
		if self.owner == "barrier":
			self.color = GREY	
		if self.owner == "path" :
			self.color == YELLOW

	def draw(self,window,font):
		self.set_color()

		# draw rect
		x,y = self.pos.x,self.pos.y
		len = self.len
		pygame.draw.rect(window,self.color,(x,y,x+len,y+len))
		if self.owner == "path":
			pygame.draw.rect(window,YELLOW,(x,y,x+len,y+len))
		pygame.draw.lines(window,(0,0,0), True, [(x,y),(x+len,y),(x+len,y+len),(x,y+len)], width = 5)

		# draw text
		# if not self.owner and self.is_check:
		# 	g_cost_label = font.render(f"{self.g_cost}", 1, (0,0,0))
		# 	window.blit(g_cost_label, (x + len - g_cost_label.get_width()- 5,y + 5))

		# 	h_cost_label = font.render(f"{self.h_cost}", 1, (0,0,0))
		# 	window.blit(h_cost_label, (x + 5,y + 5))

		# 	f_cost_label = font.render(f"{self.f_cost}", 1, (0,0,0))
		# 	window.blit(f_cost_label, (x + len/2 - f_cost_label.get_width()/2,y + len/2 - f_cost_label.get_height()/2))

	def visit(self,cells,to_visits):

		index = cells.index(self)
		
		cell = self.check_left(index,cells)
		if not cell == None:
			to_visits[cell] = cell.f_cost
		cell = self.check_right(index,cells)
		if not cell == None:
			to_visits[cell] = cell.f_cost
		cell = self.check_up(index,cells)
		if not cell == None:
			to_visits[cell] = cell.f_cost
		cell = self.check_down(index,cells)
		if not cell == None:
			to_visits[cell] = cell.f_cost


		self.is_visited = True

	def check_left(self,index,cells):

		if not index % COLS == 0 and not cells[index-1].owner == "barrier":
			if (cells[index - 1].h_cost > self.h_cost + 1 or cells[index-1].h_cost == 0):
				cells[index - 1].h_cost = self.h_cost + 1
				cells[index - 1].update(self)
				cells[index - 1].is_check = True
				return cells[index - 1]

	def check_right(self,index,cells):

		if not (index + 1) % COLS == 0 and not cells[index+1].owner == "barrier":
			if (cells[index + 1].h_cost > self.h_cost + 1 or cells[index+1].h_cost == 0): 
				cells[index + 1].h_cost = self.h_cost + 1
				cells[index + 1].update(self)
				cells[index+1].is_check = True
				return cells[index + 1]

	def check_up(self,index,cells):

		if index - COLS >= 0 and not cells[index-COLS].owner == "barrier": 
			if (cells[index - COLS].h_cost > self.h_cost + 1 or cells[index - COLS].h_cost == 0):
				cells[index - COLS].h_cost = self.h_cost + 1
				cells[index - COLS].update(self)
				cells[index-COLS].is_check = True
				return cells[index - COLS]

	def check_down(self,index,cells):
		if index + COLS < COLS**2 and not cells[index+COLS].owner == "barrier":
			if (cells[index + COLS].h_cost > self.h_cost + 1  or cells[index + COLS].h_cost == 0):
				cells[index + COLS].h_cost = self.h_cost + 1
				cells[index + COLS].update(self)
				cells[index + COLS].is_check = True
				return cells[index + COLS]

	def update(self,last):
		self.f_cost = self.g_cost + self.h_cost
		self.last = last

	def set_in_path(self):
		self.set_owner("path")
		if not self.last.owner == "source":
			self.last.set_in_path()

	def set_owner(self,owner):
		self.owner = owner