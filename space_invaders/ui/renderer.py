from pathlib import Path
from typing import Optional

import pygame
from pygame import mixer

from space_invaders import config
from space_invaders.core.game import Game, StepEvents
from space_invaders.core.entities import FastEnemy


class PygameRenderer:
    """Gère la fenêtre Pygame, le chargement des ressources et le rendu du jeu."""

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption(config.GAME_TITLE)

        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))

        if config.ICON_IMAGE.exists():
            icon = pygame.image.load(str(config.ICON_IMAGE))
            pygame.display.set_icon(icon)

        self.background = pygame.image.load(str(config.BACKGROUND_IMAGE))
        self.player_img = pygame.image.load(str(config.PLAYER_IMAGE))
        self.enemy_img = pygame.image.load(str(config.ENEMY_IMAGE))
        self.fast_enemy_img = pygame.image.load(str(config.UFO_IMAGE))
        self.bullet_img = pygame.image.load(str(config.BULLET_IMAGE))

        self.score_font = pygame.font.Font("freesansbold.ttf", config.SCORE_FONT_SIZE)
        self.game_over_font = pygame.font.Font("freesansbold.ttf", config.GAME_OVER_FONT_SIZE)

        self.laser_sound = self._load_sound(config.LASER_SOUND)
        self.explosion_sound = self._load_sound(config.EXPLOSION_SOUND)
        self._init_music()

    def _load_sound(self, path: Path) -> Optional[mixer.Sound]:
        """Charge un effet sonore s'il existe sur le disque."""
        if path.exists():
            try:
                return mixer.Sound(str(path))
            except pygame.error:
                return None
        return None

    def _init_music(self) -> None:
        """Démarre la musique de fond si le fichier audio existe."""
        if config.BACKGROUND_MUSIC.exists():
            try:
                if not mixer.get_init():
                    mixer.init()
                mixer.music.load(str(config.BACKGROUND_MUSIC))
                mixer.music.play(-1)
            except pygame.error:
                pass

    def play_events(self, events: StepEvents) -> None:
        """Déclenche les effets sonores associés aux événements du jeu."""
        if events.shot_fired and self.laser_sound is not None:
            self.laser_sound.play()
        if events.enemy_hit and self.explosion_sound is not None:
            self.explosion_sound.play()

    def render(self, game: Game) -> None:
        """Dessine l'état courant du jeu puis rafraîchit l'écran."""
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))

        for enemy in game.enemies:
            if isinstance(enemy, FastEnemy):
                self.screen.blit(self.fast_enemy_img, (enemy.x, enemy.y))
            else:
                self.screen.blit(self.enemy_img, (enemy.x, enemy.y))

        if game.bullet.is_fired():
            self.screen.blit(self.bullet_img, (game.bullet.x, game.bullet.y))

        if game.power_bullet.is_fired():
            pygame.draw.rect(self.screen, (255, 220, 0),
                             (game.power_bullet.x, game.power_bullet.y, 8, 18))

        self.screen.blit(self.player_img, (game.player.x, game.player.y))

        score_surface = self.score_font.render(f"Score : {game.score}", True, (255, 255, 255))
        self.screen.blit(score_surface, (config.SCORE_POS_X, config.SCORE_POS_Y))

        if game.game_over:
            over_surface = self.game_over_font.render("GAME OVER", True, (255, 255, 255))
            self.screen.blit(over_surface, (config.GAME_OVER_POS_X, config.GAME_OVER_POS_Y))

        pygame.display.update()

    def quit(self) -> None:
        """Ferme proprement Pygame."""
        pygame.quit()