import random
import pygame
Types=["Diamond","Hearts","Clubs","Spades"]
Ranks=list(range(1,14))


def rank_label(rank):
    return {1:"Ace",11:"Jack",12:"Queen",13:"King"}.get(rank,str(rank))



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
    def __repr__(self):
        return rank_label(self.rank)+self.type[0].upper()
def deck_cards():
    deck=[]
    for type in Types:
        for rank in Ranks:
            deck.append(Cards(rank,type))
    return deck

def place_on_tableu(card,pile):
    if not pile:
        return card.rank==13
    top=pile[-1]
    return top.face_up and top.color()!=card.color() and top.rank==card.rank+1

def plac_on_foundations(card,pile):
    if not pile:
        return card.rank==1
    top=pile[-1]
    return top.type ==card.type and card.rank==top.rank+1
def card_moving(src,index,dest):
    cards=src[index:]
    del src[index:]
    dest.extend(cards)
    if src and not src[-1].face_up:
        src[-1].face_up=True

deck=deck_cards()
random.shuffle(deck)
print(len(deck))
print (deck[:5])

tableu=[[]for _ in range(7)]
for i in range(7):
    for _ in range(i+1):
        tableu[i].append(deck.pop())
    tableu[i][-1].face_up=True
stock=deck
waste=[]
foundations=[[],[],[],[]]


for pile in foundations:
    print(pile)
print(len(stock))





CARD_W,CARD_H=80,120
GAP=20
MARGIN=20
WIDTH=MARGIN*2+7*
