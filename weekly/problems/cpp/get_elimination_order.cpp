/*******************************************************************************************************************************************************************************
 * Array Manipulation Challenge: Get Elimination Order in String
 * Problem Statement:
You are given a string s consisting only of uppercase English letters ('A' to 'Z'). 
Your task is to perform a sequence of elimination rounds on the string until it becomes empty, following these rules:

In each round:
1. Form adjacent pairs from left to right:

    Pair the 1st and 2nd characters, 3rd and 4th, and so on.
    If the length of the string is odd, the last character is not paired and is carried over to the next round.

2. For each pair (a, b):

    Remove the character that comes earlier in lexicographical order (i.e., 'A' < 'B' < ... < 'Z').
    If both characters are the same, remove the first one.

3. After forming the next string from remaining characters, repeat the process on the resulting string.

4. If a single character remains at the end of any round, remove it in the next round.

Return a list of all characters removed, in the exact order they were eliminated.

Example 1: 
Input: "ABCD"
Output: "A B C D"

Explanation:  
In the first round, pairs are (A, B) and (C, D). A is removed, then C is removed, leaving "BD". In the next round, B is removed, leaving "D", which is then removed.

Example 2:
Input: "AABBC"
Output: "A A B C"

Explanation:  
In the first round, pairs are (A, A), (B, B), and C is carried over. A is removed, then B is removed, leaving "AC". In the next round, A is removed, leaving "C", which is then removed.

********************************************************************************************************************************************************************************/
#include <vector>
#include <string>
#include <iostream>
#include <utility> // for std::pair

using namespace std;
vector<char> solution(string s) {
    vector<char> results;

    // Continue until the string is empty
    while (!s.empty()) {
        string new_str = "";
        vector<pair<char, char>> result_pairs;
        
        // Edge case
        if (s.length() == 1) {
            results.push_back(s[0]);
            break;
        }
        // Form the pair
        for (int i = 0; i + 1 < s.length(); i+=2) {
            pair<char, char> form_pairs(s[i], s[i+1]);
            result_pairs.push_back(form_pairs);
        }
        
        // Process data in the pair
        for(const auto& pair : result_pairs) {
            if (pair.first < pair.second) {
                results.push_back(pair.first);
                new_str += pair.second;
            } else if (pair.first > pair.second) {
                results.push_back(pair.second);
                new_str += pair.first;
            } else {
                results.push_back(pair.second);
                new_str += pair.first;
            }
        }
        
        
        // Rememeber if n is odd, then don't forget to add the last character
        if (s.length() % 2 != 0 and s.length() > 1) {
            new_str += s[s.length()-1];
        }
        
        s = new_str;
    }

    return results;
}

int main() {
    // Example usage
    string input = "ABCD";
    vector<char> elimination_order = solution(input);
    
    // Output the result
    for (char c : elimination_order) {
        cout << c << " "; // Print each eliminated character
    }
    
    return 0;
}
