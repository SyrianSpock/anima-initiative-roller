import argparse
from collections import namedtuple
import logging
import operator
import random
import yaml

Player = namedtuple('Player', ['name', 'initiative'])

def parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('file', type=str, help='File with modifiers.')

    return parser.parse_args()

def read_modifiers(yaml_file):
    with open(yaml_file) as file:
        return yaml.load(file)

def roll_initiative(name, modifier):
    initiative = modifier + roll_open()
    return Player(name=name, initiative=initiative)

def roll_open(base_roll=0, success=90, fail=3):
    roll = roll_100()
    logging.debug("Rolling {}, rolled {}, with success {}".format(base_roll, roll, success))
    if roll >= success:
        return roll_open(base_roll= roll + base_roll, success=success+1)
    else:
        res = roll + base_roll
        if base_roll == 0 and roll <= fail:
            res -= roll_100()
        return res

def roll_100():
    return random.randint(1,100)

def main():
    args = parse_arguments()

    modifiers = read_modifiers(args.file)
    players = [roll_initiative(player, modifiers[player]) for player in modifiers]
    players = sorted(players, key=lambda player: player.initiative, reverse=True)

    for player in players:
        print('{}:\t{}'.format(player.name, player.initiative))

if __name__ == '__main__':
    main()
