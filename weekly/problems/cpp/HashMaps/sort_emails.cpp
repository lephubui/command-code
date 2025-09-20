/* Problem Statement: 
 * Given a string representing an inbox log where each email is represented as "sender_email, message_content" and emails are separated by semicolons,
 * write a function to organize the inbox by counting the number of emails from each sender. 
 * The function should return a list of pairs (sender_email, count) sorted by count in descending order. 
 * If two senders have the same count, they should be sorted alphabetically by their email addresses.
 * Example:
 * Input: "alice@example.com, Hello Bob; bob@example.com, Hi Alice; alice@example.com, Are you there?"
 * Output: [("alice@example.com", 2), ("bob@example.com", 1)]
 * 
 */
#include <algorithm>
#include <sstream>
#include <unordered_map>
#include <vector>
#include <string>
#include <utility>
#include <iostream>

using namespace std;
vector<pair<string, int>> organize_inbox(const string& inbox_string) {
    unordered_map<string, int> senderMap;
    stringstream ss(inbox_string);
    string message;
    
    // Break down the log string into individual logs by splitting
    while (getline(ss, message, ';')) {
        // Get the string between simicolon
        size_t comma_pos = message.find(",");
        string sender = message.substr(0, comma_pos);
        
        // Remove space between them
        size_t start = sender.find_first_not_of(" ");
        size_t end = sender.find_last_not_of(" ");
        string trimmed = (start == string::npos) ? "" : sender.substr(start, end - start + 1);
        
        // Check if it's in the map
        auto it = senderMap.find(trimmed);
        // Add to map
        senderMap[trimmed] += 1;
        
    }
    
    // Parsing map to res
    vector<pair<string, int>> res;
    for (auto &entry : senderMap) {
        res.push_back(make_pair(entry.first, entry.second));
    }
    
    // Sort them within decreasing count of sender email
    sort(res.begin(), res.end(), [](const pair<string, int>& a, const pair<string, int>& b) {
        if (a.second != b.second) {
            return a.second > b.second; // Descending count
        }
        return a.first < b.first; // Ascending email if count are equal
    });
    
    return res;
}

int main() {
    string inbox = "alice@example.com, Hello Bob; bob@example.com, Hi Alice; alice@example.com, Are you there?";
    vector<pair<string, int>> organized = organize_inbox(inbox);

    for (const auto& entry : organized) {
        cout << "(" << entry.first << ", " << entry.second << ")" << endl;
    }

    return 0;
}