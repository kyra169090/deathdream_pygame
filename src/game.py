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
        except:
            pass
        from scene_manager import city_part4_familyhouse

        # Start with location1
        self.current_scene = city_part4_familyhouse
        self.inventory = Inventory()


    def run(self):
        running = True
        selected_item = None
        hand_cursor = pygame.image.load('../assets/images/other/pointer.png')
        
        while running:
            moving_mouse_pos = pygame.mouse.get_pos()
            # print(moving_mouse_pos)
            hover = False
            
            # The Pygame event loop (for a point&click mousedown is enough)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos

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

                    # Check if the current scene has dialogue and if it's shown
                    if self.current_scene.show_dialogue:
                        if self.current_scene.text_rect.collidepoint(mouse_pos):
                            self.current_scene.click_dialogue()

            # If pointer should be shown or not
            for box in self.current_scene.boxes:
                if pygame.Rect(box.x, box.y, box.width, box.height).collidepoint(moving_mouse_pos):
                    hover = True
                    break

            # Render the current scene first
            self.current_scene.render(self.screen, self.inventory)

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