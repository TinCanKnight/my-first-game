import pygame
import sys
import math
import base64
import io

pygame.init()

# 화면 크기
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AABB / Circle / OBB / SAT")

# 색상
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 180, 0)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)

# -----------------------------
# Base64 이미지
# -----------------------------
_ROCKET = (
    "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"
    "bmNvZGVyqAZ/7gAAAABJRU5ErkJggg=="
)

_STONE = (
    "iVBORw0KGgoAAAANSUhEUgAAAEYAAABGCAYAAABxLuKEAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFn"
    "ZVJlYWR5ccllPAAAAyFpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/"
    "IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6"
    "bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuNS1jMDE0IDc5LjE1MTQ4MSwgMjAxMy8w"
    "My8xMy0xMjowOToxNSAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9y"
    "Zy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIg"
    "eG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDov"
    "L25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20v"
    "eGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9w"
    "IENDIChXaW5kb3dzKSIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDo3NUZCNjNFQjczMzQxMUUzQjlD"
    "NUI3NDgxQTNDMkQ3OCIgeG1wTU06RG9jdW1lbnRJRD0ieG1wLmRpZDo3NUZCNjNFQzczMzQxMUUzQjlD"
    "NUI3NDgxQTNDMkQ3OCI+IDx4bXBNTTpEZXJpdmVkRnJvbSBzdFJlZjppbnN0YW5jZUlEPSJ4bXAuaWlk"
    "Ojc1RjNEOEQwNzMzNDExRTNCOUM1Qjc0ODFBM0MyRDc4IiBzdFJlZjpkb2N1bWVudElEPSJ4bXAuZGlk"
    "Ojc1RkI2M0VBNzMzNDExRTNCOUM1Qjc0ODFBM0MyRDc4Ii8+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3Jk"
    "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"
    "AAAAAElFTkSuQmCC"
)

def decode_base64_image(base64_string):
    image_bytes = base64.b64decode(base64_string)
    image_file = io.BytesIO(image_bytes)
    return pygame.image.load(image_file).convert_alpha()

#이미지 크기 자동 조정
def choose_scale(w, h):
    max_side = max(w, h)

    if max_side >= 180:
        return 0.4
    elif max_side >= 90:
        return 0.5
    else:
        return 1.0

#이미지 크기를 오브젝트 크기로
def load_base64_image_auto(base64_string):
    surface = decode_base64_image(base64_string)
    w, h = surface.get_size()

    scale = choose_scale(w, h)
    new_w = max(1, int(w * scale))
    new_h = max(1, int(h * scale))

    scaled = pygame.transform.smoothscale(surface, (new_w, new_h))
    return scaled, new_w, new_h

def get_rotated_corners(cx, cy, w, h, angle_deg):
    rad = math.radians(angle_deg)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    half_w = w / 2
    half_h = h / 2

    local_points = [
        (-half_w, -half_h),
        ( half_w, -half_h),
        ( half_w,  half_h),
        (-half_w,  half_h),
    ]

    world_points = []
    for lx, ly in local_points:
        rx = lx * cos_a - ly * sin_a
        ry = lx * sin_a + ly * cos_a
        world_points.append((cx + rx, cy + ry))

    return world_points

def dot(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1]

def subtract(p1, p2):
    return (p1[0] - p2[0], p1[1] - p2[1])

def normalize(v):
    length = math.hypot(v[0], v[1])
    if length == 0:
        return (0, 0)
    return (v[0] / length, v[1] / length)

def get_axes(points):
    axes = []
    count = len(points)

    for i in range(count):
        p1 = points[i]
        p2 = points[(i + 1) % count]

        edge = subtract(p2, p1)
        normal = (-edge[1], edge[0])
        normal = normalize(normal)
        axes.append(normal)

    return axes

def project_polygon(points, axis):
    projections = [dot(point, axis) for point in points]
    return min(projections), max(projections)

def overlap_on_axis(points1, points2, axis):
    min1, max1 = project_polygon(points1, axis)
    min2, max2 = project_polygon(points2, axis)
    return max1 >= min2 and max2 >= min1

def sat_collision(points1, points2):
    axes1 = get_axes(points1)
    axes2 = get_axes(points2)
    axes = axes1 + axes2

    for axis in axes:
        if not overlap_on_axis(points1, points2, axis):
            return False
    return True

def circle_collision(c1, r1, c2, r2):
    dx = c1[0] - c2[0]
    dy = c1[1] - c2[1]
    distance_sq = dx * dx + dy * dy
    radius_sum = r1 + r2
    return distance_sq <= radius_sum * radius_sum


# -----------------------------
# 이미지 로드 + 크기 자동 설정
# -----------------------------
player_surface, player_size_w, player_size_h = load_base64_image_auto(_ROCKET)
center_surface, center_size_w, center_size_h = load_base64_image_auto(_STONE)

# -----------------------------
# 이동하는 로켓
# -----------------------------
player_x = 100
player_y = 100
player_speed = 5

player_angle = 0
player_rotation_speed = 2

# -----------------------------
# 중앙 고정 돌
# -----------------------------
center_x = WIDTH // 2
center_y = HEIGHT // 2

rotation_angle = 0
base_rotation_speed = 1
boost_rotation_speed = 4


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # 이동
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    # 플레이어 회전
    if keys[pygame.K_a]:
        player_angle += player_rotation_speed
    if keys[pygame.K_s]:
        player_angle -= player_rotation_speed

    # 화면 밖 제한
    if player_x < 0:
        player_x = 0
    if player_x > WIDTH - player_size_w:
        player_x = WIDTH - player_size_w
    if player_y < 0:
        player_y = 0
    if player_y > HEIGHT - player_size_h:
        player_y = HEIGHT - player_size_h

    # 중앙 오브젝트 회전
    rotation_speed = base_rotation_speed
    if keys[pygame.K_z]:
        rotation_speed += boost_rotation_speed

    rotation_angle += rotation_speed
    if rotation_angle >= 360:
        rotation_angle -= 360

    # -----------------------------
    # 플레이어 Bounding
    # -----------------------------
    player_rect = pygame.Rect(player_x, player_y, player_size_w, player_size_h)
    player_center = player_rect.center
    player_radius = min(player_size_w, player_size_h) // 2

    player_obb = get_rotated_corners(
        player_rect.centerx,
        player_rect.centery,
        player_size_w,
        player_size_h,
        player_angle
    )

    player_rotated_surface = pygame.transform.rotate(player_surface, -player_angle)
    player_rotated_rect = player_rotated_surface.get_rect(center=player_rect.center)

    player_xs = [p[0] for p in player_obb]
    player_ys = [p[1] for p in player_obb]
    player_aabb = pygame.Rect(
        min(player_xs),
        min(player_ys),
        max(player_xs) - min(player_xs),
        max(player_ys) - min(player_ys)
    )

    # -----------------------------
    # 중앙 오브젝트 Bounding
    # -----------------------------
    rotated_surface = pygame.transform.rotate(center_surface, -rotation_angle)
    rotated_rect = rotated_surface.get_rect(center=(center_x, center_y))

    center_obb = get_rotated_corners(
        center_x,
        center_y,
        center_size_w,
        center_size_h,
        rotation_angle
    )

    xs = [p[0] for p in center_obb]
    ys = [p[1] for p in center_obb]
    center_aabb = pygame.Rect(
        min(xs),
        min(ys),
        max(xs) - min(xs),
        max(ys) - min(ys)
    )

    center_radius = min(center_size_w, center_size_h) // 2

    # -----------------------------
    # 충돌 판정
    # -----------------------------
    circle_hit = circle_collision(player_center, player_radius, (center_x, center_y), center_radius)
    aabb_hit = player_aabb.colliderect(center_aabb)
    obb_hit = sat_collision(player_obb, center_obb)

    # -----------------------------
    # 그리기
    # -----------------------------
    screen.fill(WHITE)

    # 실제 오브젝트
    screen.blit(player_rotated_surface, player_rotated_rect)
    screen.blit(rotated_surface, rotated_rect)

    # AABB
    pygame.draw.rect(screen, RED, player_aabb, 2)
    pygame.draw.rect(screen, RED, center_aabb, 2)

    # 원형 Bounding
    pygame.draw.circle(screen, BLUE, player_center, player_radius, 2)
    pygame.draw.circle(screen, BLUE, (center_x, center_y), center_radius, 2)

    # OBB
    pygame.draw.polygon(screen, GREEN, player_obb, 2)
    pygame.draw.polygon(screen, GREEN, center_obb, 2)

    # 텍스트 출력
    circle_text = "Circle: HIT" if circle_hit else "Circle: MISS"
    aabb_text = "AABB: HIT" if aabb_hit else "AABB: MISS"
    obb_text = "OBB: HIT" if obb_hit else "OBB: MISS"

    screen.blit(font.render(circle_text, True, BLACK), (20, 20))
    screen.blit(font.render(aabb_text, True, BLACK), (20, 60))
    screen.blit(font.render(obb_text, True, BLACK), (20, 100))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()