#include <sstream>
#include <map>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;
std::vector<std::vector<int>> analyze_competition(const std::string& logs) {
    stringstream ss(logs);
    string sentence;
    vector<string> sentence_list;
    
    // Got each sentence to list of sentence between a comma
    while (getline(ss, sentence, ',')) {
        sentence_list.push_back(sentence);
    }
    
    map<int, vector<int>> mapStudents;
    // helper trim
    auto trim = [](const string& s) {
        const string ws = " \t\n\r";
        size_t start = s.find_first_not_of(ws);
        if (start == string::npos) return string();
        size_t end = s.find_last_not_of(ws);
        return s.substr(start, end - start + 1);
    };
    
    // Iterate through each sentence
    for (auto &each : sentence_list) {
        // trim leading/trailing whitespace (entries may have leading space after comma)
        string entry = trim(each);
        if (entry.empty()) continue;
        
        // get it streams
        stringstream letitss(entry);
        string studentId;
        string result;
        string timeTaken;
        string score;
        
        // Get student Id and result first
        letitss >> studentId >> result >> timeTaken;
        // attempt to read score (may not exist for fail entries)
        if (!(letitss >> score)) {
            score = "";
        }
        
        int id = stoi(studentId);
        // ensure vector exists: [score, solved_count, penalties]
        if (mapStudents.find(id) == mapStudents.end()) {
            mapStudents[id] = vector<int>{0, 0, 0};
        }
        
        if (result == "solve") {
            int difficulty = 0;
            if (!score.empty()) {
                difficulty = stoi(score);
            }
            mapStudents[id][0] += difficulty; // total score
            mapStudents[id][1] += 1;          // solved count
        } else if (result == "fail") {
            mapStudents[id][2] += 1;          // penalty count
        }
    }
    
    // collect only students with positive score
    vector<pair<int, vector<int>>> items;
    for (auto &p : mapStudents) {
        if (p.second.size() >= 1 && p.second[0] > 0) {
            items.emplace_back(p.first, p.second);
        }
    }
    
    // sort by descending score
    sort(items.begin(), items.end(), [](const auto &a, const auto &b) {
        return a.second[0] > b.second[0];
    });
    
    vector<vector<int>> result;
    result.reserve(items.size());
    for (auto &p : items) {
        result.push_back({p.first, p.second[0], p.second[1], p.second[2]});
    }
    return result;
}