import pygame

WIDTH = 1000
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

        screen.fill('gray')

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
        for count, piece in enumerate(Board.whitePiecesTaken):
            piece.image = pygame.transform.scale(piece.image, (40, 40))
            piece.draw((850 + (15 * count), 50))
        for count, piece in enumerate(Board.blackPiecesTaken):
            piece.image = pygame.transform.scale(piece.image, (40, 40))
            piece.draw((850 + (15 * count), 450))

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
    def getTranslation(square, direction, magnitude) -> str:
        """ Return a coordinate pair of a square given the direction, magnitude, and starting square.  Returns None if square would be invalid. """

        if direction == 'up':
            return f'{Board.letters[Board.letters.index(square[0])]}{int(square[1]) + magnitude}'
        if direction == 'down':
            return f'{Board.letters[Board.letters.index(square[0])]}{int(square[1]) - magnitude}'
        if direction == 'left':
            return f'{Board.letters[Board.letters.index(square[0]) - magnitude]}{int(square[1])}'
        if direction == 'right':
            return f'{Board.letters[Board.letters.index(square[0]) + magnitude]}{int(square[1])}'
        if direction == 'upleft':
            return f'{Board.letters[Board.letters.index(square[0]) - magnitude]}{int(square[1]) + magnitude}'
        if direction == 'upright':
            return f'{Board.letters[Board.letters.index(square[0]) + magnitude]}{int(square[1]) + magnitude}'
        if direction == 'downleft':
            return f'{Board.letters[Board.letters.index(square[0]) - magnitude]}{int(square[1]) - magnitude}'
        if direction == 'downright':
            return f'{Board.letters[Board.letters.index(square[0]) + magnitude]}{int(square[1]) - magnitude}'

    @staticmethod
    def getPossibleEdges(square):
        """ Return a tuple of all the edges the square is touching. """

        edges = list()

        if square[0] == 'a':
            edges.append('left')
        if square[0] == 'h':
            edges.append('right')
        if square[1] == '1':
            edges.append('bottom')
        if square[1] == '8':
            edges.append('top')

        return tuple(edges)

    @staticmethod
    def setupBoard():
        Board.board['e5'] = Piece('white', 'e5')
        Board.board['d6'] = Rook('white', 'd6')
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
    """ Base class for the chess pieces. """

    def __init__(self, color, square, image='easteregg.png'):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.square = square
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.allowedDirections = (
            'up', 'down', 'left', 'right', 'upleft', 'upright', 'downleft', 'downright')

    def getPossibleMoves(self):
        """ Return a tuple of all possible moves. """

        moves = list()
        directions = dict()
        for allowedDirection in self.allowedDirections:
            directions[allowedDirection] = 1

        edges = Board.getPossibleEdges(self.square)

        illegalDirections = set()

        if 'top' in edges:
            illegalDirections.add('up')
            illegalDirections.add('upleft')
            illegalDirections.add('upright')
        if 'bottom' in edges:
            illegalDirections.add('down')
            illegalDirections.add('downleft')
            illegalDirections.add('downright')
        if 'left' in edges:
            illegalDirections.add('left')
            illegalDirections.add('upleft')
            illegalDirections.add('downleft')
        if 'right' in edges:
            illegalDirections.add('right')
            illegalDirections.add('upright')
            illegalDirections.add('downright')

        for d in illegalDirections:
            if d in directions.keys():
                del directions[d]

        while len(directions) != 0:
            for direction, magnitude in directions.copy().items():
                move_d = Board.getTranslation(
                    self.square, direction, magnitude)

                # move is valid if square is empty or if square is occupied by opposing piece
                if (Board.board[move_d] == None) or (Board.board[move_d] != None and Board.board[move_d].color != self.color):
                    moves.append(move_d)

                directions[direction] += 1
                edges_d = Board.getPossibleEdges(move_d)
                stop_condition = (direction in ['left', 'upleft', 'downleft'] and 'left' in edges_d) or (
                    direction in ['right', 'upright', 'downright'] and 'right' in edges_d) or (
                    direction in ['up', 'upleft', 'upright'] and 'top' in edges_d) or (
                    direction in ['down', 'downleft', 'downright'] and 'bottom' in edges_d) or (Board.board[move_d] != None)
                # if sightline is obstructed by a piece or an edge has been reached
                if stop_condition:
                    del directions[direction]

        return tuple(moves)

    def draw(self, coords):
        # pImage = pygame.transform.scale(self.image, (80,80))
        screen.blit(self.image, coords)

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
    """ The pawn. Has a first move mechanic as well as en passant. """

    def __init__(self, color, square,  image='whitepawn.png'):
        """ Init pawn instance. """
        Piece.__init__(self, color, square, image)
        self.firstMove = True

    def getPossibleMoves(self) -> (str):
        """ Return a tuple of all possible moves. """

        moves = list()
        edges = Board.getPossibleEdges(self.square)

        # check if pawn is at top/bottom
        if (self.color == 'white' and 'top' in edges) or (self.color == 'black' and 'bottom' in edges):
            return tuple(moves)

        # up or down depending on color
        if self.color == 'white':
            direction = 'up'
        else:
            direction = 'down'

        edges = Board.getPossibleEdges(self.square)

        if Board.board[Board.getTranslation(self.square, direction, 1)] == None:
            moves.append(Board.getTranslation(self.square, direction, 1))
            # first move of a pawn can be 2 spaces forward
            if self.firstMove and Board.board[Board.getTranslation(self.square, direction, 2)] == None:
                moves.append(Board.getTranslation(self.square, direction, 2))

        # left edge case
        if 'left' not in edges:
            upper_left = Board.getTranslation(
                self.square, direction + 'left', 1)
            if Board.board[upper_left] != None and Board.board[upper_left].color != self.color:
                moves.append(upper_left)

        # right edge case
        if 'right' not in edges:
            upper_right = Board.getTranslation(
                self.square, direction + 'right', 1)
            if Board.board[upper_right] != None and Board.board[upper_right].color != self.color:
                moves.append(upper_right)

        return tuple(moves)


class Rook(Piece):
    """ The rook. """

    def __init__(self, color, square,  image='whiterook.png'):
        Piece.__init__(self, color, square, image)
        self.image = pygame.transform.scale(self.image, (90, 90))
        self.allowedDirections = (
            'up', 'down', 'left', 'right')


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
