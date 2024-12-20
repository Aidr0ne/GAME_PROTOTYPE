def r0(stone, B, C, D):
    # Test recipe
    # 9x stone for a "big stone"
    if stone.amount >= 9:
        return True, stone, B, C, D
    return False, stone, B, C, D

    # All Recipe functions must return True/False
    # Also Please add comments to this file so we know what we are looking at

def r1(Dust, a, b, c):
    # Stone_chunk
    if Dust >= 10:
        return True, Dust - 10, a, b, c
    return False, Dust - 10, a, b, c

def r2(chunk, a, b, c):
    # Stone_cube
    # 7x chunks for a cube
    if chunk >= 10:
        return True, chunk - 7, a, b, c
    return False, chunk, a, b, c