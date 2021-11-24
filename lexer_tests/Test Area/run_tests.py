import os
import re
from shutil import copyfile

log_file = open("log.txt", "w")
brief_file = open("brief_results.txt", "w")

for dir in sorted(os.listdir("../PA1_input_output_samples")):
    full_dir = "../PA1_input_output_samples/" + dir
    copyfile(full_dir + "/input.txt", "input.txt")
    os.system("python3 ../../compiler.py")
    log_file.write(
        f"\n\n\n\n=====================================>>>>> Running Test {dir}..."
    )
    brief_file.write(
        f"\n\n=====================================>>>>> Running Test {dir}..."
    )
    log_file.write("\n\n              *** tokens.txt diffrences ***\n")
    os.system(
        f'diff -y -B -W 250 -w  --suppress-common-lines ./tokens.txt "{full_dir}/tokens.txt" >> log.txt'
    )
    os.system(
        f'diff -y -B -W 250 -w -q ./tokens.txt "{full_dir}/tokens.txt" >> brief_results.txt'
    )
    log_file.write("\n\n              *** lexical_errors.txt diffrences ***\n")
    os.system(
        f'diff -y -B -W 250 -w  --suppress-common-lines ./lexical_errors.txt "{full_dir}/lexical_errors.txt" >> log.txt'
    )
    os.system(
        f'diff -y -B -W 250 -w -q ./lexical_errors.txt "{full_dir}/lexical_errors.txt" >> brief_results.txt'
    )
    log_file.write("\n\n              *** symbol_table.txt diffrences ***\n")

    a = sorted(
        [
            re.sub("[0-9]+\.\t", "", i.replace("\n", ""))
            for i in open(full_dir + "/symbol_table.txt", "r").readlines()
        ]
    )
    b = sorted(
        [
            re.sub("[0-9]+\.\t", "", i.replace("\n", ""))
            for i in open("symbol_table.txt", "r").readlines()
        ]
    )
    if a != b:
        os.system(
            f'diff -y -B -W 250 -w  --suppress-common-lines ./symbol_table.txt "{full_dir}/symbol_table.txt" >> log.txt'
        )
