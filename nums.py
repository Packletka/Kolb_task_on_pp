from functools import reduce


for num in range(1, 10001):
    if int(reduce(lambda x, y: x * y, list(int(_) for _ in str(num)))) == num:
        print(num)
