import itertools
from itertools import product
# Ймовірності безвідмовної роботи елементів системи
P_dict = {'E1': 0.88,
          'E2': 0.42,
          'E3': 0.05,
          'E4': 0.62,
          'E5': 0.44,
          'E6': 0.13,
          'E7': 0.22,
          'E8': 0.63,
          'E9': 0.27
          }
sequence = list(P_dict.keys())
state_table = []        # список можливих станів
for i in range(1,len(sequence)+1):
    state_table += list(itertools.combinations(sequence, i))
#print(state_table)

# граф представлення зв'язків системи
graph = { 'E1': {'E3', 'E4'},
          'E2': {'E3', 'E5'},
          'E3': {'E4', 'E5'},
          'E4': {'E7', 'E8'},
          'E5': {'E6'},
          'E6': {'E7', 'E9'},
          'E7': {'E8', 'E9'},
          'E8': {'E8'},
          'E9': {'E9'}
        }

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


if len(graph) == 0:
    print("P_system = 0")
elif len(graph) == 1:
    key = list(P_dict.keys())[0]
    print("P_system = ", + P_dict[key])
else:
    sources = ['E1', 'E2']  # введіть початкові вершини
    finishes = ['E8', 'E9'] # введіть кінцеві вершини

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
    #print(state_table)
    #print(all_paths)
    duplic.sort()
    no_duplic = list(duplic for duplic,_ in itertools.groupby(duplic))
    #print(len(no_duplic))
    P_states = []

    for elem_list in no_duplic:     # працездатні стани системи
        dif = set(sequence) - set(elem_list)
        p_state = 1
        for i in elem_list:
            p_state *= P_dict[i]
        for j in dif:
            p_state *= (1 - P_dict[j])
        P_states.append(p_state)
    # print(P_states)
    P_system = sum(P_states)    # ймовірність безвідмовної роботи системи
    print('P_system =',round(P_system, 6))



