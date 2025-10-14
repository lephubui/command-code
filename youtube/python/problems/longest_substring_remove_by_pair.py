from string import ascii_lowercase
def solution(S, Q):
    # Store into hash map for each characters 
    precals = {}
    res = []
    for c1 in ascii_lowercase:
        for c2 in ascii_lowercase:
            if c1 == c2:
                continue
            max_run = 0
            counter = 0
            for char in S:
                if char != c1 and char != c2:
                    counter += 1
                    max_run = max(max_run, counter)
                else:
                    counter = 0
            precals[(c1, c2)] = max_run
    
    # Iterating through each pair and get max number of character
    for pair in Q:
        if pair in precals:
            res.append(precals[pair])
    
    return res
    
if __name__ == "__main__":
    S = "abcabcab"
    Q = [('a', 'b'), ('b', 'c'), ('a', 'c')]
    print(solution(S, Q))  # Output: [2, 2, 2]

    S = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    Q = [('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b'), ('a', 'b')]
    print(solution(S, Q))  # Output: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  
