# Not implemented -->


from typing import List


def add_error_to_file(string):
    with open("lexical_errors.txt", "w") as file:
        pass


def add_symbols_to_symbol_table(symbols):
    with open("symbol_table.txt", "w") as file:
        for counter, symbol in enumerate(symbols):
            file.write(f"{counter}.\t{symbol}\n")


# <--


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
