from os import listdir
from os.path import isfile, join
import re


# Takes a string input of the form '1. g4 f5 2. gxf5 g6 3. fxg6 hxg6 4. Bg5 Qxg5# 1-0'
# and parses it into a list of move tuples such as [('g4', 'f5'), ('gxf5', 'g6'), ('fxg6', 'hxg6'), ('Bg5', 'Qxg5')]
# Notes:
#	1. Removes the scoring element at the end of the input string: '1-0' in the example above
#	2. Removes the '#' from the last move in the game
#	3. If the player who went first won (there are an odd number of moves), the last tuple will have None as its second element
def parseGame(gameLine):

	gameData = gameLine.split(' ')

	# make sure the game ends by listing the winner, and remove that
	if re.match('\A\d+-\d+\Z', gameData[len(gameData) - 1]) == None:
		return None
	winner = gameData.pop()

	# remove the '#' indicating the game ended
	lastMove = gameData[len(gameData) - 1]
	if not lastMove.endswith('#'):
		return None
	gameData[len(gameData) - 1] = lastMove[:len(lastMove) - 1]

	moveList = []
	firstPlayerMove = None
	for i in xrange(len(gameData)):
		if i % 3 == 0:
			if re.match('\A\d+\.\Z', gameData[i]) == None:
				return None
		elif i % 3 == 1:
			firstPlayerMove = gameData[i]
		else:
			moveList.append((firstPlayerMove, gameData[i]))
			firstPlayerMove = None

	# the player who went first won, so there is an odd number of moves
	if firstPlayerMove != None:
		moveList.append((firstPlayerMove, None))
	return moveList


def main():
	data_folder = 'data/'
	for f in listdir(data_folder):
		if not isfile(join(data_folder, f)):
			continue

		file_reader = open(join(data_folder, f), 'r')

		lineNum = 0
		for line in file_reader:
			line = line.strip()
			if lineNum % 2 == 0:
				print 'Parsing', line
			else:
				print parseGame(line)
				print
			lineNum += 1


if __name__=="__main__":
    main()