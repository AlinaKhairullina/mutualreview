
import json

from datetime import datetime

from collections import Counter

def team_density(data, i, j, density_mutual): #Плотность вокруг каждой пары на промежутке [-3*m; 3*m]
    k = 0 #количество ревью за [-3*m; 3*m]

    
    for p, value in enumerate(data):
        if (value['timestamp'] - data[j]['timestamp']).total_seconds() > 3*m:
            break

        if ((value['timestamp'] - data[i]['timestamp']).total_seconds()/60 >= -3*m) and ((value['timestamp'] - data[j]['timestamp']).total_seconds()/60 <= 3*m):
            k += 1
    if k < len(programmers)/3:   #убираем из списка подозрительных ревью те, которые превышают пороговое значение (треть от количества программистов)
        density_mutual.append({'pair': (min(data[i]['reviewer'], data[j]['reviewer']), max(data[i]['reviewer'], data[j]['reviewer'])), 'density': round(k/m/6, 2), 'time': (data[i]['timestamp'], data[j]['timestamp']) }) #плотность проставленных оценок: количество ревью/6*m минут

    return density_mutual

def personal_density(data, i, j, density_pers):
    d1 = 0
    d2 = 0
    for k in data:

        if k['reviewer'] == data[i]['reviewer'] and abs(data[i]['timestamp'] - k['timestamp']).total_seconds()/60 <= (45/2):
            d1 += 1

        if k['reviewer'] == data[j]['reviewer'] and abs(data[j]['timestamp'] - k['timestamp']).total_seconds()/60 <= (45/2):
            d2 += 1

        if ( k['timestamp'] - data[j]['timestamp']).total_seconds()/60 > 45:
            break

    if not (d1 > 2 or d2 > 2): #будем считать что если reviewer сделал более 2 коммитов в течение 45 минут, то он идет последовательно

        density_pers.append({'pair': (min(data[i]['reviewer'], data[j]['reviewer']), max(data[i]['reviewer'], data[j]['reviewer'])), 'density': (d1, d2), 'time': (data[i]['timestamp'], data[j]['timestamp'])})

    return density_pers

def number_of_pairs(density):
    pairs_density = [] #все подозрительные пары, у которых плотность ниже порогового значения

    for i in density:
        pairs_density.append(i['pair'])
    return dict(Counter(pairs_density))

f = open("mutual_code_review_small.jsonl", "r")

data = [] #dataset

m = 10 #parametr

count = 0 

fast_mutual = [] #mutual suspicious reviews

density_mutual = [] #density of reviews on the interval [-3*m; 3*m], список из словарей 

density_pers = []

for i, line in enumerate(f):

    data.append(json.loads(line)) 
    print(i)

    d = datetime.strptime( data[i]['timestamp'], "%Y-%m-%d %H:%M:%S.000000000")

    data[i]['timestamp'] = d
    

data.sort(key = lambda time : time['timestamp']) #sort by time

used = []
programmers = []

for i, value in enumerate(data):

    if value['author'] not in programmers:
        programmers.append(value['author'])

    for j in range(i + 1, len(data)):

        if (data[j]['timestamp']- value['timestamp'] ).total_seconds() / 60 > m:

            break

        if (value.get('reviewer') == data[j].get('author')) and (value.get('author') == data[j].get('reviewer')):

            if (used != data[j]) :
                fast_mutual.append((value, data[j]))

                density_mutual = team_density(data, i, j, density_mutual) #сразу вычисляем плотность каждой пары 

                density_pers = personal_density(data, i, j, density_pers) #вычисляем плотность проставления ревью от каждого программиста

                used = data[j]

print("The number of suspicios_mutual_reviews:", len(fast_mutual))

pairs = []

for i in fast_mutual:
    pairs.append((min(i[0]['author'], i[0]['reviewer']), max(i[0]['author'], i[0]['reviewer'])))

elements = dict(Counter(pairs)) #statistics of pairs 

for  elem in elements:
    elements[elem] = round(elements[elem]%100/len((fast_mutual)), 3)

elements = sorted(elements.items(), key = lambda value: value[1])
print("Statistics of pairs: ") #print statistics of pairs
for i in elements:
    print(i[0], ": ", i[1], "%", sep = "")

density_mutual.sort(key = lambda den: den['density'])

pairs_team_den = sorted(number_of_pairs(density_mutual).items(), key = lambda den: den[1]) 

print("Team density:")
for i in density_mutual:
    print(i['pair'],":", i['density'])

print("The number of each suspicious team pairs:")
for i in pairs_team_den:
    print( i[0], ':', i[1])


density_pers.sort(key = lambda den : den['density'])

print("Personal density:")
for i in density_pers:
    print(i['pair'],":", i['density'])

pairs_personal_den = sorted(number_of_pairs(density_pers).items(), key = lambda num: num[1])

print("The number of each suspicious personal pairs:")

for i in pairs_personal_den:
    print(i[0], ':', i[1])

reviews = []
for i, v in enumerate(density_mutual):
    if i < 3:
        reviews.append(v)
    elif v['density'] != density_mutual[2]['density']:
        break
    else:
        while v['density'] == density_mutual[2]['density']:
            reviews.append(v)
            break

for i, v in enumerate(density_pers):

    if i < 3:
        if next(filter(lambda x: x['time'][0] == v['time'][0], reviews), 0) == 0 :
            reviews.append(v)

    elif v['density'] != density_pers[2]['density']:
        break

    else:
        while v['density'] == density_pers[2]['density']:
            if next(filter(lambda x: x['time'] == v['time'], reviews), 0) == 0 :
                reviews.append(v)   
            break


result = []

for i, v in enumerate(reversed(elements)):
    for j in reviews:
        if i < 3 and v[0] == j['pair']:
            result.append(j)


print("The most suspicious mutual reviews:")
tmp = 0
for i in result:
    for j in data:
        if i['time'][0] == j['timestamp']:
            if tmp%2 == 0 and tmp != 0:
                print("\n")
            tmp += 1
            print(j)
        if i['time'][1] == j['timestamp']:
            tmp += 1
            print(j, end= "")
print("\n")
