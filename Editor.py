import pygame

class Editor:
	def __init__(self, width, height, title):
		pygame.init()
		self.window_width = width
		self.window_height = height
		self.is_program_run = True
		self.initWindow(
			self.window_width,
			self.window_height, 
			title
		)
		self.clock = pygame.clock.Clock()


	def initWindow(self, width, height, title):
		self.window = pygame.display.set_mode(
			(width, height)
		)
		pygame.display.set_caption(title)
		self.window_width = width
		self.window_height = height

	def update(self):
		pygame.display.flip()

	def draw(self):
		self.window.blit()

	def checkEvents(self):
		for event in pygame.event.get():
			match event.type:
				case pygame.QUIT:
					self.is_program_run = False
					break

	def run(self):
		while self.is_program_run:
			self.clock.tick(self.FPS) # frame rate
			self.checkEvents()
			self.update()
			self.draw()
			
	
