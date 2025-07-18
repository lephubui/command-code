/******************************************************************************************************************************************************************
Array Manipulation Challenge: Knight Tournament in a Circle
Problem Statement
In a medieval tournament, n knights stand in a circular formation, and each is assigned an initial strength — a positive integer between 1 and 100 inclusive.

The tournament consists of a series of jousting rounds, where:

    1. Each knight simultaneously fights the knight to their immediate right.

    2. A knight's strength is updated to the difference between their strength and the strength of the opponent to their right:
        new_strength[i] = strength[i] - strength[(i + 1) % n];

    3. After all matches in a round are resolved:
        Knights whose strength is now less than or equal to zero are eliminated before the next round begins.

The tournament continues until one of the following occurs:

    1. Only one knight remains standing.

    2. All remaining knights have equal strength (a stalemate).

Your Task:
Implement a function that simulates this tournament and returns the total number of rounds before it ends.

Constraints
1 ≤ n ≤ 100

1 ≤ strengths[i] ≤ 100 for all i

All strengths are integers

Example:

Suppose we have knights with strengths [100, 50, 30, 20]. The game would proceed as follows:

Round 1:

Knight 1 fights Knight 2: (100 - 50 = 50)
Knight 2 fights Knight 3: (50 - 30 = 20)
Knight 3 fights Knight 4: (30 - 20 = 10)
Knight 4 fights Knight 1: (20 - 100 = -80) (Knight 4 is out)
Updated strengths: [50, 20, 10] (Knight 4 removed)

Round 2:

Knight 1 fights Knight 2: (50 - 20 = 30)
Knight 2 fights Knight 3: (20 - 10 = 10)
Knight 3 fights Knight 1: (10 - 50 = -40) (Knight 3 is out)
Updated strengths: [30, 10] (Knight 3 removed)
Round 3:

Knight 1 fights Knight 2: (30 - 10 = 20)
Knight 2 fights Knight 1: (10 - 30 = -20) (Knight 2 is out)
Updated strengths: [20] (Knight 2 removed)
The tournament ends with only one knight standing, so the number of rounds is 3. 
Thus, tournament([100, 50, 30, 20]) returns 3.

*****************************************************************************************************************************************************************/

#include <vector>
#include <algorithm>
#include <iostream>

using namespace std;

bool areAllElementsEqual(const std::vector<int>& vec) {
    if (vec.empty()) {
        return true; // Or handle empty vector as needed
    }
    return std::all_of(vec.begin(), vec.end(), [&](int element){
        return element == vec[0];
    });
}

int tournament(std::vector<int> knights) {
    int counter = 0;
    
    while (knights.size() > 1) {        
        // Check if all knights have the same strength (stalemate)
        if(areAllElementsEqual(knights)){
            break;
        }
        
        // New round
        counter++;

        int n = knights.size();
        vector<int> new_knights(n);

        // Find new knight strength
        for (int k = 0; k < n; k++) {
            new_knights[k] = knights[k] - knights[(k + 1) % n];
        }
        
        vector<int> survived_knights;
        // Check if which knight is defeated 
        for (int& knight : new_knights) {
            if (knight > 0) {
                survived_knights.push_back(knight);
            }
        }
        
        knights = survived_knights;
    }

    return counter;
}

int main() {
    // Example usage
    vector<int> knights = {100, 50, 30, 20};
    int rounds = tournament(knights);
    cout << "Total rounds: " << rounds << endl; // Output: Total rounds: 3
    
    // Test stalemate scenario
    // vector<int> stalemate_knights = {10, 10, 10};
    // cout << "\nTesting stalemate scenario:" << endl;
    // int stalemate_rounds = tournament(stalemate_knights);
    // cout << "Total rounds: " << stalemate_rounds << endl;
    
    return 0;
}