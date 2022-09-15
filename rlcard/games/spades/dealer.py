from rlcard.games.spades.player import SpadesPlayer
from rlcard.utils import init_standard_deck
import numpy as np
import random

class SpadesDealer:

    def __init__(self, python_random: random.Random):
        ''' Initialize a Spades dealer class
        '''
        self.python_random = python_random
        self.reset()
        self.hand = []
        self.status = 'alive'
        self.score = 0

    def shuffle(self) -> None:
        ''' Shuffle the deck
        '''
        self.python_random.shuffle(self.deck)

    def deal_card(self, player: SpadesPlayer):
        ''' Distribute one card to the player

        Args:
            player_id (int): the target player's id
        '''
        card = self.deck.pop()
        player.hand.append(card)
    
    def reset(self) -> None:
        self.deck = init_standard_deck()
        self.shuffle()
