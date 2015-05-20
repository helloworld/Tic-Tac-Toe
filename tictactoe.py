from itertools import permutations
import pickle as pkl
import os.path
import random

def printBoard(board):
	print("|".join(board[0:3]))
	print("|".join(board[3:6]))
	print("|".join(board[6:9]))
	print()


def stringBoard(perm, limit):
	newBoard = '---------'
	for n in range(limit+1):
		if n % 2 == 0:
			newBoard = insertX(newBoard, perm.index(n))
		else:
			newBoard = insertO(newBoard, perm.index(n))
	return newBoard

def insertX(board, index):
	return board[:index] + "X" + board[index+1:]

def insertO(board, index):
	return board[:index] + "O" + board[index+1:]

def moveIsPossible(board):
	for row in [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]:
		(first, second, third) = row
		if (board[first] == board[second] and board[second] == board[third]) and (board[first] != "-"):
 			return False
		if(board.count("-") == 0):
			return False
	return True

def getWinner(board):
	for row in [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]:
		(first, second, third) = row
		if (board[first] == board[second] and board[second] == board[third]) and (board[first] != "-"):
 			return board[first]
		if(board.count("-") == 0):
			return "-"
	raise ValueError('Game should be playable') 

def createDatabase():
	database = {'---------': [1,1,1,1,1,1,1,1,1]}
	sequence = [0,1,2,3,4,5,6,7,8,]
	filledBoards = list(permutations(sequence, 9))
	for i in filledBoards:
		for limit in range(9):
			board = stringBoard(i, limit)
			if(moveIsPossible(board)):
				database[board] = [1,1,1,1,1,1,1,1,1]
	return database


def weightedChoice(weights, board):
	for i, mark in enumerate(board):
		if(mark != "-"):
			weights[i] = 0

	totals = []
	running_total = 0

	for w in weights:
	    running_total += w
	    totals.append(running_total)

	rnd = random.random() * running_total
	for i, total in enumerate(totals):
	    if rnd < total:
	        return i


def train(database):
	for i in range(1000000):
		print(i)
		database = trainRun(database)
		print("-----------------------")

	return database

def trainRun(database):
	board = "---------"
	turn = "X"
	xBoards = []
	oBoards = []
	selectedIndexes = []

	while(moveIsPossible(board)):
		if(turn == "X"):
			oldBoard, board, pos = xTurn(board, database)
			xBoards.append((oldBoard, pos))
			turn = "O"
		elif(turn == "O"):
			oldBoard, board, pos = oTurn(board, database)
			oBoards.append((oldBoard, pos))
			turn = "X"
		print("\t", board)

	winner = getWinner(board)
	print("Winner", winner)
	printBoard(board)

	if(winner == "X"):
		for i in xBoards[:-1]:
			database[i[0]][i[1]] += 3
		for i in oBoards[:-1]:
			if(database[i[0]][i[1]] > 1):
				database[i[0]][i[1]] -= 1
	elif(winner == "O"):
		for i in oBoards[:-1]:
			database[i[0]][i[1]] += 3
		for i in xBoards[:-1]:
			if(database[i[0]][i[1]] > 1):
				database[i[0]][i[1]] -= 1
	else:
		for i in oBoards[:-1]:
			database[i[0]][i[1]] += 1
		for i in xBoards[:-1]:
			database[i[0]][i[1]] += 1

	return database

def xTurn(board, database):
	currentBoardProbabilities = database[board]
	selectedIndex = weightedChoice(currentBoardProbabilities, board)
	newBoard = insertX(board, selectedIndex)
	return board, newBoard, selectedIndex

def oTurn(board, database):
	currentBoardProbabilities = database[board]
	selectedIndex = weightedChoice(currentBoardProbabilities, board)
	newBoard = insertO(board, selectedIndex)
	return board, newBoard, selectedIndex

def getProbabilities():
	if(os.path.exists('./probabilities.pkl')):
		probabilities = pkl.load(open('probabilities.pkl', 'rb'))
	else:
		if(os.path.exists('./database.pkl')):
			db = pkl.load(open('database.pkl', 'rb'))
		else:
			db = createDatabase()
			pkl.dump(database, open( 'database.pkl', 'wb'))

		probabilities = train(db)
		pkl.dump(db, open('probabilities.pkl', 'wb'))

	return probabilities

def main():
	probabilities = getProbabilities()

if __name__ == '__main__':
	main()


