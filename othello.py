# 오델로 게임

import random, sys, pygame, time, copy
from pygame.locals import *
from tkinter import *

FPS = 10  # 화면을 얼마나 업데이트할지
windowWidth = 640
windowHeight = 480
spaceSize = 50  #보드 각 격자의 너비와 높이
boardWidth = 8  # 8 x 8 보드
boardHeight = 8
whiteTile = 'whiteTile'
blackTile = 'blackTile'
emptySpace = 'emptySpace'
speed = 25  # 1 ~ 100 사이 정수 (숫자가 클수록 애니메이션 빨라짐)

xmargin = int((windowWidth - (boardWidth * spaceSize)) / 2)  # 왼쪽과 오른쪽에 띄어야 하는 공간
ymargin = int((windowHeight - (boardHeight * spaceSize)) / 2)  # 위쪽과 아래쪽에 띄어야 하는 공간

white = (255,255,255)
black = (0,0,0)
skyblue = (0,50,255)

textbgcolor1 = skyblue
gridlinecolor = black
textcolor = white

def main():
    global mainClock, displaysurf, font, bigfont, bgimage

    pygame.init()
    mainClock = pygame.time.Clock()
    displaysurf = pygame.display.set_mode((windowWidth,windowHeight))
    pygame.display.set_caption('오델로')
    font = pygame.font.Font('MaplestoryLight.ttf',16)
    bigfont = pygame.font.Font('MaplestoryBold.ttf',32)

    boardImage = pygame.image.load('board1.png')  
    boardImage = pygame.transform.smoothscale(boardImage,(boardWidth * spaceSize, boardHeight * spaceSize)) # smoothscale() 사용하여 이미지 늘릴 수 있음
    boardImageRect = boardImage.get_rect() # 위치 획득
    boardImageRect.topleft = (xmargin, ymargin)
    bgimage = pygame.image.load('background.png') 
    bgimage = pygame.transform.smoothscale(bgimage,(windowWidth, windowHeight))
    bgimage.blit(boardImage, boardImageRect) #이미지와 이미지 좌표

    while True:
        if runGame() == False:
            break

def runGame():
    mainBoard = getNewBoard() #보드와 게임 리셋
    resetBoard(mainBoard)
    turn = random.choice(['computer','player'])

    drawBoard(mainBoard)
    playerTile, computerTile = enterPlayerTile()
    newGameSurf = font.render('게임 다시 시작',True, textcolor, textbgcolor1)
    newGameRect = newGameSurf.get_rect()
    newGameRect.topright = (windowWidth - 8, 10)

    while True:
        if turn == 'player':
            if getValidMoves(mainBoard, playerTile) == []:  # 더이상 놓을 수 없으면 종료
                break
                
            movexy = None
            while movexy == None:  # 플레이어가 유효한 수를 놓을 때까지
                checkForQuit()
                for event in pygame.event.get():  # 이벤트 처리
                    if event.type == MOUSEBUTTONUP:
                        mousex, mousey = event.pos
                        if newGameRect.collidepoint((mousex, mousey)): #새 게임 시
                            return True
                        movexy = getSpaceClicked(mousex, mousey)  # movexy 설정
                        if movexy != None and not isValidMove(mainBoard,playerTile, movexy[0], movexy[1]):
                            movexy = None

                drawBoard(mainBoard)  # 게임보드 그리기
                drawInfo(mainBoard, playerTile, computerTile, turn)
                displaysurf.blit(newGameSurf, newGameRect)
                mainClock.tick(FPS)
                pygame.display.update()

            makeMove(mainBoard, playerTile, movexy[0], movexy[1], True)  # 수 놓고 차례 끝내기
            if getValidMoves(mainBoard, computerTile) != [] :
                turn = 'computer' # 놓을 수 있는 수가 있으면 컴퓨터 차례

        else:
            if getValidMoves(mainBoard, computerTile) == []: # 컴퓨터가 놓을 수 있는 수 없으면 종료
                break

            drawBoard(mainBoard)
            drawInfo(mainBoard, playerTile, computerTile, turn)
            displaysurf.blit(newGameSurf, newGameRect)
            pauseUntil = time.time() + random.randint(5,15) * 0.1  # 컴퓨터가 생각하는 것처럼 시간멈춤
            while time.time() < pauseUntil:
                pygame.display.update()

            x,y = getComputerMove(mainBoard, computerTile) #수 놓고 차례 끝내기
            makeMove(mainBoard, computerTile, x, y, True)
            if getValidMoves(mainBoard, playerTile) != []:
                turn = 'player' # 놓을 수 있는 수가 있으면 플레이어 차례

    drawBoard(mainBoard)
    scores = getScoreOfBoard(mainBoard) #최종 점수 보여주기

    if scores[playerTile] > scores[computerTile]:
        text = ('%s 점 차로 플레이어의 승리입니다!' %(scores[playerTile] - scores[computerTile]))
    elif scores[playerTile] < scores[computerTile]:
        text = ('%s 점 차로 컴퓨터의 승리입니다!' %(scores[computerTile] - scores[playerTile]))
    else:
        text = '무승부입니다!'

    textSurf = font.render(text,True, textcolor, textbgcolor1)
    textRect = textSurf.get_rect()
    textRect.center = (int(windowWidth / 2), int(windowHeight / 2))
    displaysurf.blit(textSurf, textRect)
    displaysurf.blit(newGameSurf, newGameRect)

    while True:
        checkForQuit() # 플레이어가 누를 때까지
        for event in pygame.event.get():  # 이벤트 처리
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if newGameRect.collidepoint((mousex,mousey)):
                    return True
        displaysurf.blit(newGameSurf, newGameRect)
        pygame.display.update()
        mainClock.tick(FPS)

def translateBoard(x,y):
    return xmargin + x * spaceSize + int(spaceSize / 2), ymargin + y * spaceSize + int(spaceSize / 2)

def animateTileChange(tilesToFlip, tileColor, additionalTile):
    if tileColor == whiteTile:  # 이전에 있었던 타일 그리기
        additionalTileColor = white
    else:
        additionalTileColor = black
    additionalTileX, additionalTileY = translateBoard(additionalTile[0], additionalTile[1])
    pygame.draw.circle(displaysurf,additionalTileColor, (additionalTileX, additionalTileY), int(spaceSize / 2) -4)
    pygame.display.update()

    for rgbValues in range(0,255,int(speed * 2.55)):
        if rgbValues > 255:
            rgbValues = 255
        elif rgbValues < 0:
            rgbValues = 0

        for x,y in tilesToFlip:
            centerx, centery = translateBoard(x,y)
            pygame.draw.circle(displaysurf, additionalTileColor, (centerx, centery), int(spaceSize / 2) -4)  # 색 변수 수정
        pygame.display.update()
        mainClock.tick(FPS)
        checkForQuit()

def getSpaceClicked(mousex, mousey):
    for x in range(boardWidth): # 마우스가 클릭한 위치의 좌표 반환
        for y in range(boardHeight):
            if mousex > x * spaceSize + xmargin and mousex < (x+1) * spaceSize + xmargin and mousey > y * spaceSize + ymargin and mousey < (y+1) * spaceSize + ymargin:
                return (x,y)
    return None

def drawBoard(board):
    displaysurf.blit(bgimage, bgimage.get_rect())  # 보드 배경 그리기
    for x in range(boardWidth):  #  검정색, 흰색 타일 그리기
        for y in range(boardHeight):
            centerx, centery = translateBoard(x,y)
            if board[x][y] == whiteTile or board[x][y] == blackTile:
                if board[x][y] == whiteTile:
                    tileColor = white
                else:
                    tileColor = black
                pygame.draw.circle(displaysurf, tileColor, (centerx,centery), int(spaceSize /2)-4)
                
def drawInfo(board, playerTile, computerTile, turn):
    scores = getScoreOfBoard(board)  # 화면 아래에 점수와 차례 나타내기
    scoreSurf = font.render("플레이어 점수: %s   컴퓨터 점수: %s    %s의 차례입니다." %(str(scores[playerTile]),str(scores[computerTile]),turn.title()),True,textcolor)
    scoreRect = scoreSurf.get_rect()
    scoreRect.bottomleft = (10, windowHeight - 5)
    displaysurf.blit(scoreSurf, scoreRect)

def resetBoard(board):
    for x in range(boardWidth):  # 보드 비우고 시작위치에 타일 놓기
        for y in range(boardHeight):
            board[x][y] = emptySpace
    
    whitecnt = 0 
    blackcnt = 0
    startBoard = []
    for i in range(4): # 초기 상태 흰돌/ 검은돌 랜덤
        boardChoice = random.choice(['whiteTile','blackTile'])
        if boardChoice == 'whiteTile':
            whitecnt += 1
        else:
            blackcnt += 1
        startBoard.append(boardChoice)
    board[3][3] = startBoard[0]
    board[3][4] = startBoard[1]
    board[4][3] = startBoard[2]
    board[4][4] = startBoard[3]

    if whitecnt >= 3 or blackcnt >= 3: # 각 돌이 3개 이상 배치되지 않게
        resetBoard(board)
    
def getNewBoard():
    board = [] # 빈 새로운 보드
    for i in range(windowWidth):
        board.append([emptySpace] * boardHeight)
    return board

def isValidMove(board, tile, xstart, ystart):
    if board[xstart][ystart] != emptySpace or not isOnBoard(xstart,ystart):  # 놓을 수 없는 곳에 놓으려하면 False
        return False

    board[xstart][ystart] = tile  # 보드에 타일 임시로 놓기

    if tile == whiteTile:
        otherTile = blackTile
    else:
        otherTile = whiteTile

    tilesToFlip = []
    for xdirection, ydirection in [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]:
        x,y = xstart, ystart
        x += xdirection
        y += ydirection
        if isOnBoard(x,y) and board[x][y] == otherTile: # 내 타일 옆에 상대편 타일이 있는지 확인
            x += xdirection
            y += ydirection
            if not isOnBoard(x,y):
                continue
            while board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not isOnBoard(x,y):
                    break
            if not isOnBoard(x,y):
                continue
            if board[x][y] == tile: # 뒤집을 타일이 있으므로 원래 위치로 간 다음 중간 타일 표시
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append([x,y])
    board[xstart][ystart] = emptySpace # 공간 비우기
    if len(tilesToFlip) == 0: # 뒤집을 타일이 없으면 False
        return False
    return tilesToFlip

def isOnBoard(x,y):
    return x >= 0 and x < boardWidth and y >= 0 and y < boardHeight  # 좌표가 보드의 좌표면 True

def getValidMoves(board,tile):
    validMoves = [] # 모든 가능한 수의 좌표 리스트 반환
    for x in range(boardWidth):
        for y in range(boardHeight):
            if isValidMove(board,tile,x,y) != False:
                validMoves.append((x,y))
    return validMoves

def getScoreOfBoard(board):
    wscore = 0  # 타일 수로 점수 
    bscore = 0
    for x in range(boardWidth):
        for y in range(boardHeight):
            if board[x][y] == whiteTile:
                wscore += 1
            if board[x][y] == blackTile:
                bscore += 1
    return {whiteTile:wscore, blackTile:bscore}

def enterPlayerTile():
    textSurf = font.render('어떤 색의 돌을 선택하시겠습니까?', True, textcolor, textbgcolor1)
    textRect = textSurf.get_rect()
    textRect.center = (int(windowWidth / 2), int(windowHeight / 2))

    wSurf = bigfont.render('흰 돌', True, textcolor, textbgcolor1)
    wRect = wSurf.get_rect()
    wRect.center = (int(windowWidth / 2) -60, int(windowHeight / 2) +40)

    bSurf = bigfont.render('검은 돌',True, textcolor, textbgcolor1)
    bRect = bSurf.get_rect()
    bRect.center = (int(windowWidth / 2) +60, int(windowHeight / 2) +40)

    while True:  # 플레이어가 색깔을 고를 때까지
        checkForQuit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if wRect.collidepoint((mousex,mousey)):
                    return [whiteTile,blackTile]
                elif bRect.collidepoint((mousex,mousey)):
                    return [blackTile,whiteTile]

        displaysurf.blit(textSurf, textRect)
        displaysurf.blit(wSurf, wRect)
        displaysurf.blit(bSurf, bRect)
        pygame.display.update()
        mainClock.tick(FPS)

def makeMove(board, tile, xstart, ystart, realMove = False):
    tilesToFlip = isValidMove(board, tile, xstart, ystart) # xstart, ystart에 타일 놓고 뒤집기
    if tilesToFlip == False:
        return False

    board[xstart][ystart] = tile
    if realMove:
        animateTileChange(tilesToFlip, tile, (xstart,ystart))

    for x,y in tilesToFlip:
        board[x][y] = tile
    return True

def isOnCorner(x,y):  # 위치가 코너에 있으면 True
    return (x == 0 and y == 0) or (x == boardWidth and y == 0) or (x == 0 and y == boardHeight) or (x == boardWidth and y == boardHeight)

def getComputerMove(board, computerTile):  # 컴퓨터 차례에서 어떤 수가 좋은지 판단하고 가능한 수 반환
    possibleMoves = getValidMoves(board, computerTile)
    random.shuffle(possibleMoves) # 가능한 움직임 순서 랜덤선택

    for x,y in possibleMoves: # 가능한 코너 차지
        if isOnCorner(x,y):
            return [x,y]
        
    bestScore = -1  # 가장 점수를 많이 얻을 수 기억
    for x,y in possibleMoves:
        dupeBoard = copy.deepcopy(board)
        makeMove(dupeBoard, computerTile, x, y)
        score = getScoreOfBoard(dupeBoard)[computerTile]
        if score > bestScore:
            bestMove = [x,y]
            bestScore = score
    return bestMove

def checkForQuit():
    for event in pygame.event.get((QUIT, KEYUP)): # 이벤트 처리
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

if __name__ == '__main__':
    main()
