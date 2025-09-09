/*
Find the next uphill point in a 2D grid.
Given a 2D grid representing a hiking trail, and a starting position (row, column),
write a function to find the next uphill point from the current position.
An uphill point is defined as a point that has a higher value than the current point.
If there are multiple uphill points, return the one with the highest value.
If there are no uphill points, return -1.

*/
#include <iostream>
#include <vector>

using namespace std;

int find_next_uphill(const vector<vector<int>>& grid, pair<int, int> position) {
    int row = position.first;
    int col = position.second;
    vector<pair<int, int>> directions = {
        {-1, 0}, // Up
        {1, 0}, // Down
        {0, -1}, // Left
        {0, 1},  // Right
        {-1, -1}, // Top left Diagonally
        {-1, 1}, // Top right diagnoally
        {1, -1}, // Bottom left diagonally
        {1, 1}  // Bottom right diagonally
    };
    int next_val = grid[row][col];
    for (const auto& dir : directions) {
        int new_r = row + dir.first;
        int new_c = col + dir.second;
        if (new_r >= 0 && new_r < grid.size() && new_c >= 0 && new_c < grid[0].size() && grid[new_r][new_c] > next_val) {
            next_val = grid[new_r][new_c];
        }
    }
    return next_val != grid[row][col] ? next_val : -1;
}

int main() {
    std::vector<std::vector<int>> trail_grid = {
        {1, 2, 3},
        {6, 5, 8},
        {7, 4, 9}
    };  // Representing a hiking trail
    std::pair<int, int> start_position = {1, 1};  // Starting in the middle of the grid
    // Prints the value uphill from the start position or -1 if there's no uphill
    std::cout << find_next_uphill(trail_grid, start_position) << std::endl;
    return 0;
}