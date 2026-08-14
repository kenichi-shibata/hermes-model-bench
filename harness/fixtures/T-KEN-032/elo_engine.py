def update(winner, loser, ratings):
    ratings[winner] = ratings.get(winner, 1500) + 32
    ratings[loser] = ratings.get(loser, 1500) - 32
    return ratings
