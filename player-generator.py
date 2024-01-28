import random, math

class Player:
    """
    Level,Profession,Sword,Shield,Magic_Level,Average_Weekly_Time_Minutes,Gold_Spent
    8,Wizard,21,22,9,54,18239
    12,Knight,31,25,3,72,89012
    """

    def __init__(self):
        self.randomize()

    def randomize(self):
        # Profile of our player will be based on the level and profession.
        # These are the first values we will roll.
        self.level = random.randint(1, 500)
        self.profession = random.choice(['Wizard', 'Knight', 'Rogue', 'Cleric'])
        self.randomize_skills()
        self.randomize_gold_time()

    def randomize_skills(self):
        """
        Randomizes skills based on class and level. It should be somehow
        correlated.
        """
        if self.profession == 'Wizard' or self.profession == 'Cleric':
            mean_sword_shield = int(10 + self.level * 1.3)
            mean_magic = int(5 + self.level * 2.8)
            self.sword = random.randint(mean_sword_shield - 3, mean_sword_shield + 3)
            self.shield = random.randint(mean_sword_shield - 3, mean_sword_shield + 3)
            self.magic_level = random.randint(mean_magic - 2, mean_magic + 3)
        elif self.profession == 'Knight':
            mean_sword_shield = int(10 + self.level * 2.8)
            mean_magic = int(2 + self.level * 1.1)
            self.sword = random.randint(mean_sword_shield - 3, mean_sword_shield + 3)
            self.shield = random.randint(mean_sword_shield - 3, mean_sword_shield + 3)
            self.magic_level = random.randint(mean_magic - 1, mean_magic + 2)
        elif self.profession == 'Rogue':
            mean_sword = int(10 + self.level * 1.4)
            mean_magic = int(2 + self.level * 1.8)
            mean_shield = int(10 + self.level * 2.2)
            self.sword = random.randint(mean_sword - 3, mean_sword + 3)
            self.shield = random.randint(mean_shield - 3, mean_shield + 3)
            self.magic_level = random.randint(mean_magic - 1, mean_magic + 2)

    def randomize_gold_time(self):
        """
        Randomizes time and gold spent based on level.
        This should be somewhat lightly-exponential.
        """
        mean_time = int(30 * math.exp(self.level/115))
        mean_gold = int(4200 * math.exp( (self.level - 20) / 70) )
        self.average_weekly_time_minutes = random.randint(mean_time - 15, mean_time + 50)
        self.gold_spent = random.randint(mean_gold - 100, mean_gold + 100)


def generate_players(n):
    """
    Generates n players and returns them as a list
    """
    players = []
    for i in range(n):
        players.append(Player())
    return players

def create_export_players(csv_file):
    """
    Exports players to a csv file
    """
    players = generate_players(50000)
    with open(csv_file, 'w') as f:
        f.write('Level,Profession,Sword,Shield,Magic_Level,Average_Weekly_Time_Minutes,Gold_Spent\n')
        for player in players:
            f.write('{},{},{},{},{},{},{}\n'.format(player.level, player.profession, player.sword, player.shield, player.magic_level, player.average_weekly_time_minutes, player.gold_spent))

if __name__ == '__main__':
    create_export_players('players.csv')