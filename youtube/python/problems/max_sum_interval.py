
def solution(arr, queries):
    # Precals arr interval maximum
    n = len(arr)
    precalc = [[0]*n for _ in range(n)]
    res = []
    
    for l in range(n):
        curr_sum = 0
        max_val = float('-inf')
        for r in range(l, n):
            curr_sum += arr[r]
            max_val = max(curr_sum, max_val)
            precalc[l][r] = max_val
    
    print("Precalculated", precalc)
    for query in queries:
        res.append(precalc[query[0]][query[1]])

    return res

if __name__ == "__main__":
    arr = [2, -1, 4, -2, 3]
    queries = [(0, 2), (1, 4)]
    print(solution(arr, queries))  # Output: [5, 4]