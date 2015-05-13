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

def isWin(board):
	for row in [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]:
		(first, second, third) = row
		if (board[first] == board[second] and board[second] == board[third]) and (board[first] != "-"):
 			return True
		if(board.count("-") == 0):
			return True
	return False

def main():
	database = {'---------': 0}
	sequence = [0,1,2,3,4,5,6,7,8,]
	filledBoards = list(permutations(sequence, 9))
	for i in filledBoards:
		for limit in range(9):
			board = stringBoard(i, limit)
			if(not isWin(board)):
				database[board] = 0
	print(len(database))


if __name__ == '__main__':
	from itertools import permutations
	main()


