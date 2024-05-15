import json
import os
import re
import pygame
from Model.EnemyData import EnemyData
from Model.WaveData import WaveData
class ConfigurationManager:

    def sort_list(self,input_list):
        # Разделение элементов на две группы: с цифрами в начале и без цифр
        with_digits = []
        without_digits = []
        for item in input_list:
            item=os.path.splitext(item)[0]
            if re.match(r'^\d+', item):
                with_digits.append(item)
            else:
                without_digits.append(item)

        # Сортировка элементов с цифрами в начале по числовому значению
        with_digits.sort(key=lambda x: int(re.match(r'^\d+', x).group(0)))

        # Сортировка элементов без цифр в начале по алфавиту
        without_digits.sort()

        # Объединение отсортированных списков
        sorted_list = with_digits + without_digits

        return sorted_list

    def process_characters_in_folder(self):
        alien_type_dict={}
        folder_path = "../configurations/characters"
        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):
                character_name = os.path.splitext(filename)[0]
                character_data = self.load_character(character_name)
                lives = character_data.get("lives", 1)
                speed = character_data.get("speed", 1)
                value = character_data.get("value", 50)
                description = character_data.get("description", "")
                new_alien_data = EnemyData(character_name, speed, value, lives, description)
                alien_type_dict[character_name] = new_alien_data
        return alien_type_dict


    def process_wave_in_folder(self):
        waves_dict = {}
        folder_path = "../configurations/waves"
        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):
                wave_name = os.path.splitext(filename)[0]
                wave_data = self.load_wave(wave_name)
                if wave_data:
                    if wave_data=="error":
                        continue
                    description=""
                    obstacles_data = wave_data.get("obstacles", {})
                    obstacles = (obstacles_data.get("shape"), obstacles_data.get("count", 0))
                    duration = wave_data.get("duration", 0) * 1000
                    background_color = wave_data.get("background color",None)

                    if duration!=0:
                        description += f"Время: {duration//1000} с "
                    else:
                        description +="Без времени "
                    if obstacles[1]!=0:
                        description+=f"Кол. препятсвий: {obstacles[1]} "
                    else:
                        description+="Без препятсвий "
                    enemies = []
                    description +="Враги: "
                    for enemy_data in wave_data.get("enemies", []):
                        alien_type = enemy_data.get("type", "Alien")
                        enemy_info = {"type": alien_type}

                        description +=alien_type

                        if alien_type in ("Extra", "Generator"):
                            interval = enemy_data.get("interval")
                            if interval is not None:
                                enemy_info.update({"interval": interval})
                        else:
                            generate_type = enemy_data.get("generate_type")
                            if generate_type:
                                enemy_info.update({"generate_type": generate_type})
                                if generate_type == "matrix":
                                    enemy_info.update(
                                        {"rows": enemy_data.get("rows", 1), "columns": enemy_data.get("columns", 1)})
                                elif generate_type == "spawning":
                                    enemy_info["interval"] = enemy_data.get("interval", 20000)
                        description +=","
                        enemies.append(enemy_info)
                    description=description[: -1]
                    waves_dict[wave_name] = WaveData(wave_name, duration, enemies, obstacles, background_color,description)

        return waves_dict

    def load_wave(self, wave_name):
        wave_filename = os.path.join("../configurations/waves", f"{wave_name}.json")
        try:
            if os.path.exists(wave_filename):
                with open(wave_filename, encoding='utf-8') as f:
                    return json.load(f)
            else:
                return []
        except:
            return "error"

    def load_character(self,character_name):
        character_filename=os.path.join("../configurations/characters", f"{character_name}.json")
        if os.path.exists(character_filename):
            with open(character_filename) as f:
                return json.load(f)
        else:
            return []

    def load_images(self,image_folder):
        images = []
        image_files = os.listdir(image_folder)
        for filename in image_files:
            path = os.path.join(image_folder, filename)
            sprite_image=pygame.image.load(path).convert_alpha()
            scaled_sprite =pygame.transform.scale(sprite_image, (sprite_image.get_width() * 3, sprite_image.get_height() * 3))
            images.append(scaled_sprite)
        return images




