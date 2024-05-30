from pygame import Surface
from pygame.sprite import Sprite

from event import EatenEvent
from .sprites import TextObject
from .view import View
from ui.sprites.map_sprite import MapSprite
from config import config


class FruitIndex(Sprite):
    def __init__(
            self,
            x: int,
            y: int
    ):
        Sprite.__init__(self)
        self.fruit_sprites = []
        self.image = Surface((32, 6 * 32))
        self.rect = self.image.get_rect()
        self.funcs = []
        self.rect.bottomright = (x, y)

    def update(self, *args, **kwargs):
        self.image.fill(config["bg_color"])
        for i, sprite in enumerate(self.fruit_sprites):
            self.image.blit(sprite.image, (0, i * sprite.image.get_height()))


class GameplayView(View):
    def _build(self):
        from pygame.font import Font
        from pygame import Vector2

        score = TextObject(
            lambda: f"Score: {self.model.score}",
            font=Font(None, 30)
        )
        score.rect.move_ip(20, 5)

        lives = TextObject(
            lambda: f"Lives: {self.model.lives}",
            font=Font(None, 30)
        )
        lives.rect.move_ip(20, 30)

        self.fruit_index = FruitIndex(self.parent_view.width, self.parent_view.height)
        self.map_sprite = MapSprite(
            self.model.map_,
            Vector2(
                self.parent_view.width // 2,
                self.parent_view.height // 2
            )
        )
        self._sprite_group.add(
            score,
            lives,
            self.fruit_index,
            self.map_sprite
        )

        from event.event_manager import ev_manager
        ev_manager.add_handler(EatenEvent, self.__get_eaten_event_handler())

    def render(self, bg_color: int) -> Surface:
        menu_surface = Surface((self.parent_view.width, self.parent_view.height))
        menu_surface.fill(bg_color)
        self._sprite_group.update()
        self._sprite_group.draw(menu_surface)
        return menu_surface

    def __get_eaten_event_handler(self):
        from model.object import Fruit
        from .sprites.fruit_sprite import FruitSprite
        from ui.sprites.spritesheet import SpriteSheet
        from pygame import Vector2

        fruit_index = self.fruit_index

        def handler(event: EatenEvent):
            nonlocal fruit_index
            if isinstance(event.game_object, Fruit):
                event.game_object._position = Vector2(0, len(fruit_index.fruit_sprites))
                fruit_index.fruit_sprites.append(
                    FruitSprite(
                        event.game_object,
                        SpriteSheet(
                            r"resource/fruit.png",
                            (32, 32),
                            (32, 32)
                        )
                    )
                )

        return handler
