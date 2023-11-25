use std::process::{Command, Stdio};

/// Executes a command to echo "Hello World" and prints the status and stdout.
fn main() {
    use std::process::{Command, exit};

    // Spawn a new child process to execute the "echo" command
    let mut child = Command::new("echo")
        .arg("Hello World")
        .stdout(Studio::piped())
        .spawn()
        .expect("Failed to execute command");

    // Wait for the child process to complete and get the output
    let output = child.wait_with_output()
        .expect("Failed to wait on child");

    // Print the status of the child process
    println!("Status: {}", output.status);

    // Print the stdout of the child process
    println!("Stdout: {}", String::from_utf8_lossy(&output.stdout));
}