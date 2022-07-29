import tkinter as tk

window = tk.Tk()

GATE_UNAVAILABLE_PHOTO = tk.PhotoImage(file='gate_unavailable.png')
GATE_AVAILABLE_PHOTO = tk.PhotoImage(file='gate_available.png')
TILE_UNAVAILABLE_PHOTO = tk.PhotoImage(file='tile_unavailable.png')
TILE_AVAILABLE_PHOTO = tk.PhotoImage(file='tile_available.png')
TILE_SELECTED_PHOTO = tk.PhotoImage(file='tile_selected.png')
LEGGY_TILE_PHOTO = tk.PhotoImage(file='tile_legendary.png')
GLYPH_SOCKET_PHOTO = tk.PhotoImage(file='glyph_socket.png')
GLYPH_PHOTO = tk.PhotoImage(file='glyph.png')
DRUID_PHOTO = tk.PhotoImage(file='bg_druid.png')
ROGUE_PHOTO = tk.PhotoImage(file='bg_rogue.png')

MAGIC_TILE_AFFIXES = {
    0:  (5,  ' Strength', 'Common'),
    1:  (5,  ' Intelligence', 'Common'),
    2:  (5,  ' Willpower', 'Common'),
    3:  (5,  ' Dexterity', 'Common'),
    4:  (2,  '% Damage Reduction', 'Magic'),
    5:  (1,  '% Dodge Chance', 'Magic'),
    6:  (10, '% Fire Resistance', 'Magic'),
    7:  (10, '% Cold Resistance', 'Magic'),
    8:  (10, '% Lightning Resistance', 'Magic'),
    9:  (10, '% Poison Resistance', 'Magic'),
    10: (10, '% Shadow Resistance', 'Magic'),
    11: (3,  '% Damage Reduction from Elites, Bosses and Players', 'Magic'),
    12: (5,  '% Reduced Duration of Enemy Control Impairing Effects', 'Magic'),
    13: (5,  '% Increased Duration of Control Impairing Effects', 'Magic'),
    14: (5,  '% Increased Damage to Stunned Targets', 'Magic'),
    15: (5,  '% Increased Damage to Enemies in Melee Range', 'Magic'),
    16: (5,  '% Increased Damage to Enemies out of Melee Range', 'Magic'),
    17: (3,  '% Reduced cost for skills', 'Magic'),
    18: (3,  '% Cooldown Reduction', 'Magic'),
    19: (3,  '% Movement Speed', 'Magic'),
    20: (2,  '% Magic Find', 'Magic'),
    21: (5,  '% Gold Find', 'Magic')
}

LEGENDARY_AFFIXES = {
    'Rogue':
        {
            0: 'Deadly Poison\nYour poisons also slow the enemy by 10% and they take 25 damage per second for '
               '5 seconds. Stacks 5 times.',
            1: 'Armed to the teeth\nYou can equip a dagger as a third weapon and gain its stats and legendary affixes.'
               '\nDexterity > 200: You also gain its attack damage.',
            2: 'Trap Mastery\nLightning Traps periodically appear around you dealing 400 damage after 2 seconds to'
               'nearby enemies. Intelligence > 100: after 0.5 seconds.',
            3: 'Assassination\nYour basic melee and ranged attacks are critical hits while in the Shadow Realm.\n'
               'Strength > 100: All your critical hits deal +50% damage.',
            4: 'Crossbow Specialization\nYour ranged attacks with crossbows have a 30% chance to stun the target for'
               '1 second.',
            5: 'Bow Specialization´\nYour bow attacks and skill have +50% range and ignore X armor rating, where X is '
               'your combined Strength and Intelligence',
            6: 'Parthian shot\nWhile mounted, you can perform basic ranged attacks.\nDexterity > 250: and use ranged '
               'skills.',
            7: 'Adrenaline Rush\nAfter being the victim of a critical strike, gain immunity to stun and +50% resource '
               'generation for 10 seconds.',
            8: 'Cheat Death\nWhen taking fatal damage, survive with 1 HP instead and become immune to all damage for 2 '
               'seconds. Can only occur once a minute.',
            9: "On razor's edge\nFor each % life missing, deal that much % more dmg."
        },
    'Druid':
        {
            0: 'Thick hide\nIncrease your armor by 30% while shapeshifted'
               '\nStrength > 150: and 2 seconds after leaving a shapeshift form.',
            1: 'Harsh winds\nYour tornado skills deal 1 additional physical damage for each point in Willpower'
               '\nWillpower > 200: and knock back enemies hit.',
            2: 'Shapeshifter\nFor 4 seconds after changing your form, deal 20% increased damage with all skills.',
            3: 'Alpha\nYour wolf skills are also performed by your wolf companions on their nearest enemy.',
            4: 'Circle of life\nYour skills heal you for 5% of their damage for each enemy they kill',
            5: 'Staff Specialization´\nYour skills and basic attacks have a 5% chance to stun the enemy hit while '
               'wielding a quarterstaff.',
            6: 'Run with the pack\nFor each wolf companion following you, you both get +30% movement speed. '
               'You stay in wolf form as long as you do not use a non-wolf skill.',
            7: 'Roar\nYour bear skills have a 10% chance to fear enemies.',
            8: 'Afterlife\nWhen taking fatal damage, survive with 1 HP instead and heal yourself for 1000 health. '
               'Can only occur once a minute.',
            9: 'Raven spy\nPlayers in a 300yd radius are shown on the map\nIntelligence > 50: and their health bar.'
        }
}

STAT_BENEFITS = {
    'Rogue': 'Rogue\n'
             '1 Strength\n-Increases Resource Generation by 0.05%\n-Increases Defense by 1\n'
             '1 Intelligence\n-Increases Critical Strike Chance by 0.05%\n'
             '-Increases All Resistance by 0.1%\n'
             '1 Willpower\n-Increases Healing Received by 0.1%\n'
             '1 Dexterity\n-Increases Skill Damage by 0.05%\n'
             '-Increases Chance to Dodge attacks by 0.05%\n'
             '\n(NOT CONFIRMED)',
    'Druid': 'Druid\n'
             '1 Strength\n-Increases Critical Strike Chance by 0.05%\n-Increases Defense by 1\n'
             '1 Intelligence\n-Increases Resource Generation by 0.05%\n'
             '-Increases All Resistance by 0.1%\n'
             '1 Willpower\n-Increases Skill Damage by 0.05%\n-Increases Healing Received by 0.1%\n'
             '1 Dexterity\n-Increases Chance to Dodge attacks by 0.05%\n'
             '\n(NOT CONFIRMED)',
}

RESPEC_COSTS = [pow(5, x) for x in range(20)]

GLYPH_COST = 50
