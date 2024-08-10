import pygame
import json
import os

def load_scenes(width, height):
    # Correctly resolve the path to the JSON file
    json_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'locations', 'location1.json')
    
    with open(json_path) as f:
        data = json.load(f)

    scenes = []
    for scene_data in data["scenes"]:
        # Construct the full path to the background image
        background_image_path = os.path.join(os.path.dirname(__file__), '..', scene_data["background"])
        background_image = pygame.transform.scale(
            pygame.image.load(background_image_path),
            (width, height)
        )

        box = pygame.Rect(
            scene_data["box_position"]["x"],
            scene_data["box_position"]["y"],
            scene_data["box_position"]["width"],
            scene_data["box_position"]["height"]
        )

        scene = {
            "name": scene_data["name"],
            "background_image": background_image,
            "box": box,
            "next_scene": scene_data["next_scene"]
        }

        scenes.append(scene)
    return scenes
