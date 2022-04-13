from typing import TYPE_CHECKING, Dict, List, Tuple, Optional

if TYPE_CHECKING:
    from entities.card import Card


def get_largest_kind_group(cards: List["Card"]) -> List["Card"]:
    groups = group_cards_by_rank(cards)
    card_groups = groups.values()
    largest_group = max(card_groups, key=len)

    return largest_group


def group_cards_by_rank(cards: List["Card"]) -> Dict[int, List["Card"]]:
    groups = {}

    for card in cards:
        rank_cards = groups.get(card.rank, [])
        rank_cards.append(card)
        groups[card.rank] = rank_cards

    return groups


def get_pairs(cards: List["Card"]) -> List[List["Card"]]:
    groups = group_cards_by_rank(cards)
    card_groups = groups.values()
    pairs = [cards for cards in card_groups if len(cards) == 2]

    sorted_pairs = sorted(
        pairs, key=lambda pair: pair[0].rank, reverse=True
    )

    return sorted_pairs


def get_full_house_groups(cards: List["Card"]) -> Tuple[Optional[List[Card]], Optional[List[Card]]]:
    groups = group_cards_by_rank(cards)
    card_groups = groups.values()

    three_of_a_kind_group = None
    two_of_a_kind_group = None

    for cards in card_groups:
        if len(cards) == 3:
            three_of_a_kind_group = cards
        elif len(cards) == 2:
            two_of_a_kind_group = cards

    return (two_of_a_kind_group, three_of_a_kind_group)
