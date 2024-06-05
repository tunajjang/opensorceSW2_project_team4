import pygame
import random

# 게임 초기화
pygame.init()

# 화면 설정
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

# 게임 제목
pygame.display.set_caption("PyShooting: 지구를 지켜라")

# FPS 설정
clock = pygame.time.Clock()

# 배경 이미지
background = pygame.image.load('background.png')

# 전투기 이미지
fighter = pygame.image.load('fighter.png')
fighter_size = fighter.get_rect().size
fighter_width = fighter_size[0]
fighter_height = fighter_size[1]
fighter_x_pos = (screen_width / 2) - (fighter_width / 2)
fighter_y_pos = screen_height - fighter_height - 10

# 폭발 이미지
explosion_image = pygame.image.load('explosion.png')

# 미사일 이미지
missile_image = pygame.image.load('missile.png')
missile_size = missile_image.get_rect().size
missile_width = missile_size[0]

# 운석 이미지 파일 목록
asteroid_images = ['rock1.png', 'rock2.png', 'rock3.png', 'rock4.png',
                   'rock5.png', 'rock6.png', 'rock7.png', 'rock8.png']

# 배경 음악
pygame.mixer.music.load('background.mp3')
pygame.mixer.music.play(-1)

# 미사일 발사 사운드
missile_sound = pygame.mixer.Sound('missile.wav')

# 미사일 리스트
missiles = []

# 운석 리스트
asteroids = []

# 운석 폭발 시간 관리
explosions = []

# 초기 목숨 설정
lives = 5

# 목숨 이미지 로드
heart_image = pygame.image.load('heart.png')
heart_size = heart_image.get_rect().size
heart_width = heart_size[0]
heart_height = heart_size[1]

# 운석 생성 함수
def create_asteroid():
    asteroid_img = pygame.image.load(random.choice(asteroid_images))
    asteroid_x_pos = random.randint(0, screen_width - asteroid_img.get_rect().width)
    asteroid_y_pos = 0 - asteroid_img.get_rect().width
    asteroid_speed = random.randint(5, 15)
    return [asteroid_img, asteroid_x_pos, asteroid_y_pos, asteroid_speed]

# 게임 오버 화면 출력 함수
def game_over():
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, (255, 0, 0))
    screen.blit(text, (screen_width/2 - text.get_width()/2, screen_height/2 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(2000)
    pygame.quit()

# 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                missile_x_pos = fighter_x_pos + (fighter_width / 2) - (missile_width / 2)
                missile_y_pos = fighter_y_pos
                missiles.append([missile_x_pos, missile_y_pos])
                missile_sound.play()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and fighter_x_pos > 0:
        fighter_x_pos -= 5
    if keys[pygame.K_RIGHT] and fighter_x_pos < screen_width - fighter_width:
        fighter_x_pos += 5

    # 미사일 위치 업데이트
    missiles = [[m[0], m[1] - 10] for m in missiles if m[1] > 0]

    # 운석 생성
    if random.randint(1, 100) < 5:
        asteroids.append(create_asteroid())

    # 운석 위치 업데이트
    asteroids = [[a[0], a[1], a[2] + a[3], a[3]] for a in asteroids if a[2] < screen_height]

    # 충돌 처리
    for missile in missiles:
        for asteroid in asteroids:
            if (missile[0] > asteroid[1] and missile[0] < asteroid[1] + asteroid[0].get_rect().width) and \
               (missile[1] > asteroid[2] and missile[1] < asteroid[2] + asteroid[0].get_rect().height):
                missiles.remove(missile)
                asteroids.remove(asteroid)
                explosions.append([explosion_image, asteroid[1], asteroid[2], pygame.time.get_ticks()])
                break

    # 전투기와 운석 충돌 처리
    for asteroid in asteroids:
        if ((fighter_x_pos + fighter_width / 3) < asteroid[1] + asteroid[0].get_rect().width / 3 < (fighter_x_pos + fighter_width - fighter_width / 3) or
            (fighter_x_pos + fighter_width / 3) < asteroid[1] + asteroid[0].get_rect().width - asteroid[0].get_rect().width / 3 < (fighter_x_pos + fighter_width - fighter_width / 3)) and \
           ((fighter_y_pos + fighter_height / 3) < asteroid[2] + asteroid[0].get_rect().height / 3 < (fighter_y_pos + fighter_height - fighter_height / 3) or
            (fighter_y_pos + fighter_height / 3) < asteroid[2] + asteroid[0].get_rect().height - asteroid[0].get_rect().height / 3< (fighter_y_pos + fighter_height - fighter_height / 3)):
            lives -= 1
            asteroids.remove(asteroid)
            if lives == 0:
                game_over()
                running = False

    # 화면 그리기
    screen.blit(background, (0, 0))
    screen.blit(fighter, (fighter_x_pos, fighter_y_pos))

    for missile in missiles:
        screen.blit(missile_image, (missile[0], missile[1]))
    
    for asteroid in asteroids:
        screen.blit(asteroid[0], (asteroid[1], asteroid[2]))

    # 폭발 효과 그리기
    current_time = pygame.time.get_ticks()
    explosions = [explosion for explosion in explosions if current_time - explosion[3] < 500]
    for explosion in explosions:
        screen.blit(explosion[0], (explosion[1], explosion[2]))

    for i in range(lives):
        screen.blit(heart_image, (10 + i*(heart_width + 10), 10))
        
    pygame.display.update()
    clock.tick(60)

pygame.quit()
