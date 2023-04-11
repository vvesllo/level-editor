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
		self.value = False

		self.initWindow(
			self.window_width,
			self.window_height, 
			title
		)
	
		self.__ui_elements = [
			UI.UIButton(
				"Open File", # label
				Vector.Vec2(10, 10), # position
				Vector.Vec2(180, 50), # size
				self.open_file
			),
			UI.UILabel(
				"Label 1", # label
				Vector.Vec2(10, 130), # position
				Vector.Vec2(180, 50), # size
			),
			UI.UIButton(
				"print", # label
				Vector.Vec2(10, 65), # position
				Vector.Vec2(180, 50), # size
				lambda: ("Hello world")
			),
			UI.UICheckBox(
				"Show rect", # label
				Vector.Vec2(195, 65), # position
				Vector.Vec2(180, 50), # size
				self.value
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
			"*.*")
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
		for ui_element in self.__ui_elements:
			if isinstance(ui_element, UI.UIButton) or \
				isinstance(ui_element, UI.UICheckBox):
				ui_element.checkHover(pygame.mouse.get_pos())

			ui_element.update()
			
		pygame.display.flip()

	def draw(self):
		self.window.fill("black")
		for ui_element in self.__ui_elements:
			self.window.blit(
				ui_element.getSurface(),
				ui_element.getPosition().get()
			)


		if self.value:
			pygame.draw.rect(
				self.window,
				pygame.Color("red"),
				pygame.Rect(200, 200, 60, 60)
			)

		pygame.display.update()

	def checkEvents(self):
		for event in pygame.event.get():
			match event.type:
				case pygame.QUIT:
					self.is_program_run = False
					break
				case pygame.MOUSEBUTTONDOWN:
					b1, _, _ = pygame.mouse.get_pressed()
					for ui_element in self.__ui_elements:
						if isinstance(ui_element, UI.UIButton):
							if ui_element.isHovered():
								print(ui_element.click(b1))
								self.update()
						elif isinstance(ui_element, UI.UICheckBox):
							if ui_element.isHovered():
								self.value = ui_element.click(b1)
								self.update()
					break

	def run(self):
		while self.is_program_run:
			self.clock.tick(self.FPS) # frame rate
			self.checkEvents()
			self.update()
			self.draw()
			
	
