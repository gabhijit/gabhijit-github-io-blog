from pokerhand import PokerHand

import time

if __name__ == '__main__':

    with open('poker.txt', 'r') as f:
        then = time.time()
        scores = []
        for line in f:
            hand1 = line[0:14]
            hand2 = line[15:]
            pass #print "Hand 1:", hand1, "Hand 2:", hand2.strip()
            ph1, ph2 = PokerHand.from_str(hand1), PokerHand.from_str(hand2)
            scores.append(ph1.score)
            scores.append(ph2.score)
            if ph1 < ph2:
                print "Winner:", hand2.strip(), "Score:", ph2.score, "Loosing Score:", ph1.score
            elif ph2 < ph1:
                print "Winner:", hand1.strip(), "Score:", ph1.score, "Loosing Score:", ph2.score
            else:
                print "Equal:", hand1.strip(), ":", hand2.strip(), "Score:", ph1.score
            print "-------"
        now = time.time()

        print now - then
        d = dict()
        for score in set(scores):
            d.setdefault(score, scores.count(score))

        print d
