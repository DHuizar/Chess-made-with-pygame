import pygame

WIDTH = 800
HEIGHT = 800
fps = 60
timer = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

run = True

# chess board
# - 64 clickable tiles
# - have chess board be like an array
# - if user clicks a tile with a piece in it, user can move piece


class Board:
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    coordinates = {'a': 0,
                   'b': 100,
                   'c': 200,
                   'd': 300,
                   'e': 400,
                   'f': 500,
                   'g': 600,
                   'h': 700,
                   '1': 700,
                   '2': 600,
                   '3': 500,
                   '4': 400,
                   '5': 300,
                   '6': 200,
                   '7': 100,
                   '8': 0}

    def __init__(self):
        self.board = dict()
        self.clickedSquare = None
        for row in range(8):
            for col in range(8):
                self.board[f'{Board.letters[row]}{8 - col}'] = None
        # print(self.board)
        self.setupBoard()

    def drawBoard(self):
        """" Draws board on the screen"""
        is_black = False
        tile_x = 0
        tile_y = 0

        for row in range(8):
            for col in range(8):
                # Draw a tile with current x and y values
                tile = pygame.Rect(tile_x, tile_y, 100, 100)
                if is_black:
                    pygame.draw.rect(screen, 'black', tile)
                    is_black = False
                else:
                    pygame.draw.rect(screen, 'white', tile)
                    is_black = True
                tile_y += 100
            if is_black:
                is_black = False
            else:
                is_black = True
            tile_x += 100
            tile_y = 0
        pygame.display.flip()

    def drawPieces(self):
        for square, piece in self.board.items():
            if piece != None:
                piece.draw(Board.getCoords(square))

    def clickSquare(self, mouse_position):
        if self.clickedSquare != None:
            self.drawBoard()
            self.drawPieces()
        self.clickedSquare = self.whichSquare(mouse_position)
        if self.clickedSquare != None:
            tile_x, tile_y = Board.getCoords(self.clickedSquare)
            tile = pygame.Rect(tile_x, tile_y, 100, 100)

            pygame.draw.rect(screen, (153, 245, 130), tile)
            if self.board[self.clickedSquare] != None:
                self.board[self.clickedSquare].draw(
                    Board.getCoords(self.clickedSquare))
                self.board[self.clickedSquare].showPossibleMoves()

    def whichSquare(self, coords):
        letter = ''
        num = 0
        if 0 < coords[0] < 100:
            letter = 'a'
        elif 100 < coords[0] < 200:
            letter = 'b'
        elif 200 < coords[0] < 300:
            letter = 'c'
        elif 300 < coords[0] < 400:
            letter = 'd'
        elif 400 < coords[0] < 500:
            letter = 'e'
        elif 500 < coords[0] < 600:
            letter = 'f'
        elif 600 < coords[0] < 700:
            letter = 'g'
        elif 700 < coords[0] < 800:
            letter = 'h'

        if 0 < coords[1] < 100:
            num = 8
        elif 100 < coords[1] < 200:
            num = 7
        elif 200 < coords[1] < 300:
            num = 6
        elif 300 < coords[1] < 400:
            num = 5
        elif 400 < coords[1] < 500:
            num = 4
        elif 500 < coords[1] < 600:
            num = 3
        elif 600 < coords[1] < 700:
            num = 2
        elif 700 < coords[1] < 800:
            num = 1

        if letter == '' or num == 0:
            return None

        assert (letter != '')
        assert (num != 0)
        return f'{letter}{num}'

    @staticmethod
    def getCoords(square, centered=False):
        if centered:
            return (Board.coordinates[square[0]] + 50, Board.coordinates[square[1]] + 50)
        else:
            return (Board.coordinates[square[0]], Board.coordinates[square[1]])

    def setupBoard(self):
        for i in range(8):
            self.board[f'{Board.letters[i]}7'] = Pawn(
                'black', f'{Board.letters[i]}7', 'COORDINATES', image='blackpawn.png')
            self.board[f'{Board.letters[i]}2'] = Pawn(
                'white', f'{Board.letters[i]}2', 'COORDINATES', image='whitepawn.png')


# chess pieces each piece has their own class
# - create a class for each piece
# - if we click the chess piece once it will allow movement
#
class Pawn:
    # each piece needs a position and image to follow along with it and needs to be able to move

    def __init__(self, color, square, currentposition, image='whitepawn.png'):
        self.color = color
        self.square = square
        self.currentposition = currentposition
        self.image = pygame.image.load(image)
        self.firstMove = True

    def draw(self, coords):
        # pImage = pygame.transform.scale(self.image, (80,80))
        screen.blit(self.image, coords)

    def showPossibleMoves(self):
        if self.firstMove:
            if self.color == 'white':
                pygame.draw.circle(screen, (153, 245, 130), Board.getCoords(
                    f'{self.square[0]}{int(self.square[1]) + 1}', centered=True), 10)
                pygame.draw.circle(screen, (153, 245, 130), Board.getCoords(
                    f'{self.square[0]}{int(self.square[1]) + 2}', centered=True), 10)
            else:
                pygame.draw.circle(screen, (153, 245, 130), Board.getCoords(
                    f'{self.square[0]}{int(self.square[1]) - 1}', centered=True), 10)
                pygame.draw.circle(screen, (153, 245, 130), Board.getCoords(
                    f'{self.square[0]}{int(self.square[1]) - 2}', centered=True), 10)
        else:
            if self.color == 'white':
                pygame.draw.circle(screen, (153, 245, 130), Board.getCoords(
                    f'{self.square[0]}{int(self.square[1]) + 1}', centered=True), 10)
            else:
                pygame.draw.circle(screen, (153, 245, 130), Board.getCoords(
                    f'{self.square[0]}{int(self.square[1]) - 1}', centered=True), 10)


gameBoard = Board()
gameBoard.drawBoard()
gameBoard.drawPieces()


while run:
    # screen.fill('white')
    timer.tick(fps)
    # print(mouse_position)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            # pygame.draw.circle(screen, 'red', mouse_position, 10)
            gameBoard.clickSquare(mouse_position)

    pygame.display.flip()
pygame.quit()
