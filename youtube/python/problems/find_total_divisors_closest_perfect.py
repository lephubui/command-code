import math

def solution(arr):
    res = []
    map_precals = {}
    for num in range(1, 101):
        sq = num*num
        map_precals[sq] = count_divisors(sq)

    for n in arr:
        closest_perfect_n = find_closest_perfect_square(n)
        res.append(map_precals[closest_perfect_n])
    
    return res

def find_closest_perfect_square(n):
    sqrt_n = math.sqrt(n)
    
    floor_sqrt_n = math.floor(sqrt_n)
    ceil_sqrt_n = math.ceil(sqrt_n)
    
    # Find the floor^2 and ceil^2
    floor_squared = floor_sqrt_n*floor_sqrt_n
    ceil_squared = ceil_sqrt_n*ceil_sqrt_n
    
    diff_floor = abs(n - floor_squared)
    diff_ceil = abs(n - ceil_squared)
    
    if diff_floor <= diff_ceil:
        return floor_squared
    else:
        return ceil_squared

def count_divisors(n) :
    cnt = 0
    for i in range(1, (int)(math.sqrt(n)) + 1) :
        if (n % i == 0) :
            
            # If divisors are equal,
            # count only one
            if (n / i == i) :
                cnt = cnt + 1
            else : # Otherwise count both
                cnt = cnt + 2
                
    return cnt