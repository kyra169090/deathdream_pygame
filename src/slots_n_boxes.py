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
            if item.name != "Crowbar":
                inventory.remove_item(item)
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

class Node:
    def __init__(self, background_image, changed_background_image=None):
        self.background_image = background_image
        self.changed_background_image = changed_background_image  # Background after lightbulb is used
        self.boxes = []
        self.objects = []
        self.slots = []
        pygame.font.init()
        self.font = pygame.font.Font(None, 50)
        self.text_rect = pygame.Rect(50, 10, 1400, 70)
        self.dialogue_queue = []
        self.show_dialogue = False

    def update(self, delta_time):
        pass

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

        # Render dialogue if it's active
        if self.show_dialogue and self.dialogue_queue:
            dialogue_entry = self.dialogue_queue[0]  # Get the first dialogue in the queue
            self.render_text(screen, dialogue_entry["text"], dialogue_entry["color"])

    def render_text(self, screen, text, color=(255, 255, 255)):
        pygame.draw.rect(screen, (0, 0, 0), self.text_rect)
        rendered_text = self.font.render(text, True, color)
        screen.blit(rendered_text, (self.text_rect.x + 10, self.text_rect.y + 10))

    def start_dialogue(self, dialogue):
        """Start a sequence of dialogues."""
        self.dialogue_queue = [
        {"text": entry[0], "color": entry[1]} if isinstance(entry, tuple) else {"text": entry, "color": (255, 255, 255)}
        for entry in dialogue
        ]
        self.current_dialogue_index = 0
        self.show_dialogue = True

    def click_dialogue(self):
        """Handle dialogue clicking to progress or end."""
        if self.dialogue_queue:
            self.dialogue_queue.pop(0)  # Remove the current dialogue
            if not self.dialogue_queue:  # If there ar no more dialogues
                self.show_dialogue = False