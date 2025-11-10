#!/usr/bin/env python3
"""Quick script to swap names from 'LastName, FirstName' to 'FirstName LastName'"""

with open('club_players.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

with open('club_players.txt', 'w', encoding='utf-8') as f:
    for line in lines:
        if ',' in line and not line.strip().startswith('#'):
            # Split on comma, reverse, and rejoin
            parts = line.strip().split(',', 1)
            f.write(f"{parts[1].strip()} {parts[0].strip()}\n")
        else:
            f.write(line)
