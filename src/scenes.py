import pygame
from objects import GameObject
from slots_n_boxes import Slot, Box, Node


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
    def __init__(self, background_image, next_scene):
        super().__init__(background_image)
        self.isOpen = False  # Initialize the door as closed
        self.next_scene = next_scene  # Store the next scene
        self.slots = [
            Slot(x=920, y=480, width=270, height=430, required_item="Crowbar", action=self.use_crowbar)
        ]
        self.boxes = [
            Box(x=300, y=960, width=1180, height=64, next_scene=None)
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
            self.new_box = Box(x=920, y=480, width=270, height=430, next_scene=self.next_scene)
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
            Box(x=900, y=400, width=200, height=200, next_scene=None),
            Box(x=600, y=400, width=200, height=400, next_scene=None)
        ]

    def render(self, screen, inventory):
        super().render(screen, inventory)

# creepy house last room
class CityPart3Room(Node):
    def __init__(self, background_image, changed_background_image, next_scene):
        super().__init__(background_image, changed_background_image)
        self.ceiling_broken = False
        self.next_scene = next_scene  # Store the next scene
        self.slots = [
            Slot(x=900, y=130, width=110, height=120, required_item="Crowbar", action=self.break_ceiling)
        ]
        self.boxes = [
            Box(x=0, y=950, width=850, height=70, next_scene=None)
        ]
        pygame.mixer.init()
        self.breathing_sound = pygame.mixer.Sound('../assets/sounds/citypart3room/breathing_sound.mp3')
        self.break_sound = pygame.mixer.Sound('../assets/sounds/break_sound.mp3')

        # Flag to check if breathing sound has been played already
        self.breathing_sound_played = False

    def break_ceiling(self):
        # Changing the background image
        if not self.ceiling_broken and self.changed_background_image:
            self.break_sound.play()
            self.background_image = self.changed_background_image
            self.add_new_box()
            self.add_new_item_to_screen()
            self.ceiling_broken = True

    def add_new_box(self):
        # Add the new box and set its next scene
        self.new_box = Box(x=900, y=850, width=150, height=80, next_scene=self.next_scene)
        self.boxes.append(self.new_box)

    def add_new_item_to_screen(self):
        # Add the new box and set its next scene
        self.new_item = GameObject(name="Key", image_path="../assets/images/scenes/location3/key.png", x=845, y=900, width=65, height=20)
        self.objects.append(self.new_item)

    def render(self, screen, inventory):
        super().render(screen, inventory)
        # Play the breathing sound only once when the player first enters
        if not self.breathing_sound_played:
            self.breathing_sound.play()
            self.breathing_sound_played = True

class CityPart3RoomLetter(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=0, y=0, width=300, height=1024, next_scene=None),
            Box(x=1300, y=0, width=200, height=1024, next_scene=None)
        ]
        pygame.mixer.init()
        self.paper_sound = pygame.mixer.Sound('../assets/sounds/paper_collect.mp3')

        self.paper_sound_played = False

    def render(self, screen, inventory):
        super().render(screen, inventory)
        if not self.paper_sound_played:
            self.paper_sound.play()
            self.paper_sound_played = True


class CityPart3CorridorWardrobe(Node):
    def __init__(self, background_image, changed_background_image, next_scene1, next_scene2):
        super().__init__(background_image, changed_background_image)
        self.next_scene1 = next_scene1  # Store the next scene
        self.next_scene2 = next_scene2  # Store the next scene

        self.slots = [
            Slot(x=700, y=600, width=100, height=150, required_item="Key", action=self.use_key)
        ]
        self.boxes = [
            Box(x=0, y=910, width=950, height=110, next_scene=None)
        ]
        self.new_box = None
        pygame.mixer.init()
        self.unlocking_sound = pygame.mixer.Sound('../assets/sounds/unlocking.mp3')

    def use_key(self):
        # Change the background image to show the lit room
        if self.changed_background_image:
            self.unlocking_sound.play()
            pygame.time.delay(1000)
            self.background_image = self.changed_background_image
            self.add_new_boxes()

    def add_new_boxes(self):
        # Add the new box and set its next scene
        self.new_box1 = Box(x=365, y=795, width=180, height=100, next_scene=self.next_scene1)
        self.new_box2 = Box(x=655, y=790, width=180, height=100, next_scene=self.next_scene2)
        self.boxes.append(self.new_box1)
        self.boxes.append(self.new_box2)

    def render(self, screen, inventory):
        super().render(screen, inventory)

class CityPart3Photo1(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=0, y=0, width=1500, height=1024, next_scene=None)
        ]
        pygame.mixer.init()
        self.paper_sound = pygame.mixer.Sound('../assets/sounds/paper_collect.mp3')
        self.paper_sound_played = False

    def render(self, screen, inventory):
        super().render(screen, inventory)
        if not self.paper_sound_played:
            self.paper_sound.play()
            self.paper_sound_played = True


class CityPart3Photo2(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=0, y=0, width=1500, height=1024, next_scene=None)
        ]
        pygame.mixer.init()
        self.paper_sound = pygame.mixer.Sound('../assets/sounds/paper_collect.mp3')
        self.paper_sound_played = False

    def render(self, screen, inventory):
        super().render(screen, inventory)
        if not self.paper_sound_played:
            self.paper_sound.play()
            self.paper_sound_played = True