import pygame
from pygame.locals import (
    KEYDOWN,
    K_ESCAPE,
    MOUSEBUTTONDOWN,
    QUIT
)

pygame.init()
width = 1200
length = 900
screen = pygame.display.set_mode((width, length))
largefont = pygame.font.SysFont('arial', 70)
smallfont = pygame.font.SysFont('arial', 40)
rows = 6
colsl = 0
colsr = 7
totcols = colsr-colsl
sqlen = 100
holeradius = 40
holethickness = 3
yellow = (255, 221, 0)
red = (219, 22, 22)
grey = (210, 212, 214)
purple = (149, 50, 168)
green = (78, 168, 50)
turn = 1
colors = [yellow, red, purple, green]
totturns = 4
circleobjs = []
filledheight = [rows-1]*totcols
winner = False
board = [[0 for j in range(totcols)] for i in range(rows)]
running = True

def win(board, player):
    for i in range(totcols-3):
        for j in range(rows):
            if board[j][i] == board[j][i+1] == board[j][i+2] == board[j][i+3] == player:
                return(True)
        for i in range(totcols):
            for j in range(rows-3):
                if board[j][i] == board[j+1][i] == board[j+2][i] == board[j+3][i] == player:
                    return(True)
        for i in range(totcols-3):
            for j in range(rows-3):
                if board[j][i] == board[j+1][i+1] == board[j+2][i+2] == board[j+3][i+3] == player:
                    return(True)
        for i in range(totcols-3):
            for j in range(3, rows):
                if board[j][i] == board[j-1][i+1] == board[j-2][i+2] == board[j-3][i+3] == player:
                    return(True)

def nextturn(turn):
    if turn < totturns:
        turn +=1
    else:
        turn = 1
    return(turn)

while running:
    screen.fill((255, 255, 255))
    circleobjs = []
    xoffset = (width-((colsr+colsl)*sqlen))/2
    yoffset = length-(sqlen*rows)-75
    leftbound = xoffset+(sqlen*colsl)
    rightbound = xoffset+(sqlen*colsr)
    totcols = colsr-colsl
    for i in range(rows):
        circleobjs.append([])
        for j, k in enumerate(range(colsl, colsr)):
            pygame.draw.rect(screen, (24, 103, 214), (k*sqlen+xoffset, i*sqlen+yoffset, sqlen, sqlen))
            if board[i][j] > 0:
                color = colors[int(board[i][j]-1)]
            else:
                color = (255, 255, 255)
            pygame.draw.circle(screen, (0, 0, 0), ((k*sqlen)+(sqlen/2)+xoffset, (i*sqlen)+(sqlen/2)+yoffset), holeradius+holethickness)
            circleobjs[i].append(pygame.draw.circle(screen, color, ((k*sqlen)+(sqlen/2+xoffset), (i*sqlen)+(sqlen/2)+yoffset), holeradius))
    basefont = pygame.font.SysFont('arial', 70)
    addmargin = 50
    addrectlen = 40
    addrowbtnl = pygame.draw.rect(screen, (191, 21, 21), (leftbound-addrectlen-addmargin, 500, 40, 40))
    addtxt = basefont.render('+', False, (0, 0, 0))
    addrowbtnr = pygame.draw.rect(screen, (191, 21, 21), (rightbound+addmargin, 500, addrectlen, addrectlen))
    addcolbtn = pygame.draw.rect(screen, (191, 21, 21), (width/2-(addrectlen/2), yoffset-addmargin-addrectlen, addrectlen, addrectlen))
    screen.blit(addtxt, (leftbound-addrectlen-addmargin+1, 473))
    screen.blit(addtxt, (rightbound+addmargin+1, 473))
    screen.blit(addtxt, (width/2-(addrectlen/2)+1, yoffset-addrectlen-addmargin-27))
    totmargin = (2*addmargin)+addrectlen
    while winner:
        wintxt = smallfont.render('Player '+str(turn)+' wins!', False, (0, 0, 0))
        resettxt = smallfont.render('Reset', False, (0, 0, 0))
        winrectlen = wintxt.get_width()
        resetrectlen = resettxt.get_width()
        pygame.draw.rect(screen, grey, ((width-winrectlen)/2, length/2-90, winrectlen+20, 60))
        resetrect = pygame.draw.rect(screen, grey, ((width-resetrectlen)/2, length/2-10, resetrectlen+20, 60))
        screen.blit(wintxt, ((width-winrectlen)/2+10, length/2-80))
        screen.blit(resettxt, ((width-resetrectlen)/2+10, length/2))
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if resetrect.collidepoint(pygame.mouse.get_pos()):
                    circleobjs = []
                    board = [[0 for j in range(totcols)] for i in range(rows)]
                    filledheight = [rows-1]*totcols
                    turn = 1
                    rows = 6
                    colsl = 0
                    colsr = 7
                    totcols = colsr-colsl
                    winner = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
                pygame.quit()
            elif event.type == QUIT:
                running = False
                pygame.quit()
        pygame.display.flip()
    mousepos = pygame.mouse.get_pos()
    for i, j in enumerate(circleobjs):
        for k, l in enumerate(j):
            if board[i][k] == 0 and l.collidepoint(mousepos):
                pygame.draw.circle(screen, grey, (l.centerx, l.centery), holeradius)
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            if addrowbtnl.collidepoint(mousepos):
                for k, l in enumerate(board):
                    board[k] = [0]+l
                filledheight = [rows-1]+filledheight
                colsl -= 1
                turn = nextturn(turn)
                if (totcols*sqlen) > (width-2*totmargin):
                    sqlen = int((width-2*totmargin)/totcols)
                    holeradius = int(sqlen*0.4)
            elif addrowbtnr.collidepoint(mousepos):
                for k, l in enumerate(board):
                    board[k] += [0]
                filledheight += [rows-1]
                colsr += 1
                turn = nextturn(turn)
                if (totcols*sqlen) > (width-2*totmargin):
                    sqlen = int((width-2*totmargin)/totcols)
                    holeradius = int(sqlen*0.4)
            elif addcolbtn.collidepoint(mousepos):
                rows += 1
                board.insert(0, [0 for i in range(totcols)])
                filledheight = [i+1 for i in filledheight]
                turn = nextturn(turn)
                if (rows*sqlen) > (length-85-addmargin-addrectlen):
                    sqlen = int((length-85-addmargin-addrectlen)/rows)
                    holeradius = int(sqlen*0.4)
            else:
                for i, j in enumerate(circleobjs):
                    for k, l in enumerate(j):
                        if board[i][k] == 0 and l.collidepoint(mousepos):
                            dropx = l.centerx
                            dropy = mousepos[1]
                            board[filledheight[k]][k] = turn
                            filledheight[k]-=1
                            if win(board, turn):
                                winner = True
                                break
                            turn = nextturn(turn)
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False
            pygame.quit()
        elif event.type == QUIT:
            running = False
            pygame.quit()
    pygame.display.flip()
pygame.quit()
