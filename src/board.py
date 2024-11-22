from src.sprites import SPRITES_DICT
from src.utilities import *
from src.constants import *
from src.pieces import *


class Board:
    def __init__(self) -> None:
        # Board state attributes
        self.array = init_empty_board()
        self.active_pieces = {"w": [], "b": []}
        self.captured_pieces = {"w": [], "b": []}
        fill_board(self)
        # GUI attributes
        self.sprites = init_board_sprites()
        init_piece_sprites(self)
        # Games state attributes
        self.active_colour = "w"  # or 'b'
        self.castling_availability = {
            "white_kingside": True,
            "white_queenside": True,
            "black_kingside": True,
            "black_queenside": True,
        }
        self.enpassant = {
            "target_piece": None,
            "target_pos": None,
            "target_square": "",
            "target_colour": "",
            "pieces": [],
        }
        self.halfmove_clock = (
            0  # This is the number of halfmoves since the last capture or pawn move
        )
        self.fullmove_number = 1
        self.checkmate = False
        self.gamelog = ""  # To keep track of turns in PGN format

    def update(self, move: str):
        # move = short_to_long_algebraic(move, self)
        # Assuming move is given in UCI format 'e2e4' (long algebraic notation)
        origin_square = move[:2]
        origin_square_idx = name_to_idx(origin_square)
        destination_square = move[2:4]
        destination_square_idx = name_to_idx(destination_square)

        # Check if piece is valid
        piece = self.array[origin_square_idx[0]][origin_square_idx[1]]
        if piece == None:
            raise Exception(f"No piece is available on {origin_square}.")
        elif piece.colour != self.active_colour:
            raise Exception(f"The piece you are trying to move does not belong to you.")

        # Check if requested move is valid (for LLM outputs)
        legal_moves = piece.get_legal_moves(self)
        if destination_square not in legal_moves:
            raise Exception(f"{move} is an illegal move. Please try again.")

        # Verify capture
        capture = verify_capture(self, piece, destination_square_idx)

        # Update enpassant property
        update_enpassant(self, piece, origin_square_idx, destination_square_idx)

        # Verify if castling is requested and return what kind of castling
        castling = None
        if type(piece) == King:
            castling = verify_castling(piece, move, self.castling_availability)

        # Move pieces on the board
        self.move_piece(piece, origin_square_idx, destination_square_idx, castling)

        # Update castling rights
        if type(piece) == King or type(piece) == Rook:
            update_castling_availability(self, piece, origin_square)

        # Handle piece promotion if applicable
        promotion = ""
        if type(piece) == Pawn:
            promotion = handle_promotion(self, piece, destination_square_idx)
            # promotion = move[4] if len(move) == 5 else '' # based on LLM output

        # Verify check given new board state
        check = verify_check_after_move(self)
        if check:
            verify_checkmate(self)

        # Update gamelog
        self.update_gamelog(
            piece,
            origin_square,
            destination_square,
            capture,
            check,
            castling,
            promotion,
        )

        # Update game state
        self.swap_active_colour()
        if type(piece) == Pawn or capture:
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1
        if piece.colour == "b":
            self.fullmove_number += 1

    def print(self, mode="-clean"):
        board = self.array
        if mode == "-clean":
            for row in board:
                row = list(
                    map(lambda x: x.id if issubclass(type(x), Piece) else x, row)
                )
                row = list(map(lambda x: " " if x == None else x, row))
                print(row)
        elif mode == "-FEN":
            pass
        elif mode == "-raw":
            for row in board:
                print(row)
        else:
            raise Exception(
                "Board.print(): valid arguments for 'mode' are '-clean', '-FEN' or '-raw'."
            )

    def get_piece(self, square: str) -> Piece:
        index = name_to_idx(square)
        return self.array[index[0]][index[1]]

    def swap_active_colour(self):
        if self.active_colour == "w":
            self.active_colour = "b"
        elif self.active_colour == "b":
            self.active_colour = "w"

    def update_gamelog(
        self,
        piece: Piece,
        origin_square: str,
        destination_square: str,
        capture: bool = False,
        check: bool = False,
        castling: str = "",
        promotion: str = "",
    ):
        piece_str = piece.id.upper() if type(piece) != Pawn else ""

        check_str = ""
        if self.checkmate == True:
            check_str = "#"
        elif check == True:
            check_str = "+"

        capture_str = ""
        if capture and type(piece) != Pawn:
            capture_str = "x"
        elif capture and type(piece) == Pawn:
            capture_str = (
                f"{origin_square[0]}x"  # add column origin file if piece is a pawn
            )

        move_str = f"{piece_str}{capture_str}{destination_square}{promotion}{check_str}"
        if castling == "queenside":
            move_str = "0-0-0"
        elif castling == "kingside":
            move_str = "0-0"

        if self.active_colour == "w":
            self.gamelog += f"{self.fullmove_number}. {move_str} "
        elif self.active_colour == "b":
            self.gamelog += f"{move_str} "

    def move_piece(
        self,
        piece: Piece,
        origin_square_idx: tuple,
        destination_square_idx: tuple,
        castling: str,
    ):
        if castling is None:
            self.array[destination_square_idx[0]][destination_square_idx[1]] = piece
            self.array[origin_square_idx[0]][origin_square_idx[1]] = None
            piece.rect.center = self.sprites[idx_to_name(destination_square_idx)][
                "rect"
            ].center
            return

        if castling == "kingside" and self.active_colour == "w":
            rook_old_pos, rook_new_pos = name_to_idx("h1"), name_to_idx("f1")
            king_old_pos, king_new_pos = origin_square_idx, name_to_idx("g1")
            castle(self, piece, rook_old_pos, rook_new_pos, king_old_pos, king_new_pos)
            return

        if castling == "kingside" and self.active_colour == "b":
            rook_old_pos, rook_new_pos = name_to_idx("h8"), name_to_idx("f8")
            king_old_pos, king_new_pos = origin_square_idx, name_to_idx("g8")
            castle(self, piece, rook_old_pos, rook_new_pos, king_old_pos, king_new_pos)
            return

        if castling == "queenside" and self.active_colour == "w":
            rook_old_pos, rook_new_pos = name_to_idx("a1"), name_to_idx("d1")
            king_old_pos, king_new_pos = origin_square_idx, name_to_idx("c1")
            castle(self, piece, rook_old_pos, rook_new_pos, king_old_pos, king_new_pos)
            return

        if castling == "queenside" and self.active_colour == "b":
            rook_old_pos, rook_new_pos = name_to_idx("a8"), name_to_idx("d8")
            king_old_pos, king_new_pos = origin_square_idx, name_to_idx("c8")
            castle(self, piece, rook_old_pos, rook_new_pos, king_old_pos, king_new_pos)
            return


# Helper functions


def verify_check_after_move(board: Board):
    # Verifies whether a succesful move results to a check

    # Step 0: Find position of enemy king -> to be replaced later with a better implementation
    opposite_king_id = "k" if board.active_colour == "w" else "K"
    opposite_king_pos = None
    for rank in range(0, len(board.array)):
        for file in range(0, len(board.array[rank])):
            piece = board.array[rank][file]
            if piece != None and piece.id == opposite_king_id:
                opposite_king_pos = idx_to_name((rank, file))
                break

    # Step 1: calculate squares under threat
    pieces = board.active_pieces[board.active_colour]
    squares_under_threat = []
    for piece in pieces:
        squares_under_threat += piece.get_attacking_squares(board)

    # Step 2: verify check
    if opposite_king_pos in squares_under_threat:
        return True

    return False


def verify_checkmate(board: Board):
    opposite_colour = "b" if board.active_colour == "w" else "w"

    possible_moves_for_opposite_colour = []
    for piece in board.active_pieces[opposite_colour]:
        possible_moves_for_opposite_colour += piece.get_legal_moves(board)

    if len(possible_moves_for_opposite_colour) == 0:
        board.checkmate = True


def verify_castling(piece: Piece, move: str, castling_availability: dict) -> str:
    # Used to move pieces correctly in case castling is requested
    if move == "e1g1" or move == "e1h1" or move == "e8g8" or move == "e8h8":
        return "kingside"
    if move == "e1c1" or move == "e1a1" or move == "e8c8" or move == "e8a8":
        return "queenside"
    return None


def update_castling_availability(board: Board, piece: Piece, square_of_origin: str):
    if (
        board.castling_availability["white_kingside"] == False
        and board.castling_availability["white_queenside"] == False
        and board.castling_availability["black_kingside"] == False
        and board.castling_availability["black_queenside"] == False
    ):
        return

    if type(piece) == King:
        if square_of_origin == "e1" and piece.colour == "w":
            board.castling_availability["white_kingside"] = False
            board.castling_availability["white_queenside"] = False
        elif square_of_origin == "e8" and piece.colour == "b":
            board.castling_availability["black_kingside"] = False
            board.castling_availability["black_queenside"] = False
        return

    if type(piece) == Rook:
        if square_of_origin == "a1" and piece.colour == "w":
            board.castling_availability["white_queenside"] = False
        elif square_of_origin == "h1" and piece.colour == "w":
            board.castling_availability["white_kingside"] = False
        elif square_of_origin == "a8" and piece.colour == "b":
            board.castling_availability["black_queenside"] = False
        elif square_of_origin == "h8" and piece.colour == "b":
            board.castling_availability["black_kingside"] = False
        return


def castle(self, piece, rook_old_pos, rook_new_pos, king_old_pos, king_new_pos):
    rook = self.array[rook_old_pos[0]][rook_old_pos[1]]
    king = piece
    self.array[rook_old_pos[0]][rook_old_pos[1]] = None
    self.array[rook_new_pos[0]][rook_new_pos[1]] = rook
    self.array[king_old_pos[0]][king_old_pos[1]] = None
    self.array[king_new_pos[0]][king_new_pos[1]] = king
    rook.rect.center = self.sprites[idx_to_name(rook_new_pos)]["rect"].center
    piece.rect.center = self.sprites[idx_to_name(king_new_pos)]["rect"].center
    return


def verify_capture(board: Board, piece: Piece, destination_square_idx: tuple):
    # Handle normal captures
    destination_content = board.array[destination_square_idx[0]][
        destination_square_idx[1]
    ]
    if destination_content != None and destination_content.colour != piece.colour:
        captured_piece = destination_content
        capture_piece(board, captured_piece)
        return True

    # Handle enpassant captures
    if (
        type(piece) == Pawn
        and idx_to_name(destination_square_idx) == board.enpassant["target_square"]
    ):
        captured_piece = board.enpassant["target_piece"]
        captured_piece_pos = board.enpassant["target_pos"]
        board.array[captured_piece_pos[0]][captured_piece_pos[1]] = None
        capture_piece(board, captured_piece)
        return True

    return False


def capture_piece(board: Board, captured_piece: Piece):
    if captured_piece.colour == "w":
        board.active_pieces["w"].remove(captured_piece)
        board.captured_pieces["w"].append(captured_piece)
    elif captured_piece.colour == "b":
        board.active_pieces["b"].remove(captured_piece)
        board.captured_pieces["b"].append(captured_piece)


def update_enpassant(
    board: Board, piece: Piece, origin_square_idx: tuple, destination_square_idx: tuple
):
    # Reset enpassant if the opportunity was not used
    if board.enpassant["target_colour"] == piece.colour:
        board.enpassant = {
            "target_piece": None,
            "target_pos": None,
            "target_square": "",
            "target_colour": "",
            "pieces": [],
        }

    move_length = abs(origin_square_idx[0] - destination_square_idx[0])
    if type(piece) != Pawn or move_length != 2:
        return

    left_square_idx = (destination_square_idx[0], destination_square_idx[1] - 1)
    left_square_content = board.array[left_square_idx[0]][left_square_idx[1]]

    right_square_idx = (destination_square_idx[0], destination_square_idx[1] + 1)
    right_square_content = board.array[right_square_idx[0]][right_square_idx[1]]

    if type(left_square_content) != Pawn and type(right_square_content) != Pawn:
        return

    target_modifier = 1 if piece.colour == "w" else -1
    board.enpassant["target_piece"] = piece
    board.enpassant["target_pos"] = destination_square_idx
    board.enpassant["target_square"] = idx_to_name(
        (destination_square_idx[0] + target_modifier, destination_square_idx[1])
    )
    board.enpassant["target_colour"] = piece.colour
    board.enpassant["pieces"] = [left_square_content, right_square_content]
    print(board.enpassant)


def handle_promotion(board: Board, pawn: Piece, destination_square_idx: tuple):
    if (pawn.colour == "w" and destination_square_idx[0] == 0) or (
        pawn.colour == "b" and destination_square_idx[0] == 7
    ):
        new_piece = Queen(pawn.colour)
        square_rect = board.sprites[idx_to_name(destination_square_idx)]["rect"]
        new_piece.rect = new_piece.img.get_rect(topleft=(square_rect.x, square_rect.y))
        board.array[destination_square_idx[0]][destination_square_idx[1]] = new_piece
        board.active_pieces[pawn.colour].remove(pawn)
        board.active_pieces[pawn.colour].append(new_piece)
        return "=" + new_piece.id
    return ""


def init_empty_board() -> list:
    return [[None for _ in range(8)] for _ in range(8)]


def fill_board(board: list) -> None:
    # WHITE PIECES
    set_piece(Rook, "w", "a1", board)
    set_piece(Knight, "w", "b1", board)
    set_piece(Bishop, "w", "c1", board)
    set_piece(Queen, "w", "d1", board)
    set_piece(King, "w", "e1", board)
    set_piece(Bishop, "w", "f1", board)
    set_piece(Knight, "w", "g1", board)
    set_piece(Rook, "w", "h1", board)

    # WHITE PAWNS
    white_pawn_squares = ["a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2"]
    for square in white_pawn_squares:
        set_piece(Pawn, "w", square, board)

    # BLACK PIECES
    set_piece(Rook, "b", "a8", board)
    set_piece(Knight, "b", "b8", board)
    set_piece(Bishop, "b", "c8", board)
    set_piece(Queen, "b", "d8", board)
    set_piece(King, "b", "e8", board)
    set_piece(Bishop, "b", "f8", board)
    set_piece(Knight, "b", "g8", board)
    set_piece(Rook, "b", "h8", board)

    # BLACK PAWNS
    black_pawn_squares = ["a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7"]
    for square in black_pawn_squares:
        set_piece(Pawn, "b", square, board)


def set_piece(piece_type: Piece, colour: str, square: str, board: Board) -> None:
    # Initialize new piece
    new_piece = piece_type(colour)
    # Update board with new piece at specified square
    index_loc = name_to_idx(square)
    board.array[index_loc[0]][index_loc[1]] = new_piece
    # Update active piece dictionary with new piece
    if colour == "w":
        board.active_pieces["w"].append(new_piece)
    elif colour == "b":
        board.active_pieces["b"].append(new_piece)


def init_board_sprites() -> dict:
    # Creates a dictionary used by pygame to draw to screen:
    #   - key = square on the board
    #   - value = data needed for pygame to draw a GUI (image, rect)

    gui_dict = {}

    is_light = False  # simple bool to alternate between light/dark squares
    for row in range(0, len(BOARD_REF)):
        is_light = not is_light
        for col in range(0, len(BOARD_REF[row])):
            square_name = BOARD_REF[row][col]
            square_img = (
                SPRITES_DICT["square_light"]
                if is_light
                else SPRITES_DICT["square_dark"]
            )

            x = col * CELL_WIDTH
            y = row * CELL_HEIGHT
            square_rect = square_img.get_rect(topleft=(x, y))

            gui_dict[square_name] = {
                "img": square_img,  # Used to store sprite to draw to screen
                "rect": square_rect,  # Used to store the square's hitbox
            }
            is_light = not is_light

    return gui_dict


def init_piece_sprites(board: Board):
    # Initializes the rect of pieces to their corresponding square
    # Inneficient because this could be done when calling fill_board() and set_piece()
    # but at least the backend and frontend operations are decoupled and I can more easily swap to a different frontend when needed
    # + it is an operation done a initialization and not at runtime
    for piece in board.active_pieces["w"] + board.active_pieces["b"]:
        square = idx_to_name(piece.get_position(board.array))
        square_rect = board.sprites[square]["rect"]
        piece.rect = piece.img.get_rect(topleft=(square_rect.x, square_rect.y))


def short_to_long_algebraic(short_algebraic: str, board: Board) -> str:
    # Remove check notation ('+' or '#') to simplify parsing
    if short_algebraic[-1] == "+" or short_algebraic[-1] == "#":
        short_algebraic = short_algebraic[:-1]

    # Kingside castling
    if short_algebraic == "0-0":
        long_algebraic = "e1g1" if board.active_colour == "w" else "e8g8"
        return long_algebraic

    # Queenside castling
    if short_algebraic == "0-0-0":
        long_algebraic = "e1c1" if board.active_colour == "w" else "e8c8"
        return long_algebraic

    destination_square = short_algebraic[-2:]
    destination_square_idx = name_to_idx(destination_square)

    # Pawn move (e.g. 'e2', 'd6')
    if len(short_algebraic) == 2:
        # For a normal pawn move we only need to check the same colomn/file
        direction_rank = (
            1 if board.active_colour == "w" else -1
        )  # used to iterate through the same column in the right direction (up/down)
        for i in range(1, 3):
            origin_square_idx = (
                destination_square_idx[0] + i * direction_rank,
                destination_square_idx[1],
            )
            content = board.array[origin_square_idx[0]][origin_square_idx[1]]
            if type(content) == Pawn and destination_square in content.get_legal_moves(
                board
            ):
                return idx_to_name(origin_square_idx) + destination_square

    # Pawn capture (e.g. 'cxd4', 'exd4')
    if len(short_algebraic) == 4 and short_algebraic[0].islower():
        direction_rank = 1 if board.active_colour == "w" else -1
        origin_file = short_algebraic[0]
        direction_file = 1 if origin_file > destination_square[0] else -1
        origin_square_idx = (
            destination_square_idx[0] + direction_rank,
            destination_square_idx[1] + direction_file,
        )
        return idx_to_name(origin_square_idx) + destination_square

    # Piece move or capture (e.g. 'Bf5', 'Qc2', 'Bxc2', 'Nxc2')
    if short_algebraic[0].isupper():
        piece_id = short_algebraic[0]
        for piece in board.active_pieces[board.active_colour]:
            if piece.id.upper() != piece_id:
                continue
            if destination_square in piece.get_legal_moves(board):
                origin_square = idx_to_name(piece.get_position(board.array))
                return origin_square + destination_square
    # TODO: implement checks for when two pieces could do the move (for rooks and knights)

    raise Exception("Error: invalid move")

    """
    castling = 0-0 or 0-0-0
    pawn move = e3, d6
    pawn capture = cxd4, exd4
    piece move = Bf5, Qc2
    piece capture = Bxc2 (taking a queen), Nxc2 (taking a bishop)
    check = Bb5+, Qxb5+
    checkmate = Qxb5#
    """
