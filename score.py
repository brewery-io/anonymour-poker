import getopt
import sys
import json
import operator

def straight_flush(cards):

	suits = {
		"diamonds": 0,
		"clubs": 0,
		"hearts": 0,
		"spades": 0
	}

	hand_of_five = []
	flush_hand = []
	for card in cards:
		suits[card["suit"]] += 1

	for suit in suits:
		if suits[suit] > 4:
			for card in cards:
				if card['suit'] == suit:
					flush_hand.append(card)

	if len(flush_hand) > 4:
		if flush_hand[-1]['name'] == 'ace' and flush_hand[0]['name'] == '2' and flush_hand[1]['name'] == '3' and flush_hand[2]['name'] == '4' and flush_hand[3]['name'] == '5':
			hand_of_five.extend([flush_hand[-1], flush_hand[0], flush_hand[1], flush_hand[2], flush_hand[3]]);
			return hand_of_five

	last_card = 0
	counter = 0
	for card in flush_hand:
		if last_card == 0:
			last_card = card['value']
			hand_of_five.append(card)
		elif card['value'] - 1 == last_card:
			if len(hand_of_five) < 5:
				last_card = card['value']
				hand_of_five.append(card)
		else:
			if len(hand_of_five) < 5:
				last_card = card['value']
				hand_of_five = []
				hand_of_five.append(card)

	if len(hand_of_five) == 5:
		return hand_of_five

	return False

def four_of_a_kind(cards):

	matches = {}

	hand_of_five = [];

	for card in cards:
		if card['name'] in matches:
			matches[card['name']] += 1
		else:
			matches[card['name']] = 1

	for match in matches:
		if matches[match] == 4:
			for card in cards:
				if card['name'] == match:
					hand_of_five.append(card)
			if cards[-1]['name'] != match:
				hand_of_five.append(cards[-1])
			else:
				hand_of_five.append(cards[-5])

			return hand_of_five

	return False

def full_house(cards):

	trips = {}
	trips_count = 0
	hand_of_five = []

	for card in cards:
		if card['value'] in trips:
			trips[card['value']] += 1
		else:
			trips[card['value']] = 1

	for trip in trips:
		if trips[trip] == 3:
			trips_count += 1

	if trips_count == 1:
		for trip in trips:
			if trips[trip] == 3:
				for card in cards:
					if card['value'] == trip:
						hand_of_five.append(card)
	elif trips_count == 2:
		first_trip = True
		for trip in trips:
			if trips[trip] == 3:
				if first_trip:
					first_trip = False
				else:
					for card in cards:
						if card['value'] == trip:
							hand_of_five.append(card)

	if len(hand_of_five) == 3:

		pairs = {}
		pairs_count = 0

		for card in cards:
			if card not in hand_of_five:
				if card['value'] in pairs:
					pairs[card['value']] += 1
				else:
					pairs[card['value']] = 1

		for pair in pairs:
			if pairs[pair] > 1:
				pairs_count += 1

		if pairs_count == 1:
			for pair in pairs:
				if pairs[pair] > 1:
					for card in cards:
						if len(hand_of_five) != 5:
							if card['value'] == pair:
								hand_of_five.append(card)
			return hand_of_five

		elif pairs_count == 2:
			for card in cards:
				if card['value'] == pairs.keys()[1]:
					hand_of_five.append(card)
			return hand_of_five


	return False

def flush(cards):

	suits = {
		"diamonds": 0,
		"clubs": 0,
		"hearts": 0,
		"spades": 0
	}

	hand_of_five = []

	for card in cards:
		suits[card["suit"]] += 1

	for suit in suits:
		if suits[suit] > 4:
			for card in cards:
				if card['suit'] == suit:
					hand_of_five.append(card)

			while len(hand_of_five) > 5:
				del(hand_of_five[0])

			return hand_of_five
		else:
			return False

def straight(cards):

	hand_of_five = []
	unique = []
	unique_names = []

	for card in cards:
		if card['name'] not in unique_names:
			unique.append(card)
			unique_names.append(card['name'])

	last_card = 0
	counter = 0
	for card in (unique):
		if last_card == 0:
			last_card = card['value']
			hand_of_five.append(card)
		elif card['value'] - 1 == last_card:
			last_card = card['value']
			hand_of_five.append(card)
		else:
			last_card = card['value']
			hand_of_five = []
			hand_of_five.append(card)

	if len(hand_of_five) == 5:
		return hand_of_five
	elif len(hand_of_five) > 5:
		return hand_of_five[-5:]

	elif unique[-1]['name'] == 'ace' and unique[0]['name'] == '2' and unique[1]['name'] == '3' and unique[2]['name'] == '4' and unique[3]['name'] == '5':
		hand_of_five.extend([unique[-1], unique[0], unique[1], unique[2], unique[3]]);
		return hand_of_five


	return False

def three_of_a_kind(cards):

	trips = {}
	trips_count = 0
	hand_of_five = []

	for card in cards:
		if card['value'] in trips:
			trips[card['value']] += 1
		else:
			trips[card['value']] = 1

	for trip in trips:
		if trips[trip] == 3:
			trips_count += 1

	if trips_count == 1:
		for trip in trips:
			if trips[trip] == 3:
				for card in cards:
					if card['value'] == trip:
						hand_of_five.append(card)
		for card in cards:
			if len(hand_of_five) != 5:
				if card not in hand_of_five:
					hand_of_five.append(card)
			else:
				return hand_of_five
	elif trips_count == 2:
		first_trip = True
		for trip in trips:
			if trips[trip] == 3:
				if first_trip == True:
					first_trip = False
				else:
					for card in cards:
						if card['value'] == trip:
							hand_of_five.append(card)
		for card in cards:
			if len(hand_of_five) != 5:
				if card not in hand_of_five:
					hand_of_five.append(card)
			else:
				return hand_of_five


	return False

def two_pairs(cards):

	pairs = {}
	pairs_count = 0
	hand_of_five = []

	for card in cards:
		if card['value'] in pairs:
			pairs[card['value']] += 1
		else:
			pairs[card['value']] = 1

	for pair in pairs:
		if pairs[pair] == 2:
			pairs_count += 1

	pairs_list = pairs.items()

	if pairs_count == 2:
		for pair in list(reversed(pairs_list)):
			if pair[1] == 2:
				for card in list(reversed(cards)):
					if card['value'] == pair[0]:
						hand_of_five.append(card)

	elif pairs_count == 3:
		sorted_pairs = sorted(pairs.items(), key=operator.itemgetter(0))
		i = 0
		for pair in list(reversed(sorted_pairs)):
			if i < 3 and pair[1] == 2:
				for card in cards:
					if card['value'] == pair[0]:
						hand_of_five.append(card)
			i += 1

	if cards[-1] not in hand_of_five:
		hand_of_five.append(cards[-1])
	elif cards[-3] not in hand_of_five:
		hand_of_five.append(cards[-3])
	else:
		hand_of_five.append(cards[-5])

	if len(hand_of_five) == 5:
		return list(reversed(hand_of_five))

	return False

def one_pair(cards):

	pairs = {}
	pairs_count = 0;
	hand_of_five = []

	for card in cards:
		if card['name'] in pairs:

			pairs[card['name']] += 1
		else:
			pairs[card['name']] = 1

	for pair in pairs:
		if pairs[pair] == 2:
			pairs_count += 1

	if pairs_count == 1:
		for pair in pairs:
			if pairs[pair] == 2:
				for card in cards:
					if card['name'] == pair:
						hand_of_five.append(card)

				card_no = -1
				for card in reversed(cards):
					if len(hand_of_five) < 5:
						if card['name'] == pair:
							card_no -= 1
						else:
							hand_of_five.append(card)
							card_no -= 1

		return hand_of_five

	return False

def high_card(cards):

	return cards[-5:]

def sort_hand(cards):

	if straight_flush(cards):
		return (8, straight_flush(cards), "Straight Flush")
	elif four_of_a_kind(cards):
		return (7, four_of_a_kind(cards), "Four of a Kind")
	elif full_house(cards):
		return (6, full_house(cards), "Full House")
	elif flush(cards):
		return (5, flush(cards), "Flush")
	elif straight(cards):
		return (4, straight(cards), "Straight")
	elif three_of_a_kind(cards):
		return (3, three_of_a_kind(cards), "Three of a Kind")
	elif two_pairs(cards):
		return (2, two_pairs(cards), "Two Pairs")
	elif one_pair(cards):
		return (1, one_pair(cards), "One Pair")
	elif high_card(cards):
		return (0, high_card(cards), "High Card")

def score(cards):

	(score_prefix, hand, hand_name) = sort_hand(cards)
	score = [str(score_prefix), 00, 00, 00, 00, 00]
	scorestr = ""

	score[1] = str(hand[4]['value']).zfill(2)
	score[2] = str(hand[3]['value']).zfill(2)
	score[3] = str(hand[2]['value']).zfill(2)
	score[4] = str(hand[1]['value']).zfill(2)
	score[5] = str(hand[0]['value']).zfill(2)

	for sub in score:
		scorestr += sub

	result = {}

	result["cards"] = cards
	result["hand_of_five"] = hand
	result["score"] = score
	result["scorestr"] = scorestr
	result["hand_name"] = hand_name

	return json.dumps(result)

def api_main(cards):
	cards_list = json.loads(cards)
	sorted_cards_list = sorted(cards_list, key = lambda x: x["value"])

	score(sorted_cards_list)

def main(argv):

	try:
		opts, args = getopt.getopt(argv, "c:", ["cards="])

		cards_list = json.loads(opts[0][1])
		sorted_cards_list = sorted(cards_list, key = lambda x: x["value"])	#sort it

		score(sorted_cards_list)

	except getopt.GetoptError:
		usage()
		sys.exit(2)

if __name__ == "__main__":
	main(sys.argv[1:])
