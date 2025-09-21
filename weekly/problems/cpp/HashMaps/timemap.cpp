/* Leetcode problem 981. Time Based Key-Value Store
 * Design a time-based key-value data structure that can store multiple values for the same key at different
 * timestamps and retrieve the value at a given timestamp.
 */

#include <unordered_map>
#include <vector>
#include <string>
#include <iostream>

using namespace std;
class TimeMap {
public:
    // Craete a hasmap keyTimeMap which stores string as key and a srted maps as value
    unordered_map<string, vector<pair<int, string>>> keyTimeMap;

    TimeMap() {        
    }
    
    void set(string key, string value, int timestamp) {
        // Push '(timestamp, value)' pair in 'key' bucket
        keyTimeMap[key].push_back({timestamp, value});
    }
    
    string get(string key, int timestamp) {
        // If the key does not exist im map we will return empty string
        if (keyTimeMap.find(key) == keyTimeMap.end()) {
            return "";
        }

        if (timestamp < keyTimeMap[key][0].first) {
            return "";
        }

        // Using binary search on the array of pairs
        int left = 0;
        int right = keyTimeMap[key].size();

        while (left < right) {
            int mid = (left + right) / 2;
            if (keyTimeMap[key][mid].first <= timestamp) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }

        // If iterator points to first element it means, no time <= timestamp exists
        if (right == 0) {
            return "";
        }

        // Return value store at the end of right vector
        return keyTimeMap[key][right - 1].second;
    }
};

/**
 * Your TimeMap object will be instantiated and called as such:
 * TimeMap* obj = new TimeMap();
 * obj->set(key,value,timestamp);
 * string param_2 = obj->get(key,timestamp);
 */

 int main() {
    TimeMap* obj = new TimeMap();
    obj->set("foo", "bar", 1);
    string param_2 = obj->get("foo", 1); // return "bar"
    string param_3 = obj->get("foo", 3); // return "bar", since there is no value corresponding to foo at timestamp 3 and timestamp 2, then the only value is at timestamp 1 is "bar"
    obj->set("foo", "bar2", 4);
    string param_4 = obj->get("foo", 4); // return "bar2"
    string param_5 = obj->get("foo", 5); // return "bar2"

    cout << param_2 << endl;
    cout << param_3 << endl;
    cout << param_4 << endl;
    cout << param_5 << endl;
    return 0;
 }