"""Level data for VC-Arkanoid

Level Format:
    - Each level is a list of strings
    - Each string represents a row of bricks
    - Characters:
        'n' = Normal brick (1 hit)
        's' = Silver brick (2 hits)
        'g' = Gold brick (indestructible)
        ' ' = Empty space
"""

LEVELS = [
    # Level 1: Introduction
    [
        "gggggggggg",
        "ssssssssss",
        "nnnnnnnnnn",
        "nnnnnnnnnn",
        "nnnnnnnnnn",
    ],

    # Level 2: Boss Stage (Doh)
    [
        "          ",
        "          ",
        "          ",
        "          ",
        "          ",
    ],

    # Level 3: Pyramid
    [
        "    nn    ",
        "   ssss   ",
        "  gggggg  ",
        " ssssssss ",
        "nnnnnnnnnn",
    ],

    # Level 4: Checkerboard
    [
        "n s n s n ",
        " s n s n s",
        "n s n s n ",
        " s n s n s",
        "n s n s n ",
    ],

    # Level 5: Fortress
    [
        "ggnnnnnngg",
        "gssssssssg",
        "gnn ss nng",
        "gn ssss ng",
        "gggggggggg",
    ],

    # Level 6: Diamond
    [
        "     n    ",
        "    sss   ",
        "   nnnnn  ",
        "  sssssss ",
        "   nnnnn  ",
        "    sss   ",
        "     n    ",
    ],

    # Level 7: Stripes
    [
        "nnnnnnnnnn",
        "ssssssssss",
        "gggggggggg",
        "ssssssssss",
        "nnnnnnnnnn",
    ],

    # Level 8: Maze
    [
        "g n n n ng",
        "g s   s ng",
        "g n n n ng",
        "g s   s ng",
        "gggggggggg",
    ],

    # Level 9: Cross
    [
        "    nn    ",
        "    ss    ",
        "nnnnggnnnn",
        "ssssggssss",
        "    nn    ",
        "    ss    ",
    ],

    # Level 10: Final Challenge
    [
        "gsgsgsgsgs",
        "sngngngngn",
        "gsgsgsgsgs",
        "sngngngngn",
        "gsgsgsgsgs",
        "nnnnnnnnnn",
    ],
]
