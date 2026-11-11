import random
import pygame
Types=["Diamond","Hearts","Clubs","Spades"]
Ranks=list(range(1,14))
class Cards:
    def __init__(self,Ranks,Types):
        self.rank=self.rank
        self.type=self.type
        self.face_up=False


    def color(self):
        if self.rank in ("Diamond","Hearts"):
            return "red"
        else:
            return "black"