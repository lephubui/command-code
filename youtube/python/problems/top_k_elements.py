def topKFrequent(self, nums, k):
    """
    :type nums: List[int]
    :type k: int
    :rtype: List[int]
    """
    if k == len(nums):
        return nums

    # Use counter to build hash map
    # count = Counter(nums)
    map = {}

    for num in nums:
        if num not in map:
            map[num] = 1
        else:
            map[num] += 1
    
    # Sort by frequency (descending) and return top k elements
    sorted_items = sorted(map.items(), key=lambda x: x[1], reverse=True)
    
    # Extract the keys (numbers) of the top k frequent elements
    return [item[0] for item in sorted_items[:k]]

if __name__ == "__main__":
    # Test case 1: Original example
    nums = [1,1,1,2,2,3]
    k = 2
    result = topKFrequent(None, nums, k)
    print(f"Test 1 - nums: {nums}, k: {k}")
    print(f"Output: {result}")  # Expected: [1, 2]
    print()
    
    # Test case 2: Single element
    nums = [1]
    k = 1
    result = topKFrequent(None, nums, k)
    print(f"Test 2 - nums: {nums}, k: {k}")
    print(f"Output: {result}")  # Expected: [1]
    print()
    
    # Test case 3: All elements have same frequency
    nums = [1,2,3,4,5]
    k = 3
    result = topKFrequent(None, nums, k)
    print(f"Test 3 - nums: {nums}, k: {k}")
    print(f"Output: {result}")  # Expected: any 3 elements
    print()
    
    # Test case 4: k equals array length
    nums = [4,1,-1,2,-1,2,3]
    k = 4
    result = topKFrequent(None, nums, k)
    print(f"Test 4 - nums: {nums}, k: {k}")
    print(f"Output: {result}")  # Expected: all unique elements
    print()
    
    # Test case 5: Negative numbers
    nums = [-1,-1,2,2,2,3]
    k = 2
    result = topKFrequent(None, nums, k)
    print(f"Test 5 - nums: {nums}, k: {k}")
    print(f"Output: {result}")  # Expected: [2, -1]