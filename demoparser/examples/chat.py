import sys

from demoparser.parser import DemoParser


color_map = {
    "\001": "\x1b[0m",
    "\002": "\x1b[0;31m",
    "\003": "\x1b[0;34m",
    "\004": "\x1b[0;32m",
    "\005": "\x1b[1;32m",
    "\006": "\x1b[1;33m",
    "\007": "\x1b[1;31m"
}

ansi_colors = [
    '\x1b[0;34m',
    '\x1b[0;32m',
    '\x1b[0;36m',
    '\x1b[0;35m',
    '\x1b[0;33m',
    '\x1b[0;37m',
    '\x1b[1;30m',
    '\x1b[1;34m',
    '\x1b[1;32m',
    '\x1b[1;36m',
    '\x1b[1;31m',
    '\x1b[1;35m',
    '\x1b[1;33m',
    '\x1b[1;37m'
]


def print_color(text):
    t = text
    for k, v in color_map.items():
        t = t.replace(k, v)

    print(t)


def server_text(msg):
    print_color(msg.text)


def game_chat(msg):
    params = {}

    if msg.msg_name.endswith('AllDead'):
        params['dead'] = '\x1b[0;31m* DEAD *\x1b[0m '
    else:
        params['dead'] = ''

    params['name'] = '{}{}\x1b[0m'.format(
        ansi_colors[msg.ent_idx % 14], msg.params[0]
    )
    params['message'] = msg.params[1]

    fmt = "{dead}{name}: {message}".format(**params)
    print(fmt)


if __name__ == "__main__":
    d = DemoParser(sys.argv[1])
    d.add_callback('SayText', server_text)
    d.add_callback('SayText2', game_chat)
    d.parse()
