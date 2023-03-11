import pygame

WIDTH = 800
HEIGHT = 800
fps = 60
timer = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

run = True

pygame.mixer.init()
chess_hit = pygame.mixer.Sound('chess-hit.wav')


class Board:
    """
    Class representing the game board.
    - 64 clickable tiles
    - have chess board be like an array
    - if user clicks a tile with a piece in it, user can move piece
    """
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

    board = dict()
    for row in range(8):
        for col in range(8):
            board[f'{letters[row]}{8 - col}'] = None
    clickedSquare = None
    clickedPiece = None
    viewingMoves = False

    whitePiecesTaken = list()
    blackPiecesTaken = list()

    # @staticmethod
    # def __init__():
    #     for row in range(8):
    #         for col in range(8):
    #             Board.board[f'{Board.letters[row]}{8 - col}'] = None
    #     # print(self.board)
    #     Board.setupBoard()

    @staticmethod
    def drawBoard():
        """" Draws board on the screen. """
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

    @staticmethod
    def drawPieces():
        """ Draws every piece currently on the board on the screen. """
        for square, piece in Board.board.items():
            if piece != None:
                piece.draw(Board.getCoords(square))

    @staticmethod
    def clickSquare(mouse_position):
        """ Execute the click of the board upon player click. """
        if Board.clickedSquare != None:
            Board.drawBoard()
            Board.drawPieces()

        Board.clickedSquare = Board.whichSquare(mouse_position)
        if Board.clickedSquare != None:  # checking if we didnt click between the squares
            if Board.viewingMoves:
                if Board.clickedSquare in Board.clickedPiece.getPossibleMoves():  # execute move

                    Board.movePiece(Board.clickedPiece.square,
                                    Board.clickedSquare)
                Board.clickedPiece = None
                Board.viewingMoves = None
            else:
                tile_x, tile_y = Board.getCoords(Board.clickedSquare)
                tile = pygame.Rect(tile_x, tile_y, 100, 100)

                pygame.draw.rect(screen, (153, 245, 130), tile)
                # if clicked square contains a piece
                if Board.board[Board.clickedSquare] != None:
                    Board.clickedPiece = Board.board[Board.clickedSquare]
                    Board.viewingMoves = True
                    Board.board[Board.clickedSquare].draw(
                        Board.getCoords(Board.clickedSquare))
                    Board.board[Board.clickedSquare].drawPossibleMoves()

    @staticmethod
    def movePiece(square, destination):
        """ Move a piece to another square. """

        if Board.board[destination] != None:  # if a piece is there
            if Board.board[destination].color == 'white':
                Board.whitePiecesTaken.append(Board.board[destination])
            else:
                Board.blackPiecesTaken.append(Board.board[destination])
        Board.board[destination] = Board.board[square]
        Board.board[destination].square = destination

        if isinstance(Board.board[destination], Pawn):
            Board.board[destination].firstMove = False

        Board.board[square] = None

        Board.drawBoard()
        Board.drawPieces()
        chess_hit.play()

    @staticmethod
    def whichSquare(coords) -> str:
        """ Return the coordinate pair of the square that corresponds to the given coordinates. """
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
    def getCoords(square, centered=False) -> (int):
        """ Return a tuple containing the x and y values of the given square. """
        if centered:
            return (Board.coordinates[square[0]] + 50, Board.coordinates[square[1]] + 50)
        else:
            return (Board.coordinates[square[0]], Board.coordinates[square[1]])

    @staticmethod
    def getTranslation(square, x, y) -> str:
        """ Return a coordinate pair of the given square + x + y. """
        return f'{Board.letters[Board.letters.index(square[0]) + x]}{int(square[1]) + y}'

    @staticmethod
    def setupBoard():
        for i in range(8):
            Board.board[f'{Board.letters[i]}4'] = Pawn(
                'black', f'{Board.letters[i]}4',  image='blackpawn.png')
            Board.board[f'{Board.letters[i]}2'] = Pawn(
                'white', f'{Board.letters[i]}2',  image='whitepawn.png')


# chess pieces each piece has their own class
# - create a class for each piece
# - if we click the chess piece once it will allow movement
# class inherited_class(Sprite)

# # class square(rectangle):
#     def __init__(self):
#         rectangle.__init__(self)

class Piece(pygame.sprite.Sprite):
    def __init__(self, color, square, image='easteregg.png'):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.square = square
        self.image = pygame.image.load(image)

    # def getPossibleMoves(self):
    #     """ Return a tuple of all possible moves. """

    #     moves = list()
    #     edges = self.getPossibleEdges()
    #     directions = {'up': 1,
    #                   'down': 1,
    #                   'left': 1,
    #                   'right': 1,
    #                   'upper left': 1,
    #                   'upper right': 1,
    #                   'bottom left': 1,
    #                   'bottom right': 1}

    #     # up or down depending on color
    #     if self.color == 'white':
    #         i = 1
    #     else:
    #         i = -1

    #     if 'up' in edges:
    #         del directions['up']
    #         del directions['upper left']
    #         del directions['upper right']
    #     if 'down' in edges:
    #         del directions['down']
    #         del directions['bottom left']
    #         del directions['bottom right']
    #     if 'left' in edges:
    #         del directions['left']
    #         del directions['upper left']
    #         del directions['buttom left']
    #     if 'right' in edges:
    #         del directions['right']
    #         del directions['upper right']
    #         del directions['buttom right']

    #     while len(directions) != 0:
    #         for d in directions:

    #     return tuple(moves)

    def draw(self, coords):
        # pImage = pygame.transform.scale(self.image, (80,80))
        screen.blit(self.image, coords)

    def getPossibleEdges(self):
        """ Return a tuple of all the edges the piece is touching. """

        edges = list()

        if self.square[0] == 'a':
            edges.append('left')
        if self.square[0] == 'h':
            edges.append('right')
        if self.square[1] == '1':
            edges.append('bottom')
        if self.square[1] == '8':
            edges.append('top')

        return tuple(edges)

    def drawPossibleMoves(self):
        """ Draw circles for possible moves. """

        for move in self.getPossibleMoves():
            if Board.board[move] != None:
                pygame.draw.circle(screen, (153, 245, 130),
                                   Board.getCoords(move, centered=True), 50, width=5)
            else:
                pygame.draw.circle(screen, (153, 245, 130),
                                   Board.getCoords(move, centered=True), 15)


class Pawn(Piece):
    # each piece needs a position and image to follow along with it and needs to be able to move

    def __init__(self, color, square,  image='whitepawn.png'):
        """ Init pawn instance. """
        Piece.__init__(self, color, square, image)
        self.firstMove = True

    def getPossibleMoves(self) -> (str):
        """ Return a tuple of all possible moves. """

        moves = list()
        edges = self.getPossibleEdges()

        # check if pawn is at top/bottom
        if (self.color == 'white' and 'top' in edges) or (self.color == 'black' and 'bottom' in edges):
            return tuple(moves)

        # up or down depending on color
        if self.color == 'white':
            i = 1
        else:
            i = -1

        edges = self.getPossibleEdges()

        if Board.board[Board.getTranslation(self.square, 0, i)] == None:
            moves.append(Board.getTranslation(self.square, 0, i))
            # first move of a pawn can be 2 spaces forward
            if self.firstMove and Board.board[Board.getTranslation(self.square, 0, 2*i)] == None:
                moves.append(Board.getTranslation(self.square, 0, 2*i))

        # left edge case
        if 'left' not in edges:
            upper_left = Board.getTranslation(self.square, -1, i)
            if Board.board[upper_left] != None and Board.board[upper_left].color != self.color:
                moves.append(upper_left)

        # right edge case
        if 'right' not in edges:
            upper_right = Board.getTranslation(self.square, 1, i)
            if Board.board[upper_right] != None and Board.board[upper_right].color != self.color:
                moves.append(upper_right)

        return tuple(moves)


b = Board()
Board.setupBoard()
Board.drawBoard()
Board.drawPieces()


while run:
    timer.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            Board.clickSquare(mouse_position)

    pygame.display.flip()
pygame.quit()
