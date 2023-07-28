import logging
import argparse
import copy
from queue import PriorityQueue
from collections import defaultdict

def configure_logging(verbose, output_file):
    log_level = logging.DEBUG if verbose else logging.INFO
    if output_file is None:
        logging.basicConfig(
            format='%(message)s',
            level=log_level
        )
    else:
        logging.basicConfig(
            format='%(message)s',
            level=log_level,
            filename=output_file,
            filemode='w'
        )


SPELLS = {
    # Magic Missile costs 53 mana. It instantly does 4 damage.
    'magic_missile': { 'name': 'Magic Missile', 'mana': 53, 'damage': 4 },
    # Drain costs 73 mana. It instantly does 2 damage and heals you for 2 hit points.
    'drain': { 'name': 'Drain', 'mana': 73, 'damage': 2, 'hp': 2 },
    # Shield costs 113 mana. It starts an effect that lasts for 6 turns. While it is active, your armour is increased by 7.
    'shield': { 'name': 'Shield', 'mana': 113, 'effect': { 'duration': 6, 'armour': 7 } },
    # Poison costs 173 mana. It starts an effect that lasts for 6 turns. At the start of each turn while it is active, it deals the boss 3 damage.
    'poison': { 'name': 'Poison', 'mana': 173, 'effect': { 'duration': 6, 'damage': 3 } },
    # Recharge costs 229 mana. It starts an effect that lasts for 5 turns. At the start of each turn while it is active, it gives you 101 new mana.
    'recharge': { 'name': 'Recharge', 'mana': 229, 'effect': { 'duration': 5, 'mana': 101 } }
}


class Player:
    def __init__(self, hp, mana):
        self.hp = hp
        self.mana = mana
        self.armour = 0
        self.armour_bonus = 0
        self.armour_duration = 0
        self.mana_regen = 0
        self.mana_regen_duration = 0
        self.spells_cast = ""

    def count_spells_cast(self):
        return len(self.spells_cast)

    def get_key(self):
        return f"P: H{self.hp} M{self.mana} AD{self.armour_duration} MD{self.mana_regen_duration}"

    def get_effective_armour(self):
        return self.armour + (self.armour_bonus if self.armour_duration > 0 else 0)

    def start_any_turn(self):
        if self.armour_duration > 0:
            self.armour_duration -= 1
        if self.mana_regen_duration > 0:
            self.mana += self.mana_regen
            self.mana_regen_duration -= 1

    def start_own_turn(self):
        self.start_any_turn()

    def start_boss_turn(self):
        self.start_any_turn()

    def find_castable_spells(self, boss):
        spells = [k for k,v in SPELLS.items() if self.mana >= v['mana']]
        # this is being called at the end of a round,
        # and at the start of the next round all durations will tick down 1 point
        # so anything that has 1 tick left now will be castable next turn
        if self.armour_duration > 1 and 'shield' in spells: spells.remove('shield')
        if self.mana_regen_duration > 1 and 'recharge' in spells: spells.remove('recharge')
        if boss.poison_duration > 1 and 'poison' in spells: spells.remove('poison')
        return spells

    def cast_magic_missile(self, boss):
        magic_missile = SPELLS['magic_missile']
        self.mana -= magic_missile['mana']
        boss.hp -= magic_missile['damage']
        self.spells_cast += 'm'

    def cast_drain(self, boss):
        drain = SPELLS['drain']
        self.mana -= drain['mana']
        self.hp += drain['hp']
        boss.hp -= drain['damage']
        self.spells_cast += 'd'

    def cast_shield(self, boss):
        shield = SPELLS['shield']
        self.mana -= shield['mana']
        self.armour_bonus = shield['effect']['armour']
        self.armour_duration = shield['effect']['duration']
        self.spells_cast += 's'

    def cast_poison(self, boss):
        poison = SPELLS['poison']
        self.mana -= poison['mana']
        boss.receive_poison(poison['effect'])
        self.spells_cast += 'p'

    def cast_recharge(self, boss):
        recharge = SPELLS['recharge']
        self.mana -= recharge['mana']
        self.mana_regen = recharge['effect']['mana']
        self.mana_regen_duration = recharge['effect']['duration']
        self.spells_cast += 'r'


class PlayerTwo(Player):
    def start_own_turn(self):
        self.hp -= 1
        super().start_own_turn()


class Boss:
    def __init__(self, hp, damage):
        self.hp = hp
        self.damage = damage
        self.poison_duration = 0
        self.poison_damage = 0

    def get_key(self):
        return f"B: H{self.hp} PD{self.poison_duration}"

    def start_turn(self):
        if self.poison_duration > 0:
            self.hp -= self.poison_damage
            self.poison_duration -= 1

    def receive_poison(self, poison):
        self.poison_duration = poison['duration']
        self.poison_damage = poison['damage']


class Fight:
    def __init__(self, player, boss, mana_spent, next_spell):
        self.player = player
        self.boss = boss
        self.mana_spent = mana_spent
        self.next_spell = next_spell

    def get_key(self):
        return (self.player.get_key(), self.boss.get_key(), self.mana_spent, self.next_spell)

    def __lt__(self, other):
        return self.mana_spent < other.mana_spent


# Using a PriorityQueue for fights, ordered by least mana spent,
# only works because the list of spells are ordered from cheapest to most expensive,
# and queuing up the next spell uses that order.
# If you go up to SPELLS and bump Magic Missile down,
# you're going to get a different result.
def run_fights(fights):
    scenarios = set()
    while not fights.empty():
        fight = fights.get()[1]
        fight_key = fight.get_key()
        if fight_key in scenarios: continue
        scenarios.add(fight_key)
        player = fight.player
        boss = fight.boss
        mana_spent = fight.mana_spent

        # player's turn
        player.start_own_turn()
        if player.hp <= 0: continue
        boss.start_turn()
        if boss.hp <= 0: return mana_spent, player.spells_cast
        getattr(player, 'cast_'+fight.next_spell)(boss)
        mana_spent += SPELLS[fight.next_spell]['mana']

        # boss's turn
        player.start_boss_turn()
        boss.start_turn()
        if boss.hp <= 0: return mana_spent, player.spells_cast
        player.hp -= max(1, boss.damage - player.get_effective_armour())
        if player.hp <= 0: continue

        # we only get here if both combatants are still alive. time to queue next spell(s)
        for spell in player.find_castable_spells(boss):
            fights.put((mana_spent, Fight(copy.copy(player), copy.copy(boss), mana_spent, spell)))
    return 0, None


# What is the least amount of mana you can spend and still win the fight?
def part_one(args) -> None:
    fights = PriorityQueue()
    for spell_name in SPELLS:
        fight = Fight(
            Player(hp=50, mana=500), Boss(hp=55, damage=8),
            mana_spent=0, next_spell=spell_name
        )
        fights.put((0, fight))
    (least_mana_spent, winning_spell_combo) = run_fights(fights)
    logging.info(f"Part One: {least_mana_spent} (expected 953) using spells: {winning_spell_combo}")


# At the start of each player turn (before any other effects apply), you lose 1 hit point.
# Now what's the least amount of mana you can spend and still win the fight?
def part_two(args) -> None:
    fights = PriorityQueue()
    for spell_name in SPELLS:
        fight = Fight(
            PlayerTwo(hp=50, mana=500), Boss(hp=55, damage=8),
            mana_spent=0, next_spell=spell_name
        )
        fights.put((0, fight))
    (least_mana_spent, winning_spell_combo) = run_fights(fights)
    logging.info(f"Part Two: {least_mana_spent} (expected 1289) using spells: {winning_spell_combo}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output-file', default=None)
    parser.add_argument('-v', '--verbose', default=False, action='store_true')
    parser.add_argument('-p', '--part', type=int, default=1)
    args = parser.parse_args()
    configure_logging(args.verbose, args.output_file)

    if args.part == 1: part_one(args)
    elif args.part == 2: part_two(args)
