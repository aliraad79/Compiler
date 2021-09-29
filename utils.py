def print_pretty(char):
    phrase = char
    if char == "\n":
        phrase = "\\n"
    elif char == "\t":
        phrase = "\\t"
    elif char == " ":
        phrase = "space"
    elif char == "":
        phrase = "EOF"
    return phrase