import argparse
from collections import namedtuple
from collections.abc import Iterable
import logging
import operator
import random
import yaml

Player = namedtuple('Player', ['name', 'initiative', 'fail'])

def parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('file', type=str, help='File with modifiers.')

    return parser.parse_args()

def read_modifiers(yaml_file):
    with open(yaml_file) as file:
        modifiers = yaml.load(file)

        failures = {}
        for player in modifiers:
            if isinstance(modifiers[player], Iterable):
                failures = {player: elem['fail'] for elem in modifiers[player][1:]}
                modifiers[player] = modifiers[player][0]

        return modifiers, failures

def roll_initiative(name, modifier, fail):
    initiative = modifier + roll_open()
    return Player(name=name, initiative=initiative, fail=fail)

def roll_open(base_roll=0, success=90, fail=3):
    roll = roll_100()
    logging.debug("Rolling {}, rolled {}, with success {}".format(base_roll, roll, success))
    if roll >= success:
        return roll_open(base_roll= roll + base_roll, success=success+1, fail=fail)
    else:
        res = roll + base_roll
        if base_roll == 0 and roll <= fail:
            res -= roll_100()
        return res

def roll_100():
    return random.randint(1,100)

def show_initiatives(players):
    for player in players:
        print('{}:\t{}'.format(player.name, player.initiative))

def main():
    args = parse_arguments()

    modifiers, failures = read_modifiers(args.file)
    players = [roll_initiative(player, modifiers[player], failures.get(player, 3)) for player in modifiers]

    players = sorted(players, key=lambda player: player.initiative, reverse=True)
    show_initiatives(players)

if __name__ == '__main__':
    main()
