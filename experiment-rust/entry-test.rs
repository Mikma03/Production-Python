// fn main() {
//     println!("Hello, world!");
//     println!("Hello, world!_01");
// }

use std::process::Command;

fn main() {
    // Creating a new command to execute 'ls -lh'
    let output = Command::new("ls")
        .arg("-lh") // Adding an argument to the command
        .output() // Executes the command as a child process and captures the output
        .expect("Failed to execute command"); // Handling errors if the command fails to execute

    // Printing the output of the command
    println!("Output: {}", String::from_utf8_lossy(&output.stdout));
}