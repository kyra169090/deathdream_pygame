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
        if not self.items:  # Do not render the inventory if it's empty
            return

        y = 5  # Y position of the inventory bar
        item_spacing = 130  # Space between items
        min_item_width = 90  # Minimum width for items
        inventory_width = max(len(self.items) * item_spacing, 450)  # Minimum width for inventory bar
        bar_height = 110
        screen_width = screen.get_width()

        # Center the inventory bar
        bar_x = (screen_width - inventory_width) // 2

        # Create a semi-transparent background for the inventory
        background = pygame.Surface((inventory_width, bar_height), pygame.SRCALPHA)
        background.fill((211, 211, 211, 128))  # Light-gray color with 50% opacity
        screen.blit(background, (bar_x, y))

        # Centering the items
        total_item_width = len(self.items) * item_spacing
        item_x = bar_x + (inventory_width - total_item_width) // 2  # Start position for items

        # Render each item in the inventory
        for item in self.items:
            scale_factor = 2 if item.name == "Key" else 1
            item.render(screen, item_x, y, scale_factor)

            if item == self.selected_item:
                # Create a highlight effect for the selected item
                highlight_surface = pygame.Surface((min_item_width, bar_height), pygame.SRCALPHA)
                highlight_surface.fill((255, 255, 0, 78))  # Yellow highlight with some transparency
                screen.blit(highlight_surface, (item_x, y))
            item_x += item_spacing  # Move to the next item position

    def select_item(self, item):
        self.selected_item = item