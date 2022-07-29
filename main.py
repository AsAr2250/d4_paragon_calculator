import random
import math
import winsound as ws

from tooltip import create_tooltip
from data import *


class Character:
    def __init__(self, inspected_board_id_list, character_class, level=49, gold=5, has_gold_drop=False,
                 glyphs=1, glyphs_max=1, leggy_count=0, current_respec_cost=RESPEC_COSTS[0]):
        self.inspected_board_id_list = inspected_board_id_list
        self.character_class = character_class
        self.level = level
        self.gold = gold
        self.has_gold_drop = has_gold_drop
        self.glyphs = glyphs
        self.glyphs_max = glyphs_max
        self.leggy_count = leggy_count
        self.current_respec_cost = current_respec_cost
        self.stat_counts = {}
        self.stat_sheet = ''
        self.currently_viewed_board_id = (0, 0)

    def update_stat_sheet(self):
        stat_string = ''
        for affix_id in range(4):
            if affix_id in self.stat_counts.keys():
                multiplier = 1 * self.stat_counts[affix_id][0] + 1.2 * self.stat_counts[affix_id][1]
                value = multiplier * MAGIC_TILE_AFFIXES[affix_id][0]
                if '.' in str(value) and str(value).split('.')[1] == '0':
                    value = int(str(value).split('.')[0])
                stat_string += f'{value} {MAGIC_TILE_AFFIXES[affix_id][1]}\n'
        for affix_id, counts in self.stat_counts.items():
            if affix_id not in (0, 1, 2, 3):
                multiplier = 1 * counts[0] + 1.2 * counts[1]
                value = round(multiplier * MAGIC_TILE_AFFIXES[affix_id][0], 1)
                if '.' in str(value) and str(value).split('.')[1] == '0':
                    value = int(str(value).split('.')[0])
                stat_string += f'{value} {MAGIC_TILE_AFFIXES[affix_id][1]}\n'
        stat_summary_label.config(text=stat_string)
        if stat_string == '':
            stat_summary_label.config(bg='black')
        else:
            stat_summary_label.config(bg='bisque3')
        self.stat_sheet = stat_string


class MetaWidget:
    def __init__(self, button, row, column, board_id=(0, 0), availability=0):
        self.button = button
        self.row = row
        self.column = column
        self.board_id = board_id
        self.availability = availability


class Tile(MetaWidget):
    """ Common and magic tiles are currently handled the same. We thus group common tiles under the 'magic' rarity. """
    legendary_affix_ids_revealed = []

    def __init__(self, button, row, column, board_id=(0, 0), availability=0, rarity='magic', boosted=False):
        super().__init__(button, row, column, board_id, availability)
        self.button.config(command=lambda: select_tile(self.row, self.column, self.board_id))
        self.rarity = rarity
        self.boosted = boosted
        if self.rarity not in ('center_tile', 'socket'):
            self.affix_id, self.affix = self.roll_affix()
        if self.rarity == 'magic':
            create_tooltip(self.button, f'{self.affix[2]}\n{self.affix[0]}{self.affix[1]}')
        elif self.rarity == 'center_tile':
            create_tooltip(self.button, STAT_BENEFITS[character.character_class])
        elif self.rarity == 'legendary':
            create_tooltip(self.button, f'Legendary\n{self.affix}')
        elif self.rarity == 'socket':
            create_tooltip(self.button, f'Socket a glyph to empower surrounding\ncommon and magic tiles by 20%.')

    def roll_affix(self):
        if self.rarity == 'magic':
            affix_id = random.randint(0, len(MAGIC_TILE_AFFIXES) + 10)
            # give rogues more dexterity and druids more willpower
            if affix_id > len(MAGIC_TILE_AFFIXES) - 1:
                if character.character_class == 'Rogue':
                    affix_id = 3
                elif character.character_class == 'Druid':
                    affix_id = 2
            return affix_id, MAGIC_TILE_AFFIXES[affix_id]
        elif self.rarity == 'rare':
            pass
        elif self.rarity == 'legendary':
            affix_id = -1
            while affix_id == -1:
                random_affix_id = random.randint(0, len(LEGENDARY_AFFIXES) - 1)
                if random_affix_id not in Tile.legendary_affix_ids_revealed:
                    affix_id = random_affix_id
            return affix_id, LEGENDARY_AFFIXES[affix_id]

    def update_image(self):
        if self.rarity == 'magic':
            if self.availability == 0:
                self.button.config(image=TILE_UNAVAILABLE_PHOTO)
            if self.availability == 1:
                self.button.config(image=TILE_AVAILABLE_PHOTO)
            if self.availability == 2:
                self.button.config(image=TILE_SELECTED_PHOTO)
        if self.rarity == 'socket':
            if self.availability == 0:
                self.button.config(image=GLYPH_SOCKET_PHOTO)
            if self.availability == 1:
                self.button.config(image=GLYPH_PHOTO)


class Gate(MetaWidget):
    def __init__(self, button, row, column, board_id=(0, 0), availability=0,):
        super().__init__(button, row, column, board_id, availability)
        self.button.config(command=lambda: use_gate(self.row, self.column))
        create_tooltip(self.button, 'Move to adjacent board')

    def update_image(self):
        if self.availability == 0:
            self.button.config(image=GATE_UNAVAILABLE_PHOTO)
        if self.availability == 1:
            self.button.config(image=GATE_AVAILABLE_PHOTO)


def init_board(old_board_id=(0, 0), new_board_id=(0, 0), additional_tile_count=90):
    new_tiles, new_gates = [], []
    if old_board_id == (0, 0) and new_board_id == (0, 0):
        # initialize center tile
        center_tile_button = tk.Button(window, image=LEGGY_TILE_PHOTO, highlightthickness=0, bd=0)
        center_tile_button.grid(row=10, column=10)
        new_tiles.append(Tile(button=center_tile_button, row=10, column=10, availability=2, rarity='center_tile'))
    else:
        # define legendary tile
        legendary_tile_button = tk.Button(window, image=LEGGY_TILE_PHOTO, highlightthickness=0, bd=0)
        new_tiles.append(Tile(button=legendary_tile_button, row=10, column=10, board_id=new_board_id, availability=0,
                              rarity='legendary'))

    # define gates
    for num, coords in enumerate([(0, 10), (10, 20), (20, 10), (10, 0)]):
        gate_button = tk.Button(window, image=GATE_UNAVAILABLE_PHOTO, command=use_gate,
                                highlightthickness=0, bd=0)
        gate_button.grid(row=coords[0], column=coords[1])
        new_gates.append(Gate(button=gate_button, row=coords[0], column=coords[1], board_id=new_board_id))

    # initialize vertical and horizontal tiles
    for i in range(1, 20):
        if i != 10:
            tile_button = tk.Button(window, image=TILE_UNAVAILABLE_PHOTO, highlightthickness=0, bd=0)
            tile_button.grid(row=10, column=i)
            new_tiles.append(Tile(button=tile_button, row=10, column=i, board_id=new_board_id))
            if i in (9, 11) and new_board_id == (0, 0):
                new_tiles[-1].availability = 1
                new_tiles[-1].update_image()
            tile_button = tk.Button(window, image=TILE_UNAVAILABLE_PHOTO, highlightthickness=0, bd=0)
            tile_button.grid(row=i, column=10)
            new_tiles.append(Tile(button=tile_button, row=i, column=10, board_id=new_board_id))
            if i in (9, 11) and new_board_id == (0, 0):
                new_tiles[-1].availability = 1
                new_tiles[-1].update_image()

    # add random magic tiles
    added_tiles = 0
    while added_tiles < additional_tile_count:
        row_num = random.randint(1, 19)
        col_num = random.randint(1, 19)
        is_free = True
        is_adjacent = False
        if row_num == 10 or col_num == 10:
            is_free = False
        for t in new_tiles:
            if (new_board_id, row_num, col_num) == (t.board_id, t.row, t.column):
                is_free = False
            if (new_board_id, row_num) == (t.board_id, t.row) and (col_num == t.column + 1 or col_num == t.column - 1):
                is_adjacent = True
            if (new_board_id, col_num) == (t.board_id, t.column) and (row_num == t.row + 1 or row_num == t.row - 1):
                is_adjacent = True
        if is_free and is_adjacent:
            tile_button = tk.Button(window, image=TILE_UNAVAILABLE_PHOTO, highlightthickness=0, bd=0)
            tile_button.grid(row=row_num, column=col_num)
            new_tiles.append(Tile(button=tile_button, row=row_num, column=col_num, board_id=new_board_id))
            added_tiles += 1

    # add sockets
    added_sockets = 0
    placed_socket_coords = (99, 99)
    for num_adjacent_tiles in (4, 3):
        tries = 0
        while added_sockets < 2 and tries < 200:
            tries += 1
            row_num = random.randint(1, 19)
            col_num = random.randint(1, 19)
            is_free = True
            adjacent_tiles = 0
            for t in new_tiles:
                if (new_board_id, row_num, col_num) == (t.board_id, t.row, t.column):
                    is_free = False
                if (new_board_id, row_num) == (t.board_id, t.row) and (
                        col_num == t.column + 1 or col_num == t.column - 1):
                    adjacent_tiles += 1
                if (new_board_id, col_num) == (t.board_id, t.column) and (row_num == t.row + 1 or row_num == t.row - 1):
                    adjacent_tiles += 1
            too_close_to_last_socket = True
            if row_num - 4 > placed_socket_coords[0] or row_num + 4 < placed_socket_coords[0] \
                    or col_num - 4 > placed_socket_coords[1] or col_num + 4 < placed_socket_coords[1]:
                too_close_to_last_socket = False
            if is_free and not too_close_to_last_socket and adjacent_tiles == num_adjacent_tiles:
                socket_button = tk.Button(window, image=GLYPH_SOCKET_PHOTO, highlightthickness=0, bd=0)
                socket_button.grid(row=row_num, column=col_num)
                new_tiles.append(Tile(button=socket_button, row=row_num, column=col_num, rarity='socket',
                                      board_id=new_board_id))
                added_sockets += 1
                placed_socket_coords = (row_num, col_num)

    return new_tiles, new_gates


def select_tile(row, column, board_id):
    for tile in tile_list:
        if tile.row == row and tile.column == column and tile.board_id == board_id and tile.availability != 1:
            if tile.rarity == 'socket' and character.glyphs:
                character.glyphs -= 1
                glyph_label.config(text=f'Glyphs: {character.glyphs}')
                tile.availability = 1
                tile.update_image()
                apply_glyph_bonus(row, column, board_id)
                if character.glyphs == 0:
                    glyph_label.config(bg='grey')
                if (character.level > 49 or character.glyphs < character.glyphs_max) \
                        and character.gold >= character.current_respec_cost:
                    respec_button.config(bg='dark olive green')
            if tile.rarity == 'center_tile':
                character.gold += 1
                gold_label.config(text=f'Gold: {character.gold}')
                if (character.level > 49 or character.glyphs < character.glyphs_max) \
                        and character.gold >= character.current_respec_cost:
                    respec_button.config(bg='dark olive green')
                if character.gold >= GLYPH_COST:
                    buy_glyph_button.config(bg='dark olive green')
            return
    if character.level == 100:
        return
    for tile in tile_list:
        if tile.row == row and tile.column == column and tile.board_id == board_id:
            tile.availability = 2
            tile.update_image()
            character.level += 0.5
            level_label.config(text=f'Level: {math.ceil(character.level)}')
            if tile.rarity in ('common', 'magic'):
                if tile.boosted:
                    if tile.affix_id not in character.stat_counts.keys():
                        character.stat_counts[tile.affix_id] = [0, 1]
                    else:
                        character.stat_counts[tile.affix_id][1] += 1
                else:
                    if tile.affix_id not in character.stat_counts.keys():
                        character.stat_counts[tile.affix_id] = [1, 0]
                    else:
                        character.stat_counts[tile.affix_id][0] += 1
                character.update_stat_sheet()
            if tile.rarity == 'legendary':
                character.leggy_count += 1
                leggy_label.place(x=1440, y=758)
                leggy_count_label.config(text=f'{character.leggy_count}', bg='bisque3')
                leggy_count_label.place(x=1500, y=770)
        if tile.availability == 0 and tile.board_id == board_id and tile.rarity != 'socket':
            if (row == tile.row and (column == tile.column + 1 or column == tile.column - 1)) \
                    or (column == tile.column and (row == tile.row + 1 or row == tile.row - 1)):
                tile.availability = 1
                tile.update_image()
    for gate in gate_list:
        if gate.board_id == board_id:
            if row == gate.row and (column == gate.column + 1 or column == gate.column - 1) \
                    or (column == gate.column and (row == gate.row + 1 or row == gate.row - 1)):
                gate.availability = 1
                gate.update_image()
    if (character.level > 49 or character.glyphs < character.glyphs_max) \
            and character.gold >= character.current_respec_cost:
        respec_button.config(bg='dark olive green')


def apply_glyph_bonus(row, column, board_id):
    for tile in tile_list:
        if tile.board_id == board_id and tile.rarity == 'magic':
            if tile.row + tile.column + 2 >= row + column >= tile.row + tile.column - 2 \
                    and tile.row - tile.column + 2 >= row - column >= tile.row - tile.column - 2:
                tile.boosted = True
                if tile.affix_id in (0, 1, 2, 3):
                    new_affix_value = round(1.2 * tile.affix[0])
                else:
                    new_affix_value = round(1.2 * tile.affix[0], 1)
                if '.' in str(new_affix_value) and str(new_affix_value).split('.')[1] == '0':
                    new_affix_value = int(str(new_affix_value).split('.')[0])
                tile.affix = (new_affix_value, tile.affix[1], tile.affix[2])
                create_tooltip(tile.button, f'{tile.affix[2]}\n{tile.affix[0]}{tile.affix[1]}')
                if tile.availability == 2:
                    for affix_id, counts in character.stat_counts.items():
                        if affix_id == tile.affix_id:
                            character.stat_counts[affix_id][0] = counts[0] - 1
                            character.stat_counts[affix_id][1] = counts[1] + 1
    character.update_stat_sheet()


def use_gate(row, column):
    # check if clicked gate is available
    clicked_gate = None
    for gate in gate_list:
        if row == gate.row and column == gate.column and character.currently_viewed_board_id == gate.board_id:
            clicked_gate = gate
    if not clicked_gate.availability:
        return

    # update board id
    old_board_id = character.currently_viewed_board_id
    new_board_id = None
    direction = None
    old_adjacent_tile_coords = None
    if (clicked_gate.row, clicked_gate.column) == (0, 10):
        direction = 'up'
        new_board_id = (old_board_id[0] - 1, old_board_id[1])
        old_adjacent_tile_coords = (1, 10)
    elif (clicked_gate.row, clicked_gate.column) == (10, 20):
        direction = 'right'
        new_board_id = (old_board_id[0], old_board_id[1] + 1)
        old_adjacent_tile_coords = (10, 19)
    elif (clicked_gate.row, clicked_gate.column) == (20, 10):
        direction = 'down'
        new_board_id = (old_board_id[0] + 1, old_board_id[1])
        old_adjacent_tile_coords = (19, 10)
    elif (clicked_gate.row, clicked_gate.column) == (10, 0):
        direction = 'left'
        new_board_id = (old_board_id[0], old_board_id[1] - 1)
        old_adjacent_tile_coords = (10, 1)

    # check if adjacent tile to clicked gate had been selected prior to using the gate
    old_adjacent_tile_availability = 0
    for tile in tile_list:
        if tile.board_id == clicked_gate.board_id and (tile.row, tile.column) == old_adjacent_tile_coords:
            old_adjacent_tile_availability = tile.availability

    # if gate leads to new board, create widgets
    if new_board_id not in character.inspected_board_id_list:
        new_tiles, new_gates = init_board(old_board_id=old_board_id, new_board_id=new_board_id)
        tile_list.extend(new_tiles)
        gate_list.extend(new_gates)

        # and drop gold
        if not character.has_gold_drop:
            gold_amount = character.level
            if 21 in character.stat_counts.keys():
                multiplier = character.stat_counts[21][0] + 1.2 * character.stat_counts[21][1]
                gold_amount *= (1 + multiplier * MAGIC_TILE_AFFIXES[21][0] / 100)
            gold_amount = int(round(gold_amount))
            gold_drop_button.config(text=f'{gold_amount} GOLD', command=lambda: pick_up_gold(gold_amount))
            pos_id = random.randint(1, 4)
            place_dict = {
                1: (50, 50),
                2: (850, 50),
                3: (50, 900),
                4: (850, 900)
            }
            gold_drop_button.place(x=place_dict[pos_id][0], y=place_dict[pos_id][1])
            character.has_gold_drop = True

    # adjust availability of destination gate and adjacent tile
    exit_gate_coords_by_direction = {
        'up': (20, 10),
        'right': (10, 0),
        'down': (0, 10),
        'left': (10, 20)
    }
    for coming_direction, exit_gate_coords in exit_gate_coords_by_direction.items():
        if direction == coming_direction:
            for gate in gate_list:
                if gate.board_id == new_board_id and (gate.row, gate.column) == exit_gate_coords:
                    gate.availability = 1
                    gate.update_image()
    if old_adjacent_tile_availability == 2:
        adjacent_tile_coords_by_direction = {
            'up': (19, 10),
            'right': (10, 1),
            'down': (1, 10),
            'left': (10, 19)
        }
        for coming_direction, adjacent_tile_coords in adjacent_tile_coords_by_direction.items():
            if direction == coming_direction:
                for tile in tile_list:
                    if tile.board_id == new_board_id and (tile.row, tile.column) == adjacent_tile_coords:
                        if tile.availability == 0:
                            tile.availability = 1
                            tile.update_image()

    # grid and grid_forget widgets according to new board id
    for widget_list in [tile_list, gate_list]:
        for widget in widget_list:
            if widget.board_id != new_board_id:
                widget.button.grid_forget()
            else:
                widget.button.grid(row=widget.row, column=widget.column)

    # update viewed board by character
    character.inspected_board_id_list.append(new_board_id)
    character.currently_viewed_board_id = new_board_id


def pick_up_gold(amount):
    character.gold += amount
    gold_label.config(text=f'Gold: {character.gold}')
    gold_drop_button.place_forget()
    if (character.level > 49 or character.glyphs < character.glyphs_max) \
            and character.gold >= character.current_respec_cost:
        respec_button.config(bg='dark olive green')
        character.has_gold_drop = False
    if character.gold >= GLYPH_COST:
        buy_glyph_button.config(bg='dark olive green')


def respec():
    if (character.level == 49 and character.glyphs == character.glyphs_max) \
            or character.gold < character.current_respec_cost:
        return
    for tile in tile_list:
        if tile.boosted:
            tile.affix = MAGIC_TILE_AFFIXES[tile.affix_id]
            create_tooltip(tile.button, f'{tile.affix[2]}\n{tile.affix[0]}{tile.affix[1]}')
            tile.boosted = False
        if tile.board_id == (0, 0) and (tile.row, tile.column) in ((9, 10), (10, 9), (10, 11), (11, 10)):
            tile.availability = 1
        else:
            tile.availability = 0
        tile.update_image()

    # reset character
    old_cost_index = RESPEC_COSTS.index(character.current_respec_cost)
    updated_cost = RESPEC_COSTS[old_cost_index + 1]
    character.__init__(inspected_board_id_list=character.inspected_board_id_list,
                       character_class=character.character_class, level=49,
                       gold=character.gold - character.current_respec_cost, has_gold_drop=character.has_gold_drop,
                       glyphs=character.glyphs_max, glyphs_max=character.glyphs_max,
                       current_respec_cost=updated_cost)
    character.update_stat_sheet()
    leggy_count_label.config(text='0')
    level_label.config(text='Level: 49')
    gold_label.config(text=f'Gold: {character.gold}')
    glyph_label.config(text=f'Glyphs: {character.glyphs}', bg='mediumslateblue')
    respec_button.config(text=f'Respec ({updated_cost}g)', bg='grey')

    # grid and grid_forget widgets according to new board id
    for widget_list in [tile_list, gate_list]:
        for widget in widget_list:
            if widget.board_id != (0, 0):
                widget.button.grid_forget()
            else:
                widget.button.grid(row=widget.row, column=widget.column)

    # play OST
    ws.PlaySound('d4ost.wav', ws.SND_ASYNC)


def buy_glyph():
    if character.gold >= GLYPH_COST:
        character.gold -= GLYPH_COST
        gold_label.config(text=f'Gold: {character.gold}')

        character.glyphs += 1
        character.glyphs_max += 1
        glyph_label.config(text=f'Glyphs: {character.glyphs}', bg='mediumslateblue')
        if character.gold < character.current_respec_cost:
            respec_button.config(bg='grey')
        if character.gold < GLYPH_COST:
            buy_glyph_button.config(bg='grey')


def switch_class(chosen_class):
    global character, tile_list, gate_list
    for widget in tile_list + gate_list:
        widget.button.destroy()
    tile_list, gate_list = [], []
    if chosen_class == character.character_class:
        return
    else:
        old_class_gold = character.gold
        character = Character(inspected_board_id_list=[(0, 0)], character_class=chosen_class, gold=old_class_gold)
        # update character image
        new_character_photo = None
        if character.character_class == 'Rogue':
            character_label.config(image=ROGUE_PHOTO)
        elif character.character_class == 'Druid':
            character_label.config(image=DRUID_PHOTO)
        level_label.config(text='Level: 49')
        gold_label.config(text=f'Gold: {old_class_gold}')
        glyph_label.config(text=f'Glyphs: {character.glyphs}')
        respec_button.config(text=f'Respec ({RESPEC_COSTS[0]}g)')
        stat_summary_label.config(text=character.stat_sheet)
        leggy_count_label.config(text='0')
        tile_list, gate_list = init_board()


if __name__ == '__main__':
    window.title('Paragon Board Calculator')
    window.geometry('1565x1200')
    window.iconbitmap('tile_legendary.ico')
    window.config(bg='grey')

    # place stone background
    bg_stone_photo = tk.PhotoImage(file='bg1.png')
    bg_stone_label = tk.Label(window, image=bg_stone_photo)
    bg_stone_label.place(x=0, y=0)

    # place druid character image
    character_label = tk.Label(window, image=DRUID_PHOTO)
    character_label.place(x=1012, y=0)

    # create class dropdown menu and generate character
    OptionList = ['Druid', 'Rogue']
    var_chosen_class = tk.StringVar(window)
    var_chosen_class.set(OptionList[0])
    class_dropdown = tk.OptionMenu(window, var_chosen_class, *OptionList, command=switch_class)
    class_dropdown.config(width=10, font=('Algerian', 12))
    class_dropdown.grid(row=0, column=22)
    character = Character(inspected_board_id_list=[(0, 0)], character_class=OptionList[0])

    # create character level label
    level_label = tk.Label(window, text='Level: 49', font=('Algerian', 11), bg='peru')
    level_label.place(x=1025, y=555)

    # create character gold label
    gold_label = tk.Label(window, text=f'Gold: {character.gold}', font=('Algerian', 11), bg='gold')
    gold_label.place(x=1025, y=590)

    # create character gold label
    glyph_label = tk.Label(window, text=f'Glyphs: {character.glyphs}', font=('Algerian', 11), bg='mediumslateblue')
    glyph_label.place(x=1025, y=625)

    # create respec button
    respec_button = tk.Button(window, text=f'Respec ({RESPEC_COSTS[0]}g)', command=respec)
    respec_button.config(width=13, font=('Algerian', 12), bg='grey')
    respec_button.place(x=1025, y=670)

    # create respec button
    buy_glyph_button = tk.Button(window, text='Buy glyph (50g)', command=buy_glyph)
    buy_glyph_button.config(width=13, font=('Algerian', 12), bg='grey')
    buy_glyph_button.place(x=1025, y=710)

    # initialize gold drop button
    gold_drop_button = tk.Button(window, text='324 Gold', command=pick_up_gold)
    gold_drop_button.config(width=8, font=('Algerian', 12), fg='white', bg='grey10', highlightthickness=0, bd=0)

    # initialize stat summary
    stat_summary_label = tk.Label(window, text=character.stat_sheet, font=('Algerian', 10), bg='black',
                                  anchor="e", justify=tk.LEFT)
    stat_summary_label.place(x=1013, y=758)

    # initialize leggy affix count label:
    leggy_label = tk.Label(window, image=LEGGY_TILE_PHOTO)
    leggy_count_label = tk.Label(window, text='1', font=('Algerian', 14), bg='black')

    tile_list, gate_list = init_board()

    ws.PlaySound('d4ost.wav', ws.SND_ASYNC)

    window.mainloop()
