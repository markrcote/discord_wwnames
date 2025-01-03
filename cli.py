import queue
import signal
import threading
from time import sleep

from cardgames.card_game import Player
from cardgames.blackjack import Blackjack

player = None
game = Blackjack()
cmd_q = queue.Queue()
cmd_listener_thread = None


def process_command(cmd):
    output = []

    if cmd == 'quit':
        raise KeyboardInterrupt
    elif cmd == 'help':
        output.extend([
            'Commands:',
            '  quit',
            '  help',
            '  hit',
            '  stand',
            '  bet <amount>',
            '  split',
            '  double',
            '  insurance',
            '  surrender',
        ])
    elif cmd == 'hit':
        game.hit(player)
    elif cmd =='stand':
        game.stand(player)
    elif cmd.startswith('bet'):
        try:
            amount = int(cmd.split(' ')[1])
        except ValueError:
                output.append('Invalid bet amount')
        else:
            game.bet(amount)
    elif cmd =='split':
        game.split(player)
    elif cmd == 'double':
        game.double(player)
    elif cmd == 'insurance':
        game.insurance(player)
    elif cmd =='surrender':
        game.surrender(player)
    else:
        output.append('Unknown command')
    return output


def cmd_listener():
    while True:
        try:
            cmd = input('> ')
        except EOFError:
            cmd = 'quit'
        print(f'command: {cmd}')
        cmd_q.put(cmd)
        if cmd == 'quit':
            break


def setup_cmd_listener():
    global cmd_listener_thread
    cmd_listener_thread = threading.Thread(target=cmd_listener, daemon=True)
    cmd_listener_thread.start()


def teardown_cmd_listener():
    cmd_listener_thread.join(1)


if __name__ == "__main__":
    output = game.tick()
    if output:
        print('\n'.join(output))

    player_name = input('Enter your name: ')
    player = Player(player_name)
    print(f'Welcome {player.name}')
    game.sit_down(player)

    setup_cmd_listener()

    try:
        while True:
            output = game.tick()
            if output:
                print('\n'.join(output))
            try:
                cmd = cmd_q.get(timeout=5)
            except queue.Empty:
                cmd = None
            output = None
            if cmd:
                output = process_command(cmd)

            if output:
                print('\n'.join(output))
    except KeyboardInterrupt:
        # Ctrl-C doesn't exactly work here because the cmd_listener thread is
        # stuck on the blocking input() call.  Fixing this requires a more
        # complex input routine.
        pass

    print('tearing down')
    teardown_cmd_listener()
    print('done')
