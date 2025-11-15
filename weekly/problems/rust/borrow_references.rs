// This function demonstrates borrowing references in Rust.
// It takes a reference to a String and prints it without taking ownership.
// The main function creates a String, borrows it, and then prints it again to show ownership is retained.
// No ownership is transferred; only a reference is passed.
// This prevents issues related to ownership and borrowing in Rust.
// The code compiles and runs successfully.

// Write a function that takes a reference to a String and prints it
fn borrow_title(new_title: &String) {
    println!("This is my book title: {}", new_title);
}
fn main() {
    // Create a new String variable named book_title
    let book_title = String::from("Rust Programming");
    // Borrow the book_title using the function
    borrow_title(&book_title);
    // Print the book_title to show that ownership is retained
    println!("I still own the book {}", book_title);
}