#!/usr/bin/env python3
import os
import sys
import requests
from dotenv import load_dotenv
from typing import List, Dict, Optional

# Load environment variables
load_dotenv()

class SteamGameChecker:
    def __init__(self):
        self.api_key = os.getenv('STEAM_API_KEY')
        if not self.api_key:
            print("Error: STEAM_API_KEY not found in environment variables")
            print("Please create a .env file with your Steam API key")
            sys.exit(1)
        
        self.base_url = "http://api.steampowered.com"
    
    def get_steam_id(self, custom_url: str) -> Optional[str]:
        """Get Steam ID from custom URL"""
        url = f"{self.base_url}/ISteamUser/ResolveVanityURL/v0001/"
        params = {
            'key': self.api_key,
            'vanityurl': custom_url
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if data['response']['success'] == 1:
            return data['response']['steamid']
        return None
    
    def get_owned_games(self, steam_id: str) -> List[Dict]:
        """Get list of owned games for a Steam ID"""
        url = f"{self.base_url}/IPlayerService/GetOwnedGames/v0001/"
        params = {
            'key': self.api_key,
            'steamid': steam_id,
            'include_appinfo': 1,
            'include_played_free_games': 1
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if 'response' in data and 'games' in data['response']:
            return data['response']['games']
        return []
    
    def check_games(self, games_file: str, steam_id: str) -> None:
        """Check if games from file are owned by the Steam ID"""
        try:
            with open(games_file, 'r', encoding='utf-8') as f:
                games_to_check = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Error: Games file '{games_file}' not found")
            return
        
        owned_games = self.get_owned_games(steam_id)
        owned_game_names = {game['name'].lower() for game in owned_games}
        
        # Separate games into owned and not owned
        owned = []
        not_owned = []
        
        for game in games_to_check:
            if game.lower() in owned_game_names:
                owned.append(game)
            else:
                not_owned.append(game)
        
        print("\nGame Ownership Check Results:")
        print("-" * 50)
        
        if owned:
            print("\nOwned Games:")
            print("-" * 20)
            for game in sorted(owned):
                print(f"✓ {game}")
        
        if not_owned:
            print("\nNot Owned Games:")
            print("-" * 20)
            for game in sorted(not_owned):
                print(f"✗ {game}")
        
        print("\nSummary:")
        print(f"Total games checked: {len(games_to_check)}")
        print(f"Owned: {len(owned)}")
        print(f"Not owned: {len(not_owned)}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python steam_game_check.py <games_file> <steam_id_or_custom_url>")
        sys.exit(1)
    
    games_file = sys.argv[1]
    steam_id_or_url = sys.argv[2]
    
    checker = SteamGameChecker()
    
    # Check if input is a custom URL
    if not steam_id_or_url.isdigit():
        steam_id = checker.get_steam_id(steam_id_or_url)
        if not steam_id:
            print(f"Error: Could not resolve Steam ID for custom URL: {steam_id_or_url}")
            sys.exit(1)
    else:
        steam_id = steam_id_or_url
    
    checker.check_games(games_file, steam_id)

if __name__ == "__main__":
    main() 