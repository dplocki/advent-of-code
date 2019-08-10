from queue import PriorityQueue
import copy
from dataclasses import dataclass, field


MAGIC_MISSLE = 'm'
MAGIC_MISSLE_COST = 53
MAGIC_MISSLE_EFFECT = 4
DRAIN = 'd'
DRAIN_COST = 73
DRAIN_EFFECT = 2
SHIELD = 's'
SHIELD_COST = 113
SHIELD_LENGHT = 6
SHIELD_EFFECT = 7
POISON = 'p'
POISON_COST = 173
POISON_LENGHT = 6
POISON_EFFECT = 3
RECHARGE = 'r'
RECHARGE_COST = 229
RECHARGE_LENGHT = 5
RECHARGE_EFFECT = 101


class State():
    def __init__(self):
        self.player_hit_points = 50
        self.player_armor = 0
        self.player_mana = 500
        self.used_mana = 0

        self.boss_hit_points = 0
        self.boss_damage = 0

        self.effect_shield_timer = 0
        self.effect_poison_timer = 0
        self.effect_recharge_timer = 0

        self.difficulty_level_adjustment = 0

    def avaiable_spells(self):
        if self.player_mana >= MAGIC_MISSLE_COST:
            yield MAGIC_MISSLE

        if self.player_mana >= DRAIN_COST:
            yield DRAIN

        if self.effect_shield_timer == 0 and self.player_mana >= SHIELD_COST:
            yield SHIELD

        if self.effect_poison_timer == 0 and self.player_mana >= POISON_COST:
            yield POISON

        if self.effect_recharge_timer == 0 and self.player_mana >= RECHARGE_COST:
            yield RECHARGE

    def is_player_alive(self):
        return self.player_hit_points > 0

    def is_boss_dead(self):
        return self.boss_hit_points <= 0

    def has_player_win(self):
        return self.is_player_alive() and self.is_boss_dead()

    def cast_spell(self, spell):
        if spell == MAGIC_MISSLE:
            self.player_mana -= MAGIC_MISSLE_COST
            self.used_mana += MAGIC_MISSLE_COST
            self.boss_hit_points -= MAGIC_MISSLE_EFFECT

        if spell == DRAIN:
            self.player_mana -= DRAIN_COST
            self.used_mana += DRAIN_COST
            self.player_hit_points += DRAIN_EFFECT
            self.boss_hit_points -= DRAIN_EFFECT

        if spell == SHIELD:
            self.player_mana -= SHIELD_COST
            self.used_mana += SHIELD_COST
            self.effect_shield_timer = SHIELD_LENGHT

        if spell == POISON:
            self.player_mana -= POISON_COST
            self.used_mana += POISON_COST
            self.effect_poison_timer = POISON_LENGHT

        if spell == RECHARGE:
            self.player_mana -= RECHARGE_COST
            self.used_mana += RECHARGE_COST
            self.effect_recharge_timer = RECHARGE_LENGHT

    def timer_spell_effect(self):
        if self.effect_recharge_timer > 0:
            self.player_mana += RECHARGE_EFFECT
            self.effect_recharge_timer -= 1

        if self.effect_poison_timer > 0:
            self.boss_hit_points -= POISON_EFFECT
            self.effect_poison_timer -= 1

        if self.effect_shield_timer > 0:
            self.player_armor = SHIELD_EFFECT
            self.effect_shield_timer -= 1
        else:
            self.player_armor = 0

    def get_neighborns_states(self):
        # Player turn
        self.player_hit_points -= self.difficulty_level_adjustment
        self.timer_spell_effect()
        for spell in self.avaiable_spells():
            neighborn = copy.copy(self)
            neighborn.cast_spell(spell)

            # Boss turn
            neighborn.timer_spell_effect()
            if neighborn.is_boss_dead():
                yield neighborn
            else:
                neighborn.player_hit_points -= max(1, neighborn.boss_damage - neighborn.player_armor)
                if neighborn.is_player_alive():
                    yield neighborn


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: State=field(compare=False)


def parse_input_to_fighter_class(input_lines):
    result = State()

    for line in input_lines:
        tokens = line.split(': ')
        setattr(result, 'boss_' + tokens[0].lower().replace(' ', '_'), int(tokens[1]))
    
    return result


def load_input_file(file_name):
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def solution_for_first_part(state: State) -> int:
    posibilities = PriorityQueue()
    posibilities.put(PrioritizedItem(0, state))

    while not posibilities.empty():
        current_state = posibilities.get().item
        if current_state.has_player_win():
            return current_state.used_mana

        for next in current_state.get_neighborns_states():
            posibilities.put(PrioritizedItem(next.used_mana, next))

    return None


def solution_for_second_part(state: State) -> int:
    state.difficulty_level_adjustment = 1
    return solution_for_first_part(state)


# The input is taken from: https://adventofcode.com/2015/day/22/input
inital_state = parse_input_to_fighter_class(load_input_file('input.22.txt'))
inital_state_hard = copy.copy(inital_state)

print("Solution for the first part:", solution_for_first_part(inital_state))
print("Solution for the second part:", solution_for_second_part(inital_state))
