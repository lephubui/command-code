# Implementation of a min-heap data structure in Python
import heapq

class MinHeap:
    def __init__(self):
        self.heap = []

    def insert(self, val):
        """Insert a new value into the heap."""
        heapq.heappush(self.heap, val)

    def extract_min(self):
        """Extract the minimum value from the heap."""
        if not self.heap:
            return None
        return heapq.heappop(self.heap)
    
    def get_min(self):
        """Get the minimum value without removing it from the heap."""
        if not self.heap:
            return None
        return self.heap[0]
    
    def size(self):
        """Return the size of the heap."""
        return len(self.heap)
    
    def is_empty(self):
        """Check if the heap is empty."""
        return len(self.heap) == 0

if __name__ == "__main__":
    min_heap = MinHeap()
    min_heap.insert(5)
    min_heap.insert(3)
    min_heap.insert(8)
    print("Min value:", min_heap.get_min())  # Output: Min value: 3
    print("Extracted min:", min_heap.extract_min())  # Output: Extracted min: 3
    print("New min value:", min_heap.get_min())  # Output: New min value: 5
    print("Heap size:", min_heap.size())  # Output: Heap size: 2