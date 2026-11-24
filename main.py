from space_invaders.core.game import Game
from space_invaders.ui.input_handler import InputHandler
from space_invaders.ui.renderer import PygameRenderer


def main() -> None:
    game = Game()
    input_handler = InputHandler()
    renderer = PygameRenderer()

    running = True
    try:
        while running:
            running = input_handler.process_events(game)
            events = game.update()
            renderer.play_events(events)
            renderer.render(game)
    finally:
        renderer.quit()


if __name__ == "__main__":
    main()