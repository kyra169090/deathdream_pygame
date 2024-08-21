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
        # Rendering the inventory in an upper bar, as a list of images
        x = 20
        y = 5
        for item in self.items:
            item.render(screen, x, y)
            x += 130  # space between items