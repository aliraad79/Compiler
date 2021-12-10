from anytree.render import RenderTree


def add_errors_to_file(line_number, error_dict):
    with open("lexical_errors.txt", "w") as file:
        # No error
        if not bool(error_dict):
            file.write("There is no lexical error.")
            return
        for i in range(0, line_number + 1):
            _string = ""
            try:
                for error in error_dict[i]:
                    _string += f"({error[1]}, {error[0]}) "

                file.write(f"{str(i + 1)}.\t{_string}\n")
            except KeyError:
                # if one line hasn't any token
                pass


def add_symbols_to_file(symbols):
    # Add all symbols to list
    for i in ["if", "else", "void", "int", "repeat", "break", "until", "return"]:
        if i not in symbols:
            symbols.append(i)
    with open("symbol_table.txt", "w") as file:
        for counter, symbol in enumerate(symbols):
            file.write(f"{counter + 1}.\t{symbol}\n")


def add_tokens_to_file(line_number: int, token_dict):
    with open("tokens.txt", "w") as file:
        for i in range(0, line_number + 1):
            _string = ""
            try:
                for token in token_dict[i]:
                    _string += f"({token.type}, {token.lexeme}) "
                file.write(f"{i + 1}.\t{_string}\n")
            except KeyError:
                # if one line hasn't any token
                pass


def print_scanner_log(
    buffer, char, next_char, selected_state, next_state, can_be_continued, line_number=1
):

    print(f"------- {line_number} -------")
    print(f"Current char : {repr(char)} Next char : {repr(next_char)}")
    print(f"Buffer = {buffer}")
    print(f"Can be continued {can_be_continued}")
    print(f"Present =>\t {selected_state.next_edges if selected_state else ''}")
    print(f"NExt =>\t\t {next_state.next_edges if next_state else ''}")


def write_syntax_errors_to_file(errors):
    with open("syntax_errors.txt", "w") as file:
        if len(errors) == 0:
            file.write("There is no syntax error.")
            return
        for error in errors:
            file.write(error + "\n")


def write_parse_tree_to_file(parse_tree):
    with open("parse_tree.txt", "w") as file:
        for pre, fill, node in RenderTree(parse_tree):
            file.write(f"{pre}{node.name}\n")


def print_parser_log(current_node, curret_token, return_nodes):
    print("________________________________________________")
    print(f"Return Nodes => {[(i, j.name) for i,j in return_nodes]}")
    print(f"current Node ==> {current_node}")
    print(f"Current token ==> {curret_token}")


def format_non_terminal(non_terminal: str):
    non_terminal = non_terminal.replace("_", "-")
    return str(non_terminal[0]).upper() + non_terminal[1:]


def reverse_format_non_terminal(non_terminal: str):
    non_terminal = non_terminal.replace("-", "_")
    return str(non_terminal).lower()


def return_firsts():
    with open("../firsts.txt", "r") as file:
        all_firsts = list(map(str.split, file.readlines()))
    return {str(line[0]).lower(): line[1:] for line in all_firsts}


def return_follows():
    with open("../follows.txt", "r") as file:
        all_follows = list(map(str.split, file.readlines()))
    return {str(line[0]).lower(): line[1:] for line in all_follows}
