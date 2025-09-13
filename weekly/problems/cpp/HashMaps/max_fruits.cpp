#include <iostream>
#include <unordered_map>
#include <algorithm> // For max_element

using namespace std;

int main() {
    // Inventory unordered_map for a grocery shop
    unordered_map<string, int> inventory = {{"apples", 30}, {"bananas", 45}, {"oranges", 25}, {"pears", 10}};

    // Calculate the total items in the inventory and print it
    int total = 0;
    for (const auto& pair : inventory) {
        total += pair.second;
    }

    cout << "The total number of fruits in the basket is: " << total << endl;

    // Find the average quantity of fruits in the inventory and print it
    double average = static_cast<double>(total) / inventory.size();
    cout << "The average number of fruits in the basket is: " << average << endl;

    // Find the minimum quantity of a single fruit type in the inventory and print it
    int min_fruit = min_element(inventory.begin(), inventory.end(), 
        [](const auto& a, const auto&b) {
            return a.second < b.second;
        })->second;
    cout << "The fruit with the least quantity is: " << min_fruit << endl;

    // Find the maximum quantity of a single fruit type in the inventory and print it
    int max_fruit = max_element(inventory.begin(), inventory.end(), 
        [](const auto& a, const auto&b) {
            return a.second < b.second;
        })->second;
    
    cout << "The fruit with the most quantity is: " << max_fruit << endl;

    return 0;
}