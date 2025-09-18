// Your task is to implement a simple Library Management system to check if a book is available by its ID using HashMaps in C++

#include <iostream>
#include <unordered_map>
#include <string>

int main() {

    // TODO: Implement a search in 'library_catalog' to check if the 'book_id' exists and print the book details or "Book not found in the library catalog."
    // Define a 'library_catalog' using unordered_map with a few books. 
    // Each book id as key and another unordered_map as value containing details like title, author, and year_published
    std::unordered_map<int, std::unordered_map<std::string, std::string>> library_catalog = {
        {101, {{"title", "1984"}, {"author", "George Orwell"}, {"year_published", "1949"}}},
        {102, {{"title", "To Kill a Mockingbird"}, {"author", "Harper Lee"}, {"year_published", "1960"}}},
        {103, {{"title", "The Great Gatsby"}, {"author", "F. Scott Fitzgerald"}, {"year_published", "1925"}}}
    };

    // Assign a 'book_id' variable with the id of the book you want to check
    int book_id = 102;

    // Implement a search in 'library_catalog' to check if the 'book_id' exists and print the book details or "Book not found in the library catalog."
    auto it = library_catalog.find(book_id);
    if (it != library_catalog.end()) {
        const auto& details = it->second;
        std::cout << "Book found:\n";
        std::cout << "Title: " << details.at("title") << "\n";
        std::cout << "Author: " << details.at("author") << "\n";
        std::cout << "Year Published: " << details.at("year_published") << "\n";
    } else {
        std::cout << "Book not found in the library catalog." << std::endl;
    }

    return 0;
}