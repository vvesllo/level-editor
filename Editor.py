import UI
import Vector
import Tile
import pygame
from tkinter import filedialog

class Editor:
	def __init__(self, width, height, title):
		pygame.init()
		self.window_width = width
		self.window_height = height
		self.is_program_run = True
		self.show_menu = True
		self.speed = 20
		self.cell_size = 64
		self.tileset = pygame.image.load("tileset.png")
		self.values = {
			"show_grid": True
		}

		self.FPS = 60
		self.MAX_COLS = 150
		self.MAX_ROWS = 100


		self.scroll = Vector.Vec2(0, 0)

		self.grid_color = pygame.Color(0xff, 0xff, 0xff, 0x10)

		self.tiles = []
		self.tile_list = [
			Tile.Tile(
				self.tileset,
				(0, 0, self.cell_size, self.cell_size),
				Vector.Vec2(0, 0)
			),
			Tile.Tile(
				self.tileset,
				(self.cell_size, 0, self.cell_size, self.cell_size),
				Vector.Vec2(0, 0)
			),
			Tile.Tile(
				self.tileset,
				(0, self.cell_size, self.cell_size, self.cell_size),
				Vector.Vec2(0, 0)
			),
			Tile.Tile(
				self.tileset,
				(self.cell_size, self.cell_size, self.cell_size, self.cell_size),
				Vector.Vec2(0, 0)
			)
		]
		
		for row in range(self.MAX_ROWS):
			r = [-1] * self.MAX_COLS
			self.tiles.append(r)

		for tile in range(0, self.MAX_COLS):
			self.tiles[self.MAX_ROWS - 1][tile] = 0


		self.initWindow(
			self.window_width,
			self.window_height, 
			title
		)
	
		self.__ui_elements = (
			UI.UIButton(
				"Exit",
				Vector.Vec2(10, 10),
				Vector.Vec2(110, 40),
				self.endProgram
			),
			UI.UIButton(
				"Hello world",
				Vector.Vec2(10, 55),
				Vector.Vec2(110, 40),
				lambda: ("Hello world")
			),
			UI.UICheckBox(
				"Show grid",
				Vector.Vec2(110+15, 10),
				Vector.Vec2(110, 40),
				"show_grid",
				self.values["show_grid"]
			)
		)

		self.clock = pygame.time.Clock()

	def initWindow(self, width, height, title):
		self.window = pygame.display.set_mode(
			(width, height)
		)
		pygame.display.set_caption(title)
		self.window_width = width
		self.window_height = height

	def update(self):
		for ui_element in self.__ui_elements:
			if isinstance(ui_element, UI.UIButton) or \
				isinstance(ui_element, UI.UICheckBox):
				ui_element.checkHover(pygame.mouse.get_pos())

			ui_element.update()
		
		mouse_position = pygame.mouse.get_pos()
		b1, _, b3 = pygame.mouse.get_pressed()

		pos = pygame.mouse.get_pos()
		mouse_col = (pos[0] + self.scroll.x) // self.cell_size
		mouse_row = (pos[1] + self.scroll.y) // self.cell_size

		mouse_col = int(mouse_col)
		mouse_row = int(mouse_row)

		if mouse_position[0] > 0 and mouse_position[0] < self.window_width and\
			mouse_position[1] > 0 and mouse_position[1] < self.window_height:
			if b1:
				self.tiles[mouse_row][mouse_col] = (
					Tile.Tile(
						pygame.image.load("tileset.png"),
						(0, 0, self.cell_size, self.cell_size),
						Vector.Vec2(mouse_col*self.cell_size, mouse_row*self.cell_size)
					)
				)
			elif b3:
				self.tiles[mouse_row][mouse_col] = None

		pygame.display.flip()

	def drawGrid(self):
		for c in range(self.MAX_COLS + 1):
			pygame.draw.line(
				self.window,
				self.grid_color,
				(c * self.cell_size - self.scroll.x, 0),
				(c * self.cell_size - self.scroll.x, self.window_height),
				2
			)
		for c in range(self.MAX_ROWS + 1):
			pygame.draw.line(
				self.window,
				self.grid_color,
				(0, c * self.cell_size - self.scroll.y),
				(self.window_width, c * self.cell_size - self.scroll.y),
				2
			)

	def draw(self):
		# background color
		self.window.fill(pygame.Color(0x1A, 0x1A, 0x20))
		
		if self.values["show_grid"]:
			self.drawGrid()

		for y, row in enumerate(self.tiles):
			for x, tile in enumerate(row):
				if isinstance(tile, Tile.Tile):
					self.window.blit(
						tile.getSurface(),
						(x * self.cell_size - self.scroll.x, y * self.cell_size - self.scroll.y)
					)

		if self.show_menu:
			for ui_element in self.__ui_elements:
				self.window.blit(
					ui_element.getSurface(),
					ui_element.getPosition().get()
				)
		pygame.display.update()

	def checkEvents(self):
		for event in pygame.event.get():
			match event.type:
				case pygame.QUIT:
					self.is_program_run = False
					break
				case pygame.KEYDOWN:
					if event.key == pygame.K_TAB:
						self.show_menu = not self.show_menu

					break
				case pygame.MOUSEBUTTONDOWN:
					if not self.show_menu:
						break
					b1, _, _ = pygame.mouse.get_pressed()
					for ui_element in self.__ui_elements:
						if isinstance(ui_element, UI.UIButton):
							if ui_element.isHovered():
								print(ui_element.click(b1))
						elif isinstance(ui_element, UI.UICheckBox):
							if ui_element.isHovered():
								self.values[ui_element.getKey()] = ui_element.click(b1)
					break

	def checkKeys(self):
		pressed_keys = pygame.key.get_pressed()
		if pressed_keys[pygame.K_a]:
			if self.scroll.x > 0:
				self.scroll.x -= self.speed
		if pressed_keys[pygame.K_d]:
			if self.scroll.x < self.MAX_COLS * self.cell_size - (self.window_width / self.cell_size) * self.cell_size:
				self.scroll.x += self.speed

		if pressed_keys[pygame.K_w]:
			if self.scroll.y > 0:
				self.scroll.y -= self.speed
		if pressed_keys[pygame.K_s]:
			if self.scroll.y < self.MAX_ROWS * self.cell_size - (self.window_height / self.cell_size) * self.cell_size:
				self.scroll.y += self.speed

		

	def run(self):
		while self.is_program_run:
			self.clock.tick(self.FPS) # frame rate
			self.checkEvents()
			self.checkKeys()
			self.update()
			self.draw()
			
	



	# other
	# other
	# other
	# other
	# other

	def openFile(self):
		return (
			self.ask_filepath_to_open(
				(
					('All Files', '*.*'),
					('Level Colliders File', '*.lcf'),
					('Level Decoration File', '*.ldf'),
					('Text Document', '*.txt')
				),
			"*.*")
		)
	def askFilepathToOpen(self, filetypes, default_extension):
		return filedialog.askopenfilename(
			filetypes=filetypes,
			defaultextension=default_extension
		)

	def endProgram(self):
		self.is_program_run = False
		return True