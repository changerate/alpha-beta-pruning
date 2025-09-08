# Carlos Vargas 
# July 5th, 2025

# CS 4200 - Artificial Intelligence
# Professor Daisy Tang 
# California State Polytechnic University - Pomona










# =================================================================================================
#                              globals and imports
# =================================================================================================



import time
import os # For clearing the terminal



BOARD_HEIGHT = 8
BOARD_LENGTH = 8
TO_WIN = 4

MAX_DEPTH = 7
MAX_TIME = 5 # seconds

offensiveMultiplier = 1
defensiveMultiplier = 4
WEIGHTS = {'XOneInPattern': 1 * offensiveMultiplier, 
           'XTwoInPattern': 10 * offensiveMultiplier, 
           'XThreeInPattern': 1000 * offensiveMultiplier, 
           'XFourInPattern': 10000 * offensiveMultiplier, 
           'XForcedWinPattern': 10000 * offensiveMultiplier, 
           'OOneInPattern': -1 * defensiveMultiplier, 
           'OTwoInPattern': -10 * defensiveMultiplier, 
           'OThreeInPattern': -1000 * defensiveMultiplier, 
           'OFourInPattern': -10000 * defensiveMultiplier,
           'OForcedWinPattern': -10000 * defensiveMultiplier, 
           'XCenterSquaresMultiple': 0.5, 
           'OCenterSquaresMultiple': -0.5}



















# =================================================================================================
#                              functions
# =================================================================================================



def setup(): 
    print(f"\n\nWelcome to the alpha-beta pruning algorithm\nthat's battling you in a game of tic-tac-toe.\n")
    return [['-' for i in range(BOARD_LENGTH)] for x in range(BOARD_HEIGHT)]





def printBoard():
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']    
    rows = [letters[i] for i in range(len(b))]
    boardLength = len(b[0])
    boardHeight = len(b)

    print(end= '  ')
    for i in range(boardLength): 
        print(i+1, end=' ')
    print()
    
    for row in range(boardHeight):
        print(rows[row], end=' ')
        for col in range(boardLength):
            print(b[row][col], end=' ')
        print()
    print()




def getAMove():
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']    
    rows = [letters[i] for i in range(8)]

    while True:
        move = input("Enter your move: ")

        # check for legality 
        if len(move) != 2:
            print("Invalid entry try again.")
            continue
        try:
            rowMove = move[0]
            colMove = int(move[1])
        except: 
            print("Invalid entry try again.")
            continue

        # check for legality 
        if rowMove.upper() not in rows: 
            print("Invalid entry try again.")
            print(f"{rowMove} is not ok.")    
            continue
        if BOARD_LENGTH < colMove or colMove < 1:
            print("Invalid entry try again.")
            print(f"{colMove} is not ok.")    
            continue

        rowMove = rows.index(rowMove.upper())
        colMove -= 1 # update to index notation

        # check for legality 
        if b[rowMove][colMove] != '-':
            print("Invalid entry try again.")
            continue
            
        
        print()
        b[rowMove][colMove] = 'O'
        return b
    




def checkGameOver(): 
    winner = check4Winner()
        
    if winner == WEIGHTS['OFourInPattern']:
        print("you win\n\n")
        exit(0)
    if winner == WEIGHTS['XFourInPattern']:
        print("The AI wins\n\n")
        exit(0)
    if winner != False:
        print("The game is a draw!")
        exit(0)
    print()





def check4Winner():
    empty = 0
    for row in range(len(b)):
        for col in range(len(b[0])): 
            player = b[row][col]

            if player != '-' and (checkForwardWinsRecursive(player, 1, row, col+1) or checkBelowWinsRecursive(player, 1, row+1, col)): 
                if player == 'X':
                    return WEIGHTS['XFourInPattern']
                else: return WEIGHTS['OFourInPattern']
            elif player == '-':
                empty += 1
    
    if empty == 0: 
        return 0.5 # draw

    return False






def checkForwardWinsRecursive(player, inARow, row, col): 
    if inARow >= TO_WIN:
        return True
    
    if col < BOARD_LENGTH: 
        if b[row][col] == player: 
            inARow += 1
        else: return False
    else: return False
    
    return checkForwardWinsRecursive(player, inARow, row, col+1)




    
def checkBelowWinsRecursive(player, inARow, row, col): 
    if inARow >= TO_WIN:
        return True
    
    if row < BOARD_HEIGHT: 
        if b[row][col] == player: 
            inARow += 1
        else: return False
    else: return False
    
    return checkBelowWinsRecursive(player, inARow, row+1, col)













# =================================================================================================
#                          minimax with a-b pruning 
# =================================================================================================



def evaluate(depth): 
    """
    this is assuming an 8x8 board with four in a row to win
    """
    score = 0
    
    # Count all 4-in-a-row patterns
    for pattern in getAllNPatterns():
        if pattern == "XXXX":
            return WEIGHTS['XFourInPattern']
        if pattern == "OOOO":
            return WEIGHTS['OFourInPattern']

        XCount = pattern.count('X')
        OCount = pattern.count('O')

        # Skip if both players have pieces (blocked line)
        if XCount > 0 and OCount > 0:
            continue

        # immediate threats 
        if OCount == TO_WIN - 1: score -= 1200
        if OCount == TO_WIN - 2: score -= 50
        
        # forced win (open spot)
        if XCount == 3 and OCount == 0: 
            score += WEIGHTS['XFourInPattern'] * 0.50
        if OCount == 3 and XCount == 0: 
            score += WEIGHTS['OFourInPattern'] * 0.95
        
        if XCount > 0:
            if XCount == 1: score += WEIGHTS['XOneInPattern']
            elif XCount == 2: score += WEIGHTS['XTwoInPattern']
            elif XCount == 3: score += WEIGHTS['XThreeInPattern']
            elif XCount == 4: score += WEIGHTS['XFourInPattern']
        if OCount > 0:
            if OCount == 1: score += WEIGHTS['OOneInPattern']
            elif OCount == 2: score += WEIGHTS['OTwoInPattern']
            elif OCount == 3: score += WEIGHTS['OThreeInPattern']
            elif OCount == 4: score += WEIGHTS['OFourInPattern']
    
    # Small bonus for center control
    score += countCenterSquares('X') * WEIGHTS['XCenterSquaresMultiple']
    score += countCenterSquares('O') * WEIGHTS['OCenterSquaresMultiple']

    return score

    
    
    

def makeAMove():
    """
    this function first generates a list of possible moves to make.
    Then it orders it by highest if it's the AI and by lowest if it's the min player.
    I decided to cutoff 30% of the end of the list and found that it still works beautifully.
    With each move it evaluates the min score which in turn evaluates the max score. 
    """
    best = -1000000
    depth = MAX_DEPTH
    mi = mj = 0
    alpha = -1000000 
    beta = 1000000
    timeStart = time.time()
    
    print("AI is thinking...")

    moves = []
    for i in range(BOARD_HEIGHT):
        for j in range(BOARD_LENGTH):
            if b[i][j] == '-':
                b[i][j] = 'X'
                moveScore = evaluate(depth)
                moves.append((moveScore, i, j))
                b[i][j] = '-'
                
    moves.sort(reverse=True)
    moves = moves[:round(len(moves)*0.70)] # shorten the list to the first some %

    for moveScore, i, j in moves:
        b[i][j] = 'X'
        score = minMove(depth - 1, alpha, beta, timeStart)
        if score > best:
            mi = i
            mj = j
            best = score
        alpha = max(alpha, score)
        b[i][j] = '-'  
    
    # convert mi ji to coords on the board 
    print(f"My move is {getLetterIndex(mi).lower()}{mj+1}")
    b[mi][mj] = 'X'
    print()
    
    
    


def minMove(depth, alpha, beta, timeStart):
    """
    Simulates the user's move
    """
    best = 1000000
    winner = check4Winner()

    if time.time() - timeStart > MAX_TIME - 0.1:
        return evaluate(depth - 1)
    if winner:
        return winner
    if winner == 0.5:
        # draw
        return winner
    if depth == 0:
        return evaluate(depth) 
    
    # Get all possible moves
    moves = []
    for i in range(BOARD_HEIGHT):
        for j in range(BOARD_LENGTH):
            if b[i][j] == '-':
                b[i][j] = 'O'
                moveScore = evaluate(depth) 
                moves.append((moveScore, i, j))
                b[i][j] = '-'

    # Sort moves by evaluation of worst for AI
    moves.sort()
    moves = moves[:round(len(moves)*0.70)] # shorten the list to the first some %

    for moveScore, i, j in moves:
        b[i][j] = 'O'  # opponent's move
        score = maxMove(depth - 1, alpha, beta, timeStart)
        if score < best:
            best = score
        beta = min(beta, score) 
        b[i][j] = '-' 
        
        # ALPHA BETA PRUNING
        if beta <= alpha:
            break 
    
    return best








def maxMove(depth, alpha, beta, timeStart):
    """
    AI move
    """
    best = -1000000
    winner = check4Winner()

    if time.time() - timeStart > MAX_TIME - 0.8:
        return evaluate(depth - 1)
    if winner:
        return winner
    if winner == 0.5:
        # draw
        return winner
    if depth == 0:
        return evaluate(depth)

    # Get all possible moves
    moves = []
    for i in range(BOARD_HEIGHT):
        for j in range(BOARD_LENGTH):
            if b[i][j] == '-':
                b[i][j] = 'X'
                moveScore = evaluate(depth)
                moves.append((moveScore, i, j))
                b[i][j] = '-'
    
    # Sort moves by evaluation by best
    moves.sort(reverse=True)
    moves = moves[:round(len(moves)*0.70)] # shorten the list to the first some %
    
    for moveScore, i, j in moves:
        b[i][j] = 'X'  
        score = minMove(depth - 1, alpha, beta, timeStart)
        if score > best:
            best = score
        alpha = max(alpha, score) 
        b[i][j] = '-' 
        
        # ALPHA BETA PRUNING
        if beta <= alpha:
            break 
    
    return best





    

def getAllNPatterns(): 
    patterns = []

    for row in range(BOARD_HEIGHT):
        rowStr = ''.join(b[row])  # Convert row to string once
        for col in range(BOARD_LENGTH - TO_WIN + 1):
            pttrn = rowStr[col:col+TO_WIN]
            if pttrn != '----':
                patterns.append(pttrn)

    # Vertical patterns - build column strings 
    colStrings = [''.join(b[row][col] for row in range(BOARD_HEIGHT)) 
                   for col in range(BOARD_LENGTH)]
    
    for colStr in colStrings:
        for row in range(BOARD_HEIGHT - TO_WIN + 1):
            pttrn = colStr[row:row+TO_WIN]
            if pttrn != '----':
                patterns.append(pttrn)

    return patterns




def countCenterSquares(player):
    """
    this is assuming an 8x8 board
    """
    count = 0
    for row in range(2, 6):
        for col in range(2, 6):
            if b[row][col] == player:
                count += 1
                
    return count

        


def getLetterIndex(rowIndex):
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']    
    rows = [letters[i] for i in range(BOARD_HEIGHT)]
    return rows[rowIndex]






    
    



    
    

# ====================================================================================
# ====================================================================================
#                                  MAIN
# ====================================================================================
# ====================================================================================
if __name__ == "__main__":
    # --------- clear the terminal
    def clear_terminal():
        os.system('cls' if os.name == 'nt' else 'clear')
    clear_terminal()
    
    # example of a draw: 
    b = [['O','X','O','O','X','-','O','O'],['O','O','O','X','O','O','X','-'],['X','X','X','O','X','X','X','O'],['O','X','O','O','X','O','X','X'],['O','X','O','O','X','X','O','O'],['O','O','X','X','O','O','X','X'],['X','X','O','X','O','X','X','O'],['X','X','O','X','O','X','O','X']]

    b = setup()
    printBoard()
    
    aiFirst = input("Who would you like to go first? Human or AI? (human or ai): ")
    if aiFirst.lower() == 'ai': 
        makeAMove()
    while True: 
        getAMove()
        printBoard()
        checkGameOver()
        makeAMove()
        printBoard()
        checkGameOver()
        