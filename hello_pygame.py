import pygame
import sys

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My First Pygame")

# 기본 폰트와 크기 설정
font = pygame.font.SysFont("Arial", 24)

# 원의 초기 위치
circle_x = 400
circle_y = 300
# 원이 움직이는 픽셀 수
circle_speed = 5
# 원의 반지름
circle_radius = 50 

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    #키보드 입력 확인
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        circle_x -= circle_speed
    if keys[pygame.K_RIGHT]:
        circle_x += circle_speed
    if keys[pygame.K_UP]:
        circle_y -= circle_speed
    if keys[pygame.  K_DOWN]:
        circle_y += circle_speed
        
    # 화면 경계 제한 (Boundary Check)
    # 왼쪽/오른쪽 벽 체크
    if circle_x < circle_radius:
        circle_x = circle_radius
    elif circle_x > SCREEN_WIDTH - circle_radius:
        circle_x = SCREEN_WIDTH - circle_radius

    # 위쪽/아래쪽 벽 체크
    if circle_y < circle_radius:
        circle_y = circle_radius
    elif circle_y > SCREEN_HEIGHT - circle_radius:
        circle_y = SCREEN_HEIGHT - circle_radius
        
    #화면 채우기
    screen.fill(WHITE)
    #원 그리기
    pygame.draw.circle(screen, BLUE, (circle_x, circle_y), circle_radius)
    
    #FPS 표시
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, BLACK)
    screen.blit(fps_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()