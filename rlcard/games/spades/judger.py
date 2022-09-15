from typing import List, Sequence, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from rlcard.games.base import Card
    from rlcard.games.spades.game import SpadesGame, SpadesHand
    from rlcard.games.spades.player import SpadesPartnership, SpadesPlayer

import numpy as np


class SpadesJudger:
    def __init__(self):
        self.rank2score = {
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "T": 10,
            "J": 11,
            "Q": 12,
            "K": 13,
            "A": 14,
        }
        self.suit2score = {"S": 13, "H": 0, "D": 0, "C": 0}

    def judge_game(
        self, partnership1: "SpadesPartnership", partnership2: "SpadesPartnership"
    ) -> None:
        """Judge the winner of the game

        Args:
            game (class): target game class
        """
        partnership1_score = partnership1.score
        partnership2_score = partnership2.score
        if (partnership1_score > 500) or (partnership2_score > 500):
            if partnership1_score > partnership2_score:
                partnership1.won_game = True
                for player in partnership1.players:
                    player.won_game = True
            else:
                partnership2.won_game = True
                for player in partnership2.players:
                    player.won_game = True

    def judge_nil(self, player: "SpadesPlayer") -> int:
        if player.hand_tricks_won > 0:
            return -100
        else:
            return 100

    def judge_hand(self, partnership: "SpadesPartnership") -> int:
        """
        Judge the hand

        Args:
            partnership (SpadesPartnership): A partnership of players

        Returns:
            int: Hand score
        """
        hand_bid = partnership.hand_bid
        hand_tricks_won = partnership.hand_tricks_won

        score = 0
        extra_hands = hand_tricks_won - hand_bid
        for player in partnership.players:
            if player.hand_bid == 0:
                score += self.judge_nil(player)
        if hand_tricks_won >= hand_bid:
            score += (hand_bid * 10) + (extra_hands)
            partnership.game_sandbags += extra_hands
            partnership.running_multihand_sandbags += extra_hands
        else:
            score -= hand_bid * 10

        if partnership.running_multihand_sandbags >= 10:
            partnership.running_multihand_sandbags -= 10
            score -= 100
        return score

    def judge_card_value(self, card: "Card") -> int:
        """Judge the trick of a given cards set

        Args:
            card (Card): card

        Returns:
            trick (int): the trick of the given card
        """
        return self.suit2score[card.suit] + self.rank2score[card.rank]

    def judge_trick(self, cards: Sequence["Card"]) -> int:
        """
        Which player won the trick?

        Args:
            cards (Sequence[Card]): Sequence of cards

        Returns:
            int: Pointer to which card won trick
        """
        trick_suit = cards[0].suit
        highest_index_card = 0
        highest_value_card = 0
        for i, card in enumerate(cards):
            if (card.suit == trick_suit) or (card.suit == "S"):
                current_value_card = self.judge_card_value(card)
                if current_value_card > highest_value_card:
                    highest_value_card = current_value_card
                    highest_index_card = i
        return highest_index_card
