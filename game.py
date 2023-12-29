import random

def fisher_yates_shuffle(arr):
    n = len(arr)
    for i in range(n-1, 0, -1):
        j = random.randint(0, i)
        arr[i], arr[j] = arr[j], arr[i]
    return arr

class Card:
    def __init__(self, number, suit):
        self.number = number
        self.suit = suit
    
    def __repr__(self):
        return f"{self.number} {self.suit}"
    
def high_cards(cards):
    numbers = [card.number for card in cards]
    return sorted(numbers, reverse=True)[:5]

def pair_check(cards):
    tracker = {}
    pair_nums = []
    numbers = [card.number for card in cards]
    for number in numbers:
        if number in tracker:
            tracker[number] += 1
        else:
            tracker[number] = 1
    for number in tracker:
        if tracker[number] == 2:
            pair_nums.append(number)
    sorted_list = sorted(pair_nums, reverse=True)
    if len(sorted_list):
        if len(sorted_list) == 1:
            #print(sorted_list)
            return sorted_list
        else:
            return sorted_list[:2]
    else:
        #print("false")
        return False

def three_kind(cards):
    tracker = {}
    pair_nums = []
    numbers = [card.number for card in cards]
    for number in numbers:
        if number in tracker:
            tracker[number] += 1
        else:
            tracker[number] = 1
    for number in tracker:
        if tracker[number] == 3:
            pair_nums.append(number)
    sorted_list = sorted(pair_nums, reverse=True)
    if len(sorted_list):
        return sorted_list[0]
    else:
        #print("false")
        return False

def straight_check(cards):
    numbers = [card.number for card in cards]
    if 14 in numbers:
        numbers.append(1)
    numbers = sorted(numbers, reverse=False)
    non_dups = set(numbers)
    non_dups = list(non_dups)
    #print(list(non_dups))
    straight_count = 1
    highest_card = 0
    if len(non_dups) >= 5:
        for index in range(0, len(non_dups)):
            if index-1 >= 0:
                if non_dups[index]-1 == non_dups[index-1]:
                    straight_count += 1
                else:
                    straight_count = 1
            if straight_count >= 5:
                highest_card = non_dups[index]
    if highest_card:
        return highest_card
    else:
        return False
    
def flush_check(cards):
    suits = [card.suit for card in cards]
    tracker = {}
    flush_suit = ''
    flush_cards = []
    for suit in suits:
        if suit in tracker:
            tracker[suit] += 1
            if tracker[suit] >= 5:
                flush_suit = suit
        else:
            tracker[suit] = 1
    if flush_suit:
        #print("cards: ", cards)
        #print("suit: ", flush_suit)
        for card in cards:
            if card.suit == flush_suit:
                flush_cards.append(card.number)
        flush_cards = sorted(flush_cards, reverse=True)
        #print("FLUSH: ", flush_cards[:5])
        return flush_cards[0]
    else:
        return False

def full_house_check(cards):
    if pair_check(cards) and three_kind(cards):
        #print(cards)
        # 1. Ranking of Three-of-a-Kind:
        # Primary Factor: The rank of the three-of-a-kind is the most critical factor in comparing Full Houses. The higher the numerical rank of the three-of-a-kind, the stronger the hand. For instance, a Full House with three Kings will always beat a Full House with three Queens.
        # 2. Pair Comparison:
        # Secondary Factor: If two players have the same three-of-a-kind, the rank of the pair is used as a tie-breaker. The higher pair wins. For example, if one player has 10-10-10-3-3 (Tens full of Threes) and another has 10-10-10-4-4 (Tens full of Fours), the second player wins.
        # 3 of a kind first and then pair
        return [three_kind(cards), pair_check(cards)[0]]
    else:
        return False
    
def four_kind(cards):
    tracker = {}
    pair_nums = []
    numbers = [card.number for card in cards]
    for number in numbers:
        if number in tracker:
            tracker[number] += 1
        else:
            tracker[number] = 1
    for number in tracker:
        if tracker[number] == 4:
            pair_nums.append(number)
    sorted_list = sorted(pair_nums, reverse=True)
    if len(sorted_list):
        return sorted_list[0]
    else:
        #print("false")
        return False

def straight_flush_check(cards):
    if flush_check(cards) and straight_check(cards):
        suits = [card.suit for card in cards]
        tracker = {}
        flush_suit = ''
        flush_cards = []
        for suit in suits:
            if suit in tracker:
                tracker[suit] += 1
                if tracker[suit] >= 5:
                    flush_suit = suit
            else:
                tracker[suit] = 1
        if flush_suit:
            for card in cards:
                if card.suit == flush_suit:
                    flush_cards.append(card)
            highest_card = straight_check(flush_cards)
            if highest_card:
                #print(f"{highest_card} high {flush_suit} flush")
                return highest_card
            else:
                return False
        else:
            return False
        
def royal_flush_check(cards):
    sf = straight_flush_check(cards)
    if sf and sf == 14:
        return True
    else:
        return False

suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
numbers = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

four = False
hand_count = 0

while four == False:
    player_1_hand = []
    player_2_hand = []

    board = []
    deck = [Card(number, suit) for suit in suits for number in numbers]

    shuffled_list = fisher_yates_shuffle(deck)
    #print(shuffled_list)
    player_1_hand.append(shuffled_list.pop())
    player_2_hand.append(shuffled_list.pop())
    player_1_hand.append(shuffled_list.pop())
    player_2_hand.append(shuffled_list.pop())

    #print(player_1_hand)
    #print(player_2_hand)

    # flop
    shuffled_list.pop()
    board.append(shuffled_list.pop())
    board.append(shuffled_list.pop())
    board.append(shuffled_list.pop())

    # turn
    shuffled_list.pop()
    board.append(shuffled_list.pop())

    # river
    shuffled_list.pop()
    board.append(shuffled_list.pop())
    #print(len(shuffled_list))

    #print(board)
    #print(board + player_1_hand)

    #print(high_cards(board + player_1_hand))
    #print(pair_check(board + player_1_hand))
    #print(three_kind(board + player_1_hand))
    hand_count += 1
    cards = board + player_1_hand
    cards = [Card(4, 'Hearts'), Card(5, 'Hearts'), Card(3, 'Hearts'), Card(2, 'Hearts'), Card(8, 'Hearts'), Card(14, 'Hearts')]

    test = straight_flush_check(cards)
    if test:
        print(hand_count)
        print("here, ", test)
        print(cards)
        four = True
        break