types = dict({"": 0,
              "Normal": 1,
              "Fighting": 2,
              "Flying": 3,
              "Poison": 4,
              "Ground": 5,
              "Rock": 6,
              "Bug": 7,
              "Ghost": 8,
              "Steel": 9,
              "Fire": 10,
              "Water": 11,
              "Grass": 12,
              "Electric": 13,
              "Psychic": 14,
              "Ice": 15,
              "Dragon": 16,
              "Dark": 17,
              "Fairy": 18})
#Rows = Attacking type, Columns = Defending type
typeAdvantage = [
#   ??? Normal Fighting Flying Poison Ground Rock Bug Ghost Steel Fire Water Grass Electric Psychic Ice Dragon Dark Fairy
#???
    [1,    1,      1,      1,     1,     1,    1,   1,   1,    1,    1,   1,    1,      1,      1,    1,   1,    1,    1],
#Normal
    [1,    1,      1,      1,     1,     1,    .5,  1,   0,    .5,   1,   1,    1,      1,      1,    1,   1,    1,    1],
#Fighting
    [1,    2,      1,      .5,    .5,    1,    2,   .5,  0,    2,    1,   1,    1,      1,      .5,   2,   1,    2,    .5],
#Flying
    [1,    1,      2,      1,     1,     1,    .5,  2,   1,    .5,   1,   1,    2,      .5,     1,    1,   1,    1,    1],
#Poison
    [1,    1,      1,      1,     .5,    .5,   .5,  1,   .5,   0,    1,   1,    2,      1,      1,    1,   1,    1,    2],
#Ground
    [1,    1,      1,      0,     2,     1,    2,   .5,  1,    2,    2,   1,    .5,     2,      1,    1,   1,    1,    1],
#Rock
    [1,    1,      .5,     2,     1,     .5,   1,   2,   1,    .5,   2,   1,    1,      1,      1,    2,   1,    1,    1],
#Bug
    [1,    1,      .5,     .5,    .5,    1,    1,   1,   .5,   .5,   .5,  1,    2,      1,      2,    1,   1,    2,    .5],
#Ghost
    [1,    0,      1,      1,     1,     1,    1,   1,   2,    1,    1,   1,    1,      1,      2,    1,   1,    .5,    1],
#Steel
    [1,    1,      1,      1,     1,     1,    2,   1,   1,    .5,   .5,  .5,   1,      .5,     1,    2,   1,    1,    2],
#Fire
    [1,    1,      1,      1,     1,     1,    .5,  2,   1,    2,    .5,  .5,   2,      1,      1,    2,   .5,   1,    1],
#Water
    [1,    1,      1,      1,     1,     2,    2,   1,   1,    1,    2,   .5,   .5,     1,      1,    1,   .5,   1,    1],
#Grass
    [1,    1,      1,      .5,    .5,    2,    2,   .5,  1,    .5,   .5,  2,    .5,     1,      1,    1,   .5,   1,    1],
#Electric
    [1,    1,      1,      2,     1,     0,    1,   1,   1,    1,    1,   2,    .5,     .5,     1,    1,   .5,   1,    1],
#Psychic
    [1,    1,      2,      1,     2,     1,    1,   1,   1,    .5,   1,   1,    1,      1,      .5,   1,   1,    0,    1],
#Ice
    [1,    1,      1,      2,     1,     2,    1,   1,   1,    .5,   .5,  .5,   2,      1,      1,    .5,  2,    1,    1],
#Dragon
    [1,    1,      1,      1,     1,     1,    1,   1,   1,    .5,   1,   1,    1,      1,      1,    1,   2,    1,    0],
#Dark
    [1,    1,      .5,     1,     1,     1,    1,   1,   2,    1,    1,   1,    1,      1,      2,    1,   1,    .5,   .5],
#Fairy   
    [1,    1,      2,      1,     .5,    1,    1,   1,   1,    .5,   .5,  1,    1,      1,      1,    1,   2,    2,    1]
]


def TypeAdvantage(typea1, typea2, typeb1, typeb2):
    t1 = types[typea1 if typea1 == typea1 else '']
    t2 = types[typea2 if typea2 == typea2 else '']
    t3 = types[typeb1 if typeb1 == typeb1 else '']
    t4 = types[typeb2 if typeb2 == typeb2 else '']
    return typeAdvantage[t1][t3] * typeAdvantage[t2][t3] * typeAdvantage[t1][t4] * typeAdvantage[t2][t4]
	