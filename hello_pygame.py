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
# 원의 반지름
circle_radius = 50
#원의 속도
base_speed = 4
dash_speed = 8

# 에너지 시스템 설정
energy = 100
max_energy = 100
#대쉬 가능 여부
can_dash = True 

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0) # 에너지 바 색상용

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    #키보드 입력 확인
    keys = pygame.key.get_pressed()
    
    #대쉬 가능 상태 체크 (에너지가 10 이하로 떨어지면 잠금)
    if energy <= 10:
        can_dash = False
    #에너지가 다시 100(최대치)이 되면 잠금 해제
    if energy >= max_energy:
        can_dash = True
    
    #대쉬 상태 판정
    is_dashing = (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and energy > 0 and can_dash
    
    #대쉬 상태에 따른 속도와 색상 결정
    if is_dashing:#대쉬중
        current_speed = dash_speed
        circle_color = RED
    elif not can_dash:#대쉬 불가능
        current_speed = base_speed
        circle_color = (150, 150, 150)
    else:#평상시
        current_speed = base_speed
        circle_color = BLUE
    
    moved = False
    if keys[pygame.K_LEFT]:
        circle_x -= current_speed
        moved = True
    if keys[pygame.K_RIGHT]:
        circle_x += current_speed
        moved = True
    if keys[pygame.K_UP]:
        circle_y -= current_speed
        moved = True
    if keys[pygame.K_DOWN]:
        circle_y += current_speed
        moved = True
        
    # 이동 중이면서 대쉬 상태일 때만 에너지 소모 (틱당 1)
    if is_dashing and moved:
        energy -= 1
        if energy < 0: energy = 0
    # 대쉬 중이 아닐 때 에너지 회복 (틱당 1, 최대 100)
    elif not is_dashing:
        energy += 1
        if energy > max_energy: energy = max_energy
        
    #화면 경계 제한
    circle_x = max(circle_radius, min(SCREEN_WIDTH - circle_radius, circle_x))
    circle_y = max(circle_radius, min(SCREEN_HEIGHT - circle_radius, circle_y))
        
    #화면 채우기
    screen.fill(WHITE)
    # 원 그리기 (상태에 따라 색상 변경)
    pygame.draw.circle(screen, circle_color, (int(circle_x), int(circle_y)), circle_radius)
    
    # 에너지 UI 표시 (텍스트 + 바)
    energy_text = font.render(f"Energy: {energy}", True, BLACK)
    screen.blit(energy_text, (10, 40))
    # 에너지 바 배경
    pygame.draw.rect(screen, BLACK, (10, 70, 100, 10), 2)
    # 에너지 바 내용물
    pygame.draw.rect(screen, GREEN, (10, 70, energy, 10))
    
    #FPS 표시
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, BLACK)
    screen.blit(fps_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()