import UI
import Vector
import pygame
from tkinter import filedialog

class Editor:
	def __init__(self, width, height, title):
		pygame.init()
		self.FPS = 60
		self.window_width = width
		self.window_height = height
		self.is_program_run = True
		self.initWindow(
			self.window_width,
			self.window_height, 
			title
		)
		
		self.__ui_elements = [
			UI.UIButton(
				"Open File", # label
				Vector.Vec2(10, 10), # position
				Vector.Vec2(150, 70), # size
				self.open_file
			),
			UI.UIButton(
				"print", # label
				Vector.Vec2(10, 90), # position
				Vector.Vec2(150, 70), # size
				lambda: ("Hello world")
			)
		]

		self.clock = pygame.time.Clock()

	def open_file(self):
		return (
			self.ask_filepath_to_open(
				(
					('All Files', '*.*'),
					('Level Colliders File', '*.lcf'),
					('Level Decoration File', '*.ldf'),
					('Text Document', '*.txt')
				),
			"*.ldf")
		)
	def ask_filepath_to_open(self, filetypes, default_extension):
		return filedialog.askopenfilename(
			filetypes=filetypes,
			defaultextension=default_extension
		)
	def initWindow(self, width, height, title):
		self.window = pygame.display.set_mode(
			(width, height)
		)
		pygame.display.set_caption(title)
		self.window_width = width
		self.window_height = height

	def update(self):
		mouse_position = pygame.mouse.get_pos()
		for ui_element in self.__ui_elements:
			ui_element.checkHover(pygame.mouse.get_pos())
			ui_element.update()
			
		pygame.display.flip()

	def draw(self):
		for ui_element in self.__ui_elements:
			self.window.blit(
				ui_element.getSurface(),
				ui_element.getPosition().get()
			)

	def checkEvents(self):
		for event in pygame.event.get():
			match event.type:
				case pygame.QUIT:
					self.is_program_run = False
					break
				case pygame.MOUSEBUTTONDOWN:
					b1, _, _ = pygame.mouse.get_pressed()
					for ui_element in self.__ui_elements:
						if ui_element.isHovered():
							print(ui_element.click(b1))
							self.update()
					break

	def run(self):
		while self.is_program_run:
			self.clock.tick(self.FPS) # frame rate
			self.checkEvents()
			self.update()
			self.draw()
			
	
