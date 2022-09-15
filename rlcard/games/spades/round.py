from enum import Enum
import logging
from typing import Dict, List, Tuple, Union, cast
from rlcard.games.base import Card
from rlcard.games.spades.judger import SpadesJudger
from rlcard.games.spades.actions import BidAction, PlayAction
from rlcard.games.spades.player import SpadesPartnership


class SpadesHand:
    max_tricks: int = 13
    num_players: int = 4

    def __init__(
        self,
        partnerships: Tuple[SpadesPartnership, SpadesPartnership],
        game_pointer: int,
        judger: SpadesJudger,
    ) -> None:
        self.partnerships = partnerships
        self.players = [
            self.partnerships[0].players[0],
            self.partnerships[1].players[0],
            self.partnerships[0].players[1],
            self.partnerships[1].players[1],
        ]
        self.spades_broken = False
        self.game_pointer = game_pointer
        self.judger = judger
        self.current_trick: Dict[int, Card] = {}
        self.trick_counter = 0
        self.bid_counter = 0
        self.hand_completed = False
        self.trick_history: List[Dict[int, Card]] = []
        self.logger = logging.getLogger(self.__class__.__name__)

    def proceed_round(
        self,
        action: Union[BidAction, PlayAction],
    ):
        """
        Call other classes functions to keep one round running

        Args:
            players (Tuple[SpadesPlayer, SpadesPlayer, SpadesPlayer, SpadesPlayer]): The list of players that play the game
            action (Action): A legal action taken by the player

        Returns:
            (int): The game_pointer that indicates the next player
        """
        if action not in self.get_legal_actions():
            raise Exception(
                "{} is not legal action. Legal actions: {}".format(
                    action, self.get_legal_actions()
                )
            )

        if isinstance(action, BidAction):
            self.bid_counter += 1

        current_player = self.players[self.game_pointer]

        if action == BidAction.BID_0:
            current_player.hand_bid = BidAction.BID_0.value
        elif action == BidAction.BID_1:
            current_player.hand_bid = BidAction.BID_1.value
        elif action == BidAction.BID_2:
            current_player.hand_bid = BidAction.BID_2.value
        elif action == BidAction.BID_3:
            current_player.hand_bid = BidAction.BID_3.value
        elif action == BidAction.BID_4:
            current_player.hand_bid = BidAction.BID_4.value
        elif action == BidAction.BID_5:
            current_player.hand_bid = BidAction.BID_5.value
        elif action == BidAction.BID_6:
            current_player.hand_bid = BidAction.BID_6.value
        elif action == BidAction.BID_7:
            current_player.hand_bid = BidAction.BID_7.value
        elif action == BidAction.BID_8:
            current_player.hand_bid = BidAction.BID_8.value
        elif action == BidAction.BID_9:
            current_player.hand_bid = BidAction.BID_9.value
        elif action == BidAction.BID_10:
            current_player.hand_bid = BidAction.BID_10.value
        elif action == BidAction.BID_11:
            current_player.hand_bid = BidAction.BID_11.value
        elif action == BidAction.BID_12:
            current_player.hand_bid = BidAction.BID_12.value
        elif action == BidAction.BID_13:
            current_player.hand_bid = BidAction.BID_13.value

        elif action == PlayAction.PLAY_CARD_0:
            self.current_trick[self.game_pointer] = current_player.hand.pop(
                PlayAction.PLAY_CARD_0.value
            )
        elif action == PlayAction.PLAY_CARD_1:
            self.current_trick[self.game_pointer] = current_player.hand.pop(
                PlayAction.PLAY_CARD_1.value
            )
        elif action == PlayAction.PLAY_CARD_2:
            self.current_trick[self.game_pointer] = current_player.hand.pop(
                PlayAction.PLAY_CARD_2.value
            )
        elif action == PlayAction.PLAY_CARD_3:
            self.current_trick[self.game_pointer] = current_player.hand.pop(
                PlayAction.PLAY_CARD_3.value
            )
        elif action == PlayAction.PLAY_CARD_4:
            self.current_trick[self.game_pointer] = current_player.hand.pop(
                PlayAction.PLAY_CARD_4.value
            )
        elif action == PlayAction.PLAY_CARD_5:
            self.current_trick[self.game_pointer] = current_player.hand.pop(
                PlayAction.PLAY_CARD_5.value
            )
        elif action == PlayAction.PLAY_CARD_6:
            self.current_trick[self.game_pointer] = current_player.hand.pop(
                PlayAction.PLAY_CARD_6.value
            )
        elif action == PlayAction.PLAY_CARD_7:
            self.current_trick[self.game_pointer] = current_player.hand.pop(
                PlayAction.PLAY_CARD_7.value
            )
        elif action == PlayAction.PLAY_CARD_8:
            self.current_trick[self.game_pointer] = current_player.hand.pop(
                PlayAction.PLAY_CARD_8.value
            )
        elif action == PlayAction.PLAY_CARD_9:
            self.current_trick[self.game_pointer] = current_player.hand.pop(
                PlayAction.PLAY_CARD_9.value
            )
        elif action == PlayAction.PLAY_CARD_10:
            self.current_trick[self.game_pointer] = current_player.hand.pop(
                PlayAction.PLAY_CARD_10.value
            )
        elif action == PlayAction.PLAY_CARD_11:
            self.current_trick[self.game_pointer] = current_player.hand.pop(
                PlayAction.PLAY_CARD_11.value
            )
        elif action == PlayAction.PLAY_CARD_12:
            self.current_trick[self.game_pointer] = current_player.hand.pop(
                PlayAction.PLAY_CARD_12.value
            )

        if isinstance(action, PlayAction):
            played_card = self.current_trick[self.game_pointer]
            self.logger.info(f"Player {self.game_pointer} played {played_card}")
            if self.current_trick[self.game_pointer].suit == "S":
                self.spades_broken = True

        if len(self.current_trick) == 4:
            self.trick_counter += 1
            # player_sorted_current_trick = [
            #     card for player, card in sorted(self.current_trick.items())
            # ]
            current_trick_players, current_trick_cards = cast(
                Tuple[Tuple[int], Tuple[Card]], list(zip(*self.current_trick.items()))
            )
            winning_index = self.judger.judge_trick(current_trick_cards)
            winning_player = current_trick_players[winning_index]
            self.logger.info(f"Player {winning_player} won the trick.")
            self.players[winning_player].hand_tricks_won += 1
            self.trick_history.append(self.current_trick)
            self.current_trick = {}
            self.game_pointer = winning_player
        else:
            self.game_pointer = (self.game_pointer + 1) % self.num_players

        if self.trick_counter == self.max_tricks:
            self.logger.info(f"Hand completed")
            for partnership in self.partnerships:
                for player in partnership.players:
                    assert len(player.hand) == 0
                partnership.add_to_score(self.judger.judge_hand(partnership))
                self.logger.info(partnership)
            self.hand_completed = True

        return self.game_pointer

    def get_legal_actions(self) -> List[Enum]:
        """
        Obtain the legal actions for the current player

        Returns:
           (list):  A list of legal actions
        """
        current_player = self.players[self.game_pointer]
        if self.bid_counter < 4:
            return list(BidAction._member_map_.values())
        possible_play_actions = current_player.get_possible_play_actions()

        hand = current_player.hand

        if len(self.current_trick) == 0:
            # can play any suit, if spades not broken
            if self.spades_broken:
                return possible_play_actions
            else:
                not_spades_possible_play_actions = []
                for action, card in zip(possible_play_actions, current_player.hand):
                    if card.suit != "S":
                        not_spades_possible_play_actions.append(action)
                return not_spades_possible_play_actions
        else:
            # must follow suit, unless doesn't have suit
            legal_play_actions = []
            current_suit = next(iter(self.current_trick.values())).suit
            for action, card in zip(possible_play_actions, hand):
                if card.suit == current_suit:
                    legal_play_actions.append(action)
            if len(legal_play_actions) == 0:
                return possible_play_actions
            else:
                return legal_play_actions

    def is_over(self):
        """
        Check whether the round is over

        Returns:
            (boolean): True if the current round is over
        """
        return self.hand_completed
