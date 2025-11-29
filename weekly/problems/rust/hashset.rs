use std::collections::HashSet;

fn main() {
    // Create new HashSet
    let mut superhero_set: HashSet<&str> = HashSet::new();

    // Add superheroes to HashSet
    superhero_set.insert("Superman");
    superhero_set.insert("Batman");
    superhero_set.insert("Wonder Woman");

    // Remove a superhero from HashSet
    superhero_set.remove("Batman");

    // Check membership in HashSet
    let has_superman = superhero_set.contains("Superman");
    let has_batman = superhero_set.contains("Batman");
    println!("HashSet has Superman: {}, has Batman: {}", has_superman, has_batman);

    // len(), is_empty()
    println!("Length of HashSet: {}", superhero_set.len());
    println!("Is HashSet empty: {}", superhero_set.is_empty());

    // Ownership for HashSet
    let movie = String::from("Justice League");
    let mut movie_set = HashSet::from([movie, String::from("Aquaman")]);
    // println!("{}", movie); Causes an error since `movie` transferred ownership to `movie_set`

    // Hashsets as function parameters
    let mut movie_hashset = HashSet::new();
    movie_hashset.insert("Shazam");
    movie_hashset.insert("Batman v Superman");
    display_movie_reference(&movie_hashset);
    println!("After display_movie_reference: {:?}", movie_hashset);

    transfer_movie_ownership(movie_hashset); 
    // println!("After transfer_movie_ownership: {:?}", movie_hashset); Causes error
}

fn display_movie_reference(set: &HashSet<&str>) {
    println!("Movies in set: {:?}", set);
}

fn transfer_movie_ownership(set: HashSet<&str>) {
    println!("Transferred movies: {:?}", set);
}