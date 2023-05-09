import requests

world = eval(requests.get('https://universalis.app/api/v2/worlds').text)

server = eval(requests.get('https://universalis.app/api/v2/data-centers').text)

list = []
gs = []
china = []
for s in server:
    list.append(s['region'])
    ss = [s['name']]
    for n in s['worlds']:
        for w in world:
            if w['id'] == n:
                ss.append(w['name'])
    list.append(ss)
print(list)
