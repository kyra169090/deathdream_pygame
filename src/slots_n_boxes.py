import pygame

class Slot:
    def __init__(self, x, y, width, height, required_item, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.required_item = required_item  # Name of the item required for this slot
        self.action = action  # Function to call when the correct item is used

    def try_use_item(self, item, inventory):
        # Check if the item is the required one and use it if so
        if item.name == self.required_item:
            self.action()  # Trigger the action (e.g., turn on light)
            inventory.remove_item(item)  # Remove item from inventory
            return True
        return False

class Box:
    def __init__(self, x, y, width, height, next_scene=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.next_scene = next_scene

    def click(self):
        if self.next_scene:
            self.next_scene.render()