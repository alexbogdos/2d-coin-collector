from scripts.game import *
from scripts.levels import set_globals

screen = pyg.display.set_mode((screenW, screenH))
window = pyg.display.set_mode((pyg.display.Info().current_w, pyg.display.Info().current_h), pyg.FULLSCREEN)
background_rect = pyg.Rect(0, 0, 300, 500)
background_rect.center = center
zen_mode = False
while True:
    screen.fill((191, 90, 242))
    pyg.mouse.set_visible(True)

    if zen_mode:
        zen_mode_str = "on"
    else:
        zen_mode_str = "off"

    pyg.draw.rect(screen, (44, 44, 46), background_rect, border_radius=30)
    write_text(screen, "MAIN MENU", (center[0], center[1] - 120), font_56, "", 0)
    button_play = Button(screen, (center[0], center[1] + 20), (240, 60), 40)  # button return
    button_play.collide(pyg.mouse.get_pos())
    button_play.show("Play")
    button_zen_mode = Button(screen, (center[0], center[1] + 100), (240, 60), 40)  # button main menu
    button_zen_mode.collide(pyg.mouse.get_pos())
    button_zen_mode.show("Zen mode: " + zen_mode_str)
    button_quit = Button(screen, (center[0], center[1] + 180), (240, 60), 40)  # button quit
    button_quit.collide(pyg.mouse.get_pos())
    button_quit.show("Quit")

    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            pyg.quit()
            sys.exit()
        elif event.type == pyg.KEYDOWN:
            if event.key == pyg.K_ESCAPE:
                pyg.quit()
                sys.exit()
        elif event.type == pyg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if button_play.collision:
                    set_globals()
                    game(zen_mode)
                elif button_zen_mode.collision:
                    zen_mode = not zen_mode
                elif button_quit.collision:
                    pyg.quit()
                    sys.exit()

    screen = pyg.transform.scale(screen, (pyg.display.Info().current_w, pyg.display.Info().current_h))
    window.blit(screen, (0, 0))
    pyg.display.update()
