import pygame
import sys
from scenes import start_scene
from inventory import Inventory


class Game:
    def __init__(self):
        pygame.init()
        self.WIDTH = 1500
        self.HEIGHT = 1024

        # Screen setup
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Deathdream')
        # Music
        pygame.mixer.init()
        pygame.mixer.music.load('../assets/sounds/background_music.mp3')
        pygame.mixer.music.play(-1)

        # Start with location1
        self.current_scene = start_scene
        self.inventory = Inventory()
        

    def run(self):
        running = True
        selected_item = None

        while running:
            # The Pygame event loop (for a point&click mousedown is enough)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos

                    # Check for interactions with objects
                    for obj in self.current_scene.objects:
                        if obj.rect.collidepoint(mouse_pos):
                            obj.interact(self.inventory)
                            break

                    # Handle item selection from the inventory
                    if event.button == 1:  # Left-click
                        for item in self.inventory.items:
                            if item.rect.collidepoint(mouse_pos):
                                selected_item = item
                                break
                    # Handle interaction with slots
                    for slot in self.current_scene.slots:
                        if slot.rect.collidepoint(mouse_pos) and selected_item:
                            if slot.try_use_item(selected_item, self.inventory):
                                selected_item = None  # Clear selection if the item is used
                                break

                    # Check for interactions with boxes
                    for box in self.current_scene.boxes:
                        if pygame.Rect(box.x, box.y, box.width, box.height).collidepoint(mouse_pos):
                            self.current_scene = box.next_scene
                            break

            self.current_scene.render(self.screen, self.inventory)

        pygame.quit()