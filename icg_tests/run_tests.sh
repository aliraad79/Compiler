#!/bin/sh
echo "" > log.txt
echo "" > brief_results.txt
for dir in Tests/*; do
    echo "=====================================>>>>> Running Test ${dir}...\n"
    cp "${dir}/input.txt" ./input.txt
    python3 ../compiler.py
done