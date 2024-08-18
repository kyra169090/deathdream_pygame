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

    def has_item(self, item_name):
        return any(item.name == item_name for item in self.items)

    def render(self, screen):
        # Optionally, render the inventory on the screen
        # For example, as a list of images/icons
        x_offset = 10
        for item in self.items:
            screen.blit(item.image, (x_offset, 10))
            x_offset += item.image.get_width() + 10