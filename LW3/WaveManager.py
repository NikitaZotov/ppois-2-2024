import json

from Wave import Wave


class WaveManager:
    @staticmethod
    def load_waves_from_file(filename):
        waves = []
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                for wave_name, wave_data in data.items():
                    wave = Wave(wave_data["bat_spawn_time"], wave_data["skeleton_spawn_time"],
                                wave_data["ghost_spawn_time"], wave_data["werewolf_spawn_time"],
                                wave_data["zombie_spawn_time"])
                    waves.append(wave)
        except FileNotFoundError:
            pass
        except Exception as e:
            pass
        return waves
