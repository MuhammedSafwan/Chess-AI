import chess
import chess.svg
import chess.polyglot
import time
import traceback
import chess.pgn
import chess.engine
from flask import Flask, Response, request
import webbrowser
import pyttsx3


# Evaluating the board
pawntable = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0]

knightstable = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50]

bishopstable = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20]

rookstable = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0]

queenstable = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 5, 5, 5, 5, 5, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20]

kingstable = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30]


def evaluate_board():
    if board.is_checkmate():
        if board.turn:
            return -9999
        else:
            return 9999
    if board.is_stalemate():
        return 0
    if board.is_insufficient_material():
        return 0

    wp = len(board.pieces(chess.PAWN, chess.WHITE))
    bp = len(board.pieces(chess.PAWN, chess.BLACK))
    wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
    bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
    wb = len(board.pieces(chess.BISHOP, chess.WHITE))
    bb = len(board.pieces(chess.BISHOP, chess.BLACK))
    wr = len(board.pieces(chess.ROOK, chess.WHITE))
    br = len(board.pieces(chess.ROOK, chess.BLACK))
    wq = len(board.pieces(chess.QUEEN, chess.WHITE))
    bq = len(board.pieces(chess.QUEEN, chess.BLACK))

    material = 100 * (wp - bp) + 320 * (wn - bn) + 330 * (wb - bb) + 500 * (wr - br) + 900 * (wq - bq)

    pawnsq = sum([pawntable[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
    pawnsq = pawnsq + sum([-pawntable[chess.square_mirror(i)]
                           for i in board.pieces(chess.PAWN, chess.BLACK)])
    knightsq = sum([knightstable[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
    knightsq = knightsq + sum([-knightstable[chess.square_mirror(i)]
                               for i in board.pieces(chess.KNIGHT, chess.BLACK)])
    bishopsq = sum([bishopstable[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
    bishopsq = bishopsq + sum([-bishopstable[chess.square_mirror(i)]
                               for i in board.pieces(chess.BISHOP, chess.BLACK)])
    rooksq = sum([rookstable[i] for i in board.pieces(chess.ROOK, chess.WHITE)])
    rooksq = rooksq + sum([-rookstable[chess.square_mirror(i)]
                           for i in board.pieces(chess.ROOK, chess.BLACK)])
    queensq = sum([queenstable[i] for i in board.pieces(chess.QUEEN, chess.WHITE)])
    queensq = queensq + sum([-queenstable[chess.square_mirror(i)]
                             for i in board.pieces(chess.QUEEN, chess.BLACK)])
    kingsq = sum([kingstable[i] for i in board.pieces(chess.KING, chess.WHITE)])
    kingsq = kingsq + sum([-kingstable[chess.square_mirror(i)]
                           for i in board.pieces(chess.KING, chess.BLACK)])

    eval = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq
    if board.turn:
        return eval
    else:
        return -eval


# Searching the best move using minimax and alphabeta algorithm with negamax implementation
def alphabeta(alpha, beta, depthleft):
    bestscore = -9999
    if (depthleft == 0):
        return quiesce(alpha, beta)
    for move in board.legal_moves:
        board.push(move)
        score = -alphabeta(-beta, -alpha, depthleft - 1)
        board.pop()
        if (score >= beta):
            return score
        if (score > bestscore):
            bestscore = score
        if (score > alpha):
            alpha = score
    return bestscore


def quiesce(alpha, beta):
    stand_pat = evaluate_board()
    if (stand_pat >= beta):
        return beta
    if (alpha < stand_pat):
        alpha = stand_pat

    for move in board.legal_moves:
        if board.is_capture(move):
            board.push(move)
            score = -quiesce(-beta, -alpha)
            board.pop()

            if (score >= beta):
                return beta
            if (score > alpha):
                alpha = score
    return alpha


def selectmove(depth):
    try:
        move = chess.polyglot.MemoryMappedReader("C:/Users/your_path/books/human.bin").weighted_choice(board).move
        move = chess.polyglot.MemoryMappedReader("C:/Users/your_path/books/computer.bin").weighted_choice(board).move
        move = chess.polyglot.MemoryMappedReader("C:/Users/your_path/books/pecg_book.bin").weighted_choice(board).move
        return move
    except:
        bestMove = chess.Move.null()
        bestValue = -99999
        alpha = -100000
        beta = 100000
        for move in board.legal_moves:
            board.push(move)
            boardValue = -alphabeta(-beta, -alpha, depth - 1)
            if boardValue > bestValue:
                bestValue = boardValue
                bestMove = move
            if (boardValue > alpha):
                alpha = boardValue
            board.pop()
        return bestMove


# Speak Function for the Assistant to speak
def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Set index for voices currently 3 voices available
    engine.say(text)
    engine.runAndWait()


# Searching Dev-Zero's Move
def devmove():
    move = selectmove(3)
    speak(move)
    board.push(move)


# Searching Deuterium's Move
def deuterium():
    engine = chess.engine.SimpleEngine.popen_uci(
        "C:/Users/your_path/engines/Deuterium.exe")
    move = engine.play(board, chess.engine.Limit(time=0.1))
    speak(move.move)
    board.push(move.move)


# Searching CDrill's Move
def cdrill():
    engine = chess.engine.SimpleEngine.popen_uci(
        "C:/Users/your_path/engines/CDrill.exe")
    move = engine.play(board, chess.engine.Limit(time=0.1))
    speak(move.move)
    board.push(move.move)


# Searching Stockfish's Move
def stockfish():
    engine = chess.engine.SimpleEngine.popen_uci(
        "C:/Users/your_path/engines/stockfish.exe")
    move = engine.play(board, chess.engine.Limit(time=0.1))
    speak(move.move)
    board.push(move.move)


app = Flask(__name__)


# Introduction lines
def lines():
    speak(
        "Hello my batch number is 17")


# Front Page of the Flask Web Page
@app.route("/")
def main():
    global count, board
    if count == 1:
        lines()
        count += 1
    ret = '<html><head>'
    ret += '<style>'
    ret += 'input {font-size: 15px; }'
    ret += 'button { font-size: 15px; }'
    ret += 'body {'
    ret += 'background-image: linear-gradient(to bottom, #3D5A80, #98C1D9);'
    ret += 'background-size: 200% 200%;'
    ret += 'animation: gradient 20s ease infinite;'
    ret += '}'
    ret += '@keyframes gradient {'
    ret += '0% {'
    ret += 'background-position: 0% 50%;'
    ret += '}'
    ret += '50% {'
    ret += 'background-position: 100% 50%;'
    ret += '}'
    ret += '100% {'
    ret += 'background-position: 0% 50%;'
    ret += '}'
    ret += '}'
    ret += '</style>'
    ret += '</head><body>'
    ret += '<div style="text-align: center;"><img width=430 height=430 src="/board.svg?%f"></img></div><br/>' % time.time()
    
    ret += '<h1 style="position: absolute; top: 30px; left: 150px; color: black; font-family: Arial, sans-serif;">Chess-AI</h1>'

    
    ret += '<div style="text-align: center;">'
    
    ret += '<div style="display: inline-block; margin-right: 10px;">'
    ret += '<form action="/game/" method="post"><button name="New Game" type="submit" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer;">New Game</button></form>'
    ret += '</div>'

    ret += '<div style="display: inline-block;">'
    ret += '<form action="/undo/" method="post"><button name="Undo" type="submit" style="background-color: #008CBA; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer;">Undo Last Move</button></form>'
    ret += '</div>'

    ret += '<form action="/move/"><input type="submit" value="Make Human Move:" style="background-color: #f44336; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer;"><input name="move" type="text" style="padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer;></input></form>'

    ret += '<br><div style="display: flex; justify-content: center; margin-top: 20px;">'
    ret += '<form action="/recv/" method="post"><!--button name="Receive Move" type="submit" style="background-color: #008CBA; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer;">Receive Human Move</button--></form>'
    ret += '<span style="margin: 0 10px;"></span>'
    ret += '<form action="/dev/" method="post"><button name="Comp Move" type="submit" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer;">Make Dev Move</button></form>'
    ret += '</div>'

    ret += '<form action="/inst/" method="post"><!--button name="Instructions" type="submit" style="background-color: #f44336; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer;">Instructions</button--></form>'

    ret += '<!--div><form action="/engine/" method="post"><button name="engine" type="submit" style="background-color: #f44336; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer;">Stock</button></form>'

    ret += '</div-->'

    if board.is_stalemate():
        speak("Its a draw by stalemate")
    elif board.is_checkmate():
        speak("Checkmate")
    elif board.is_insufficient_material():
        speak("Its a draw by insufficient material")
    elif board.is_check():
        speak("Check")
    return ret


# Display Board
@app.route("/board.svg/")
def board():
    return Response(chess.svg.board(board=board, size=700), mimetype='image/svg+xml')


# Human Move
@app.route("/move/")
def move():
    try:
        move = request.args.get('move', default="")
        speak(move)
        board.push_san(move)
    except Exception:
        traceback.print_exc()
    return main()


# Recieve Human Move
@app.route("/recv/", methods=['POST'])
def recv():
    try:
        None
    except Exception:
        None
    return main()


# Make Dev-Zero Move
@app.route("/dev/", methods=['POST'])
def dev():
    try:
        devmove()
    except Exception:
        traceback.print_exc()
        speak("illegal move, try again")
    return main()


# Make UCI Compatible engine's move
@app.route("/engine/", methods=['POST'])
def engine():
    try:
        stockfish()
        # cdrill()
        # deuterium()
    except Exception:
        traceback.print_exc()
        speak("illegal move, try again")
    return main()


# New Game
@app.route("/game/", methods=['POST'])
def game():
    speak("Board Reset, Best of Luck for the next game.")
    board.reset()
    return main()


# Undo
@app.route("/undo/", methods=['POST'])
def undo():
    try:
        board.pop()
    except Exception:
        traceback.print_exc()
        speak("Nothing to undo")
    return main()






# Main Function
if __name__ == '__main__':
    count = 1
    board = chess.Board()
    webbrowser.open("http://127.0.0.1:5000/")
    app.run()
