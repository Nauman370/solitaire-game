from datetime import date
import random
import os
import json
import pygame
import copy
Type=["Diamond","Hearts","Clubs","Spades"]
Ranks=list(range(1,14))
Save_file=os.path.join(os.path.expanduser("~"),"solitaire-save.json")



def rank_label(rank):
    return {1:"A",11:"J",12:"Q",13:"K"}.get(rank,str(rank))



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
history=[]

def save_screen():
    history.append(copy.deepcopy((tableu,stock,waste,foundations)))
def undo():
    global tableu,stock,waste,waste_sel,foundations,selected,won
    if history:
        tableu,stock,waste,foundations=history.pop()
        selected=None
        waste_sel=False
        won=False
def new_game():
    global tableu,waste,foundations,selected,waste_sel,won,stock
    deck=deck_cards()
    random.shuffle(deck)
    history.clear()
    tableu=[[] for _ in range(7)]
    for i in range(7):
        for _ in range(i+1):
            tableu[i].append(deck.pop())
        tableu[i][-1].face_up=True
    stock=deck
    waste=[]
    foundations=[[],[],[],[]]
    selected=None
    waste_sel=False
    won=False
new_game()
message=""
message_timer=0
def set_message(text):
    global message, message_timer
    message= text
    message_timer=120

def card_data(card):
    return[card.rank,card.type,card.face_up]
def data_to_card(d):
    card=Cards(d[0],d[1])
    card.face_up=d[2]
    return card

def save_game():
    data = {
        "tableu": [[card_data(c) for c in pile] for pile in tableu],
        "stock": [card_data(c) for c in stock],
        "waste": [card_data(c) for c in waste],
        "foundations": [[card_data(c) for c in pile] for pile in foundations],
    }

    with open(Save_file,"w")as f:
        json.dump(data,f)
    set_message("Game saved")
def load_game():
    global tableu,stock,waste,foundations,selected,waste_sel,won
    try:
        with open(Save_file) as f:
            data=json.load(f)
        new_tableu=[[data_to_card(d)for d in pile]for pile in data["tableu"]]
        new_stock=[data_to_card(d)for d in data["stock"]]
        new_waste=[data_to_card(d)for d in data["waste"]]
        new_foundations=[[data_to_card(d)for d in pile]for pile in data["foundations"]]
    except (OSError,IndexError,ValueError,KeyError,TypeError):
        set_message("No saves")
        return
    tableu,waste,stock,foundations= new_tableu,new_waste,new_stock,new_foundations
    selected=None
    waste_sel=False
    won=False
    history.clear()
    set_message("game loaded")

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
screen=pygame.display.set_mode((WIDTH,HEIGHT),pygame.SCALED|pygame.RESIZABLE)
pygame.display.set_caption("Solitaire")
font=pygame.font.SysFont(None,30)
win_font=pygame.font.SysFont(None,72)
small_font=pygame.font.SysFont(None,26)

show_controls=True
BAR_H=100
BAR_Y=HEIGHT-BAR_H
BTN_W,BTN_H=150,34
buttons=[("Undo","undo"),("New game","new",),("Save","save"),("Load","load")]
KEYS={pygame.K_z:"undo",pygame.K_n:"new",pygame.K_s:"save",pygame.K_l:"load"}

def col_x(col):
    return MARGIN + col*(CARD_W+GAP)
def card_y(pile,index):
    y=TABLEU_Y
    for card in pile[:index]:
        y+=UP_STEP if card.face_up else DOWN_STEP
    return y
def tableu_hit(pos):
    mx,my=pos
    for col,pile in enumerate(tableu):
        x=col_x(col)
        if not(x<=mx<=x+CARD_W):
            continue
        for index in range(len(pile)-1,-1,-1):
            top=card_y(pile,index)
            if top<=my<=top+CARD_H:
                return col,index
    return None

def column_at(pos):
    mx,my=pos
    if my<TABLEU_Y:
        return None
    for col in range(7):
        if col_x(col)<=mx<=col_x(col)+CARD_W:
            return col
    return None

def foundation_at(pos):
    mx,my=pos
    if not (TOP_Y<=my<=TOP_Y + CARD_H):
        return None
    for i in range(4):
        if col_x(3+i)<=mx<=col_x(3+i)+CARD_W:
            return i
    return None

def won_game():
    return all(len(p)==13 for p in foundations)

def stock_drawing():
    if not stock and not waste:
        return
    save_screen()
    if stock:
        card=stock.pop()
        card.face_up=True
        waste.append(card)
    else:
        while waste:
            card=waste.pop()
            card.face_up=False
            stock.append(card)


def draw_type(type,cx,cy,r,color):
    if type=="Diamond":
        pygame.draw.polygon(screen,color,[(cx,cy-r),(cx+int(r*0.75),cy),(cx,cy+r),(cx-int(r*0.75),cy)])
    elif type=="Hearts":
        pygame.draw.circle(screen,color,(cx-r//2,cy-r//4),r//2+1)
        pygame.draw.circle(screen,color,(cx+r//2,cy-r//4),r//2+1)
        pygame.draw.polygon(screen,color,[(cx-r,cy-r//8),(cx+r,cy-r//8),(cx,cy+r)])
    elif type=="Spades":
        pygame.draw.circle(screen, color, (cx - r// 2, cy+r// 4),r //2 + 1)
        pygame.draw.circle(screen, color, (cx + r// 2, cy+r// 4),r//2 + 1)
        pygame.draw.polygon(screen,color,[(cx-r,cy+r//8),(cx+r,cy+r//8),(cx,cy-r)])
        pygame.draw.polygon(screen,color,[(cx,cy+r//4),(cx-r//3,cy+r),(cx+r//3,cy+r)])
    else:        
        for dx, dy in ((0, -r // 2), (-r // 2, r // 6), (r // 2, r // 6)):

            pygame.draw.circle(screen,color,(cx+dx,cy+dy),r//2)
        pygame.draw.polygon(screen,color,[(cx,cy),(cx-r//3,cy+r),(cx+r//3,cy+r)])

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

def button_rect(i):
    return pygame.Rect(30+i*(BTN_W+20),BAR_Y+56,BTN_W,BTN_H)
def do_action(action):
    if action=="undo":
        undo()
    elif action=="new":
        new_game()
    elif action=="save":
        save_game()
    elif action=="load":
        load_game()
def draw_bar():
    if not show_controls:
        return
    strip=pygame.Surface((WIDTH,BAR_H))
    strip.set_alpha(190)
    strip.fill((0,0,0))
    screen.blit(strip,(0,BAR_Y))
    line=small_font.render("Press Z for Undo  Press N for new game  Press S to save  Press L to load H to make this box go away",True,(230,230,230))
    screen.blit(line,(WIDTH//2-line.get_width()//2,BAR_Y+10))
    for i,(label,action)in enumerate(buttons):
        r=button_rect(i)
        hover=r.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(screen,(70,120,90)if hover else(40,100,65),r,border_radius=8)
        pygame.draw.rect(screen,(230,230,240),r,2,border_radius=8)
        text=font.render(label,True,(255,255,255))
        screen.blit(text,(r.centerx-text.get_width()//2,r.centery-text.get_height()//2))


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
    if selected:
        col,index=selected
        pile=tableu[col]
        for i in range(index,len(pile)):
            pygame.draw.rect(screen,(255,215,0), (col_x(col),card_y(pile,i),CARD_W,CARD_H) , 3,border_radius=8)
    if waste_sel and waste:
        pygame.draw.rect(screen,(255,215,0),(col_x(1),TOP_Y,CARD_W,CARD_H),3,border_radius=8)

    if won:
        overlay=pygame.Surface((WIDTH,HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0,0,0))
        screen.blit(overlay,(0,0))
        text=win_font.render("You win :)",True,(255,215,0))
        screen.blit(text,(WIDTH//2-text.get_width()//2,HEIGHT//2-60))
        hint=font.render("For a New game, Press N",True,(255,255,200))
        screen.blit(hint,(WIDTH//2-hint.get_width()//2,HEIGHT//2+10))
    if message_timer>0:
        msg=font.render(message,True,(255,255,200))
        screen.blit(msg,(WIDTH//2-msg.get_width()//2,146))

clock=pygame.time.Clock()
running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.KEYDOWN:
            if event.key in KEYS:
                do_action(KEYS[event.key])
            elif event.key==pygame.K_h:
                show_controls=not show_controls
            elif event.key==pygame.K_F11:
                pygame.display.toggle_fullscreen()
        if event.type ==pygame.QUIT:
            running=False
        if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
            if show_controls and event.pos[1]>= BAR_Y:
                for i,(label,action) in enumerate(buttons):
                    if button_rect(i).collidepoint(event.pos):
                        do_action(action)
                continue

            if pygame.Rect(col_x(0), TOP_Y,CARD_W,CARD_H).collidepoint(event.pos):
                stock_drawing()
                selected=None
                waste_sel=False
                continue
            if pygame.Rect(col_x(1),TOP_Y,CARD_W,CARD_H).collidepoint(event.pos):
                if waste:
                    waste_sel=not waste_sel
                    selected=None
                continue
            f=foundation_at(event.pos)
            if f is not None:
                if waste_sel and plac_on_foundations(waste[-1],foundations[f]):
                    save_screen()
                    foundations[f].append(waste.pop())
                    waste_sel=False
                    continue
                if selected is not None:
                    src_col,src_index=selected
                    save_screen()
                    if src_index==len(tableu[src_col])-1 and plac_on_foundations(tableu[src_col][src_index],foundations[f]):
                        card_moving(tableu[src_col], src_index,foundations[f])
                        selected=None
                        continue
                waste_sel=False
                selected=None
                continue

            target=column_at(event.pos)
            if waste_sel and target is not None and place_on_tableu(waste[-1],tableu[target]):
                save_screen()
                tableu[target].append(waste.pop())
                waste_sel=False
                continue
            waste_sel=False
            moved=False
            if selected is not None and target is not None and target!=selected[0]:
                src_col,src_index=selected
                moving_card=tableu[src_col][src_index]
                if place_on_tableu(moving_card,tableu[target]):
                    save_screen()
                    card_moving(tableu[src_col],src_index,tableu[target])
                    selected=None
                    moved=True
            if not moved:

                hit=tableu_hit(event.pos)
                if hit is not None:
                    col,index=hit
                    if tableu[col][index].face_up:
                     selected=hit
                    else:
                        selected=None
                else:
                    selected=None
    if message_timer>0:
        message_timer-=1
    if won_game():
        won=True
    draw_table()
    draw_bar()

    pygame.display.flip()
    clock.tick(60)
pygame.quit()



    
    