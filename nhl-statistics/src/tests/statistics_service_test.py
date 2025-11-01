import unittest
from statistics_service import StatisticsService
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),  #  4+12 = 16
            Player("Lemieux", "PIT", 45, 54), # 45+54 = 99
            Player("Kurri",   "EDM", 37, 53), # 37+53 = 90
            Player("Yzerman", "DET", 42, 56), # 42+56 = 98
            Player("Gretzky", "EDM", 35, 89)  # 35+89 = 124
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        # annetaan StatisticsService-luokan oliolle "stub"-luokan olio
        self.stats = StatisticsService(
            PlayerReaderStub()
        )

    def test_search_finds_player(self):
        player = self.stats.search("Semenko")
        self.assertEqual(player.name, "Semenko")
        self.assertEqual(player.team, "EDM")
        self.assertEqual(player.goals, 4)
        self.assertEqual(player.assists, 12)

    def test_search_returns_none(self):
        player = self.stats.search("Hintz")
        self.assertIsNone(player)

    def test_team_returns_correct_players(self):
        edm_players = self.stats.team("EDM")
        self.assertEqual(len(edm_players), 3)
        player_names = [player.name for player in edm_players]
        self.assertIn("Semenko", player_names)
        self.assertIn("Kurri", player_names)
        self.assertIn("Gretzky", player_names)

    def test_top_returns_correct_number(self):
        top_players = self.stats.top(3)
        self.assertEqual(len(top_players), 4)
        
    def test_top_returns_correct_order(self):
        top_players = self.stats.top(4)
        self.assertEqual(top_players[0].name, "Gretzky")  
        self.assertEqual(top_players[1].name, "Lemieux")  
        self.assertEqual(top_players[2].name, "Yzerman")