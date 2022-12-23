import curses, time, asyncio
from gameState import GameState

from asyncio import StreamReader
from asyncio import StreamReaderProtocol

"""
w = 119
W = 87

a = 97
A = 65

s = 115
S = 83

d = 100
D = 68

t = 116
T = 84
"""

async def get_user_input(misc_window):
    tick = 0
    while True:
        key = misc_window.getch()
        misc_window.clear()
        if key != -1:
            misc_window.addstr(1, 0, f'Pressed key ${key}')
        misc_window.addstr(0, 0, str(tick))
        misc_window.refresh()

        tick = tick + 1
        await asyncio.sleep(0.05)

async def game_loop(master_window):
    NewGame = GameState(master_window)

    playing = True

    while playing:
        key = master_window.getch()
        if key == 86 or key == 116:
            playing = False
            break
        else:
            NewGame.get_next_state(key)
            await asyncio.sleep(0.05)

    master_window.addstr(30, 0, "Goodbye!")

async def play_game(master_window, game_window, misc_window):
    await asyncio.gather(get_user_input(misc_window), game_loop(game_window))

def make_master_window(master_window):
    misc_window = master_window.subwin(2, 25, 0, 0)
    game_window = master_window.subwin(23, 25, 2, 0) # TODO: Figure out dimensions for this

    master_window.nodelay(True)
    game_window.nodelay(True)
    misc_window.nodelay(True)

    asyncio.run(play_game(master_window, game_window, misc_window))
    curses.endwin()

# https://docs.python.org/3/library/curses.html
if __name__ == "__main__":
    choice = input("Start tetris? ")
    if choice == "yes":
        curses.wrapper(make_master_window)

