from dataclasses import dataclass

from space_invaders import config
from space_invaders.core.entities import Bullet, Enemy, FastEnemy, Player


@dataclass
class StepEvents:
    """Événements survenus pendant une mise à jour de logique (pour le son/UI)."""

    shot_fired: bool = False
    enemy_hit: bool = False


class Game:
    """Gère la logique et l'état d'une partie de Space Invaders."""

    def __init__(self, num_enemies: int = config.NUM_ENEMIES) -> None:
        self.player = Player()
        self.enemies: list[Enemy] = []
        for i in range(num_enemies):
            if i % 3 == 0:
                self.enemies.append(FastEnemy())
            else:
                self.enemies.append(Enemy())
        self.bullet = Bullet()
        self.power_bullet = Bullet(config.POWER_BULLET_SPEED_Y)
        self.score: int = 0
        self.game_over: bool = False
        self._pending_shot_event: bool = False

    def trigger_fire(self) -> bool:
        """Demande au projectile de partir depuis le joueur si la partie est active."""
        if self.game_over:
            return False
        fired = self.bullet.fire_from(self.player)
        if fired:
            self._pending_shot_event = True
        return fired

    def trigger_power_fire(self) -> bool:
        """Déclenche le tir spécial si la partie est active."""
        if self.game_over:
            return False
        fired = self.power_bullet.fire_from(self.player)
        if fired:
            self._pending_shot_event = True
        return fired

    def _hide_enemies_for_game_over(self) -> None:
        """Éloigne les ennemis hors de l'écran en cas de défaite (comme dans le code initial)."""
        for enemy in self.enemies:
            enemy.y = float(config.ENEMY_HIDDEN_Y)
        self.game_over = True

    def update(self) -> StepEvents:
        """Fait avancer la logique d'une itération et renvoie les événements notables."""
        events = StepEvents(shot_fired=self._pending_shot_event)
        self._pending_shot_event = False

        if self.game_over:
            return events

        # 1. Déplacement du joueur
        self.player.update()

        # 2. Déplacement des ennemis, condition de défaite et collisions
        for enemy in self.enemies:
            if enemy.y > config.ENEMY_GAME_OVER_Y:
                self._hide_enemies_for_game_over()
                break

            enemy.update()

            if self.bullet.is_fired() and enemy.distance_to(self.bullet) < config.COLLISION_DISTANCE:
                events.enemy_hit = True
                self.bullet.reset()
                self.score += 1
                enemy.respawn()

            if self.power_bullet.is_fired() and enemy.distance_to(self.power_bullet) < config.POWER_COLLISION_DISTANCE:
                events.enemy_hit = True
                self.power_bullet.reset()
                self.score += 2
                enemy.respawn()

        # 3. Déplacement du projectile
        self.bullet.update()
        self.power_bullet.update()

        return events