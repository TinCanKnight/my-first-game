import pygame
import random
import math

# change something

pygame.init()

# -----------------------------
# 기본 설정
# -----------------------------
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fancy Particle Playground - Improved")
clock = pygame.time.Clock()

MAX_PARTICLES = 1200
particles = []

# 알파 블렌딩용 임시 레이어
glow_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)


# -----------------------------
# 유틸 함수
# -----------------------------
def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))


def lerp(a, b, t):
    return a + (b - a) * t


# -----------------------------
# 파티클 클래스
# -----------------------------
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(1.5, 5.5)

        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

        self.max_life = random.randint(45, 90)
        self.life = self.max_life

        self.start_size = random.uniform(4, 9)
        self.size = self.start_size

        # 좀 더 예쁜 파스텔/네온 계열 팔레트
        palette = [
            (255, 120, 180),  # pink
            (255, 180, 120),  # peach
            (180, 255, 200),  # mint
            (140, 220, 255),  # sky
            (220, 180, 255),  # purple
            (255, 240, 160),  # warm yellow
        ]
        self.color = random.choice(palette)

        # 미세한 흔들림용
        self.wobble = random.uniform(0, math.pi * 2)

    def update(self):
        # 위치 업데이트
        self.x += self.vx
        self.y += self.vy

        # 중력
        self.vy += 0.06

        # 살짝 공기저항
        self.vx *= 0.992
        self.vy *= 0.992

        # 미세한 흔들림
        self.wobble += 0.15
        self.x += math.sin(self.wobble) * 0.25

        # 수명 감소
        self.life -= 1

        # 수명에 따라 크기 감소
        life_ratio = self.life / self.max_life
        self.size = max(1, self.start_size * life_ratio)

    def draw(self, surf, glow_surf):
        if self.life <= 0:
            return

        life_ratio = self.life / self.max_life

        # 알파값
        alpha = int(255 * life_ratio)
        alpha = clamp(alpha, 0, 255)

        # 중심 점
        core_color = (*self.color, alpha)

        # 바깥 glow
        glow_alpha = int(90 * life_ratio)
        glow_color = (*self.color, glow_alpha)

        px, py = int(self.x), int(self.y)
        core_radius = int(self.size)
        glow_radius = int(self.size * 2.5)

        # glow 먼저
        pygame.draw.circle(glow_surf, glow_color, (px, py), glow_radius)

        # 중심 파티클
        pygame.draw.circle(glow_surf, core_color, (px, py), core_radius)

        # 핵심 밝은 점
        bright_alpha = int(200 * life_ratio)
        bright_color = (255, 255, 255, bright_alpha)
        pygame.draw.circle(glow_surf, bright_color, (px, py), max(1, core_radius // 2))

    def alive(self):
        return self.life > 0 and -50 < self.x < WIDTH + 50 and -50 < self.y < HEIGHT + 50


# -----------------------------
# 배경 그리기
# -----------------------------
def draw_background(surface, t):
    # 위->아래 그라데이션 + 시간에 따라 살짝 움직이는 색 변화
    for y in range(HEIGHT):
        ratio = y / HEIGHT

        r = int(lerp(15, 45, ratio) + 10 * math.sin(t + y * 0.01))
        g = int(lerp(20, 90, ratio) + 20 * math.sin(t * 0.8 + y * 0.015))
        b = int(lerp(50, 140, ratio) + 15 * math.sin(t * 1.2 + y * 0.02))

        r = clamp(r, 0, 255)
        g = clamp(g, 0, 255)
        b = clamp(b, 0, 255)

        pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))

    # 은은한 물결 원
    for i in range(5):
        radius = 80 + i * 70 + int(10 * math.sin(t * 2 + i))
        x = WIDTH // 2 + int(math.sin(t * 0.7 + i) * 180)
        y = HEIGHT // 2 + int(math.cos(t * 0.9 + i * 0.5) * 100)

        color = (
            clamp(80 + i * 15, 0, 255),
            clamp(120 + i * 10, 0, 255),
            clamp(180 + i * 8, 0, 255),
            20
        )

        temp = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.circle(temp, color, (x, y), radius, width=2)
        surface.blit(temp, (0, 0))


# -----------------------------
# 메인 루프
# -----------------------------
running = True
time_value = 0

while running:
    dt = clock.tick(60) / 1000.0
    time_value += 1.5 * dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse = pygame.mouse.get_pos()
    buttons = pygame.mouse.get_pressed()

    # 배경
    draw_background(screen, time_value)

    # 마우스 누르고 있으면 파티클 생성
    if buttons[0]:
        spawn_count = 10
        for _ in range(spawn_count):
            if len(particles) < MAX_PARTICLES:
                # 약간 퍼진 위치에서 생성
                offset_x = random.uniform(-8, 8)
                offset_y = random.uniform(-8, 8)
                particles.append(Particle(mouse[0] + offset_x, mouse[1] + offset_y))

    # glow surface를 완전히 지우지 않고 살짝만 덮어서 잔상 효과
    glow_surface.fill((0, 0, 0, 35))

    # 파티클 업데이트 & 그리기
    for p in particles:
        p.update()
        p.draw(screen, glow_surface)

    particles = [p for p in particles if p.alive()]

    # glow 합성
    screen.blit(glow_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

    # 간단한 안내문
    font = pygame.font.SysFont("consolas", 20)
    text = font.render(
        f"Hold Left Mouse Button  |  Particles: {len(particles)}",
        True,
        (240, 240, 255)
    )
    screen.blit(text, (20, 20))

    pygame.display.flip()

pygame.quit()