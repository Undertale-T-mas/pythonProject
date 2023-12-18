from core import *
from Resources.ResourceLoad import *


pygame.init()
pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

surf = pygame.image.load('test.png').convert_alpha()
w, h = surf.get_size()
surf = pygame.transform.scale(surf, vec2(600.0 / h * w, 600.0))
texture = Texture(surf)
surf2 = pygame.image.load('test2.png').convert_alpha()
w2, h2 = surf.get_size()
surf2 = pygame.transform.scale(surf2, vec2(600.0 / h * w, 600.0))
texture2 = Texture(surf2)
t = 0.0

render_target = RenderTarget(800, 600)
screen_target = RenderTarget(800, 600, True)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    GamingGL.begin(vec2(800, 600))

    render_target.clear(cv4.BLACK)

    texture.draw(RenderData(vec2(0, 0), bound=FRect(300 + Math.sin_deg(t * 90) * 222, 0, 500, 500)))
    texture2.draw(RenderData(vec2(0, 0)))

    screen_target.clear(cv4.TRANSPARENT)
    GamingGL.screen_transform(vec2(800, 600))
    screen_target.blit_data(render_target, RenderData(vec2(0, 0), color=cv4.RED))

 #   texture.draw(RenderData(vec2(0, 0), bound=FRect(300 + Math.sin_deg(t * 90) * 222, 0, 500, 500)))
 #   texture2.draw(RenderData(vec2(0, 0)))

    pygame.display.flip()
    t += clock.tick(60) / 1000

    GamingGL.end()
