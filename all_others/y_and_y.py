'''
Неправильно!
'''

n = int(input())
days = [int(input()) for _ in range(n)]
all_coupons = 0
dc = {}
count_big_nums = len(list(filter(lambda x: x > 100, days)))

for i in range(count_big_nums + 1):
    dc[i] = []
removed = []

for num in days:
    dc[all_coupons].append(num)
    if num > 100:
        all_coupons += 1

for key in dc:
    if key and dc[key] != []:
        removed += [key + len(list(a for b in list(dc.values())[:key] for a in b)) + dc[key].index(max(dc[key]))]
        dc[key].remove(max(dc[key]))

print(sum(a for b in dc.values() for a in b))
print(0, all_coupons) if n == 0 or days[-1] < 101 else print(1, all_coupons - 1)
[print(ind) for ind in removed]
