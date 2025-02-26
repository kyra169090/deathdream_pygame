import pygame
import sys
from inventory import Inventory


class Game:
    def __init__(self):
        pygame.init()

        # Screen setup
        self.WIDTH = 1500
        self.HEIGHT = 1024
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Deathdream')

        # Music
        try:
            pygame.mixer.init()
            pygame.mixer.music.load('../assets/sounds/background_music.mp3')
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"Music loading error: {e}")

        from scene_manager import start_scene   # Normally: start_scene, when testing: city_part_5_1_1

        # Start with location1
        self.current_scene = start_scene   # Normally: start_scene, when testing: city_part_5_1_1
        self.inventory = Inventory()
        self.clock = pygame.time.Clock()

    def run(self):
        running = True
        selected_item = None
        hand_cursor = pygame.image.load('../assets/images/other/pointer.png')
        
        while running:
            delta_time = self.clock.tick(60)
            if hasattr(self.current_scene, 'update'):
                self.current_scene.update(delta_time)
            moving_mouse_pos = pygame.mouse.get_pos()
            # print(moving_mouse_pos)
            hover = False
            
            # The Pygame event loop (for a point&click mousedown is enough)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos

                    if self.current_scene.show_dialogue:
                        if self.current_scene.text_rect.collidepoint(mouse_pos):
                            self.current_scene.click_dialogue()
                        continue

                    if not self.current_scene.show_dialogue:
                    # Handle item selection from the inventory
                        if event.button == 1:  # Left-click
                            for item in self.inventory.items:
                                if item.rect.collidepoint(mouse_pos):
                                    self.inventory.select_item(item)
                                    selected_item = item
                                    break

                        # Check for interactions with objects that can be picked up
                        for obj in self.current_scene.objects:
                            if obj.rect.collidepoint(mouse_pos):
                                obj.interact(self.inventory)
                                break

                        # Check for interactions with boxes
                        for box in self.current_scene.boxes:
                            if pygame.Rect(box.x, box.y, box.width, box.height).collidepoint(mouse_pos):
                                self.current_scene = box.next_scene
                                break

                        # Handle interaction with slots (you can use objects on them)
                        for slot in self.current_scene.slots:
                            if slot.rect.collidepoint(mouse_pos) and selected_item:
                                if slot.try_use_item(selected_item, self.inventory):
                                    self.inventory.selected_item = None  # Deselecting the item after it is used
                                    break

            # If pointer should be shown or not
            for box in self.current_scene.boxes:
                if pygame.Rect(box.x, box.y, box.width, box.height).collidepoint(moving_mouse_pos):
                    hover = True
                    break

            # Check if the current scene has changed
            new_scene = self.current_scene.render(self.screen, self.inventory)
            if new_scene is not None:
                self.current_scene = new_scene

            if hover:
                pygame.mouse.set_visible(False)
                # Draw the custom cursor image at the mouse position after everything else
                self.screen.blit(hand_cursor, (moving_mouse_pos[0] - hand_cursor.get_width() // 2, 
                                               moving_mouse_pos[1] - hand_cursor.get_height() // 2))
            else:
                # Show the default system cursor
                pygame.mouse.set_visible(True)

            pygame.display.flip()

        pygame.quit()
        sys.exit()