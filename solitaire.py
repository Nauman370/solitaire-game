import random
import pygame
Type=["Diamond","Hearts","Clubs","Spades"]
Ranks=list(range(1,14))


def rank_label(rank):
    return {1:"Ace",11:"Jack",12:"Queen",13:"King"}.get(rank,str(rank))



class Cards:
    def __init__(self,Ranks,Type):
        self.rank=Ranks
        self.type=Type
        self.face_up=False


    def color(self):
        if self.type in ("Diamond","Hearts"):
            return "red"
        else:
            return "black"
    def __repr__(self):
        return rank_label(self.rank)+self.type[0].upper()
def deck_cards():
    deck=[]
    for type in Type:
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
WIDTH=MARGIN*2+7*CARD_W+6*GAP
HEIGHT=720
TOP_Y=20
TABLEU_Y= 170
DOWN_STEP=14
UP_STEP=30

pygame.init()
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Solitaire")
font=pygame.font.SysFont(None,30)

def col_x(col):
    return MARGIN + col*(CARD_W+GAP)

def draw_type(type,cx,cy,r,color):
    if type=="Diamond":
        pygame.draw.polygon(screen,color,[(cx,cy-r),(cx+int(r*0.75),cy),(cx,cy+r),(cx-int(r*0.75),cy)])



    elif type=="Hearts":
        pygame.draw.circle(screen,color,(cx-r//2,cy-r//4),r//2+1)
        pygame.draw.circle(screen,color,(cx+r//2,cy-r//4),r//2+1)
        pygame.draw.polygon(screen,color,[(cx-r,cy-r//8),(cx+r,cy-r//8),(cx,cy+r)])
    elif type=="Spades":
        pygame.draw.circle(screen,color,(cx-r//2,cy-r//4),r//2+1)
        pygame.draw.circle(screen,color,(cx+r//2,cy-r//4),r//2+1)
        pygame.draw.polygon(screen,color,[(cx-r,cy+r//8),(cx+r,cy+r//8),cx,cy-r])
        pygame.draw.polygon(screen,color,[(cx,cy+r//4),(cx-r//3,cy+r),(cx+r//3,cy+r)])
    else:
         
         for dx, dy in ((0, -r // 2), (-r // 2, r // 6), (r // 2, r // 6)):
            pygame.draw.circle(screen,color,(cx+dx,cy+dy),r//2)
            pygame.draw.polygon(screen,color,[(cx-cy),(cx-r//3,cy+r),(cx+r//3,cy+r)])

def draw_card(card,x,y):
    rect=pygame.Rect(x,y,CARD_W,CARD_H)
    if card.face_up:
        color=(200,30,30) if card.color()=="red" else (20,20,20)
        pygame.draw.rect(screen,(250,250,245),rect,border_radius=8)
        pygame.draw.rect(screen,(60,60,60),rect, 2, border_radius=8)
        screen.blit(font.render(rank_label(card.rank),True,color),(x+8,y+6))
        draw_type(card.type,x + CARD_W-18, y+18,9,color)
        draw_type(card.type,x +CARD_W//2,y+CARD_H//2+10,20,color)
    else:
        pygame.draw.rect(screen,(40,70,160),rect,border_radius=8)
        pygame.draw.rect(screen,(230,230,240),rect.inflate(-14,-14),2,border_radius=6)
def draw_slot(x,y):
    pygame.draw.rect(screen,(18,85,45),(x,y,CARD_W,CARD_H),2,border_radius=8)
def draw_table():
    screen.fill((20,110,60))
    if stock:
        draw_card(stock[-1],col_x(0),TOP_Y)
    else:
        draw_slot(col_x(0),TOP_Y)
    if waste:
        draw_card(waste[-1],col_x(1),TOP_Y)
    else:
        draw_slot(col_x(1),TOP_Y)
    for i,pile in enumerate(foundations):
        if pile:
            draw_card(pile[-1],col_x(3+i),TOP_Y)
        else:
            draw_slot(col_x(3+i),TOP_Y)
    for col,pile in enumerate(tableu):
        x=col_x(col)
        y=TABLEU_Y
        if not pile:
            draw_slot(x,y)
        for card in pile:
            draw_card(card,x,y)
            if card.face_up:
                y+=UP_STEP
            else:

                y+=DOWN_STEP
clock=pygame.time.Clock()
running=True
while running:
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            running=False
    draw_table()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()



    
    