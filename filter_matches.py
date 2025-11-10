#!/usr/bin/env python3
"""
Badminton Match Filter Script

This script filters an Excel file containing badminton matches to keep only:
1. Matches where Team 1 (column D) OR Team 2 (column F) contains at least one player from your club
2. Matches where Team 1 OR Team 2 is blank/empty

For doubles matches (where 2 players are listed), the script handles entries separated by '/' or newlines.
"""

import argparse
import pandas as pd
import sys
from pathlib import Path


def load_club_players(players_file):
    """
    Load the list of club players from a text file.

    Args:
        players_file: Path to the text file containing player names (one per line)

    Returns:
        Set of player names (normalized to lowercase for case-insensitive matching)
    """
    try:
        with open(players_file, 'r', encoding='utf-8') as f:
            # Read lines, strip whitespace, ignore comments, convert to lowercase
            players = {
                line.strip().lower()
                for line in f
                if line.strip() and not line.strip().startswith('#')
            }

        if not players:
            print(f"Warning: No players found in {players_file}")
            return set()

        print(f"Loaded {len(players)} club players from {players_file}")
        return players

    except FileNotFoundError:
        print(f"Error: Players file '{players_file}' not found!")
        print(f"Please create this file with one player name per line.")
        sys.exit(1)


def extract_player_names(team_cell):
    """
    Extract individual player names from a team cell.
    Handles singles (1 player) and doubles (2 players separated by '/' or newline).

    Args:
        team_cell: Cell value from team column

    Returns:
        List of player names (normalized to lowercase)
    """
    if pd.isna(team_cell) or str(team_cell).strip() == '':
        return []

    team_str = str(team_cell).strip()

    # Split by common separators for doubles
    if '\n' in team_str:
        players = team_str.split('\n')
    elif '/' in team_str:
        players = team_str.split('/')
    else:
        # Single player
        players = [team_str]

    # Clean up and normalize player names
    return [p.strip().lower() for p in players if p.strip()]


def is_club_match(team1, team2, club_players):
    """
    Check if a match involves at least one club player or has a blank team.

    Args:
        team1: Team 1 cell value
        team2: Team 2 cell value
        club_players: Set of club player names (lowercase)

    Returns:
        True if match should be kept, False otherwise
    """
    # Check if either team is blank/empty
    team1_empty = pd.isna(team1) or str(team1).strip() == ''
    team2_empty = pd.isna(team2) or str(team2).strip() == ''

    if team1_empty or team2_empty:
        return True

    # Extract player names from both teams
    team1_players = extract_player_names(team1)
    team2_players = extract_player_names(team2)

    # Check if any player from either team is in the club
    all_players = team1_players + team2_players

    for player in all_players:
        if player in club_players:
            return True

    return False


def detect_team_columns(df):
    """
    Automatically detect which columns contain team data.

    Args:
        df: DataFrame to analyze

    Returns:
        Tuple of (team1_col_index, team2_col_index)
    """
    # Default assumption: column D (index 3) and F (index 5)
    # This matches the typical badminton match schedule format
    if len(df.columns) >= 6:
        return (3, 5)
    else:
        raise ValueError(f"Excel file doesn't have expected number of columns. Found: {df.columns.tolist()}")


def filter_matches(input_file, output_file, players_file, team1_col=None, team2_col=None, verbose=False):
    """
    Filter the badminton matches Excel file.

    Args:
        input_file: Path to input Excel file
        output_file: Path to output Excel file
        players_file: Path to club players text file
        team1_col: Optional column index/name for Team 1 (default: auto-detect)
        team2_col: Optional column index/name for Team 2 (default: auto-detect)
        verbose: Print verbose output
    """
    if verbose:
        print(f"\nFiltering matches from: {input_file}")
        print(f"Output will be saved to: {output_file}")
        print("-" * 60)

    # Load club players
    club_players = load_club_players(players_file)

    if not club_players:
        print("Error: No club players loaded. Cannot filter matches.")
        sys.exit(1)

    # Read the Excel file
    try:
        df = pd.read_excel(input_file)
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        sys.exit(1)

    if verbose:
        print(f"Total matches before filtering: {len(df)}")

    # Determine team columns
    if team1_col is None or team2_col is None:
        try:
            team1_idx, team2_idx = detect_team_columns(df)
            team1_col = df.columns[team1_idx]
            team2_col = df.columns[team2_idx]
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)

    if verbose:
        print(f"Using Team 1 column: {team1_col}")
        print(f"Using Team 2 column: {team2_col}")

    # Verify columns exist
    if team1_col not in df.columns or team2_col not in df.columns:
        print(f"Error: Specified columns not found in Excel file")
        print(f"Available columns: {df.columns.tolist()}")
        sys.exit(1)

    # Filter rows based on club players
    mask = df.apply(
        lambda row: is_club_match(row[team1_col], row[team2_col], club_players),
        axis=1
    )

    filtered_df = df[mask]

    print(f"Matches after filtering: {len(filtered_df)}")
    print(f"Removed {len(df) - len(filtered_df)} matches")

    if verbose:
        print("-" * 60)

    # Save to output file
    try:
        filtered_df.to_excel(output_file, index=False)
        print(f"Filtered matches saved to: {output_file}")
    except Exception as e:
        print(f"Error saving Excel file: {e}")
        sys.exit(1)


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Filter badminton match schedules to show only matches with your club players',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage with default files
  python filter_matches.py

  # Specify input and output files
  python filter_matches.py -i schedule.xlsx -o filtered_schedule.xlsx

  # Use custom players file
  python filter_matches.py -p my_players.txt

  # Specify team columns by name
  python filter_matches.py --team1-col "Team 1" --team2-col "Team 2"

  # Verbose output
  python filter_matches.py -v
        """
    )

    parser.add_argument(
        '-i', '--input',
        type=str,
        default='tmp.xlsx',
        help='Input Excel file with match schedule (default: tmp.xlsx)'
    )

    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output Excel file for filtered matches (default: <input> - Filtered.xlsx)'
    )

    parser.add_argument(
        '-p', '--players',
        type=str,
        default='club_players.txt',
        help='Text file with club player names (default: club_players.txt)'
    )

    parser.add_argument(
        '--team1-col',
        type=str,
        help='Column name or index for Team 1 (default: auto-detect column D)'
    )

    parser.add_argument(
        '--team2-col',
        type=str,
        help='Column name or index for Team 2 (default: auto-detect column F)'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Print verbose output'
    )

    args = parser.parse_args()

    # Resolve file paths
    input_file = Path(args.input)

    # Generate default output filename if not provided
    if args.output:
        output_file = Path(args.output)
    else:
        output_file = input_file.parent / f"{input_file.stem} - Filtered{input_file.suffix}"

    players_file = Path(args.players)

    # Check if input file exists
    if not input_file.exists():
        print(f"Error: Input file '{input_file}' not found!")
        sys.exit(1)

    # Check if players file exists
    if not players_file.exists():
        print(f"Error: Players file '{players_file}' not found!")
        sys.exit(1)

    # Run the filter
    filter_matches(
        input_file,
        output_file,
        players_file,
        team1_col=args.team1_col,
        team2_col=args.team2_col,
        verbose=args.verbose
    )

    print("\nDone!")


if __name__ == "__main__":
    main()
