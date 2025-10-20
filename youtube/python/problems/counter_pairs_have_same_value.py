# Problem: Given an array of integers, count the number of pairs (i, j) such that arr[i] == arr[j] and i < j.
# Example: For the array [1, 2, 3, 1, 1, 3], the pairs are (0,3), (0,4), and (3,4) for the number 1, and (2,5) for the number 3. Thus, the output should be 4.
# Constraints: The array length can be up to 10^5, and the integers can range from -10^9 to 10^9.
def count_pairs_have_same_value(arr):
    map_arr = {}
    
    for num in arr:
        if num in map_arr:
            map_arr[num] += 1
        else:
            map_arr[num] = 1
            
    counter = 0
    for key in map_arr:
        n = map_arr[key]
        counter += n * (n - 1) // 2
    
    return counter

if __name__ == "__main__":
    # Test case 1: Original example
    arr = [1, 2, 3, 1, 1, 3]
    result = solution(arr)
    print(f"Test 1 - arr: {arr}")
    print(f"Output: {result}")  # Expected: 4
    print()
    
    # Test case 2: No pairs
    arr = [1, 2, 3, 4]
    result = solution(arr)
    print(f"Test 2 - arr: {arr}")
    print(f"Output: {result}")  # Expected: 0
    print()
    
    # Test case 3: All elements same
    arr = [5, 5, 5, 5]
    result = solution(arr)
    print(f"Test 3 - arr: {arr}")
    print(f"Output: {result}")  # Expected: 6
    print()
    
    # Test case 4: Mixed elements
    arr = [-29, 91, 92, 40, 71, 89, -75, 61, 68, -27, -73, -95, 19, 3, 63, 79, 76, -18, 22, -38, -86, -44, -56, -67, 77, 64, -84, 71, 62, 21, 68, -80, 66, -6, 81, 92, 14, 13, -2, 72, 7, 60, 15, 9, -66, 55, 16, -37, 50, 1, -31, 8, 17, 84, 6, 55, 64, -45, 4, -2, 14, 59, -68, 27, 93, -3, -12, -71, 45, -6, -36, 92, -26, 44, 44, 30, 45, -48, -62, 63, -1, 92, -30, -91, -44, -73, 6, 28, -75, 67, -6, 34, 33, 56, 44, -70, -18, -68, -96, 76]
    result = solution(arr)
    print(f"Test 4 - arr: {arr}")
    print(f"Output: {result}")  # Expected: 27
    print()
    
    # Test case 5: Single element
    arr = [42]
    result = solution(arr)
    print(f"Test 5 - arr: {arr}")
    print(f"Output: {result}")  # Expected: 0
    print()