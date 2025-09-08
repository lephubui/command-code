/* Tuple Path Travel
You are given a 2D grid representing a mountain's elevation map, where each cell contains
an integer representing the elevation at that point. You start at a given position (row, column) on the grid.
Your task is to find the next step in your path to the peak of the mountain by moving only to adjacent cells (North, East, South, West)
with strictly higher elevations. The function should return the coordinates of the next cell as a tuple (row, column).
If there are multiple adjacent cells with higher elevations, return the one with the highest elevation.
If no adjacent cell has a higher elevation, return (-1, -1) to indicate that you cannot move further uphill.
*/
#include <iostream>
#include <vector>
#include <tuple>

using namespace std;
// Define the pathTraverse function which takes a mountain matrix and the current position (row, column) as parameters. The function should return the next higher position as a tuple if one is found, or {-1, -1} if there is no higher adjacent cell.
tuple<int, int> pathTraverse(vector<vector<int>> matrix, int row, int column) {
    tuple<int, int> result = {-1, -1};
    int rows = matrix.size();
    int cols = matrix[0].size();

    // Initialize the path with the starting position
    int current = matrix[row][column];
    bool flag = true;
    // Direction
    vector<pair<int, int>> directions = {{-1, 0}, {0, 1}, {1, 0}, {0, -1}};
    while (flag) {
        int store_current = current;
        int next_x = -1, next_y = -1;
        for (auto &dir : directions) {
            int r = row + dir.first;
            int c = column + dir.second;
            if (r >= 0 && r < rows && c >= 0 && c < cols && matrix[r][c] > store_current) {
                current =matrix[r][c];
                next_x = r;
                next_y = c;
            }
        }
        row = next_x;
        column = next_y;
        
        // Check if found new stek
        if (current > store_current) {
            result = make_tuple(row, column);
        } else {
            flag = false;
        }
    }
    
    return result;
}

int main() {
    // Create a matrix named 'mountain' representing ascending values, akin to the increasing elevation while hiking up a mountain.
    vector<vector<int>> mountain = {
        {1, 2, 3},
        {2, 3, 4},
        {3, 5, 6}
    };
    tuple<int, int> result = pathTraverse(mountain, 1, 1);
    
    // Output the coordinates of the next step or indicate if no higher step is available from the current position.
    cout << get<0>(result) << ", " << get<1>(result) << endl;
    
    return 0;
}