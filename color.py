

"""
"""


from enum import Enum


class Color(Enum):


    WHITE   = (255, 255, 255)
    BLACK   = (0  , 0  , 0  )
    RED     = (255, 0  , 0  )
    GREEN   = (0  , 255, 0  )
    BLUE    = (0  , 0  , 255)
    CYAN    = (0  , 255, 255)
    YELLOW  = (255, 255, 0  )
    MAGENTA = (255, 0  , 255)

    WHITE_A   = (255, 255, 255)
    BLACK_A   = (0  , 0  , 0,   127  )
    RED_A     = (255, 0  , 0,   127  )
    GREEN_A   = (0  , 255, 0,   127  )
    BLUE_A    = (0  , 0  , 255, 127)
    CYAN_A    = (0  , 255, 255, 127)
    YELLOW_A  = (255, 255, 0,   127  )
    MAGENTA_A = (255, 0  , 255, 127)
