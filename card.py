class Card:
  def __init__(self, number, color):
    self.number = number
    self.color = color

allCards = [Card(0, "red"),
            Card(0, "green"),
            Card(0, "blue"),
            Card(0, "yellow")]

colors = ["red", "green", "blue", "yellow"]
for x in colors:
    for j in range(2):
        for k in range(9):
           allCards.append(Card(k+1, x))



# TODO: add others cards
""" A standard deck of Uno cards consists of 108 cards:

    25 cards of each color (red, blue, green, and yellow)
        19 number cards (1 zero and 2 each of one through nine)
        2 Draw 2 cards
        2 Reverse cards
        2 Skip cards
    4 Wild cards
    4 Wild Draw 4 cards
 """