class Shoot:
    def __init__(self, weapon, x, y, turn_angle, damage, width, height, speed, sprite):
        self.weapon = weapon
        self.x = x
        self.y = y
        self.speed = speed
        self.width = width
        self.height = height
        self.turn_angle = turn_angle
        self.damage = damage
        self.sprite = sprite

    def set_coordinates(self, x, y):
        self.x = x
        self.y = y
