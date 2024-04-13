import pygame, time, sys, requests

HEIGHT = 800
WIDTH = 800

NONE = 0
WIN = 1
LOOSE = 2

colors = {"BLACK": (0, 0, 0), "WHITE": (255, 255, 255)}

inword = ""
man_num = 1
word = ""
hideword = ""

# API를 이용하여 랜덤한 단어를 얻는 함수
def get_word():
    global word, hideword
    # API 엔드포인트
    url = "https://random-word-api.herokuapp.com/word?lang=en"

    # GET 요청 보내기
    response = requests.get(url)

    # 응답 확인
    if response.status_code == 200:
        # JSON 형식으로 응답을 가져옴
        data = response.json()
        # 가져온 단어 출력
        word = data[0]
    else:
        word = "wony"
    
    hideword = ["_"] * len(word) #정답 길이만큼의 _ 리스트에 저장


# 이겼는지 졌는지 확인하는 함수
def win_check():
    # 이겼을 때
    str1 = ''.join(map(str, hideword))
    if str1 == word:
        return WIN
    # 졌을 때
    if man_num == 7:
        return LOOSE
    return NONE

# 입력한 글자가 단어에 있는지 확인하는 함수
def word_check(inword):
    global man_num, hideword
    yes = 0
    for i in range(len(word)):
        if(word[i] == inword): # 만약 입력 받은 알파벳이 정답에 있으면 hideword의 같은 위치에 입력 받은 알파벳 저장 
            hideword[i] = inword
            yes = 1
    # 만약 입력 받은 알파벳이 정답에 없으면 이미지 인덱스값 변경
    if yes == 0:
        man_num+=1

# 화면을 나타내는 함수
def draw(display):
    global hideword, man_num
    pygame.draw.rect(display, colors["WHITE"], [0, 0, WIDTH, HEIGHT])

    # display에 행맨 그림 띄우기
    hangman = pygame.image.load(f"D:\선린\project\hangman-pygame\img\man{man_num}.png")
    hangman = pygame.transform.scale(hangman, (500, 500))
    hangman_rect = hangman.get_rect()
    hangman_rect.centerx = WIDTH // 2
    hangman_rect.centery = HEIGHT - 500
    display.blit(hangman, hangman_rect)

    # display에 글자 출력
    font = pygame.font.Font(None, 57)
    str1 = '  '.join(map(str, hideword))
    text = font.render(str1, True, colors["BLACK"])
    text_rect = text.get_rect()
    text_rect.centerx = WIDTH // 2
    text_rect.centery = HEIGHT - 100
    display.blit(text, text_rect)

# 게임이 돌아가는 메인 함수
def main():
    pygame.init()
    display = pygame.display.set_mode([WIDTH, HEIGHT], False)
    pygame.display.set_caption("틱텍토")
    run = True
    while run:
        vicfeat = win_check()

        if vicfeat == 1: # 이겼을 때
            print("승리")
            run = True
        elif vicfeat == 2: # 졌을 때
            print("패배")
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                inword = chr(event.key)
                word_check(inword)
        pygame.display.update()
        draw(display)        
    time.sleep(2)
    pygame.quit()
    return

get_word()
main()
sys.exit()