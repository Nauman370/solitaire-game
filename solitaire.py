import random
import pygame
Types=["Diamond","Hearts","Clubs","Spades"]
Ranks=list(range(1,14))
class Cards:
    def __init__(self,Ranks,Types):
        self.rank=Ranks
        self.type=Types
        self.face_up=False


    def color(self):
        if self.rank in ("Diamond","Hearts"):
            return "red"
        else:
            return "black"


    
    def name(self):
        names={1: "Ace",11:"Jack",12:"Queen",13:"King"}
        return names.get(self.rank,str(self.rank)) + self.type[0].upper()

    def __repr__(self):
        return self.name()
def deck_cards():
    deck=[]
    for type in Types:
        for rank in Ranks:
            deck.append(Cards(rank,type))
        return deck
deck=deck_cards()
random.shuffle(deck)
print(len(deck))
print (deck[:5])

