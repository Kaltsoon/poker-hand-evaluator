from typing import TYPE_CHECKING
from rankers.hand_ranker import HandRanker
from utils import get_full_house_groups

if TYPE_CHECKING:
    from entities.hand import Hand


class FullHouseRanker(HandRanker):
    def matches(self, hand: "Hand") -> bool:
        three_of_a_kind_group, two_of_a_kind_group = get_full_house_groups(
            hand.cards
        )

        return three_of_a_kind_group is not None and two_of_a_kind_group is not None

    def wins_tie(self, hand_a: "Hand", hand_b: "Hand") -> bool:
        two_of_a_kind_group_a, three_of_a_kind_group_a = get_full_house_groups(
            hand_a.cards
        )

        two_of_a_kind_group_b, three_of_a_kind_group_b = get_full_house_groups(
            hand_b.cards
        )

        if three_of_a_kind_group_a[0].rank > three_of_a_kind_group_b[0].rank:
            return True
        if three_of_a_kind_group_b[0].rank > three_of_a_kind_group_a[0].rank:
            return False
        if two_of_a_kind_group_a[0].rank > two_of_a_kind_group_b[0].rank:
            return True

        return False
