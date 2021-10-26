# Jafar Sadeghi 97106079
# Ali Ahmadi Kafeshani 97105703

from scanner import Scanner

scanner = Scanner()

token = ""
while token != "$":
    token = scanner.get_next_token()
    # print(token)
scanner.save_to_file()