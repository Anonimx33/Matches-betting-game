from dataclasses import dataclass

@dataclass
class Team:
    name: str

@dataclass
class Score:
    goal_home: int
    goal_away: int
       
class Match:
    def __init__(self, team1: Team, team2: Team) -> None:
        self.team1 = team1
        self.team2 = team2
        
    def set_score(self, score: Score) -> None:
        self.score = score
        
    def get_score(self) -> Score:
        return self.score

class User:
    def __init__(self, username: str):
        self.username = username
        self.points = 0
    
    def place_bet(self, match: Match, score: Score):
        return Bet(self, match, score)
    
    def add_points(self, point):
        self.points += point
    
    def get_points(self):
        return self.points

class Bet:
    def __init__(self, user: User, match: Match, score: Score):
        self.match = match
        self.user = user
        self.score = score
        
    def validate_bet(self):
        sign = lambda a: True if a>0 else -1 if a<0 else False
        match_score = self.match.get_score()
        winner = match_score.goal_home - match_score.goal_away
        predicted_winner = self.score.goal_home - self.score.goal_away
        score_diff_home = abs(match_score.goal_home - self.score.goal_home)
        score_diff_away = abs(match_score.goal_away - self.score.goal_away)
        if sign(winner) and sign(predicted_winner):
            self.user.add_points(3)
            for i in range(3):
                if score_diff_home == i:
                    self.user.add_points(2-i)
                if score_diff_away == i:
                    self.user.add_points(2-i)

user1 = User('michal')
france = Team('France')
belgium = Team('Belgium')
match1 = Match(france, belgium)
bet1  = user1.place_bet(match1, Score(1,0))
match1.set_score(Score(1,0))
bet1.validate_bet()
print(user1.get_points())