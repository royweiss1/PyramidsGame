import random
import matplotlib
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import pygame
import sys

#globals:
HEIGHT = 7
WIDTH = 13
COLORS = {"Black": 0, "White": 1, "Blue": 2, "Yellow": 3, "Pink": 4}
BLUES = [[i + 6, 6 - i] for i in range(0, HEIGHT)] #spots that are ilegal fo blue


# builds a random matrix to start with
def build():
    matrix = [[COLORS.get("White")] * WIDTH for i in range(0, HEIGHT)]
    for i in range(0, HEIGHT):
        for j in range(0, WIDTH):
            if isInsideTriangle(j, HEIGHT - i - 1):
                matrix[i][j] = rollColor()
    return matrix


def rollColor():
    rnd = random.random()
    if (rnd < 1 / 3):
        return COLORS.get("Yellow")
    elif (rnd < 2 / 3):
        return COLORS.get("Blue")
    return COLORS.get("Pink")

#checks if inside the big pyramid
def isInsideTriangle(index, bound):
    return bound <= index <= WIDTH - bound - 1


# if not in sides of pyramid
def isLegalBlue(x, y):
    return y not in BLUES[x]


# index is the index of the line
def isLegalYellow(index, matrix):
    counter = matrix[index].count(COLORS.get("Yellow"))
    return counter < 4

#as the name goes
def isInMatrix(x, y):
    return 0 <= x <= HEIGHT - 1 and 0 <= y <= WIDTH - 1

#if adj to blue
def isLegalPink(x, y, matrix):
    if isInMatrix(x, y + 1) and matrix[x][y + 1] == COLORS.get("Blue"):  # up
        return False
    if isInMatrix(x, y - 1) and matrix[x][y - 1] == COLORS.get("Blue"):  # down
        return False
    if isInMatrix(x + 1, y) and matrix[x + 1][y] == COLORS.get("Blue"):  # right
        return False
    if isInMatrix(x - 1, y) and matrix[x - 1][y] == COLORS.get("Blue"):  # left
        return False


def solve(matrix):
    while not isSolved(matrix):
        for h in range(0, HEIGHT):
            for w in range(0, WIDTH):
                tup = checkSquere(h, w, matrix)
                if not tup[0]:
                    if tup[1] is "Y":
                        matrix = rollLine(h, matrix)
                    else:
                        matrix[h][w] = rollColor()
    return matrix

#goes over them and checks
def isSolved(matrix):
    for h in range(0, HEIGHT):
        for w in range(0, WIDTH):
            tup = checkSquere(h, w, matrix)
            if not tup[0]:
                return False
    return True

#returns a tupple (True/False,"" => the color) - used to reroll all of the line if yellow
def checkSquere(h, w, matrix):
    color = matrix[h][w]
    if color is COLORS.get("Blue") and not isLegalBlue(h, w):
        return False, "B"
    if color is COLORS.get("Pink") and not isLegalPink(h, w, matrix):
        return False, "P"
    if color is COLORS.get("Yellow") and not isLegalYellow(h, matrix):
        return False, "Y"
    return True, ""


def rollLine(h, matrix):
    for w in range(0, WIDTH):
        if matrix[h][w] is not COLORS.get("White"):
            matrix[h][w] = rollColor()
    return matrix


def main():
    main_window()

#pygamepart
def main_window():
    #init:
    pygame.init()
    background_colour = (234, 212, 252)
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption('Pyramids Game')
    screen.fill(background_colour)
    #buttons:
    start_button = pygame.draw.rect(screen, (0, 244, 0), (350, 500, 100, 50))
    quit_button = pygame.draw.rect(screen, (244, 0, 0), (150, 500, 100, 50))
    #text of buttons
    smallfont = pygame.font.SysFont('Ariel', 30)
    Quit = smallfont.render('Quit', True, (255, 255, 255))
    Generate = smallfont.render('Generate', True, (255, 255, 255))
    #ploting text
    screen.blit(Quit, (150, 500))
    screen.blit(Generate, (350, 500))
    #show time:
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN: # if clicked somewhere
                mouse_pos = event.pos  # gets mouse position
                if 150 <= mouse_pos[0] <= 250 and 500 <= mouse_pos[1] <= 550: # pos of quit button
                    pygame.quit()
                    sys.exit()
                if 350 <= mouse_pos[0] <= 450 and 500 <= mouse_pos[1] <= 550: # pos of generate button
                    matrix=build() # every time new matrix
                    matrix = solve(matrix)
                    visualizeGrid(matrix,screen)

#ploting the matrix:
def visualizeGrid(matrix, screen):
    grid_node_width = 46
    grid_node_height = 46
    createSquare= lambda x,y,color: pygame.draw.rect(screen, color, [x, y, grid_node_width, grid_node_height])
    y = 0  # we start at the top of the screen
    for row in matrix:
        x = 0 # for every row we start at the left of the screen again
        for item in row:
            if item is COLORS.get("White"):
                createSquare(x, y, (255, 255, 255))
            elif item is COLORS.get("Blue"):
                createSquare(x, y, (0, 0, 255))
            elif item is COLORS.get("Yellow"):
                createSquare(x, y, (255, 255, 0))
            elif item is COLORS.get("Pink"):
                createSquare(x, y, (255, 0, 255))

            x += grid_node_width # for ever item/number in that row we move one "step" to the right
        y += grid_node_height   # for every new row we move one "step" downwards
    pygame.display.update()

main()
