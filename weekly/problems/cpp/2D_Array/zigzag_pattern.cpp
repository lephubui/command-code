/*
* Given a 2D matrix of n x m integers, where n represents the number of rows and m represents the number of columns. Both n and m range from 1 to 100, inclusive.
* The matrix cells may contain either a positive, a negative integer, or zero, with values ranging from -100 to 100, inclusive.
* In this task, you are required to traverse the matrix diagonally from the top-left cell to the bottom-right cell in a zigzag pattern. 
* Start from the top-left cell, move one cell to the right (if it exists), then move one step diagonally down-left. 
* After reaching a left (bottom) boundary, move one step down (right) and start moving diagonally up-right. 
* Continue this pattern until you reach the last cell of the matrix. 
* Your task is to return a list of tuples, each tuple containing the index pair (in 0-based indexing format) of cells with negative integers encountered during your traversal.
* Examples:
* [[1, -2, 3, -4],
*  [5, -6, 7, 8],
*  [-9, 10, -11, 12]]
* Output: 
* The negative integers in this sequence and their corresponding positions in the matrix are: [-2, -9, -6, -4, -11], with indices: [(0, 1), (2, 0), (1, 1), (0, 3), (2, 2)].
* Hence, the output should be [(0, 1), (2, 0), (1, 1), (0, 3), (2, 2)].
*/
#include <vector>
#include <utility>
#include <algorithm>
#include <cstdio>

using namespace std;
std::vector<std::pair<int, int>> solution(std::vector<std::vector<int>>& matrix) {
    vector<pair<int, int>> result;
    int rows = matrix.size();
    int cols = matrix[0].size();
    
    for (int i = 0; i < rows + cols - 1; ++i) {
        int row = (i < cols) ? 0 : i - cols + 1;
        int col = (i < cols) ? i : cols - 1;
        vector<pair<int, int>> temp;
        while (row < rows && col >= 0) {
            if (matrix[row][col] < 0) temp.push_back({row, col});
            ++row;
            --col;
        }
        if (i % 2 == 0) std::reverse(temp.begin(), temp.end());
        result.insert(result.end(), temp.begin(), temp.end());
    }
    return result;
}

int main() {
    vector<vector<int>> matrix = {
        {1, -2, 3, -4},
        {5, -6, 7, 8},
        {-9, 10, -11, 12}
    };
    
    vector<pair<int, int>> negatives = solution(matrix);
    
    // Output the result
    for (const auto& p : negatives) {
        printf("(%d, %d) ", p.first, p.second);
    }
    
    return 0;
}  