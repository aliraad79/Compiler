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


def print_log(buffer, char, next_char, selected_nodes, can_be_continued, is_reach_end_of_universal, not_universal_next_nodes,line_number=1):
    print(f"------- {line_number} -------")
    print(
                f"Current char : {print_pretty(char)} Next char : {print_pretty(next_char)}"
            )
    print(f"Buffer = {buffer}")
    print(f"Can be continued {can_be_continued}")
    print(f"Is reach end of universal {is_reach_end_of_universal}")
    print(
                f"Selected Nodes = {selected_nodes}\n\t\tWith nexts = {selected_nodes[0].nexts if len(selected_nodes) >= 1 else None}"
            )
    print(f"End of universal condition = {not_universal_next_nodes}")
