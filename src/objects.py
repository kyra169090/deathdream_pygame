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

    def render(self, screen, x=None, y=None):
        if x is not None and y is not None:
            screen.blit(self.inventory_image, (x, y))
            self.rect.x = x
            self.rect.y = y
            self.rect.width = self.width/2
            self.rect.height = self.height/2
        else:
            screen.blit(self.image, self.rect.topleft)

    def interact(self, inventory):
        if self.interactable:
            inventory.add_item(self)
            self.interactable = False  # After picking up, it's no longer interactable
