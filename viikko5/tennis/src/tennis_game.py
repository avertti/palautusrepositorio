class TennisGame:

    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_score = 0
        self.player2_score = 0

    def won_point(self, player_name):
        if player_name == self.player1_name:
            self.player1_score += 1
        else:
            self.player2_score += 1

    def tied(self):
        return self.player1_score == self.player2_score

    advantage = 4

    def endgame(self):
        return (
            self.player1_score >= self.advantage or self.player2_score >= self.advantage
        )

    def tie_score(self):
        if self.player1_score == 0:
            return "Love-All"
        if self.player1_score == 1:
            return "Fifteen-All"
        if self.player1_score == 2:
            return "Thirty-All"
        return "Deuce"

    def advantage_or_win(self):
        score_difference = self.player1_score - self.player2_score
        if score_difference == 1:
            return f"Advantage {self.player1_name}"
        if score_difference == -1:
            return f"Advantage {self.player2_name}"
        if score_difference >= 2:
            return f"Win for {self.player1_name}"
        return f"Win for {self.player2_name}"

    names = {0: "Love", 1: "Fifteen", 2: "Thirty", 3: "Forty"}

    def score_names(self, points):
        return self.names.get(points, "Forty")

    def normal_score(self):
        player1_score_name = self.score_names(self.player1_score)
        player2_score_name = self.score_names(self.player2_score)
        return f"{player1_score_name}-{player2_score_name}"

    def get_score(self):
        if self.tied():
            return self.tie_score()
        if self.endgame():
            return self.advantage_or_win()
        return self.normal_score()
