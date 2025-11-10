# Badminton Match Filter

A Python script to filter badminton match schedules and display only matches involving players from your club.

## Overview

This tool helps badminton coaches and club organizers quickly filter large match schedules to see only the matches that involve their club's players. It's especially useful for tournament days with hundreds of matches across multiple courts.

The script reads an Excel file containing match schedules and filters it to show:
- Matches where at least one player from your club is participating
- Matches where one team is blank/TBD

## Features

- **Automatic column detection** - Works with standard badminton schedule formats
- **Doubles support** - Handles both singles and doubles matches
- **Case-insensitive matching** - Player names are matched regardless of case
- **Flexible input** - Supports multiple name formats (e.g., "FirstName LastName" or "LastName, FirstName")
- **Command-line options** - Customize input/output files and filtering behavior
- **Comment support** - Add comments to your player list with `#`

## Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package manager)

### Install Dependencies

```bash
pip install pandas openpyxl
```

Or using requirements.txt:

```bash
pip install -r requirements.txt
```

## Quick Start

1. **Add your club players to `club_players.txt`:**

   ```
   Noa Deprez
   Seppe Cabus
   Wout Cabus
   Lotte Baekelandt
   ```

2. **Place your match schedule Excel file in the directory** (or use the `-i` option to specify the path)

3. **Run the script:**

   ```bash
   python filter_matches.py
   ```

4. **Open the filtered output file** (e.g., `tmp - Filtered.xlsx`)

## Usage

### Basic Usage

```bash
python filter_matches.py
```

This uses the default files:
- Input: `tmp.xlsx`
- Output: `tmp - Filtered.xlsx`
- Players: `club_players.txt`

### Command-Line Options

```bash
python filter_matches.py [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `-i, --input FILE` | Input Excel file with match schedule (default: `tmp.xlsx`) |
| `-o, --output FILE` | Output Excel file for filtered matches (default: auto-generated) |
| `-p, --players FILE` | Text file with club player names (default: `club_players.txt`) |
| `--team1-col COLUMN` | Column name for Team 1 (default: auto-detect column D) |
| `--team2-col COLUMN` | Column name for Team 2 (default: auto-detect column F) |
| `-v, --verbose` | Print verbose output |
| `-h, --help` | Show help message |

### Examples

**Filter a specific schedule file:**
```bash
python filter_matches.py -i "BK Jeugd Planning.xlsx" -o "filtered_schedule.xlsx"
```

**Use a custom players file:**
```bash
python filter_matches.py -p "my_team.txt"
```

**Specify team columns by name:**
```bash
python filter_matches.py --team1-col "Team 1" --team2-col "Team 2"
```

**Verbose output:**
```bash
python filter_matches.py -v
```

**Combine multiple options:**
```bash
python filter_matches.py -i schedule.xlsx -p players.txt -v
```

## File Formats

### Excel File Format

The script expects an Excel file (.xlsx) with the following columns:
- **Column B**: Match time
- **Column C**: Table/Court number
- **Column D**: Team 1 (player names)
- **Column E**: (optional) Score or other data
- **Column F**: Team 2 (player names)

For doubles matches, player names can be:
- On separate rows (one below the other)
- Separated by `/` (e.g., "Player 1 / Player 2")
- Separated by newlines within the same cell

### Players File Format

The `club_players.txt` file should contain one player name per line:

```
# Club Players List
# Lines starting with # are comments

Noa Deprez
Seppe Cabus
Wout Cabus
Lotte Baekelandt
Aurélie Baekelandt
```

**Important:**
- Player names are matched case-insensitively
- Leading/trailing spaces are ignored
- Comments start with `#`
- Blank lines are ignored

## How It Works

1. **Load club players** from the text file (ignoring comments)
2. **Read the Excel file** using pandas
3. **Auto-detect team columns** (defaults to columns D and F)
4. **For each match:**
   - Extract player names from both teams
   - Check if any player matches your club's player list
   - Keep the match if it contains a club player OR if a team is blank
5. **Save filtered matches** to a new Excel file

## Additional Scripts

### swap_names.py

Utility script to convert player names from "LastName, FirstName" to "FirstName LastName" format in `club_players.txt`.

```bash
python swap_names.py
```

This is useful if you copied player names from a source that uses the reversed format.

## Filtering Logic

The script keeps a match if **any** of these conditions are true:

1. Team 1 contains at least one player from your club
2. Team 2 contains at least one player from your club
3. Team 1 is blank/empty
4. Team 2 is blank/empty

This ensures you see:
- All matches where your players are competing
- Matches with TBD/blank teams (which might involve your players later)

## Troubleshooting

### No players loaded

**Error:** `Warning: No players found in club_players.txt`

**Solution:** Make sure `club_players.txt` has at least one non-comment, non-blank line with a player name.

### No matches in output

**Possible causes:**
- Player names in `club_players.txt` don't match the names in the Excel file exactly
- Check for spelling differences, extra spaces, or different name formats

**Solutions:**
- Verify player names match exactly (case-insensitive, but spelling must be correct)
- Use verbose mode (`-v`) to see which columns are being used
- Check the Excel file to see the exact format of player names

### Wrong columns detected

**Error:** `Error: Excel file doesn't have expected number of columns`

**Solution:**
- Use `--team1-col` and `--team2-col` to manually specify the correct columns
- Verify your Excel file has the standard format

### File not found

**Error:** `Error: Input file 'tmp.xlsx' not found!`

**Solution:**
- Make sure the Excel file is in the same directory as the script
- Or use `-i` to specify the full path to your Excel file

## Example Output

```bash
$ python filter_matches.py -v

Filtering matches from: tmp.xlsx
Output will be saved to: tmp - Filtered.xlsx
------------------------------------------------------------
Loaded 23 club players from club_players.txt
Total matches before filtering: 353
Using Team 1 column: Uitslag
Using Team 2 column: Unnamed: 5
Matches after filtering: 154
Removed 199 matches
------------------------------------------------------------
Filtered matches saved to: tmp - Filtered.xlsx

Done!
```

## Requirements

- Python 3.6+
- pandas
- openpyxl

See `requirements.txt` for exact versions.

## License

MIT License - feel free to use and modify as needed.

## Contributing

Suggestions and improvements are welcome! Please feel free to:
- Open an issue for bugs or feature requests
- Submit a pull request with improvements

## Author

Created to help badminton coaches efficiently manage tournament schedules.
