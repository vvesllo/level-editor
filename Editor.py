import UI
import Vector
import Tile
import pygame
from tkinter import filedialog

class Editor:
	def __init__(self, width, height, title):
		pygame.init()
		self.FPS = 60
		self.window_width = width
		self.window_height = height
		self.is_program_run = True
		self.show_menu = True
		self.speed = 0.2
		self.camera_position = Vector.Vec2(0, 0)
		self.camera_velocity = Vector.Vec2(0, 0)
		self.values = {
			"show_grid": True,
			"show_rect": True
		}
		self.cell_size = 64
		self.tileset = pygame.image.load("tileset.png")

		self.tiles = []
		for _ in range(64):
			self.tiles.append(
				[None for _ in range(64)]
			)

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
			),
			UI.UICheckBox(
				"Show rect",
				Vector.Vec2(110+15, 55),
				Vector.Vec2(110, 40),
				"show_rect",
				self.values["show_rect"]
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

		mouse_col = (mouse_position[0] - self.camera_position.y) // self.cell_size
		mouse_row = (mouse_position[1] - self.camera_position.y) // self.cell_size
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

	def draw(self):
		self.window.fill("black")

		for line in self.tiles:
			for tile in line:
				if tile:
					tile.setPosition(
						tile.getPosition() + self.camera_position
					)
					self.window.blit(
						tile.getSurface(),
						tile.getPosition().get()
					)

		if self.show_menu:
			for ui_element in self.__ui_elements:
				self.window.blit(
					ui_element.getSurface(),
					ui_element.getPosition().get()
				)
		if self.values["show_rect"]:
			pygame.draw.rect(
				self.window,
				pygame.Color("red"),
				(200, 200, 50, 50)
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
		self.camera_position = Vector.Vec2(0, 0)
		if pressed_keys[pygame.K_a]:
			self.camera_position.x += self.speed
		if pressed_keys[pygame.K_d]:
			self.camera_position.x -= self.speed

		if pressed_keys[pygame.K_w]:
			self.camera_position.y += self.speed
		if pressed_keys[pygame.K_s]:
			self.camera_position.y -= self.speed

		

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