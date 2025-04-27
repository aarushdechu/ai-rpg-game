import pygame

def handle_events(buttons):
    """
    Handles Pygame events.
    Checks if any button is clicked and returns the action name.
    """
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    action = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "quit"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "quit"

    # Check if any button was clicked
    for button in buttons:
        if button.is_clicked(mouse_pos, mouse_pressed):
            action = button.action

    return action
