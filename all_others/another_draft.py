# A, B, C, D = [int(input()) for i in range(4)]
# # Синие
# blue_sum = B + D + 2 if (A != 0) & (C != 0) else 0
#
# # Красные
# red_sum = A + C + 2 if (B != 0) & (D != 0) else 0
#
# if (not red_sum) | (bool(blue_sum) & (blue_sum <= red_sum)):
#     print(B + 1, D + 1)
# elif bool(red_sum):
#     print(A + 1, C + 1)

print(list(map(int, input().split())))
