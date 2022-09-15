from enum import Enum
import logging
import random
from typing import List, Tuple

from rlcard.games.base import Card
from rlcard.games.spades.actions import PlayAction


class SpadesPlayer:
    partnership: "SpadesPartnership"

    def __init__(self, player_id, python_random: random.Random):
        """Initialize a Spades player class

        Args:
            player_id (int): id for the player
        """
        self.python_random = python_random
        self.player_id = player_id
        self.hand: List[Card] = []
        self.hand_bid = None
        self.hand_tricks_won = 0
        self.won_game = False

    def get_player_id(self):
        """Return player's id"""
        return self.player_id

    def bid(self, amount: int):
        self.hand_bid = amount

    def won_trick(self):
        self.hand_tricks_won += 1

    def get_possible_play_actions(self) -> List[Enum]:
        num_cards = len(self.hand)
        return [
            action
            for action in PlayAction._member_map_.values()
            if action.value < num_cards
        ]

    def reset_hand(self) -> None:
        self.hand_bid = 1
        self.hand_tricks_won = 0

    def attach_to_partnership(self, partnership: "SpadesPartnership") -> None:
        self.partnership = partnership

    def __repr__(self) -> str:
        return (
            f"Player {self.player_id}, bid {self.hand_bid}, won {self.hand_tricks_won}"
        )


class SpadesPartnership:
    def __init__(
        self, partnership_id: int, players: Tuple["SpadesPlayer", "SpadesPlayer"]
    ) -> None:
        self.partnership_id = partnership_id
        self.players = players
        for player in players:
            player.attach_to_partnership(self)
        self.score = 0
        self.running_multihand_sandbags = 0
        self.won_game = False
        self.game_sandbags = 0

    @property
    def hand_bid(self) -> int:
        return self.players[0].hand_bid + self.players[1].hand_bid

    @property
    def hand_tricks_won(self) -> int:
        return self.players[0].hand_tricks_won + self.players[1].hand_tricks_won

    def add_to_score(self, score: int):
        self.score += score

    def __repr__(self) -> str:
        return (
            f"Partnership {self.partnership_id} score {self.score}: {self.players[0]}; {self.players[1]}"
        )
