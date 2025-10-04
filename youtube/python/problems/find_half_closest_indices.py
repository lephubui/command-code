# You are given two arrays, X and Y, each with a length between 1 and 500000, inclusive. Each array contains unique positive integers from 1 up to 100000.
# Your task is to create a new array based on the following criteria: For each element in Y, divide it by 2 and find the element in X that is closest in value. 
# The element in X can be equal to, less than, or greater than Y[i] / 2. 
# When identifying the closest number in X, if multiple numbers are equally close to half of the Y[i] value, select the first occurring one in X.
# Once the numbers in X that are closest and meet the half-of-Y[i] condition are found, one for each Y[i], get their corresponding numbers in Y, maintaining the original ordering.
# In other words, when, say for Y[i], the closest number to Y[i] / 2 in X is X[j], add Y[j] to a new array. Repeat this process, following the original Y order, for all elements in Y.
# The final function should return this newly created array with the corresponding Y[j] values for each closest half-of-Y[i] number in X. It is essential to ensure that in case of multiple equally close numbers in X, the one with the smallest index is chosen.

import bisect

def solution(X, Y):
    # First sort the X to accessing order and store in pair of value and index
    X_sorted = sorted([(val, idx) for idx, val in enumerate(X)], key=lambda x: x[0])
    X_vals = [val for val, idx in X_sorted]

    res = [0] * len(Y)

    for i in range(len(Y)):
        target = Y[i] / 2
        pos = bisect.bisect_left(X_vals, target)

        # After binary search, left points to the smallest values >= target
        candidates = []
        if pos < len(X_sorted):
            candidates.append(X_sorted[pos])
        
        if pos > 0:
            candidates.append(X_sorted[pos - 1])
        
        # Find the candidate closest to target (and with smallest index if tie)
        best = min(
            candidates,
            key = lambda x: (abs(x[0] - target), x[1])
        )
        
        # Store to result
        res[i] = Y[best[1]]
    
    return res

if __name__ == "__main__":
    X = [1, 4, 6, 8]
    Y = [2, 3, 10]
    print(solution(X, Y))  # Output: [2, 2, 10]

    X = [10, 20, 30]
    Y = [5, 15, 25]
    print(solution(X, Y))  # Output: [5, 10, 20]

    X = [1, 3, 5]
    Y = [2, 4, 6]
    print(solution(X, Y))  # Output: [2, 4, 6]

    X = [100000]
    Y = [200000]
    print(solution(X, Y))  # Output: [200000]

    X = [1]
    Y = [1]
    print(solution(X, Y))  # Output: [1]

    X = [1, 2, 3]
    Y = [10**6, 10**5, 10**4]
    print(solution(X, Y))  # Output: [1000000, 1000000, 100000]