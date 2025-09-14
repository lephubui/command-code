#include <iostream>
#include <unordered_map>
#include <string>
#include <sstream>

int main() {
    std::unordered_map<std::string, int> word_counts;  // Initialize an unordered_map to store the word counts

    // Array of words to count
    std::string words_to_count[] = {"apple", "banana", "cherry"};

    // String in which to count words
    std::string string_to_search = "apple banana apple cherry apple banana";

    // Split the string into individual words using stringstream
    std::istringstream iss(string_to_search);
    std::string word;

    while (iss >> word) {
        // Count the appearances of each word in the string
        // and update word_counts accordingly
        for (const std::string& fruit : words_to_count) {
            if(word == fruit) {
                word_counts[fruit]++;
            }
        }
    }

    // Output the counts of each word
    for (const auto &word_to_count : words_to_count) {
        std::cout << word_to_count << ": " << word_counts[word_to_count] << std::endl;
    }

    return 0;
}