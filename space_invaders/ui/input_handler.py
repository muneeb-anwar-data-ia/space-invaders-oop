import pygame

from space_invaders.core.game import Game


class InputHandler:
    """Traduit les événements Pygame en commandes pour le jeu."""

    def process_events(self, game: Game) -> bool:
        """Traite les événements en attente. Retourne False si l'utilisateur quitte."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.player.move_left()
                elif event.key == pygame.K_RIGHT:
                    game.player.move_right()
                elif event.key == pygame.K_SPACE:
                    game.trigger_fire()

            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    game.player.stop()

        return True