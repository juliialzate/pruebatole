def handle_collisions(vuelo, mirilla, num_balas, score, mouse_pos):
    collision_pos = None
    if vuelo.rect.collidepoint(mouse_pos):
        collision_pos = vuelo.rect.center
        vuelo.alive = False
        score += 100
    return num_balas, score, collision_pos
