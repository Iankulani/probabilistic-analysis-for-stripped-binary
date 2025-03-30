# -*- coding: utf-8 -*-
"""
Created on Sun March  30 08:345:47 2025

@author: IAN CARTER KULANI

"""

from colorama import Fore
import pyfiglet
import os
font=pyfiglet.figlet_format("BINARY ANALYSIS TOOL")
print(Fore.GREEN+font)



import os
import subprocess
import sys
import random
import string
from collections import Counter
import binascii


# Function to prompt the user for C/C++ file input
def get_user_input():
    file_path = input("Enter the path of the C/C++ source file:").strip()
    return file_path


# Function to compile and strip the C/C++ file
def compile_and_strip_binary(source_file):
    # Ensure the file exists
    if not os.path.exists(source_file):
        print(f"Error: The file {source_file} does not exist.")
        sys.exit(1)

    # Generate a random output binary file name to avoid overwriting
    output_file = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) + '.out'
    
    # Compile the C/C++ file
    compile_cmd = f"gcc -o {output_file} {source_file}"  # For C; change to g++ for C++ files
    strip_cmd = f"strip {output_file}"

    try:
        subprocess.run(compile_cmd, shell=True, check=True)
        subprocess.run(strip_cmd, shell=True, check=True)
        print(f"Compilation and stripping completed: {output_file}")
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"Error during compilation or stripping: {e}")
        sys.exit(1)


# Function to calculate entropy (a measure of randomness in a binary file)
def calculate_entropy(binary_data):
    byte_counts = Counter(binary_data)
    total_bytes = len(binary_data)
    entropy = 0

    for count in byte_counts.values():
        probability = count / total_bytes
        entropy -= probability * (probability.bit_length())  # Shannon entropy formula

    return entropy


# Function to read the binary and perform the analysis
def analyze_binary(binary_file):
    try:
        with open(binary_file, 'rb') as f:
            binary_data = f.read()

        # Calculate entropy
        entropy_value = calculate_entropy(binary_data)
        print(f"Entropy of the binary file: {entropy_value:.4f}")

        # Perform other analyses (e.g., examining byte distributions or signatures)
        # This is a simple demonstration of the concept.
        byte_histogram = Counter(binary_data)
        print("Byte frequency distribution:")
        for byte, count in byte_histogram.most_common(10):
            print(f"Byte: {hex(byte)}, Count: {count}")

    except Exception as e:
        print(f"Error reading or analyzing binary file: {e}")
        sys.exit(1)


# Main function to run the tool
def main():
    # Step 1: Get user input
    source_file = get_user_input()

    # Step 2: Compile and strip the binary
    stripped_binary = compile_and_strip_binary(source_file)

    # Step 3: Analyze the stripped binary
    analyze_binary(stripped_binary)


# Run the program
if __name__ == "__main__":
    main()
