import math
import random

from space_invaders import config


class Entity:
    """Classe de base pour tout objet positionnable sur la carte."""

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def distance_to(self, other: "Entity") -> float:
        """Calcule la distance euclidienne entre cette entité et une autre."""
        return math.hypot(self.x - other.x, self.y - other.y)


class Player(Entity):
    """Représente le vaisseau contrôlé par le joueur."""

    def __init__(self, x: float = config.PLAYER_START_X, y: float = config.PLAYER_START_Y) -> None:
        super().__init__(x, y)
        self.vx: float = 0.0

    def move_left(self) -> None:
        self.vx = -config.PLAYER_SPEED

    def move_right(self) -> None:
        self.vx = config.PLAYER_SPEED

    def stop(self) -> None:
        self.vx = 0.0

    def update(self) -> None:
        """Met à jour la position horizontale en respectant les bords."""
        self.x += self.vx
        if self.x < config.PLAYER_MIN_X:
            self.x = config.PLAYER_MIN_X
        elif self.x > config.PLAYER_MAX_X:
            self.x = config.PLAYER_MAX_X


class Enemy(Entity):
    """Représente un ennemi de la flotte."""

    def __init__(self, x: float | None = None, y: float | None = None) -> None:
        spawn_x = float(random.randint(config.ENEMY_MIN_X, config.ENEMY_MAX_X)) if x is None else x
        spawn_y = float(random.randint(config.ENEMY_SPAWN_MIN_Y, config.ENEMY_SPAWN_MAX_Y)) if y is None else y
        super().__init__(spawn_x, spawn_y)
        self.vx: float = config.ENEMY_SPEED_X
        self.step_y: float = config.ENEMY_STEP_Y

    def respawn(self) -> None:
        """Replace l'ennemi en haut de l'écran après avoir été touché."""
        self.x = float(random.randint(config.ENEMY_MIN_X, config.ENEMY_MAX_X))
        self.y = float(random.randint(config.ENEMY_SPAWN_MIN_Y, config.ENEMY_SPAWN_MAX_Y))
        self.vx = config.ENEMY_SPEED_X

    def update(self) -> None:
        """Avance horizontalement et descend d'un palier en touchant un bord."""
        self.x += self.vx
        if self.x <= config.ENEMY_MIN_X:
            self.vx = abs(self.vx)
            self.y += self.step_y
        elif self.x >= config.ENEMY_MAX_X:
            self.vx = -abs(self.vx)
            self.y += self.step_y


class Bullet(Entity):
    """Représente le projectile du joueur (états : 'ready' ou 'fire')."""

    def __init__(self) -> None:
        super().__init__(0.0, float(config.BULLET_START_Y))
        self.vy: float = float(config.BULLET_SPEED_Y)
        self.state: str = "ready"

    def is_ready(self) -> bool:
        return self.state == "ready"

    def is_fired(self) -> bool:
        return self.state == "fire"

    def fire_from(self, player: Player) -> bool:
        """Déclenche le tir depuis la position du joueur si disponible."""
        if not self.is_ready():
            return False
        self.x = player.x + config.BULLET_OFFSET_X
        self.y = player.y + config.BULLET_OFFSET_Y
        self.state = "fire"
        return True

    def reset(self) -> None:
        """Ramène le projectile à l'état prêt."""
        self.y = float(config.BULLET_START_Y)
        self.state = "ready"

    def update(self) -> None:
        """Fait monter le projectile lorsqu'il est tiré."""
        if self.is_fired():
            self.y -= self.vy
            if self.y <= 0:
                self.reset()