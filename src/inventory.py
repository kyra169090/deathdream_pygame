import pygame

class Inventory:
    def __init__(self):
        self.items = []
        self.selected_item = None

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)

    def render(self, screen):
        # Rendering the inventory in an upper bar, as a list of images
        x = 100
        y = 5
        bar_width = len(self.items) * 110  # Calculate the width based on the number of items
        bar_height = 110

        # Create a semi-transparent surface for the background
        background = pygame.Surface((bar_width, bar_height), pygame.SRCALPHA)
        background.fill((211, 211, 211, 128))  # Light-gray color with 50% opacity

         # Blit the background onto the screen
        screen.blit(background, (x, y))

        # Render each item on top of the background
        item_x = x
        for item in self.items:
            item.render(screen, item_x, y)

            if item == self.selected_item:
                # Creating a semi-transparent surface to highlight the selected item
                highlight_surface = pygame.Surface((bar_width, bar_height), pygame.SRCALPHA)
                highlight_surface.fill((255, 255, 0, 78))  # Yellow color with 50% opacity

                # Blit the highlight layer onto the item
                screen.blit(highlight_surface, (item_x, y))

            item_x += 130  # space between items

    def select_item(self, item):
        self.selected_item = item