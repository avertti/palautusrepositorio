import requests
from rich.console import Console
from rich.table import Table
from rich.text import Text
from player import Player

class PlayerReader:
    def __init__(self, season):
        self.url = f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"
    
    def get_players(self):
        response = requests.get(self.url).json()

        players = []

        for player_dict in response:
            player = Player(player_dict)
            players.append(player)

        return players
class PlayerStats:
    def __init__(self, reader):
        self.players = reader.get_players()

    def top_scorers_by_nationality(self, nationality):
        players_by_nat = [player for player in self.players if player.nationality == nationality]
        
        return sorted(players_by_nat, key=lambda player: player.goals+player.assists, reverse=True )

def players_table(players, nationality, season):
    console = Console()
    
    table = Table(title=f"[bold blue]NHL Players from {nationality} ({season})", show_lines=True)
    table.add_column("Name", style="blue", no_wrap=True)
    table.add_column("Team", style="green")
    table.add_column("Goals", justify="right")
    table.add_column("Assists", justify="right")
    table.add_column("Points", justify="right")

    for player in players:
        table.add_row(player.name, player.team, str(player.goals), str(player.assists), str(player.goals + player.assists))
    
    console.print(table)


def main():
    console = Console() 
    season = console.input("[bold blue]Enter NHL season (xxxx-xx): ")
    nationality = console.input("[bold blue]Enter nationality (XXX): ")
    reader = PlayerReader(season)
    stats = PlayerStats(reader)
    players = stats.top_scorers_by_nationality(nationality)

    players_table(players, nationality, season)
    
if __name__ == "__main__":
    main()
