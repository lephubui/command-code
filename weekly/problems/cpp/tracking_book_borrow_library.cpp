/*
 * This function processes a log of book borrow and return events, tracking the total
 * time each group has borrowed books. It returns a list of groups with the longest
 * borrow time, formatted as pairs of group ID and duration.
 * 
 * You are provided with log data from a library's digital system, stored in string format. 
 * The log represents books' borrowing activities, including the book ID and the time a book is borrowed and returned. The structure of a log entry is as follows: <book_id> borrow <time>, <book_id> return <time>.
 * The time is given in the HH:MM 24-hour format, and the book ID is a positive integer between 1 and 500. The logs are separated by a comma, followed by a space (", ").
 * Your task is to create a C++ function named solution(). This function will take as input a string of logs and output a vector of pairs representing the books with the longest borrowed duration. 
 * Each pair contains two items: the book ID and the book's borrowed duration. By 'borrowed duration,' we mean the period from when the book was borrowed until it was returned. 
 * If a book has been borrowed and returned multiple times, the borrowed duration is the total cumulative sum of those durations. 
 * If multiple books share the same longest borrowed duration, the function should return all such books in ascending order of their IDs.
 * 
 * For example, if we have a log string as follows: "1 borrow 09:00, 2 borrow 10:00, 1 return 12:00, 3 borrow 13:00, 2 return 15:00, 3 return 16:00",
 * the function will return: {std::make_pair(2, "05:00")}.
 */

#include <algorithm>
#include <sstream>
#include <unordered_map>
#include <utility>
#include <vector>
#include <string>
#include <unordered_map>
#include <map>
#include <iostream>

using namespace std;

std::vector<std::pair<int, std::string>> solution(const std::string& logs) {
    vector<string> logList;
    stringstream ss(logs);
    string log;
    
    // Break down the log string into individual logs by splitting
    while(getline(ss, log, ',')) {
        logList.push_back(log);
    }
    
    unordered_map<int, pair<int, int>> timeDict;
    map<int, int> lifeDict;
    
    for (const auto &log : logList) {
        stringstream logStream(log);
        int groupId;
        string action, time;
        logStream >> groupId >> action >> time;

        // Parsing the time from HH:MM format
        int hour = stoi(time.substr(0, 2));
        int minute = stoi(time.substr(3, 2));
        int currentTime = hour * 60 + minute; // Time in minutes from start of day
        
        if (action == "borrow") {
            timeDict[groupId] = make_pair(hour, minute);
        } else {
            if (timeDict.find(groupId) != timeDict.end()) {
                // If group is return, calculate its entire borrow time
                int borrowTime = timeDict[groupId].first*60 + timeDict[groupId].second;
                int lifeTime = currentTime - borrowTime;
                lifeDict[groupId] += lifeTime;
                timeDict.erase(groupId);
            }
        }
    }
    
    // Find the longest borrow time
    auto maxBorrowTime = max_element(lifeDict.begin(), lifeDict.end(), [](const std::pair<int, int>& a, const std::pair<int, int>& b) {
        return a.second < b.second;
    });
    
    int maxBorrow = maxBorrowTime->second;
    
    // Building the result vector where each item is a pair of group ID and its borrowtime it if has the longest borrowtime
    vector<pair<int, string>> result;
    for (const auto &entry : lifeDict) {
        if (entry.second == maxBorrow) {
            int hours = entry.second / 60;
            int minutes = entry.second % 60;
            string timeString = (hours < 10 ? "0" : "") + to_string(hours) + ":" + (minutes < 10 ? "0" : "") + std::to_string(minutes);
            result.push_back(make_pair(entry.first, timeString));
        }
    }
    
    // Sorting the result in ascending order of the group IDs
    sort(result.begin(), result.end());
    
    return result;
}

int main() {
    // Example usage
    string logs = "1 borrow 09:00, 2 borrow 10:00, 1 return 12:00, 3 borrow 13:00, 2 return 15:00, 3 return 16:00";
    vector<pair<int, string>> longestBorrowed = solution(logs);
    
    // Output the result
    for (const auto& entry : longestBorrowed) {
        cout << "Group ID: " << entry.first << ", Borrowed Duration: " << entry.second << endl;
    }
    
    return 0;
}