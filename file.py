# Not implemented -->


def add_error_to_file(string):
    with open("lexical_errors.txt", "w") as file:
        pass


def add_error_to_file(symbol: str):
    with open("symbol_table.txt", "w") as file:
        pass


# <--


def add_tokens_to_file(line_number: int, token_dict):
    with open("tokens.txt", "w") as file:
        for i in range(0, line_number + 1):
            _string = ""
            try:
                for token in token_dict[i]:
                    _string += f"({token.type}, {token.lexeme}) "
                file.write(f"{i + 1}.  {_string}\n")
            except KeyError:
                # if one line hasn't any token
                pass
