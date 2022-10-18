import numpy as np
import pandas as pd


def cosine_similarity(user, current):
    
    user = set(user.split())
    current = set(str(current).split())
    
    vector = user.union(current)
    
    v1, v2 = [], []
    
    for i in vector:
        if i in user: v1.append(1)
        else: v1.append(0)
        
        if i in current: v2.append(1)
        else: v2.append(0)
    
    v1 = np.array(v1)
    v2 = np.array(v2)
    n = np.dot(v1, v2)
    d1 = np.linalg.norm(v1)
    d2 = np.linalg.norm(v2)
    d = d1*d2
    if d==0: return 0
    cosine = (n*(10**5))/d
    return cosine


def find_similar_repos(user, data):
    repos = {}
    for i in range(len(data)):
        s = data.iloc[i]
        current = s["combined"]
        res = cosine_similarity(user, current)
        repos[res] = [s["Repository Name"], s["Url"], s["Description"], s["Language"], s["Number of Stars"]]

    keys = list(repos.keys())
    keys = sorted(keys, reverse=True)
    res = {}
    for i in keys: res[i] = repos[i]
    return res

def recommender_sys(user_skills):

    data = pd.read_csv("augmented_data.csv")

    repos = find_similar_repos(user_skills, data)

    #for i in repos: print(repos[i])

    return repos
