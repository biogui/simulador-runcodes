
TAB      = " " * 4
LINE_LEN = 80

class S: # Style flags
    NONE      = ";0"
    STRONG    = ";1"
    BLUR      = ";2"
    ITALIC    = ";3"
    UNDERLINE = ";4"
    FLASH     = ";6"
    NEGATIVE  = ";7"
    STRIKE    = ";9"

class C: # Color flags
    NONE   = ";50"
    BLACK  = ";30"
    RED    = ";31"
    GREEN  = ";32"
    YELLOW = ";33"
    BLUE   = ";34"
    PURPLE = ";35"
    CYAN   = ";36"
    WHITE  = ";37"

def stylize_str(string, color=C.NONE, style=S.NONE):
    start = "\033[0{}{}m".format(style, color)
    end   = "\033[m"

    stylized_str = f"{start}{string}{end}"

    return stylized_str
