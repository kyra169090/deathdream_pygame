import asyncio
import pygame
import sys
from inventory import Inventory

# True when running in the browser build (pygbag / WebAssembly)
WEB = sys.platform == "emscripten"


class Game:
    def __init__(self):
        # Give the browser audio thread more headroom. A larger mixer buffer
        # trades a tiny amount of latency for much more stable WebAssembly audio.
        pygame.mixer.pre_init(
            frequency=44100,
            size=-16,
            channels=2,
            buffer=4096,
        )
        pygame.init()

        # Internal fixed resolution (virtual screen)
        self.WIDTH = 1500
        self.HEIGHT = 1024

        # Real screen setup. In the browser the canvas is already the game's
        # native resolution, so render directly to it instead of rescaling a
        # 1500x1024 surface every frame.
        if WEB:
            self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
            self.virtual_screen = self.window
        else:
            self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.virtual_screen = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.real_width, self.real_height = self.window.get_size()

        pygame.display.set_caption('Deathdream')

        # Music
        try:
            pygame.mixer.music.load('../assets/sounds/background_music.ogg')
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"Music loading error: {e}")

        from scene_manager import start_scene

        self.current_scene = start_scene
        self.inventory = Inventory()
        self.clock = pygame.time.Clock()

    async def run(self):
        running = True
        selected_item = None
        hand_cursor = pygame.image.load('../assets/images/other/pointer.png')

        while running:
            delta_time = self.clock.tick(60)
            if hasattr(self.current_scene, 'update'):
                self.current_scene.update(delta_time)

            # Fire a scene's delayed action (see Node.wait)
            pending = getattr(self.current_scene, 'pending', None)
            if pending and pygame.time.get_ticks() >= pending[0]:
                self.current_scene.pending = None
                pending[1]()

            # Adjust mouse pos to virtual resolution
            raw_mouse_pos = pygame.mouse.get_pos()
            mouse_pos = (
                raw_mouse_pos[0] * self.WIDTH / self.real_width,
                raw_mouse_pos[1] * self.HEIGHT / self.real_height
            )
            hover = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and not WEB:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not getattr(self.current_scene, 'pending', None):
                    click_pos = (
                        event.pos[0] * self.WIDTH / self.real_width,
                        event.pos[1] * self.HEIGHT / self.real_height
                    )

                    if self.current_scene.show_dialogue:
                        if self.current_scene.text_rect.collidepoint(click_pos):
                            self.current_scene.click_dialogue()
                        continue

                    if not self.current_scene.show_dialogue:
                        if event.button == 1:
                            for item in self.inventory.items:
                                if item.rect.collidepoint(click_pos):
                                    self.inventory.select_item(item)
                                    selected_item = item
                                    break

                        for obj in self.current_scene.objects:
                            if obj.rect.collidepoint(click_pos):
                                obj.interact(self.inventory)
                                break

                        for box in self.current_scene.boxes:
                            if pygame.Rect(box.x, box.y, box.width, box.height).collidepoint(click_pos):
                                self.current_scene = box.next_scene
                                break

                        for slot in self.current_scene.slots:
                            if slot.rect.collidepoint(click_pos) and selected_item:
                                if slot.try_use_item(selected_item, self.inventory):
                                    self.inventory.selected_item = None
                                    break

            for box in self.current_scene.boxes:
                if pygame.Rect(box.x, box.y, box.width, box.height).collidepoint(mouse_pos):
                    hover = True
                    break

            new_scene = self.current_scene.render(self.virtual_screen, self.inventory)
            if new_scene is not None:
                self.current_scene = new_scene

            if hover:
                pygame.mouse.set_visible(False)
                self.virtual_screen.blit(hand_cursor, (mouse_pos[0] - hand_cursor.get_width() // 2,
                                                       mouse_pos[1] - hand_cursor.get_height() // 2))
            else:
                pygame.mouse.set_visible(True)

            # Desktop uses a virtual resolution and needs scaling. In the
            # browser virtual_screen is the window itself, so scaling it again
            # would waste a large amount of CPU every frame.
            if not WEB:
                scaled_surface = pygame.transform.scale(
                    self.virtual_screen,
                    (self.real_width, self.real_height),
                )
                self.window.blit(scaled_surface, (0, 0))

            pygame.display.flip()
            await asyncio.sleep(0)  # let the browser draw the frame

        pygame.quit()
        sys.exit()
