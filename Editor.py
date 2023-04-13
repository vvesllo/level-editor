import UI
import Vector
import Tile
import Utilities

import pygame
import csv

class Editor:
	def __init__(self, width, height, title):
		pygame.init()
		self.window_width = width
		self.window_height = height
		self.is_program_run = True
		self.show_menu = True
		self.speed = 20
		self.cell_size = 64
		self.mouse_button_down = False
		self.tileset = pygame.image.load("tileset.png")
		self.values = {
			"show_grid": True
		}

		self.FPS = 60
		self.MAX_COLS = 150
		self.MAX_ROWS = 100


		self.scroll = Vector.Vec2(0, 0)
		self.grid_color = pygame.Color(0x59, 0x59, 0x5e)
		self.grid_width = 4

		self.current_tile = 0
		self.tiles = []
		self.tiles_textures_list = [
			Tile.Tile(
				self.tileset,
				(0, 0, self.cell_size, self.cell_size),
				Vector.Vec2(0, 0),
				True,
				Tile.TileTypeEnum.DEFAULT
			),
			Tile.Tile(
				self.tileset,
				(self.cell_size, 0, self.cell_size, self.cell_size),
				Vector.Vec2(0, 0),
				True,
				Tile.TileTypeEnum.DEFAULT
			),
			Tile.Tile(
				self.tileset,
				(0, self.cell_size, self.cell_size, self.cell_size),
				Vector.Vec2(0, 0),
				False,
				Tile.TileTypeEnum.DEFAULT
			),
			Tile.Tile(
				self.tileset,
				(self.cell_size, self.cell_size, self.cell_size, self.cell_size),
				Vector.Vec2(0, 0),
				False,
				Tile.TileTypeEnum.DEFAULT
			),
			Tile.Tile(
				self.tileset,
				(self.cell_size*2, 0, self.cell_size, self.cell_size),
				Vector.Vec2(0, 0),
				True,
				Tile.TileTypeEnum.END
			),
			Tile.Tile(
				self.tileset,
				(self.cell_size*2, self.cell_size, self.cell_size, self.cell_size),
				Vector.Vec2(0, 0),
				True,
				Tile.TileTypeEnum.JUMPER
			),

			Tile.Tile(
				self.tileset,
				(0, self.cell_size*2, self.cell_size, self.cell_size),
				Vector.Vec2(0, 0),
				False,
				Tile.TileTypeEnum.DANGER
			),
			Tile.Tile(
				self.tileset,
				(self.cell_size, self.cell_size*2, self.cell_size, self.cell_size),
				Vector.Vec2(0, 0),
				False,
				Tile.TileTypeEnum.PLAYER
			)
		]

		self.tile_list = list(zip(
			[i for i in range(len(self.tiles_textures_list))],
			self.tiles_textures_list
		))

		self.createEnptyMap()

		self.initWindow(
			self.window_width,
			self.window_height, 
			title
		)
	
		self.__ui_elements = [
			UI.UIButton(
				"Exit",
				Vector.Vec2(10, 10),
				Vector.Vec2(110, 40),
				self.endProgram
			),
			UI.UIButton(
				"Save file",
				Vector.Vec2(10, 55),
				Vector.Vec2(110, 40),
				self.saveFile
			),
			UI.UIButton(
				"Open file",
				Vector.Vec2(10, 100),
				Vector.Vec2(110, 40),
				self.openFile
			),
			UI.UICheckBox(
				"Show grid",
				Vector.Vec2(110+15, 10),
				Vector.Vec2(110, 40),
				"show_grid",
				self.values["show_grid"]
			)
		]
		help_text = """\
[HELP]
WASD-camera control
F1-previous tile
F2-next tile
Tab-hide menu""".split('\n')
		for i in range(len(help_text)):
			self.__ui_elements.append(
				UI.UILabel(
					help_text[i],
					Vector.Vec2(self.window_width-220-5, 40*i+10),
					Vector.Vec2(220, 40)
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

	def createEnptyMap(self):
		for row in range(self.MAX_ROWS):
			r = [None] * self.MAX_COLS
			self.tiles.append(r)


	def update(self):
		for ui_element in self.__ui_elements:
			if isinstance(ui_element, UI.UIButton) or \
				isinstance(ui_element, UI.UICheckBox):
				ui_element.checkHover(pygame.mouse.get_pos())

			ui_element.update()
		

		if self.mouse_button_down:
			mouse_position = pygame.mouse.get_pos()
			left_button, middle_button, right_button = pygame.mouse.get_pressed()
			pos = pygame.mouse.get_pos()
			mouse_col = int((pos[0] + self.scroll.x) // self.cell_size)
			mouse_row = int((pos[1] + self.scroll.y) // self.cell_size)

			if mouse_position[0] > 0 and mouse_position[0] < self.window_width and\
				mouse_position[1] > 0 and mouse_position[1] < self.window_height:
				if left_button:
					self.tiles[mouse_row][mouse_col] = self.tile_list[self.current_tile]
				elif right_button:
					self.tiles[mouse_row][mouse_col] = None

		pygame.display.flip()

	def drawGrid(self):
		for c in range(self.MAX_COLS + 1):
			pygame.draw.line(
				self.window,
				self.grid_color,
				(c * self.cell_size - self.scroll.x, 0),
				(c * self.cell_size - self.scroll.x, self.window_height),
				self.grid_width
			)
		for c in range(self.MAX_ROWS + 1):
			pygame.draw.line(
				self.window,
				self.grid_color,
				(0, c * self.cell_size - self.scroll.y),
				(self.window_width, c * self.cell_size - self.scroll.y),
				self.grid_width
			)

	def draw(self):
		# background color
		self.window.fill(pygame.Color(0x1A, 0x1A, 0x20))
		
		if self.values["show_grid"]: self.drawGrid()

		for y, row in enumerate(self.tiles):
			for x, tile in enumerate(row):
				if tile:
					self.window.blit(
						tile[1].getSurface(),
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
					if event.key == pygame.K_F1:
						if self.current_tile > 0:
							self.current_tile -= 1
					if event.key == pygame.K_F2:
						if self.current_tile < len(self.tile_list)-1:
							self.current_tile += 1

					break
				case pygame.MOUSEBUTTONUP:
					self.mouse_button_down = False
					break
				case pygame.MOUSEBUTTONDOWN:
					self.mouse_button_down = True
					if not self.show_menu:
						break
					left_button, _, _ = pygame.mouse.get_pressed()
					for ui_element in self.__ui_elements:
						if isinstance(ui_element, UI.UIButton):
							if ui_element.isHovered():
								print(ui_element.click(left_button))
						elif isinstance(ui_element, UI.UICheckBox):
							if ui_element.isHovered():
								self.values[ui_element.getKey()] = ui_element.click(left_button)
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



	def saveFile(self):
		"""Save type: 
			layer1;position_x1;position_y1;texture_rect_x1;texture_rect_y1;texture_rect_w1;texture_rect_h1;is_solid1;type1;tile_index1
			layer2;position_x2;position_y2;texture_rect_x2;texture_rect_y2;texture_rect_w2;texture_rect_h2;is_solid2;type2;tile_index2
		..."""
		filepath = Utilities.askFilepathToSave(
			(
				('All Files', '*.*'),
				('CSV File', '*.csv'),
				('Text Document', '*.txt')
			),
			"*.csv"
		)
		
		if not filepath: return

		level = []
		for y, line in enumerate(self.tiles):
			for x, tile in enumerate(line):
				if tile:
					level.append(f"""0;\
{x};\
{y};\
{tile[1].getRect()[0]};\
{tile[1].getRect()[1]};\
{tile[1].getRect()[2]};\
{tile[1].getRect()[3]};\
{int(tile[1].isSolid())};\
{(tile[1].getType())};\
{tile[0]}""")

		with open(filepath, 'w') as csv_file:			
			csv_file.write("\n".join(level))
		return

	def openFile(self):
		filepath = Utilities.askFilepathToOpen(
			(
				('All Files', '*.*'),
				('CSV File', '*.csv'),
				('Text Document', '*.txt')
			),
			"*.csv"
		)
		
		if not filepath: return
		self.createEnptyMap()
		with open(filepath, 'r') as csv_file:
			lines = csv_file.read().split('\n')

		for line in lines:
			numbers = line.split(';')
			self.tiles[int(numbers[2])][int(numbers[1])] = self.tile_list[int(numbers[9])]
		return
	
	def endProgram(self):
		self.is_program_run = False
		return True