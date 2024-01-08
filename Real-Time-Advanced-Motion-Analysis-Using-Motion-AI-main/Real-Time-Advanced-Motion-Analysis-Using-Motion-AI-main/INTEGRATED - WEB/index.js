// index.js

const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const { spawn } = require('child_process');
const multer = require('multer');
const fs = require('fs');

const app = express();
const port = 3000;

// Serve static files from the 'public' folder
app.use(express.static(path.join(__dirname, 'public')));
app.use(bodyParser.json());

app.get('/first', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index1.html'));
});

app.get('/second', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index2.html'));
});

app.get('/fourth', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index4.html'));
});
app.get('/fourth2', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index44.html'));
});

app.get('/videoCompression', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index33.html'));
});

app.get('/foregroundSubtraction', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index333.html'));
});
app.get('/fourth3', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index444.html'));
});

// Define a constant name for the processed video
const processedVideoName = 'output.mp4';

const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

// Endpoint for handling motion analysis form submission
app.post('/motionAnalysis/upload', upload.single('videoFile'), (req, res) => {
    const outputFolder = path.join(__dirname, 'output_folder_dmd');
    
    // Remove the existing output folder if it exists
    if (fs.existsSync(outputFolder)) {
        fs.rmSync(outputFolder, { recursive: true });
    }

    // Recreate the output folder
    fs.mkdirSync(outputFolder);

    const videoPath = path.join(outputFolder, 'input_video.mp4');
    fs.writeFileSync(videoPath, req.file.buffer);

    const pythonProcess = spawn('python', ['dmd_processing.py', videoPath, outputFolder]);

    pythonProcess.stdout.on('data', (data) => {
        console.log(`Python script output: ${data}`);
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Error from Python script: ${data}`);
    });

    pythonProcess.on('close', (code) => {
        console.log(`Python script exited with code ${code}`);
        if (code === 0) {
            // Video processed successfully, redirect to index4.html
            res.redirect('/fourth');
        } else {
            res.status(500).json({ success: false, message: 'Video processing failed' });
        }
    });
});
app.get('/download/processedVideo', (req, res) => {
    const filePath = path.join(__dirname, 'output_folder_dmd', 'output.mp4');

    // Check if the file exists
    if (fs.existsSync(filePath)) {
        // Set the appropriate headers for the download
        res.setHeader('Content-Disposition', 'attachment; filename=motion_analysis_video.mp4');
        res.setHeader('Content-Type', 'video/mp4');

        // Pipe the file stream to the response
        const fileStream = fs.createReadStream(filePath);
        fileStream.pipe(res);
    } else {
        res.status(404).send('File not found');
    }
});

// Endpoint for handling video compression form submission
app.post('/videoCompression/upload', upload.single('videoFile'), (req, res) => {
    const outputFolder = path.join(__dirname, 'output_folder2_dmd');
    const videoPath = path.join(outputFolder, 'input_video.mp4');
    const outputVideoPath = path.join(outputFolder, 'output_video.mp4');

    // Create the output folder if it does not exist
    if (!fs.existsSync(outputFolder)) {
        fs.mkdirSync(outputFolder);
    }

    // Write the uploaded video to the input path
    fs.writeFileSync(videoPath, req.file.buffer);

    // Call the Python script for video compression
    const pythonProcess = spawn('python', ['video_compression.py', videoPath, outputVideoPath, '10']);

    pythonProcess.stdout.on('data', (data) => {
        console.log(`Python script output: ${data}`);
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Error from Python script: ${data}`);
    });

    pythonProcess.on('close', (code) => {
        console.log(`Python script exited with code ${code}`);
        if (code === 0) {
            // Introduce a delay (e.g., 1 second) to allow file operations to complete
            setTimeout(() => {
                // Compression successful, redirect to index44.html
                res.redirect('/fourth2');
            }, 1000);
        } else {
            res.status(500).json({ success: false, message: 'Video compression failed' });
        }
    });
});

app.get('/download/compressedVideo', (req, res) => {
    const filePath = path.join(__dirname, 'output_folder2_dmd', 'output_video.mp4');

    // Check if the file exists
    if (fs.existsSync(filePath)) {
        // Set the appropriate headers for the download
        res.setHeader('Content-Disposition', 'attachment; filename=compressed_video.mp4');
        res.setHeader('Content-Type', 'video/mp4');

        // Pipe the file stream to the response
        const fileStream = fs.createReadStream(filePath);
        fileStream.pipe(res);
    } else {
        res.status(404).send('File not found');
    }
});
app.post('/foregroundSubtraction/upload', upload.single('videoFile'), (req, res) => {
    const outputFolder = path.join(__dirname, 'output_folder3_dmd');
    const videoPath = path.join(outputFolder, 'input_video.mp4');
    const outputVideoPath = path.join(outputFolder, 'output_video.mp4');

    // Create the output folder if it does not exist
    if (!fs.existsSync(outputFolder)) {
        fs.mkdirSync(outputFolder);
    }

    // Write the uploaded video to the input path
    fs.writeFileSync(videoPath, req.file.buffer);

    // Call the Python script for foreground subtraction
    const pythonProcess = spawn('python', ['foreground_subtraction_script.py', videoPath, outputVideoPath]);

    pythonProcess.stdout.on('data', (data) => {
        console.log(`Python script output: ${data}`);
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Error from Python script: ${data}`);
    });

    pythonProcess.on('close', (code) => {
        console.log(`Python script exited with code ${code}`);
        if (code === 0) {
            // Introduce a delay (e.g., 1 second) to allow file operations to complete
            setTimeout(() => {
                // Process successful, redirect to index4.html
                res.redirect('/fourth3');
            }, 1000);
        } else {
            res.status(500).json({ success: false, message: 'Foreground subtraction failed' });
        }
    });
});
app.post('/foregroundProcessing/upload', upload.single('videoFile'), (req, res) => {
    const outputFolder = path.join(__dirname, 'output_folder3_dmd');
    const videoPath = path.join(outputFolder, 'input_video.mp4');

    // Create the output folder if it does not exist
    if (!fs.existsSync(outputFolder)) {
        fs.mkdirSync(outputFolder);
    }

    // Write the uploaded video to the input path
    fs.writeFileSync(videoPath, req.file.buffer);

    // Call the Python script for foreground processing
    const pythonProcess = spawn('python', ['foreground_subtraction_script.py', videoPath, outputFolder]);

    pythonProcess.stdout.on('data', (data) => {
        console.log(`Python script output: ${data}`);
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Error from Python script: ${data}`);
    });

    pythonProcess.on('close', (code) => {
        console.log(`Python script exited with code ${code}`);
        if (code === 0) {
            // Introduce a delay (e.g., 1 second) to allow file operations to complete
            setTimeout(() => {
                // Processing successful, redirect to index444.html
                res.redirect('/fourth3');
            }, 1000);
        } else {
            res.status(500).json({ success: false, message: 'Foreground processing failed' });
        }
    });
});

app.get('/download/foregroundVideo', (req, res) => {
    const filePath = path.join(__dirname, 'output_folder3_dmd', 'output_video.mp4', 'foreground.mp4');

    // Check if the file exists
    if (fs.existsSync(filePath)) {
        // Set the appropriate headers for the download
        res.setHeader('Content-Disposition', 'attachment; filename=foreground.mp4');
        res.setHeader('Content-Type', 'video/mp4');

        // Pipe the file stream to the response
        const fileStream = fs.createReadStream(filePath);
        fileStream.pipe(res);
    } else {
        res.status(404).send('File not found');
    }
});


app.listen(port, () => {
    console.log(`Server is listening at http://localhost:${port}`);
});
