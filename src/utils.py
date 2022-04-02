from typing import TYPE_CHECKING, Dict, List

if TYPE_CHECKING:
    from entities.card import Card


def get_largest_kind_group(cards: List["Card"]):
    groups = group_cards_by_rank(cards)
    card_groups = groups.values()
    sorted_values = sorted(card_groups, key=len, reverse=True)

    return sorted_values[0]


def group_cards_by_rank(cards: List["Card"]):
    groups: Dict[int, List["Card"]] = {}

    for card in cards:
        rank_cards = groups.get(card.rank, [])
        rank_cards.append(card)
        groups[card.rank] = rank_cards

    return groups


def get_pairs(cards: List["Card"]):
    groups = group_cards_by_rank(cards)
    card_groups = groups.values()
    pairs = [cards for cards in card_groups if len(cards) == 2]

    sorted_pairs = sorted(
        pairs, key=lambda pair: pair[0].rank, reverse=True
    )

    return sorted_pairs


def get_full_house_groups(cards: List["Card"]):
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
