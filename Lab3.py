import itertools
from itertools import product
import math

# Потрібно ввести граф представлення зв'язків системи
graph = {'E1': {'E2', 'E3'},
         'E2': {'E4', 'E5'},
         'E3': {'E4', 'E6', 'E8'},
         'E4': {'E5', 'E6', 'E8'},
         'E5': {'E6', 'E7'},
         'E6': {'E7', 'E8'},
         'E7': {'E7'},
         'E8': {'E8'},
         }

# Потрібно ввести ймовірності безвідмовної роботи елементів системи
P_dict = {'E1': 0.50,
          'E2': 0.60,
          'E3': 0.70,
          'E4': 0.80,
          'E5': 0.85,
          'E6': 0.90,
          'E7': 0.92,
          'E8': 0.94,
          }

# Потрібно ввести початкову(початкові) та кінцеву(кінцеві) вершину для знаходження шляхів
sources = ['E1']  # початкові вершини
finishes = ['E7', 'E8']  # кінцеві вершини

def main():
    #------------Загальне резервування---------------
    mode = 'unloaded'  # ненавантажений режим роботи резерву
    K = 1              # кратність
    time = 1000        # час в годинах
    print("General ", mode, ":")
    general(mode, time, K)

    mode = 'loaded'  # навантажений режим роботи резерву
    K = 1            # кратність
    time = 1000      # час в годинах
    print("\nGeneral ", mode, ":")
    general(mode, time, K)
    # ------------Роздільне резервування-------------
    mode = 'unloaded'  # ненавантажений режим роботи резерву
    K = 1              # кратність
    time = 1000        # час в годинах
    print("\nDistributed ", mode, ":")
    distributed(mode, time, K)

    mode = 'loaded'  # навантажений режим роботи резерву
    K = 1            # кратність
    time = 1000      # час в годинах
    print("\nDistributed ", mode, ":")
    distributed(mode, time, K)


# Пошук в глибину
def dfs_paths(graph, start, goal):
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        for next in graph[vertex] - set(path):
            if next == goal:
                yield path + [next]
            else:
                stack.append((next, path + [next]))

def find_P_system(graph, P_dict, sources, finishes):

    sequence = list(P_dict.keys())
    state_table = []  # список можливих станів
    for i in range(1, len(sequence) + 1):
        state_table += list(itertools.combinations(sequence, i))

    if len(graph) == 0:
        print("P_system = 0")
    elif len(graph) == 1:
        key = list(P_dict.keys())[0]
        print("P_system = ", + P_dict[key])
    else:
        uniq_comb = list(product(sources, finishes))

        all_paths = []  # список усіх знайдених шляхів
        for pair in uniq_comb:
            for j in list(dfs_paths(graph, pair[0], pair[1])):
                all_paths.append(j)

        duplic = []
        for state in state_table:
            for path in all_paths:
                if set(path).issubset(state):
                    duplic.append(list(state))
        duplic.sort()
        no_duplic = list(duplic for duplic,_ in itertools.groupby(duplic))
        P_states = []

        for elem_list in no_duplic:     # працездатні стани системи
            dif = set(sequence) - set(elem_list)
            p_state = 1
            for i in elem_list:
                p_state *= P_dict[i]
            for j in dif:
                p_state *= (1 - P_dict[j])
            P_states.append(p_state)
        P_system = sum(P_states)    # ймовірність безвідмовної роботи системи
        # print('P_system =',round(P_system, 6))
        return round(P_system, 6)

def general(mode, time, K):
    P_system = find_P_system(graph, P_dict, sources, finishes)
    print("P_system = ", P_system)
    Q_system = 1 - P_system
    print("Q_system = ", Q_system)
    P_reserved_system = 0
    Q_reserved_system = 0
    if mode == "unloaded":
        Q_reserved_system = (1 / math.factorial(K + 1)) * Q_system
        print("Q_reserved_system = ", Q_reserved_system)
        P_reserved_system = 1 - Q_reserved_system
        print("P_reserved_system = ", P_reserved_system)
    if mode == "loaded":
        total = 1
        for i in P_dict:
            total = total * P_dict[i]
        P_reserved_system = 1 - pow(1 - total, K+1)
        print("P_reserved_system = ", P_reserved_system)
        Q_reserved_system = 1 - P_reserved_system
        print("Q_reserved_system = ", Q_reserved_system)
    T_system = round((- time) / math.log(P_system))
    print("T_system = ", T_system)
    T_reserved_system = round((- time) / math.log(P_reserved_system))
    print("T_reserved_system = ", T_reserved_system)
    G_q = Q_reserved_system / Q_system
    print("G_q = ", round(G_q, 2))
    G_p = P_reserved_system / P_system
    print("G_p = ", round(G_p, 2))
    G_t = T_reserved_system / T_system
    print("G_t = ", round(G_t, 2))
    return

def distributed(mode, time, K):
    Q_reserved_i = {}
    P_reserved_i = {}
    if mode == "loaded":
        for k in P_dict.keys():
            Q_reserved_i[k] = pow(1 - P_dict[k], K+1)
            P_reserved_i[k] = 1 - Q_reserved_i[k]
    if mode == "unloaded":
        for k in P_dict.keys():
            Q_reserved_i[k] = (1 / math.factorial(K + 1)) * (1 - P_dict[k])
            P_reserved_i[k] = 1 - Q_reserved_i[k]
    P_system = find_P_system(graph, P_dict, sources, finishes)
    print("P_system = ", P_system)
    Q_system = 1 - P_system
    print("Q_system = ", Q_system)
    T_system = round((- time) / math.log(P_system))
    print("T_system = ", T_system)
    P_reserved_system = find_P_system(graph, P_reserved_i, sources, finishes)
    print("P_reserved_system = ", P_reserved_system)
    Q_reserved_system = 1 - P_reserved_system
    print("Q_reserved_system = ", Q_reserved_system)
    T_reserved_system = round((- time) / math.log(P_reserved_system))
    print("T_reserved_system = ", T_reserved_system)
    G_q = Q_reserved_system / Q_system
    print("G_q = ", round(G_q, 2))
    G_p = P_reserved_system / P_system
    print("G_p = ", round(G_p, 2))
    G_t = T_reserved_system / T_system
    print("G_t = ", round(G_t, 2))
    return

main()












