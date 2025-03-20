# Steam Game Checker

A command-line tool to check if a Steam user owns specific games from a text file.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Get your Steam Web API key:
   - Go to https://steamcommunity.com/dev/apikey
   - Sign in with your Steam account
   - Register for a new API key
   - Copy your API key

3. Create a `.env` file in the project root and add your Steam API key:
```
STEAM_API_KEY=your_api_key_here
```

## Usage

1. Create a text file (e.g., `games.txt`) with one game name per line.

2. Run the script with:
```bash
python steam_game_check.py <games_file> <steam_id_or_custom_url>
```

Example:
```bash
python steam_game_check.py games.txt 76561198123456789
# or with custom URL
python steam_game_check.py games.txt mycustomurl
```

## Notes

- The script supports both Steam IDs and custom URLs
- Game names in the text file should match the Steam store names
- The comparison is case-insensitive
- Empty lines in the games file are ignored 