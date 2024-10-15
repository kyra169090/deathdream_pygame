from scenes import *

# Initialize scenes with the appropriate images
start_scene = Start(pygame.image.load('../assets/images/scenes/location1/location1_abandoned_city_1_1.jpg'))
city_part1_door = CityPart1Door(pygame.image.load('../assets/images/scenes/location1/location1_abandoned_city_1_2.jpg'))
city_part1_corridor = CityPart1Corridor(pygame.image.load('../assets/images/scenes/location1/location1_abandoned_city_1_3.jpg'))
city_part1_livingroom = CityPart1LivingRoom(pygame.image.load('../assets/images/scenes/location1/location1_abandoned_city_1_4.jpg'))
city_part1_pantry = CityPart1Pantry(pygame.image.load('../assets/images/scenes/location1/location1_abandoned_city_1_5_dark.jpg'), pygame.image.load('../assets/images/scenes/location1/location1_abandoned_city_1_5.jpg'))
city_part4_street1 = CityPart4Street1(pygame.image.load('../assets/images/scenes/location4/city_part_4_1.jpg'))
city_part2 = CityPart2(pygame.image.load('../assets/images/scenes/location2/location2_abandoned_city_1_1.jpg'), game_state, next_scene=city_part4_street1)
city_part2_shop = CityPart2Shop(pygame.image.load('../assets/images/scenes/location2/location2_abandoned_city_1_2.jpg'))
city_part2_shop_shelf = CityPart2ShopShelf(pygame.image.load('../assets/images/scenes/location2/location2_abandoned_city_shelf.jpg'))
city_part3 = CityPart3(pygame.image.load('../assets/images/scenes/location3/city_part_3_girl_int_the_wall_1_1.jpg'))
city_part3_corridor = CityPart3Corridor(pygame.image.load('../assets/images/scenes/location3/city_part_3_girl_int_the_wall_1_3.jpg'))
city_part3door = CityPart3Door(pygame.image.load('../assets/images/scenes/location3/city_part_3_girl_int_the_wall_1_2.jpg'), next_scene=city_part3_corridor)
city_part3_room_letter = CityPart3RoomLetter(pygame.image.load('../assets/images/scenes/location3/city_part_3_girl_int_the_wall_1_4_after_letter_v3.jpg'))
city_part3_room = CityPart3Room(pygame.image.load('../assets/images/scenes/location3/city_part_3_girl_int_the_wall_1_4.jpg'), pygame.image.load('../assets/images/scenes/location3/city_part_3_girl_int_the_wall_1_4_after.jpg'), next_scene=city_part3_room_letter)

# WARDROBE
city_part3_wardrobe_photo1 = CityPart3Photo1(pygame.image.load('../assets/images/scenes/location3/city_part_3_girl_int_the_wall_1_3_1_wardrobe_photo1.jpg'), game_state)
city_part3_wardrobe_photo2 = CityPart3Photo2(pygame.image.load('../assets/images/scenes/location3/city_part_3_girl_int_the_wall_1_3_1_wardrobe_photo2.jpg'), game_state)
city_part3_corridor_wardrobe_letter = CityPart3CorridorWardrobeLetter(pygame.image.load('../assets/images/scenes/location3/city_part_3_girl_int_the_wall_1_3_1_wardrobe_open_2.jpg'), game_state)
city_part3_corridor_wardrobe = CityPart3CorridorWardrobe(pygame.image.load('../assets/images/scenes/location3/city_part_3_girl_int_the_wall_1_3_1_wardrobe_closed.jpg'), pygame.image.load('../assets/images/scenes/location3/city_part_3_girl_int_the_wall_1_3_1_wardrobe_open.jpg'), next_scene1=city_part3_wardrobe_photo1, next_scene2=city_part3_wardrobe_photo2, next_scene3=city_part3_corridor_wardrobe_letter)

# City Part4
city_part4_street2 = CityPart4Street2(pygame.image.load('../assets/images/scenes/location4/city_part_4_2.jpg'))
city_part4_street3 = CityPart4Street3(pygame.image.load('../assets/images/scenes/location4/city_part_4_3.jpg'))
city_part4_familyhouse = CityPart4FamilyHouse(pygame.image.load('../assets/images/scenes/location4/city_part_4_4.jpg'))
city_part4_familyhouseyard = CityPart4FamilyHouseYard(pygame.image.load('../assets/images/scenes/location4/city_part_4_5.jpg'))
city_part4_familyhousefirstroom = CityPart4FamilyHouseFirstRoom(pygame.image.load('../assets/images/scenes/location4/city_part_4_6.jpg'))
city_part4_familyhousesecondroom = CityPart4FamilyHouseSecondRoom(pygame.image.load('../assets/images/scenes/location4/city_part_4_6_1.jpg'))
city_part4_familyhousethirdroom = CityPart4FamilyHouseThirdRoom(pygame.image.load('../assets/images/scenes/location4/city_part_4_6_2.jpg'))
city_part4_familyhousebasement = CityPart4FamilyHouseBasement(pygame.image.load('../assets/images/scenes/location4/city_part_4_7.jpg'))
city_part4_familyhousebasementholeintheground = CityPart4FamilyHoleInTheGround(pygame.image.load('../assets/images/scenes/location4/city_part_4_8_2.jpg'))
city_part4_familyhousebasement2 = CityPart4FamilyHouseBasement2(pygame.image.load('../assets/images/scenes/location4/city_part_4_8_1.jpg'), pygame.image.load('../assets/images/scenes/location4/city_part_4_8_1_after.jpg'), next_scene=city_part4_familyhousebasementholeintheground)
city_part4_familyhousebasement3 = CityPart4FamilyHouseBasement3(pygame.image.load('../assets/images/scenes/location4/city_part_4_9.jpg'))
city_part4_familyhousebasement3letter = CityPart4FamilyHouseBasement3Letter(pygame.image.load('../assets/images/scenes/location4/city_part_4_9_letter.jpg'))
city_part_4_8_3 = CityPart4Cave1(pygame.image.load('../assets/images/scenes/location4/city_part_4_8_3.jpg'))
city_part_4_8_4 = CityPart4Cave2(pygame.image.load('../assets/images/scenes/location4/city_part_4_8_4.jpg'))
city_part_4_8_3_letter = CityPart4Cave1Letter(pygame.image.load('../assets/images/scenes/location4/city_part_4_8_3_letter.jpg'))


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
city_part3_corridor.boxes[2].next_scene = city_part3_corridor_wardrobe
city_part3_room.boxes[0].next_scene = city_part3_corridor
city_part3_room_letter.boxes[0].next_scene = city_part3_room
city_part3_room_letter.boxes[1].next_scene = city_part3_room
# citypart3wardrobe
city_part3_corridor_wardrobe.boxes[0].next_scene = city_part3_corridor
city_part3_wardrobe_photo1.boxes[0].next_scene = city_part3_corridor_wardrobe
city_part3_wardrobe_photo2.boxes[0].next_scene = city_part3_corridor_wardrobe
city_part3_corridor_wardrobe_letter.boxes[0].next_scene = city_part3_corridor_wardrobe

city_part4_street1.boxes[0].next_scene = city_part4_street2
city_part4_street2.boxes[0].next_scene = city_part4_street3
city_part4_street3.boxes[0].next_scene = city_part4_familyhouse
city_part4_familyhouse.boxes[0].next_scene = city_part4_familyhouseyard
city_part4_familyhouseyard.boxes[0].next_scene = city_part4_familyhousefirstroom
city_part4_familyhousefirstroom.boxes[0].next_scene = city_part4_familyhousesecondroom
city_part4_familyhousefirstroom.boxes[1].next_scene = city_part4_familyhousebasement
city_part4_familyhousefirstroom.boxes[2].next_scene = city_part4_familyhouseyard
city_part4_familyhousesecondroom.boxes[0].next_scene = city_part4_familyhousethirdroom
city_part4_familyhousesecondroom.boxes[1].next_scene = city_part4_familyhousefirstroom
city_part4_familyhousethirdroom.boxes[0].next_scene = city_part4_familyhousesecondroom
city_part4_familyhousebasement.boxes[0].next_scene = city_part4_familyhousebasement2
city_part4_familyhousebasement.boxes[1].next_scene = city_part4_familyhousefirstroom
city_part4_familyhousebasement2.boxes[0].next_scene = city_part4_familyhousebasement
city_part4_familyhousebasement2.boxes[1].next_scene = city_part4_familyhousebasement3
city_part4_familyhousebasement3.boxes[0].next_scene = city_part4_familyhousebasement2
city_part4_familyhousebasement3.boxes[1].next_scene = city_part4_familyhousebasement3letter
city_part4_familyhousebasement3letter.boxes[0].next_scene = city_part4_familyhousebasement3
city_part4_familyhousebasementholeintheground.boxes[0].next_scene = city_part4_familyhousebasement2
city_part4_familyhousebasementholeintheground.boxes[1].next_scene = city_part_4_8_3
city_part_4_8_3.boxes[0].next_scene = city_part_4_8_4
city_part_4_8_4.boxes[0].next_scene = city_part_4_8_3