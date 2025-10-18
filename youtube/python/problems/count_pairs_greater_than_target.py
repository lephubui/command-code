def count_pairs_greater_than_target(arr, target):
    sorted_arr = sorted(arr)
    n = len(sorted_arr)
    counter = 0
    j = 0
    for i in range(n):
        print(f"i loop start: {i}, j start: {j}")
        while j < n and sorted_arr[j] - sorted_arr[i] <= target:
            j += 1
        print(f"i: {i}, j end: {j}")        
        counter += n - j
        print("-----")    
    return counter

if __name__ == "__main__":
    # Test case 1: Original example
    arr = [-20, -10, 0, 10, 20]
    target = 10
    result = count_pairs_greater_than_target(arr, target)
    print(f"Test 1 - arr: {arr}, target: {target}")
    # print(f"Output: {result}")  # Expected: 5
    # print()
    
    # Test case 2: No pairs greater than target
    # arr = [1, 2, 3, 4, 5]
    # target = 10
    # result = count_pairs_greater_than_target(arr, target)
    # print(f"Test 2 - arr: {arr}, target: {target}")
    # print(f"Output: {result}")  # Expected: 0
    # print()
    
    # # Test case 3: All pairs greater than target
    # arr = [20, 30, 40]
    # target = 10
    # result = count_pairs_greater_than_target(arr, target)
    # print(f"Test 3 - arr: {arr}, target: {target}")
    # print(f"Output: {result}")  # Expected: 3
    # print()
    
    # # Test case 4: Mixed values
    # arr = [5, 15, 25, 35]
    # target = 10
    # result = count_pairs_greater_than_target(arr, target)
    # print(f"Test 4 - arr: {arr}, target: {target}")
    # print(f"Output: {result}")  # Expected: 6
    # print()
    
    # # Test case 5: Negative and positive values
    # arr = [-5, 0, 5, 15, 25]
    # target = 10
    # result = count_pairs_greater_than_target(arr, target)
    # print(f"Test 5 - arr: {arr}, target: {target}")
    # print(f"Output: {result}")  # Expected: 6
    # print()