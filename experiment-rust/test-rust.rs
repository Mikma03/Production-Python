use std::process::Command;
use std::thread;

fn main() {
    let commands = vec!["ls", "pwd", "echo 'Hello World'"];

    // Spawning multiple threads, each running a different command
    let handles: Vec<_> = commands.into_iter().map(|cmd| {
        thread::spawn(move || {
            let output = Command::new("sh")
                .arg("-c")
                .arg(cmd) // Running the command
                .output()
                .expect("Failed to execute command");

            // Printing the output of each command
            println!("Output of {}: {}", cmd, String::from_utf8_lossy(&output.stdout));
        })
    }).collect();

    // Waiting for all threads to complete
    for handle in handles {
        handle.join().unwrap();
    }
}