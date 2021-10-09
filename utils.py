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
                    _string += f"({error[1]}, {error[0]})"

                file.write(f"{str(i + 1)}.\t{_string}\n")
            except KeyError:
                # if one line hasn't any token
                pass


def add_symbols_to_file(symbols):
    with open("symbol_table.txt", "w") as file:
        for counter, symbol in enumerate(symbols):
            file.write(f"{counter}.\t{symbol}\n")


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


def print_log(buffer, char, next_char, selected_state, can_be_continued, line_number=1):

    print(f"------- {line_number} -------")
    print(f"Current char : {repr(char)} Next char : {repr(next_char)}")
    print(f"Buffer = {buffer}")
    print(f"Can be continued {can_be_continued}")
