import pygame

class GameObject:
    def __init__(self, name, image_path, x, y, width, height, interactable=True):
        self.name = name
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.interactable = interactable
        self.inventory_image = pygame.transform.scale_by(self.image, 0.4)

    def render(self, screen, x=None, y=None, scale_factor=1):
        if x is not None and y is not None:
            # Dynamically scale based on the scale factor
            scaled_width = int(self.width * 0.4 * scale_factor)
            scaled_height = int(self.height * 0.4 * scale_factor)
            scaled_image = pygame.transform.scale(self.image, (scaled_width, scaled_height))

            screen.blit(scaled_image, (x, y))
            self.rect.x = x
            self.rect.y = y
            self.rect.width = scaled_width
            self.rect.height = scaled_height
        else:
            screen.blit(self.image, self.rect.topleft)

    def interact(self, inventory):
        if self.interactable:
            inventory.add_item(self)
            self.interactable = False  # After picking up, it's no longer interactable
