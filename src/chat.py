#!/usr/bin/env python3
from sys import argv

print(f"Welcome! Ask any question about {argv[1]} to begin")

user_input = input()

while user_input.lower() not in ('quit', 'exit', 'cancel'):
    print(f'Sorry, I have not read {argv[1]}')
    user_input = input()
