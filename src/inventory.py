import pygame

class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)
        print(f"Item {item.name} added to inventory.")

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            print(f"Item {item.name} removed from inventory.")

    def render(self, screen):
        # Rendering the inventory in an upper bar, as a list of images
        x = 100
        y = 5
        bar_width = len(self.items) * 130  # Calculate the width based on the number of items
        bar_height = 140

        # Create a semi-transparent surface for the background
        background = pygame.Surface((bar_width, bar_height), pygame.SRCALPHA)
        background.fill((211, 211, 211, 128))  # Light-gray color with 50% opacity

         # Blit the background onto the screen
        screen.blit(background, (x, y))

        # Render each item on top of the background
        item_x = x
        for item in self.items:
            item.render(screen, item_x, y)
            item_x += 130  # space between items