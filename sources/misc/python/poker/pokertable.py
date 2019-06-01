from pokerhand import PokerHand
from pokerhand import deck
from itertools import combinations

class PokerPlayer:

    def __init__(self):
        self._own_cards = []

    @property
    def own_cards(self):
        return self._own_cards

    def __repr__(self):
        return ",".join(self._own_cards)

class PokerTable:

    def __init__(self, players, deck):
        self._total_players = players
        self._players = [PokerPlayer() for i in range(players)]
        self._community_cards = []
        self._deck = deck
        self._burnt_cards = []

    @property
    def players(self):
        return self._players

    def deal(self):
        for i in range(2):
            for player in self._players:
                player._own_cards.append(self._deck.pop())

    def burn_card(self):
        self._burnt_cards.append(self._deck.pop())

    def flop(self):

        self.burn_card()
        for i in range(3):
            self._community_cards.append(self._deck.pop())

    def turn(self):
        self.burn_card()
        self._community_cards.append(self._deck.pop())

    def river(self):
        self.burn_card()
        self._community_cards.append(self._deck.pop())

    def __repr__(self):

        return ",".join(self._community_cards)

    def rank_players(self):
        player_hands = {}
        for i, player in enumerate(self._players):
            possible_hands = []
            for c in combinations(self._community_cards, 3):
                hand = player.own_cards + list(c)
                possible_hands.append(PokerHand.from_str(" ".join(hand)))
            player_hands[i] = sorted(possible_hands, reverse=True)[0]

        players = (sorted(player_hands.items(),
            key=lambda kv:kv[1], reverse=True))
        print (dict(players))

if __name__ == '__main__':

    table = PokerTable(8, deck(shuffled=True))
    table.deal()

    for i, player in enumerate(table.players):
        print (i, ":", player)

    table.flop()
    print(table)
    table.rank_players()

    table.turn()
    print(table)
    table.rank_players()

    table.river()
    print(table)
    table.rank_players()
