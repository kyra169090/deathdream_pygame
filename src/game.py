import pygame
import sys
from scenes import load_scenes

class Game:
    def __init__(self):
        pygame.init()

        # Constants
        self.WIDTH, self.HEIGHT = 1500, 1024
        self.BLACK = (0, 0, 0)

        # Screen setup
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Deathdream')

        # Load scenes from JSON
        self.scenes = load_scenes(self.WIDTH, self.HEIGHT)
        self.current_scene_index = 0  # Start with the first scene

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    current_scene = self.scenes[self.current_scene_index]
                    if current_scene["box"].collidepoint(mouse_pos):
                        self.current_scene_index = current_scene["next_scene"] - 1

            # Drawing the current scene
            self.draw_scene()

            pygame.display.flip()

    def draw_scene(self):
        current_scene = self.scenes[self.current_scene_index]
        self.screen.blit(current_scene["background_image"], (0, 0))
        pygame.draw.rect(self.screen, self.BLACK, current_scene["box"])
