/* Trek Path
You are given a 2D grid representing a mountain's elevation map, where each cell contains
an integer representing the elevation at that point. You start at a given position (x, y) on the grid.
Your task is to find a path from the starting position to the peak of the mountain by moving only to adjacent cells (North, East, South, West)
with strictly higher elevations. The path should be represented as a list of elevations starting from the initial position to the peak.
If there are multiple paths to the peak, return any one of them. If no path exists, return an empty list.
*/
#include <vector>
#include <iostream>
#include <algorithm>

using  namespace std;

// Define the trek_path function that takes the elevation_map, start_x, and start_y as parameters.
vector<int> trek_path(vector<vector<int>> &elevation_map, int start_x, int start_y) {
    vector<int> result;
    int rows = elevation_map.size();
    int cols = elevation_map[0].size();

    // Initialize the path with thce starting position's elevation.
    int current = elevation_map[start_x][start_y];
    result.push_back(current);
    bool flag = true;
    // Direction
    vector<pair<int, int>> directions = {{-1, 0}, {0, 1}, {1, 0}, {0, -1}};
    while (flag) {
        int store_current = current;
        int next_x = -1, next_y = -1;
        for (auto &dir : directions) {
            int r = start_x + dir.first;
            int c = start_y + dir.second;
            if (r >= 0 && r < rows && c >= 0 && c < cols && elevation_map[r][c] > store_current) {
                current =elevation_map[r][c];
                next_x = r;
                next_y = c;
            }
        }
        start_x = next_x;
        start_y = next_y;
        
        // Check if found new stek
        if (current > store_current) {
            result.push_back(current);
        } else {
            flag = false;
        }
    }

    return result;
    
}
int main() {
    std::vector<std::vector<int>> mountain = {
        {1, 2, 3},
        {2, 3, 4},
        {3, 5, 6}
    };
    std::vector<int> result = trek_path(mountain, 1, 1);
    for (int height : result) {
        std::cout << height << " ";
    }
    return 0;
}