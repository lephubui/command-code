fn main() {
    let hero_names = [String::from("Iron Man"), String::from("Thor")];
    let mut hero_powers = [2999,4500];

    // Call list_names on hero_names WITHOUT transfering ownership
    list_names(&hero_names);

    // Call move_teams in order to change all power levels to 0 and transfer ownership of of hero_names array
    move_teams(hero_names, &mut hero_powers);
    println!("Hero powers are now: {:?}", hero_powers);
}

// Implement list_names which prints out the names of the heros without transferring ownership
fn list_names(arr: &[String; 2]) {
    println!("Hero names are: {:?}", arr);
}

// Implement move_teams which prints out the hero names while transfering ownership. The powers should all be set to 0 without transferring ownership.
fn move_teams(names: [String; 2], powers: &mut [i32; 2]) {
    println!("Moving {:?} to another team", names);
    // Set power levels to 0
    powers[0] = 0;
    powers[1] = 0;
}