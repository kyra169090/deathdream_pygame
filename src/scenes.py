import pygame
from objects import GameObject
from slots_n_boxes import Slot, Box

class Node:
    def __init__(self, background_image, changed_background_image=None):
        self.background_image = background_image
        self.changed_background_image = changed_background_image  # Background after lightbulb is used
        self.boxes = []
        self.objects = []
        self.slots = []

    def render(self, screen, inventory):
        screen.blit(self.background_image, (0, 0))
        # Draw boxes
        for box in self.boxes:
            # Create a transparent surface
            transparent_surface = pygame.Surface((box.width, box.height), pygame.SRCALPHA)
            # Fill the surface with a black color and set its transparency
            transparent_surface.fill((0, 0, 0, 0))  # Adjust the last value for more or less transparency
            # Blit the transparent surface onto the screen at the box's position
            screen.blit(transparent_surface, (box.x, box.y))

        # Draw objects
        for obj in self.objects:
            if obj.interactable:  # Only draw objects that haven't been picked up
                obj.render(screen)

        inventory.render(screen)


class Start(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=1270, y=650, width=220, height=200, next_scene=None),
            Box(x=00, y=900, width=600, height=100, next_scene=None),
            Box(x=600, y=600, width=200, height=140, next_scene=None)  
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
            Box(x=300, y=930, width=800, height=100, next_scene=None)           
        ]
    def render(self, screen, inventory):
        super().render(screen, inventory)

class CityPart1Pantry(Node):
    def __init__(self, background_image, changed_background_image):
        super().__init__(background_image, changed_background_image)

         # Defining a slot where the lightbulb can be used
        self.slots = [
            Slot(x=10, y=10, width=100, height=100, required_item="Lightbulb", action=self.use_lightbulb)
        ]
        self.boxes = [
            Box(x=0, y=910, width=550, height=110, next_scene=None)           
        ]
        self.objects = [
            GameObject(name="Crowbar", image_path="../assets/images/scenes/location1/crowbar.png", x=900, y=780, width=200, height=200, interactable=False)
        ]
        pygame.mixer.init() 
        self.lightbulb_sound = pygame.mixer.Sound('../assets/sounds/lightbulb_sound.mp3')

    def use_lightbulb(self):
        # Change the background image to show the lit room
        if self.changed_background_image:
            self.lightbulb_sound.play()
            pygame.time.delay(2000)
            self.background_image = self.changed_background_image

            # Make the crowbar interactable now
            for obj in self.objects:
                if obj.name == "Crowbar":
                    obj.interactable = True

    def render(self, screen, inventory):
        super().render(screen, inventory)


# way to the shop
class CityPart2(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=300, y=900, width=700, height=120, next_scene=None),
            Box(x=810, y=615, width=180, height=150, next_scene=None)  
        ]
    def render(self, screen, inventory):
        super().render(screen, inventory)

# inside the shop
class CityPart2Shop(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=300, y=920, width=800, height=120, next_scene=None),
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
            Box(x=500, y=900, width=950, height=150, next_scene=None),
            Box(x=860, y=600, width=200, height=150, next_scene=None)  
        ]
    def render(self, screen, inventory):
        super().render(screen, inventory)


# creepy house with locked door
class CityPart3Door(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.isOpen = False  # Initialize the door as closed
        self.slots = [
            Slot(x=920, y=480, width=270, height=430, required_item="Crowbar", action=self.use_crowbar)
        ]
        self.boxes = [
            Box(x=300, y=930, width=1180, height=70, next_scene=None)
        ]
        self.new_box = None  # Placeholder for the new box
        pygame.mixer.init() 
        self.door_crowbar_sound = pygame.mixer.Sound('../assets/sounds/door_with_crowbar.mp3')

    def use_crowbar(self):
        # you can enter house after using the crowbar
        if not self.isOpen:
            self.door_crowbar_sound.play()
            pygame.time.delay(1000)
            self.isOpen = True
            self.add_new_box()


    def add_new_box(self):
        # Add the new box and set its next scene
        if self.isOpen and not self.new_box:
            self.new_box = Box(x=920, y=480, width=270, height=430, next_scene=city_part3_corridor)
            self.boxes.append(self.new_box)

    def render(self, screen, inventory):
        # If the door is open, add the extra box
        if self.isOpen and not self.new_box:
            self.add_new_box()
        super().render(screen, inventory)

# creepy house corridor
class CityPart3Corridor(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=400, y=900, width=900, height=100, next_scene=None),
            Box(x=900, y=400, width=200, height=200, next_scene=None)  
        ]

    def render(self, screen, inventory):
        super().render(screen, inventory)

# creepy house last room
class CityPart3Room(Node):
    def __init__(self, background_image, changed_background_image):
        super().__init__(background_image, changed_background_image)
        self.slots = [
            Slot(x=900, y=130, width=150, height=150, required_item="Crowbar", action=self.break_ceiling)
        ]
        self.boxes = [
            Box(x=100, y=940, width=1000, height=70, next_scene=None)
        ]
        pygame.mixer.init()
        self.breathing_sound = pygame.mixer.Sound('../assets/sounds/breathing_sound.mp3')
        self.break_sound = pygame.mixer.Sound('../assets/sounds/break_sound.mp3')

        # Flag to check if breathing sound has been played already
        self.breathing_sound_played = False

    def break_ceiling(self):
        # Changing the background image
        if self.changed_background_image:
            self.break_sound.play()
            self.background_image = self.changed_background_image

    def render(self, screen, inventory):
        super().render(screen, inventory)
        # Play the breathing sound only once when the player first enters
        if not self.breathing_sound_played:
            self.breathing_sound.play()
            self.breathing_sound_played = True

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
city_part3door = CityPart3Door(pygame.image.load('../assets/images/scenes/location3/city_part_3_girl_int_the_wall_1_2.jpg'))
city_part3_corridor = CityPart3Corridor(pygame.image.load('../assets/images/scenes/location3/city_part_3_girl_int_the_wall_1_3.jpg'))
city_part3_room = CityPart3Room(pygame.image.load('../assets/images/scenes/location3/city_part_3_girl_int_the_wall_1_4.jpg'), pygame.image.load('../assets/images/scenes/location3/city_part_3_girl_int_the_wall_1_4_after.jpg'))

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
city_part3.boxes[1].next_scene = city_part3door
city_part3door.boxes[0].next_scene = city_part3
city_part3_corridor.boxes[0].next_scene = city_part3door
city_part3_corridor.boxes[1].next_scene = city_part3_room
city_part3_room.boxes[0].next_scene = city_part3_corridor