
import numpy as np
import pandas as pd


def compute_table(A):
    B = A.copy()
    B['min'] = B.min(1)
    B['max'] = B.max(1)

    return B


def min_max_cost(A):
    s_max = A.max(1)
    s = s_max[s_max==s_max.min()].index[0]
    v = s_max[s_max==s_max.min()][0]
    print(f'Strategy:{s} \nValue:{v}')

    return s, v

def min_min_cost(A):
    s_min = A.min(1)
    s = s_min[s_min==s_min.min()].index[0]
    v = s_min[s_min==s_min.min()][0]
    print(f'Strategy:{s} \nValue:{v}')

    return s, v


def max_max_gain(A):
    s_max = A.max(1)
    s = s_max[s_max==s_max.max()].index[0]
    v = s_max[s_max==s_max.max()][0]
    print(f'Strategy:{s} \nValue:{v}')

    return s, v

def max_min_gain(A):
    s_min = A.min(1)
    s = s_min[s_min==s_min.max()].index[0]
    v = s_min[s_min==s_min.max()][0]
    print(f'Strategy:{s} \nValue:{v}')

    return s, v


def max_mim(A):
    s_min = A.min(1)
    s = s_min[s_min==s_min.max()].index[0]
    v = s_min[s_min==s_min.max()][0]
    print(f'Strategy:{s} \nValue:{v}')

    return s, v

def laplace(A, gain=True):
    s_weighted = A.mean(1)
    if gain:
        s = s_weighted[s_weighted==s_weighted.max()].index[0]
        v = s_weighted[s_weighted==s_weighted.max()][0]
    else:
        s = s_weighted[s_weighted==s_weighted.min()].index[0]
        v = s_weighted[s_weighted==s_weighted.min()][0]
    print(f'Strategy:{s} \nValue:{v}')

    return s, v

def hurwicz(A, alpha, gain=True):
    B = compute_table(A)
    s_hwz = alpha*B['max']+(1-alpha)*B['min']
    if gain:
        s = s_hwz[s_hwz==s_hwz.max()].index[0]
        v = s_hwz[s_hwz==s_hwz.max()][0]
    else:
        s = s_hwz[s_hwz==s_hwz.min()].index[0]
        v = s_hwz[s_hwz==s_hwz.min()][0]
    B['hwz'] = s_hwz
    print(f'Matrix:\n{B}')
    print(f'\nStrategy:{s} \nValue:{v}')

    return s, v

def savage_regret(A, gain=True):

    B = A.copy()

    if gain==False:
        B = -1 * B 
        #print(B)

    s_max = B.max(0)
    R = -1 * (B.add(-s_max, axis=1))
    r_max = R.max(1)
    R['maxR'] = r_max

    s = r_max[r_max==r_max.min()].index[0]
    v = r_max[r_max==r_max.min()][0]
        
    print(f'Regret Matrix:\n{R}')
    print(f'\nStrategy:{s} \nValue:{v}')

    return s, v



def dominance(A, gain=True):
    B = A.T

    n_strategies = len(A)

    wins = []
    scores = []
    ranks = []
    for i in B:
        rounds = []
        score = []
        for j in B:
            if i != j:
                diff = B[i]-B[j]

                pivot = np.where(diff.values == 0, 0, 1)
                draws = 5-np.sum(pivot)

                if gain:
                    points = np.where(diff.values > 0, 1, 0)
                else:
                    points = np.where(diff.values < 0, 1, 0)

                rounds.append(np.sum(points*pivot))
                score.append(np.sum((points*pivot)/(n_strategies-draws)))
        wins.append(rounds)
        scores.append(score)

    #print(np.array(wins))
    #print(np.array(scores))

    dominances = np.where(np.array(scores)>0.5, 1, 0)

    summary = pd.DataFrame(dominances, index = A.index)
    summary['wins'] = summary.sum(1)

    v_max = summary['wins'].max()
    s = summary['wins'][summary['wins']==v_max].index[0]
    v = summary['wins'][summary['wins']==v_max][0]
    #print(summary)
    print(f'Strategy:{s} \nValue:{v}')

    return s, v




