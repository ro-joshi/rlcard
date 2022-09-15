from copy import deepcopy
import sys
from typing import Any, Dict, List, NamedTuple, Tuple, Union
import numpy as np
import random
import logging
from rlcard.games.spades.actions import BidAction

from rlcard.games.spades import Dealer
from rlcard.games.spades import Player
from rlcard.games.spades import Judger
from rlcard.games.spades.actions import PlayAction
from rlcard.games.spades.player import SpadesPartnership, SpadesPlayer
from rlcard.games.spades.round import SpadesHand

logging.basicConfig(level=logging.INFO, stream=sys.stdout)


class PlayerGameState(NamedTuple):
    player_id: int
    hand: List[str]
    hand_history: List[Dict[int, str]]
    partnership_score: int
    hand_is_over: bool
    game_is_over: bool


class SpadesGame:
    num_players = 4
    players: List[SpadesPlayer]
    partnerships: Tuple[SpadesPartnership, SpadesPartnership]

    def __init__(self, seed=100):
        """Initialize the class Spades Game"""
        self.python_random = random.Random(seed)
        self.logger = logging.getLogger(self.__class__.__name__)

    def configure(self):
        """Specifiy some game specific parameters, such as number of players"""
        pass

    def deal_cards(self):
        self.dealer.reset()
        for i in range(13):
            for j in range(self.num_players):
                self.dealer.deal_card(self.players[j])
        for player in self.players:
            player.hand = sorted(player.hand, key=lambda x: str(x)[::-1])

    def init_game(self):
        """Initialilze the game

        Returns:
            state (dict): the first state of the game
            player_id (int): current player's id
        """
        self.dealer = Dealer(self.python_random)

        self.players = []
        for i in range(self.num_players):
            self.players.append(Player(i, self.python_random))

        # Initialize team scores to 0
        self.partnerships = (
            SpadesPartnership(0, (self.players[0], self.players[2])),
            SpadesPartnership(1, (self.players[1], self.players[3])),
        )
        self.judger = Judger()

        # Deal cards to each player
        self.deal_cards()

        # Randomly select first player
        self.dealer_pointer = self.python_random.randint(0, 3)
        self.game_pointer = (self.dealer_pointer + 1) % self.num_players

        # Start the hand
        self.current_hand = SpadesHand(
            self.partnerships, self.game_pointer, self.judger
        )
        self.logger.info(f"Current player {self.game_pointer}")
        self.logger.info(self.players[self.game_pointer].partnership)
        self.logger.info(self.current_hand.get_legal_actions())

        self.history = []

        return self.get_state(self.game_pointer), self.game_pointer

    def step(self, action: Union[PlayAction, BidAction]):
        """Get the next state

        Args:
            action (str): a specific action of spades.

        Returns:/
            dict: next player's state
            int: next plater's id
        """

        next_player_id = self.current_hand.proceed_round(action)
        if self.current_hand.is_over():
            self.dealer_pointer = (self.dealer_pointer + 1) % self.num_players
            self.game_pointer = (self.dealer_pointer + 1) % self.num_players
            for player in self.players:
                player.reset_hand()
            self.deal_cards()
            self.current_hand = SpadesHand(
                self.partnerships, self.game_pointer, self.judger
            )
        else:
            self.game_pointer = next_player_id
        self.logger.info(f"Current player {self.game_pointer}")
        self.logger.info(self.partnerships[0])
        self.logger.info(self.partnerships[1])
        current_trick = [
            f"Player {player}: {card.get_index()}"
            for player, card in self.current_hand.current_trick.items()
        ]
        self.logger.info(f"Current trick: {current_trick}")
        current_legal_actions = [
            (self.players[self.game_pointer].hand[action.value].get_index(), action)
            if isinstance(action, PlayAction)
            else action
            for action in self.current_hand.get_legal_actions()
        ]
        self.logger.info(current_legal_actions)
        next_state = self.get_state(self.game_pointer)
        return next_state, self.game_pointer

    def get_num_players(self) -> int:
        """Return the number of players in spades

        Returns:
            number_of_player (int): spades only have 1 player
        """
        return self.num_players

    @staticmethod
    def get_num_actions() -> int:
        """Return the number of applicable actions

        Returns:
            number_of_actions (int): there are only two actions (hit and stand)
        """
        return len(BidAction) + len(PlayAction)

    def get_player_id(self) -> int:
        """Return the current player's id

        Returns:
            player_id (int): current player's id
        """
        return self.game_pointer

    def get_state(self, player_id) -> PlayerGameState:
        """Return player's state

        Args:
            player_id (int): player id

        Returns:
            state (dict): corresponding player's state
        """
        player = self.players[player_id]
        hand_history: List[Dict[int, str]] = []
        for trick in self.current_hand.trick_history:
            hand = {}
            for player_id, card in trick.items():
                hand[player_id] = card.get_index()
            hand_history.append(hand)
        state = PlayerGameState(
            player_id=player_id,
            hand=[card.get_index() for card in player.hand],
            hand_history=hand_history,
            partnership_score=player.partnership.score,
            hand_is_over=self.current_hand.is_over(),
            game_is_over=self.is_over(),
        )
        return state

    def is_over(self):
        """Check if the game is over

        Returns:
            status (bool): True/False
        """

        self.judger.judge_game(self.partnerships[0], self.partnerships[1])
        for partnership in self.partnerships:
            for player in partnership.players:
                if player.won_game:
                    return True
        return False
