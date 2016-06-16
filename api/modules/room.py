import getopt
import sys
import json

def start_game(players, max_players):


def main(argv):

	try:
		opts, args = getopt.getopt(argv, "p:m:", ["players=", "max="])
		for opt in opts:
			if opt[0] == "-m":
				max_players = opt[1]
			elif opt[0] == "-p":
				players = opt[1]

		start_game(players, max_players)


	except getopt.GetoptError:
		print "error"
		sys.exit()

if __name__ == "__main__":
	main(sys.argv[1:])
