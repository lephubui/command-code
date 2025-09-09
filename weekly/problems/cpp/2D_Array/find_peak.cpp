/* Write a function that, given a 2D grid of integers representing altitudes of a mountain terrain,
 * and a starting cell (row, col) representing the base of a hike, returns the altitude of the highest peak
 * reachable from that cell by moving only to adjacent cells (North, East, South, West) with strictly higher altitudes.
 * If no higher altitude is reachable, return the altitude of the starting cell.
 */

#include <iostream>
#include <vector>

// Function to find the peak altitude reachable from a starting cell in the grid
int find_peak(std::vector<std::vector<int>> &grid, int start_row, int start_col) {
    int rows = grid.size();
    int cols = grid[0].size();
    int altitude = grid[start_row][start_col];
    // Check North, East, South, West for higher altitude
    std::vector<std::pair<int, int>> directions = {{-1, 0}, {0, 1}, {1, 0}, {0, -1}};
    for (auto &dir : directions) {
        int r = start_row + dir.first;
        int c = start_col + dir.second;
        if (r >= 0 && r < rows && c >= 0 && c < cols && grid[r][c] > altitude) {
            int peak = find_peak(grid, r, c);
            altitude = std::max( altitude,peak);
        }
    }
    return altitude;
}

int main() {
    // Example mountain terrain grid
    std::vector<std::vector<int>> mountain = {
        {1, 2, 3},
        {2, 5, 7},
        {4, 6, 9}
    };

    // Starting at the base (0, 1) representing the beginning of the hike
    std::cout << find_peak(mountain, 0, 1);  // Should print the altitude of the highest peak reachable
    return 0;
}