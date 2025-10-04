# Given an iterable of connections (pairs/tuples/lists) representing undirected links
# between people (IDs are positive integers in the range 1..1001).
# Each entry (a, b) means a and b are directly connected; (a,b) and (b,a) are equivalent
# and duplicates may appear.
#
# Task:
#   Identify the person who can reach the largest number of distinct people within
#   two degrees of connection (direct friends + friends-of-friends). Do not count
#   the person themself. If multiple people tie for the maximum reach, return the
#   smallest person ID (earliest).
#
# Notes:
#   - Input may contain lists or tuples for each connection.
#   - The algorithm builds an adjacency map, includes direct friends and their friends,
#     removes the person themself, and counts unique reachable nodes within two hops.
#   - Works for small graphs (IDs up to 1001 as specified).

def find_influencer(connections):
    friend_map = {}
    influencer = 0
    max_size = 0

    for elements in connections:
        friend_map.setdefault(elements[0], set()).add(elements[1])
        friend_map.setdefault(elements[1], set()).add(elements[0])
        
    # ensure valid start values: pick a real person and use max_size=-1 so ties of 0 are handled
    if not friend_map:
        return 0
    influencer = min(friend_map.keys())
    max_size = -1

    # For each person:
    #  - Build their friend_set (direct friends + friends-of-friends).
    #  - Remove the person themself from friend_set before counting its size.
    #  - If the size is greater than max_size, update both max_size and influencer.
    #  - If the size is equal to max_size, update influencer only if this person's id is smaller.
    for k, v in friend_map.items():
        # Start with direct friends
        friend_set = set(v)
        # Add friends-of-friends
        for friend in v:
            friend_set.update(friend_map[friend])
        # Remove the person themself before measuring
        friend_set.discard(k)
        
        friend_size = len(friend_set)
        if max_size < friend_size:
            max_size = friend_size
            influencer = k
        elif max_size == friend_size:
            if influencer > k:
                influencer = k

    return influencer

if __name__ == "__main__":
    connections = [
        [1, 2],
        [2, 3],
        [3, 4],
        [4, 5],
        [5, 6],
        [6, 1],
        [1, 3],
        [2, 4],
        [3, 5]
    ]
    print(find_influencer(connections))  # Output: 3

    connections = [
        [1, 2],
        [2, 3],
        [3, 4],
        [4, 5],
        [5, 6],
        [6, 1]
    ]
    print(find_influencer(connections))  # Output: 1

    connections = [
        [1, 2],
        [2, 3],
        [3, 4],
        [4, 5]
    ]
    print(find_influencer(connections))  # Output: 2

    connections = [
        [1, 2],
        [2, 3],
        [3, 1]
    ]
    print(find_influencer(connections))  # Output: 1

    connections = [
        [1, 2]
    ]
    print(find_influencer(connections))  # Output: 1

    connections = [(100, 200), (200, 300), (100, 300), (100, 400), (400, 500), (500, 600), (200, 600)]
    print(find_influencer(connections))  # Output: 100