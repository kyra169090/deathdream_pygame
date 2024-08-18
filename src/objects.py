import pygame

class GameObject:
    def __init__(self, name, image_path, x, y, width, height, interactable=True):
        self.name = name
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = pygame.Rect(x, y, width, height)
        self.interactable = interactable

    def render(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def interact(self, inventory):
        if self.interactable:
            inventory.add_item(self)
            self.interactable = False  # After picking up, it's no longer interactable
