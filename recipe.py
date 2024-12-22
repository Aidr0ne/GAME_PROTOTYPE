from curses import meta


def r0(stone, B, C, D):
    # Test recipe
    # 9x stone for a "big stone"
    if stone.amount >= 9:
        return True, stone.amount, B, C, D
    return False, stone.amount, B, C, D

def r1(Dust, paste, b, c):
    # Stone_chunk
    # 10x dust for a stone chunk
    # 1x paste to glue it together
    if Dust.amount >= 10 and paste.amount >= 1:
        Dust.amount - 10
        paste.amount - 1
        return True, Dust, paste, b, c
    return False, Dust, paste, b, c

def r2(chunk, paste, b, c):
    # Stone_cube
    # 7x chunks for a cube
    # 1x paste is needed to glue the chunks together
    if chunk.amount >= 7 and paste.amount >= 1:
        chunk.amount - 7
        paste.amount - 1
        return True, chunk, paste, b, c
    return False, chunk, paste, b, c

def r3(dust, water, b, c):
    # Copper Chunk
    # 10x copper dust for a copper chunk
    # 1x water is also needed to solidify the copper
    if dust.amount >= 10 and water.amount >= 1:
        dust.amount -= 10
        water.amount -= 1
        return True, dust, water, b, c
    return False, dust, water, b, c

def r4(dirt, water, a, b):
    # Paste
    # 3x Dirt and 1x water for a paste
    if dirt.amount >= 3 and water.amount >= 1:
        water.amount -= 1
        dirt.amount -= 3
        return True, dirt, water, a, b
    return False, dirt, water, a, b

def r5(copper_chunk, paste, coal_furnace, coal):
    # Copper Bar
    # 4x copper_chunk
    # 2x paste
    # 1x furnace (not consumed)
    # 6x coal
    if copper_chunk.amount >= 4 and paste.amount >= 2 and coal_furnace.amount >= 1 and coal.amount >= 6:
        copper_chunk.amount - 4
        paste.amount -= 2
        coal.amount -= 6
        return True, copper_chunk, paste, coal_furnace, coal
    return False, copper_chunk, paste, coal_furnace, coal

def r6(stone_cube, coal, paste, water):
    # Coal Furnace
    # 8x stone_cubes
    # 20x Peices of coal
    # 8x paste 
    # 10x water to fireproof it
    # the furnace works by being used as a ingrediant in any recipe
    # The more furnaces you have the more of something you can make in one click
    if stone_cube.amount >= 8 and coal.amount >= 20 and paste.amount >= 8 and water.amount >= 10:
        stone_cube.amount - 8
        coal.amount -= 20
        water.amount -= 10
        paste.amount -= 8
        return True, stone_cube, coal, paste, water
    return False, stone_cube, coal, paste, water

def r7(iron_dust, metal_paste, a, b):
    # Ion Chunk
    # 10x Iron dust needed
    # 2x metal_paste also needed to glue it togethet
    if iron_dust.amount >= 10 and metal_paste.amount >= 2:
        iron_dust.amount -= 10
        metal_paste.amount -= 2
        return True, iron_dust, metal_paste, a, b
    return False, iron_dust, metal_paste, a, b

def r8(paste, copper_dust, water, a):
    # Metal Paste
    # 3x paste
    # 1x copper_dust
    # 1x water
    if paste.amount >= 3 and copper_dust.amount >= 1 and water.amount >= 1:
        paste.amount -= 3
        copper_dust.amount -= 1
        water.amount -= 1
        return True, paste, copper_dust, water, a
    return False, paste, copper_dust, water, a
    # Metal Paste
    # 3x paste
    # 1x copper_dust
    # 1x water
