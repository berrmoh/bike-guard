const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const express = req
// Path to the Python script
const pythonScriptPath = path.join(__dirname, 'accelerometer.py');

// Path to the log file
const logFilePath = path.join(__dirname, 'mpu_data_log.txt');

// Create a write stream for logging data
const logStream = fs.createWriteStream(logFilePath, { flags: 'a' });

// Function to log data from Python script
function logDataFromPython() {
    // Spawn a child process to run the Python script
    const pythonProcess = spawn('python3', [pythonScriptPath]);

    // Listen to data events on stdout
    pythonProcess.stdout.on('data', (data) => {
        const output = data.toString();  // Convert buffer to string
        console.log(output);             // Print output to the console
        logStream.write(output);         // Write output to the log file
    });

    // Listen for errors from the Python script
    pythonProcess.stderr.on('data', (error) => {
        console.error(`Error: ${error}`);
    });

    // Listen for the script to close
    pythonProcess.on('close', (code) => {
        console.log(`Python script exited with code ${code}`);
        logStream.end();  // Close the file stream
    });
}

// Start logging data
logDataFromPython();