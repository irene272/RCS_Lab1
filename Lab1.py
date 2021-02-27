y = 0.84
hours = 2748    # для ймовірності безвідмовної роботи
lambda_hours = 2308  # для інтенсивності відмов


# Вхідна вибірка наробітків до відмови(у годинах)
t = [647, 1948, 1204, 1757, 16, 0, 2279, 353,
    450, 660, 950, 1210, 114, 1017, 1595, 370,
    32, 1725, 327, 209, 121, 1427, 1324, 293,
    602, 606, 1057, 1586, 393, 2835, 12, 866,
    353, 55, 47, 1586, 149, 604, 586, 671, 726,
    1024, 224, 998, 99, 300, 781, 232, 239, 312,
    47, 312, 1813, 257, 1602, 2422, 247, 240,
    2255, 28, 694, 1657, 102, 353, 3195, 141,
    1980, 143, 440, 1974, 472, 169, 358, 1207,
    824, 30, 39, 2167, 1761, 696, 1384, 1656,
    73, 184, 224, 873, 1117, 2667, 107, 2278,
    246, 484, 1408, 1873, 1864, 1399, 331,
    1764, 326, 12]


int_amount = 10         # Кількість інтервалів

sort_t = sorted(t)

N = len(sort_t)         # Кількість об'єктів вибірки

try:
    T_aver = sum(t)/N    # Знайдемо середній наробіток T_cp
    print("Середній наробіток: " + "\n" + "T_cp = " + str(T_aver) + "\n")
except ZeroDivisionError:
    print("Division by zero")

max_t = max(t)
try:
    h = max_t / int_amount   # Розмах вибірки h
except ZeroDivisionError:
    print("ZerroDevision error.")  


amount_in_int =[[] for i in range(int_amount)]
interv = [round(i*h, 1) for i in range(int_amount+1)]

def find_int():
    try:
        for i in range(len(interv)):
            for j in sort_t:
                if interv[i] <= j <= interv[i+1]:
                    amount_in_int[i].append(j)
    except IndexError:
         pass
find_int()

N_i = [len(i) for i in amount_in_int]   # Значення, що потрапили в інтервал N_i

f = [round( (j / (N * h) ), 6) for j in N_i] # Густина відносних частот f


rec = lambda num_list :0 if len(num_list) == 0 else num_list[0] + rec(num_list[1:])

S = [rec(f[:(i+1)])*h for i in range(len(f))]

p_0 = 1
p_t = [round((1 - i), 6) for i in S]
p_t.insert(0, p_0)

d_int = lambda pt_i_1, pt_i : round((pt_i_1 - y)/(pt_i_1 - pt_i), 2)  # d для різних інтервалів

d = d_int(p_t[0], p_t[1])       # Візьмемо d(0, 1)
P_t = [round((1 - i), 6) for i in S]

find_T_y = lambda h, d : round(h*d, 2)

T_y = find_T_y(h, d)            # Знайдемо γ-відсотковий наробіток на відмову T_y

print("γ-відсотковий наробіток на відмову при γ = " +
      str(y)  + ":"  +"\n" "T_y = " + str(T_y)  + "\n")

def find_int(hours, int_list):
    temp = []

    for i in range(len(interv)):
        if hours <= interv[i]:
            temp.append(i)
    return (temp[0] - 1)

# Знайдемо ймовірність безвідмовної роботи на заданий час годин p_t

f_int = find_int(hours, interv)
ss = rec(f[:f_int])*h + (hours - interv[f_int]) * f[f_int]
p = 1 - ss

find_p_t = lambda f_int, ss, p : round(p, 6)
print("Ймовірність безвідмовної роботи на заданий час " + str(hours) + "годин: "
      + "\n" +  "P(" + str(hours) + ") = " + str(find_p_t(f_int, ss, p)) + "\n")

# Знайдемо інтенсивність відмов на заданий час годин lambda

f_int2 = find_int(lambda_hours, interv)
fi = f[f_int]
p_t = find_p_t(f_int2, ss, p)
find_lambda = lambda f_int2, fi, p_t: round(fi/p_t, 6)

print("Інтенсивність відмов на заданий час " + str(lambda_hours) + "годин: " + "\n" +
      "lambda(" + str(lambda_hours) + ") = " + str(find_lambda(f_int2, fi, p_t)) + "\n")
