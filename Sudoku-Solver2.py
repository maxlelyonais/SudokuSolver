import pygame
import tkinter as tk

pygame.init()


HEIGHT = 450
WIDTH  = 450

surface = pygame.display.set_mode((HEIGHT,WIDTH))
pygame.display.set_caption("Sudoku_solver")

board = [
        [7, 8, ' ', 4, ' ', ' ', 1, 2, ' '],
        [6, ' ', ' ', ' ', 7, 5, ' ', ' ', 9],
        [' ',  ' ', ' ', 6, ' ', 1,  '', 7, 8],
        [' ', ' ', 7, ' ', 4, ' ', 2, 6, ' '],
        [ ' ', ' ', 1, ' ', 5, ' ', 9, 3, ' '],
        [9, ' ', 4, ' ', 6, ' ', ' ', ' ', 5],
        [' ', 7, ' ', 3, ' ', ' ', ' ', 1, 2],
        [1, 2, ' ', ' ', ' ', 7, 4, ' ', ' '],
        [' ', 4, 9, 2, ' ', 6,' ', ' ', 7]
    ]


white = (255,255,255)
black = (0,0,0)
red = (255,0,0)

Fuente = pygame.font.Font(None, 36)

grid_row_size = WIDTH // 9
grid_col_size = HEIGHT // 9
rectangles = []
storedRectangle = []
running = True
selecting = False
mouse_x = 0
mouse_y = 0

def auto_sudoku_solver(grid):

    find = find_empty(grid)

    if find:
        row,col = find
    else:
        return True

    for i in range(1,10):
        if checkingSudoku(grid,row,col,i) == False:
            grid[row][col] = i
            if auto_sudoku_solver(grid):
                return True
            grid[row][col] = ' '

    return False

def find_empty(grid):

    for i in range(9):
        for j in range(9):
            if grid[i][j] == ' ':
                return (i,j)

    return None

def open_popup():
    popup = tk.Tk()
    popup.title("Repeated Number")

    label = tk.Label(popup, text = "Repeated Number")
    label.pack(padx = 20, pady = 20)

    window_width = popup.winfo_reqwidth()
    window_height = popup.winfo_reqheight()
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()

    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    popup.geometry(f"+{x}+{y}")

    close_button = tk.Button(popup, text = "Close Popup", command = popup.destroy)

    close_button.pack(pady = 10)

    popup.mainloop()


def Winning_window():

    popup = tk.Tk()
    popup.title("Winning_window")

    label = tk.Label(popup, text = "You have won")
    label.pack(padx = 20, pady = 20)

    window_width = popup.winfo_reqwidth()
    window_height = popup.winfo_reqheight()
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()

    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    popup.geometry(f"+{x}+{y}")

    close_button = tk.Button(popup, text = "Close Popup", command = popup.destroy)

    close_button.pack(pady = 10)

    popup.mainloop()


def drawGrid():
    i = 0
    j = 0
    for x in range(0,WIDTH,grid_row_size):
        for y in range(0,HEIGHT,grid_col_size):
            rect = pygame.Rect(y,x,grid_row_size,grid_col_size)
            rectangles.append(rect)
            pygame.draw.rect(surface,white,rect,1)
            text_surface = Fuente.render(str(board[i][j]), True, white)
            text_x = rect.centerx - text_surface.get_width() // 2
            text_y = rect.centery - text_surface.get_height() // 2

            if j == 8:
               i+=1
               j=0
            else:
                j+=1

            surface.blit(text_surface, (text_x,text_y))

def select(mouse_x,mouse_y):
    for x in rectangles:
        if mouse_x < x.x + grid_row_size and mouse_x > x.x:
            if mouse_y < x.y + grid_col_size and mouse_y > x.y:

                iteracionX = mouse_x // 50 ## Fila
                iteracionY = mouse_y // 50 ## Columna

                return iteracionY,iteracionX,x
            
def checkingSudoku(grid,i,j,number):

    ## Check for rows
    for x in range(9):
        if j != x and grid[i][x] == number:
            return True
    
    ## Check for columns
    for y in range(9):
        if i != y and grid[y][j] == number:
            return True

    ## Check in blocks
    row_i = i // 3
    col_y = j // 3
    for y in range(row_i*3, (row_i*3 + 3)):
        for x in range(col_y*3, (col_y*3 + 3)):

            if grid[y][x] == number and x != j and y != i:
                return True
            
    return False
            
def WriteANumber(grid,i,j,key):
    number = 0
    if key[pygame.K_1]:
        grid[i][j] = 1
        number = 1
    elif key[pygame.K_2]:
        grid[i][j] = 2
        number = 2
    elif key[pygame.K_3]:
        grid[i][j] = 3
        number = 3
    elif key[pygame.K_4]:
        grid[i][j] = 4
        number = 4
    elif key[pygame.K_5]:
        grid[i][j] = 5
        number = 5
    elif key[pygame.K_6]:
        grid[i][j] = 6
        number = 6
    elif key[pygame.K_7]:
        grid[i][j] = 7
        number = 7
    elif key[pygame.K_8]:
        grid[i][j] = 8
        number = 8
    elif key[pygame.K_9]:
        grid[i][j] = 9
        number = 9

    if checkingSudoku(grid,i,j,number) == True:
        grid[i][j] = ' '
        open_popup()

    if checkingSudoku(grid,i,j,number) == False:
        if checkWinning(grid):
            Winning_window()

def checkWinning(grid):

    for i in range(9):
        for j in range(9):
            if grid[i][j] == ' ':
                return False

    return True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:

            mouse_x,mouse_y = event.pos
            iterX,iterY,searchingRectangle = select(mouse_x,mouse_y) ## iterX = fila y iterY = columna

            if event.button == 1 and selecting == False:
                pygame.draw.rect(surface,red,searchingRectangle)
                storedRectangle.append(searchingRectangle)
                selecting = True
            elif event.button == 1 and selecting == True:
                if searchingRectangle in storedRectangle:
                    pygame.draw.rect(surface,black,storedRectangle.pop())
                    selecting = False
                else:
                    pygame.draw.rect(surface,black,storedRectangle.pop())
                    pygame.draw.rect(surface,red,searchingRectangle)
                    storedRectangle.append(searchingRectangle)

        elif event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_c]:
                auto_sudoku_solver(board)
            elif keys[pygame.K_l]:
                print(board)
            else:
                WriteANumber(board,iterX,iterY,keys)

    drawGrid()
    pygame.display.update()