from itertools import permutations

def distance(point_1, point_2):
    return ((point_2[0] - point_1[0]) ** 2 + (point_2[1] - point_1[1]) ** 2) ** 0.5

def point_str(point, num=0, symbol='->'):
    return f"{point}[{num}] {symbol} "


start = (0,2)
points_list = [(2,5), (5,2), (6,6), (8,3)]
size = len(points_list) + 2
result_list = []

for route in permutations(points_list):
    l = [start, *route, start]
    distance_sum, temp = 0, point_str(start)
    for i in range(1, size):
        distance_sum += distance(l[i-1], l[i])
        temp += point_str(l[i], distance_sum) if i != size - 1 else (point_str(l[i], distance_sum, '=') + str(distance_sum))
    result_list.append((distance_sum, temp))

print(sorted(result_list)[0][1])