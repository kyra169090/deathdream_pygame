import pygame
from objects import GameObject
from inventory import Inventory

class Node:
    def __init__(self, background_image, lit_background_image=None):
        self.background_image = background_image
        self.lit_background_image = lit_background_image  # Background after lightbulb is used
        self.boxes = []
        self.objects = []
        self.slots = []

    def render(self, screen, inventory):
        # Draw background image
        screen.blit(self.background_image, (0, 0))
        # Draw boxes
        for box in self.boxes:
            # Create a transparent surface
            transparent_surface = pygame.Surface((box.width, box.height), pygame.SRCALPHA)
            # Fill the surface with a black color and set its transparency
            transparent_surface.fill((0, 0, 0, 100))  # Adjust the 50 for more or less transparency
            # Blit the transparent surface onto the screen at the box's position
            screen.blit(transparent_surface, (box.x, box.y))

        # Draw objects
        for obj in self.objects:
            if obj.interactable:  # Only draw objects that haven't been picked up
                obj.render(screen)

        inventory.render(screen)

        pygame.display.flip()

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

class Start(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=1270, y=650, width=220, height=200, next_scene=None),
            Box(x=600, y=900, width=400, height=140, next_scene=None),
            Box(x=400, y=600, width=300, height=140, next_scene=None)  
        ]
    def render(self, screen, inventory):
        super().render(screen, inventory)

# first house
class CityPart1Door(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=700, y=300, width=250, height=650, next_scene=None),
            Box(x=000, y=900, width=400, height=150, next_scene=None) 
        ]
    def render(self, screen, inventory):
        super().render(screen, inventory)

class CityPart1Corridor(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            #door to living room
            Box(x=970, y=350, width=150, height=220, next_scene=None),
            #door to pantry
            Box(x=700, y=350, width=120, height=400, next_scene=None),
            #going back
            Box(x=600, y=900, width=550, height=150, next_scene=None)            
        ]
    def render(self, screen, inventory):
        super().render(screen, inventory)

class CityPart1LivingRoom(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=600, y=900, width=550, height=150, next_scene=None)           
        ]
    def render(self, screen, inventory):
        super().render(screen, inventory)

class CityPart1Pantry(Node):
    def __init__(self, background_image, lit_background_image):
        super().__init__(background_image, lit_background_image)

         # Define a slot where the lightbulb can be used
        self.slots = [
            Slot(x=10, y=10, width=100, height=100, required_item="Lightbulb", action=self.use_lightbulb)
        ]
        self.boxes = [
            Box(x=300, y=900, width=550, height=120, next_scene=None)           
        ]
        self.objects = [
            GameObject(name="Crowbar", image_path="../assets/images/scenes/location1/crowbar.png", x=900, y=780, width=200, height=200)
        ]
    def use_lightbulb(self):
        # Putting lightbulb sound here
        # Change the background image to show the lit room
        if self.lit_background_image:
            self.background_image = self.lit_background_image
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
city_part1_door = CityPart1Door(pygame.image.load('../assets/images/scenes/location1/location1_abandoned_city_1_2.jpg'))
city_part1_corridor = CityPart1Corridor(pygame.image.load('../assets/images/scenes/location1/location1_abandoned_city_1_3.jpg'))
city_part1_livingroom = CityPart1LivingRoom(pygame.image.load('../assets/images/scenes/location1/location1_abandoned_city_1_4.jpg'))
city_part1_pantry = CityPart1Pantry(pygame.image.load('../assets/images/scenes/location1/location1_abandoned_city_1_5_dark.jpg'), pygame.image.load('../assets/images/scenes/location1/location1_abandoned_city_1_5.jpg'))
city_part2 = CityPart2(pygame.image.load('../assets/images/scenes/location2/location2_abandoned_city_1_1.jpg'))
city_part2_shop = CityPart2Shop(pygame.image.load('../assets/images/scenes/location2/location2_abandoned_city_1_2.jpg'))
city_part2_shop_shelf = CityPart2ShopShelf(pygame.image.load('../assets/images/scenes/location2/location2_abandoned_city_shelf.jpg'))
city_part3 = CityPart3(pygame.image.load('../assets/images/scenes/location3/city_part_3_girl_int_the_wall_1_1.jpg'))



# Link scenes to boxes (after they are created)
start_scene.boxes[0].next_scene = city_part2
start_scene.boxes[1].next_scene = city_part3
start_scene.boxes[2].next_scene = city_part1_door
city_part1_door.boxes[0].next_scene = city_part1_corridor
city_part1_door.boxes[1].next_scene = start_scene
city_part1_corridor.boxes[0].next_scene = city_part1_livingroom
city_part1_corridor.boxes[1].next_scene = city_part1_pantry
city_part1_corridor.boxes[2].next_scene = city_part1_door
city_part1_pantry.boxes[0].next_scene = city_part1_corridor
city_part1_livingroom.boxes[0].next_scene = city_part1_corridor
city_part2.boxes[0].next_scene = start_scene
city_part2.boxes[1].next_scene = city_part2_shop
city_part2_shop.boxes[0].next_scene = city_part2
city_part2_shop.boxes[1].next_scene = city_part2_shop_shelf
city_part2_shop_shelf.boxes[0].next_scene = city_part2_shop
city_part3.boxes[0].next_scene = start_scene