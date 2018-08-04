import pandas as pd

def convert_score_to_rating(score, ab, db):
    return db[0] + (score - ab[0]) * (db[1] - db[0]) / (ab[1] - ab[0])

def round_number(n):
    return round(n)

df = pd.read_csv('input/ratingFromGoogle.csv', index_col=0)

### Convert score to specific range [1,5] of rating
actual_bounds = [min(df['score']), max(df['score'])]
desired_bounds = [1.0, 5.0]
print(actual_bounds)
df['autoRating'] = df['score'].apply(lambda x: convert_score_to_rating(x, actual_bounds, desired_bounds))
df['autoRating'] = df['autoRating'].apply(round_number)

print(df.head())

### Set index name
df.index.name = 'id'

df.to_csv('input/2_convertScoreToRating.csv')