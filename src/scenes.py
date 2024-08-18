import pygame
from objects import GameObject
from inventory import Inventory

class Node:
    def __init__(self, background_image):
        self.background_image = background_image
        self.boxes = []
        self.objects = []

    def render(self, screen, inventory):
        # Draw background image
        screen.blit(self.background_image, (0, 0))
        # Draw boxes
        for box in self.boxes:
            # Create a transparent surface
            transparent_surface = pygame.Surface((box.width, box.height), pygame.SRCALPHA)
            # Fill the surface with a black color and set its transparency
            transparent_surface.fill((0, 0, 0, 70))  # Adjust the 50 for more or less transparency
            # Blit the transparent surface onto the screen at the box's position
            screen.blit(transparent_surface, (box.x, box.y))

        # Draw objects
        for obj in self.objects:
            if obj.interactable:  # Only draw objects that haven't been picked up
                obj.render(screen)

        # Render inventory
        inventory.render(screen)

        pygame.display.flip()

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

class Start(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=1270, y=650, width=220, height=200, next_scene=None),
            Box(x=600, y=900, width=400, height=140, next_scene=None)  
        ]
    def render(self, screen, inventory):
        super().render(screen, inventory)

# way to the shop
class CityPart2(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=600, y=900, width=500, height=120, next_scene=None),
            Box(x=810, y=615, width=180, height=150, next_scene=None)  
        ]
    def render(self, screen, inventory):
        super().render(screen, inventory)

# inside the shop
class CityPart2Shop(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=600, y=900, width=500, height=120, next_scene=None),
            Box(x=890, y=315, width=170, height=300, next_scene=None)
        ]
    def render(self, screen, inventory):
        super().render(screen, inventory)

# Shelf in the shop
class CityPart2ShopShelf(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=400, y=900, width=750, height=150, next_scene=None)  
        ]
        self.objects = [
            GameObject(name="Lightbulb", image_path="../assets/images/scenes/location2/lightbulb.png", x=1005, y=453, width=235, height=277)
        ]

    def render(self, screen, inventory):
        super().render(screen, inventory)

# way to the creepy house with locked door
class CityPart3(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=600, y=900, width=550, height=150, next_scene=None)  
        ]
    def render(self, screen, inventory):
        super().render(screen, inventory)

# Initialize scenes with the appropriate images
start_scene = Start(pygame.image.load('../assets/images/scenes/location1/location1_abandoned_city_1_1.jpg'))
city_part2 = CityPart2(pygame.image.load('../assets/images/scenes/location2/location2_abandoned_city_1_1.jpg'))
city_part2_shop = CityPart2Shop(pygame.image.load('../assets/images/scenes/location2/location2_abandoned_city_1_2.jpg'))
city_part2_shop_shelf = CityPart2ShopShelf(pygame.image.load('../assets/images/scenes/location2/location2_abandoned_city_shelf.jpg'))
city_part3 = CityPart3(pygame.image.load('../assets/images/scenes/location3/city_part_3_girl_int_the_wall_1_1.jpg'))



# Link scenes to boxes (after they are created)
start_scene.boxes[0].next_scene = city_part2
start_scene.boxes[1].next_scene = city_part3
city_part2.boxes[0].next_scene = start_scene
city_part2.boxes[1].next_scene = city_part2_shop
city_part2_shop.boxes[0].next_scene = city_part2
city_part2_shop.boxes[1].next_scene = city_part2_shop_shelf
city_part2_shop_shelf.boxes[0].next_scene = city_part2_shop
city_part3.boxes[0].next_scene = start_scene