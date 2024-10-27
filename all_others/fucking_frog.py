import sys

n = int(input())
ls = list(map(int, input().split()))
COPY = tuple(ls)

if n == 2:
    print(-1)
    sys.exit()

for i in range(n - 2):
    if i == 1:
        continue
    if i < 3:
        ls[i + 2] += ls[i]
    else:
        ls[i + 2] += ls[i] - ls[i - 1] if ls[i - 1] < ls[i] else 0
    if i < n - 3:
        ls[i + 3] += ls[i]
print(ls[-1])

reverse_path = [str(n)]
ind = n - 1
while ind != 0:
    if ls[ind - 2] == ls[ind] - COPY[ind] and ind != 3:
        reverse_path.append(str(ind - 1))
        ind -= 2
    elif ind != 4:
        reverse_path.append(str(ind - 2))
        ind -= 3
print(' '.join(reverse_path[::-1]))
