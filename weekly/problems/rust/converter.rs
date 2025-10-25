fn main() {
    // A temperature in Celsius
    let temp_celsius: f64 = 23.75;
    
    // TODO: Convert the temperature from a f64 to a String
    let temperature_text: String = temp_celsius.to_string();
    
    // Displaying the temperature as text
    println!("The temperature is: {}°C", temperature_text);

    // Constant with temperature as a string
    let temperature_string = "23.5";

    // Convert the temperature_string to a floating-point number and assign it to a variable
    let temperature: f64 = temperature_string.parse().unwrap();
    // Print the temperature in Celsius
    println!("The temperature is {} degrees Celsius.", temperature);

    let ten: i32 = 10; // an integer with the value 10
    let ten_string: String = ten.to_string(); // A string with the value "10"
    println!("The value of ten_string: {}", ten_string);    // Output: The value of ten_string: 10

    let twenty_five_string = "25";
    let twenty_five: i32 = twenty_five_string.parse().unwrap();
    println!("The value of twenty_five: {}", twenty_five);    // Output: The value of twenty_five: 25

    let invalid_number = "25abc";
    let number: i32 = invalid_number.parse().unwrap(); // Oops! This will panic, "25abc" is not a number!
}