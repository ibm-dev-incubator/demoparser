import sys

from demoparser.parser import DemoParser


def death(event, msg):
    for idx, key in enumerate(event['event'].keys):
        if key.name == 'attacker':
            user_id = msg.keys[idx].val_short
            attacker = d.entities.get_by_user_id(user_id)
        elif key.name == 'userid':
            user_id = msg.keys[idx].val_short
            victim = d.entities.get_by_user_id(user_id)
        elif key.name == 'weapon':
            weapon = msg.keys[idx].val_string
        elif key.name == 'headshot':
            headshot = msg.keys[idx].val_bool

    if attacker and victim:
        print("\n --- Player Death at tick {}---".format(d.current_tick))
        print("{} killed by {} with {}. Headshot? {}.\n"
              "Attacker: health = {} position = {}\n"
              "Victim: position = {}".format(
                  victim.name.decode(),
                  attacker.name.decode(),
                  weapon,
                  'Yes' if headshot else 'No',
                  attacker.health,
                  attacker.position,
                  victim.position))


if __name__ == "__main__":
    d = DemoParser(sys.argv[1])
    d.add_callback('player_death', death)
    d.parse()
