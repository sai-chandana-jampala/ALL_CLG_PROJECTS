const { Client } = require('pg');
const express = require('express');
const bodyParser = require('body-parser');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const bcrypt = require('bcrypt');
const crypto = require('crypto');
const session = require('express-session');
const app = express();
const port = 3000;

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

const encryptedFolderPath = 'encrypted_files';
const decryptedFolderPath = 'decrypted_files';

if (!fs.existsSync(encryptedFolderPath)) {
  fs.mkdirSync(encryptedFolderPath);
}

if (!fs.existsSync(decryptedFolderPath)) {
  fs.mkdirSync(decryptedFolderPath);
}

app.use(express.static(path.join(__dirname, 'public')));

const db = new Client({
  user: "postgres",
  host: "localhost",
  database: "crypto",
  password: "jsc2003",
  port: 5432,
});
db.connect();

app.use(session({
  secret: 'jsc',
  resave: false,
  saveUninitialized: false,
  // ...other options as needed
}));
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/login', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'login.html'));
});

app.get('/signup', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'signup.html'));
});

app.get('/dashboard', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'dashboard.html'));
});

app.get('/file-encryption', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'file-encryption.html'));
});

app.get('/file-decryption', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'file-decryption.html'));
});

app.get('/download-decryption', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'download-decryption.html'));
});

app.get('/image-en-dec', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'image-en-dec.html'));
});

app.get('/image-encryption', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'image-encryption.html'));
});

app.get('/download-image-encryption', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'download-image-encryption.html'));
});

app.get('/image-decryption', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'image-decryption.html'));
});

app.get('/download-image-decryption', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'download-image-decryption.html'));
});

app.get('/download/:filename', (req, res) => {
  const filename = req.params.filename;
  const filePath = path.join(__dirname, 'decrypted_files', filename);

  if (fs.existsSync(filePath)) {
    res.download(filePath, (err) => {
      if (err) {
        console.error('Error downloading file:', err);
        res.status(500).send('Error downloading file.');
      }
    });
  } else {
    res.status(404).send('File not found.');
  }
});

app.get('/download-encrypted/:filename', (req, res) => {
  const filename = req.params.filename;
  const filePath = path.join(__dirname, 'encrypted_files', filename);

  if (fs.existsSync(filePath)) {
    res.download(filePath, (err) => {
      if (err) {
        console.error('Error downloading file:', err);
        res.status(500).send('Error downloading file.');
      }
    });
  } else {
    res.status(404).send('File not found.');
  }
});

app.post('/encrypt-file', upload.single('fileToUpload'), (req, res) => {
  const filePassword = req.body.filePassword;
  const fileContent = req.file.buffer;

  const algorithm = 'aes-256-cfb';
  const key = crypto.scryptSync(filePassword, 'salt', 32);
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv(algorithm, key, iv);

  const encryptedContent = Buffer.concat([iv, cipher.update(fileContent), cipher.final()]);

  const encryptedFilePath = path.join(encryptedFolderPath, 'encrypted_file.txt');

  fs.writeFileSync(encryptedFilePath, encryptedContent);

  res.send({
    success: true,
    message: 'File encryption successful!',
    filePath: `/download/${path.basename(encryptedFilePath)}`,
  });
});

app.post('/decrypt-file', upload.single('fileToDecrypt'), (req, res) => {
  const filePassword = req.body.filePassword;
  const fileContent = req.file.buffer;

  const algorithm = 'aes-256-cfb';
  const key = crypto.scryptSync(filePassword, 'salt', 32);
  const iv = fileContent.slice(0, 16);
  const decipher = crypto.createDecipheriv(algorithm, key, iv);

  const decryptedContent = Buffer.concat([decipher.update(fileContent.slice(16)), decipher.final()]);

  const decryptedFilePath = path.join(decryptedFolderPath, 'decrypted_file.txt');
  fs.writeFileSync(decryptedFilePath, decryptedContent);

  res.send({
    success: true,
    message: 'File decryption successful!',
    filePath: `/download-decryption/${path.basename(decryptedFilePath)}`,
  });
});

app.post('/encrypt-image', upload.single('imageToUpload'), (req, res) => {
  const imagePassword = req.body.imagePassword;
  const imageData = req.file.buffer;

  const algorithm = 'aes-256-cfb';
  const key = crypto.scryptSync(imagePassword, 'salt', 32);
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv(algorithm, key, iv);

  const encryptedImageData = Buffer.concat([iv, cipher.update(imageData), cipher.final()]);

  const encryptedImagePath = path.join(encryptedFolderPath, 'encrypted_image.jpg');

  fs.writeFileSync(encryptedImagePath, encryptedImageData);

  res.send({
    success: true,
    message: 'Image encryption successful!',
    filePath: `/download-encrypted/${path.basename(encryptedImagePath)}`,
  });
});

// Add this route for image decryption
app.get('/download-decrypted-image/:filename', (req, res) => {
  const filename = req.params.filename;
  const filePath = path.join(__dirname, 'decrypted_files', filename);

  console.log('Download Decrypted Image Path:', filePath);

  if (fs.existsSync(filePath)) {
    res.download(filePath, (err) => {
      if (err) {
        console.error('Error downloading image:', err);
        res.status(500).send('Error downloading image.');
      }
    });
  } else {
    res.status(404).send('Image not found.');
  }
});

app.post('/decrypt-image', upload.single('imageToDecrypt'), (req, res) => {
  const imagePassword = req.body.imagePassword;
  const imageData = req.file.buffer;

  const algorithm = 'aes-256-cfb';
  const key = crypto.scryptSync(imagePassword, 'salt', 32);
  const iv = imageData.slice(0, 16);
  const decipher = crypto.createDecipheriv(algorithm, key, iv);

  const decryptedImageData = Buffer.concat([decipher.update(imageData.slice(16)), decipher.final()]);

  const decryptedImagePath = path.join(decryptedFolderPath, 'decrypted_image.jpg');
  fs.writeFileSync(decryptedImagePath, decryptedImageData);

  res.send({
    success: true,
    message: 'Image decryption successful!',
    filePath: `/download-image-decryption/${path.basename(decryptedImagePath)}`,
  });
});

app.post('/signup', (req, res) => {
  const { username, password } = req.body;

  // Encrypt the password using a secure hashing algorithm
  const hashedPassword = bcrypt.hashSync(password, 10);

  // Insert into the new table (no need to provide ID explicitly)
  db.query(
    `INSERT INTO new_users (username, password) VALUES ($1, $2)`,
    [username, hashedPassword],
    (err, result) => {
      if (err) {
        if (err.code === '23505') {
          res.status(400).send('Username already exists'); // Handle duplicate username error
        } else {
          console.error(err);
          res.status(500).send('Error saving user'); // Handle other database errors
        }
      } else {
        res.redirect('/dashboard.html'); // Redirect on successful signup
      }
    }
  );
});


app.post('/login', (req, res) => {
  const { username, password } = req.body;

  // Query the database to check for matching credentials
  db.query(
    'SELECT * FROM new_users WHERE username = $1',
    [username],
    (err, result) => {
      if (err) {
        console.error(err);
        res.status(500).send('Error checking credentials');
      } else if (result.rows.length === 0) {
        res.status(401).send('Invalid username or password');
      } else {
        const user = result.rows[0];
        bcrypt.compare(password, user.password, (err, isMatch) => {
          if (err) {
            console.error(err);
            res.status(500).send('Error comparing password');
          } else if (isMatch) {
            // Successful login: Set a session cookie or store user info in a session store
            req.session.userId = user.id; // Example using a session store
            res.redirect('/dashboard.html');
          } else {
            res.status(401).send('Invalid username or password');
          }
        });
      }
    }
  );
});

app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});
