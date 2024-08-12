# Password Manager

A simple, secure, and visually appealing desktop password manager built using Python and Tkinter, with MongoDB for data storage. This application allows users to securely store and manage their passwords with a master password for added security.

## Features

- **Master Password Protection:** Secure your password vault with a master password.
- **Add, View, Search, Update, and Delete Passwords:** Manage your passwords with ease.
- **Password Strength Validation:** Ensures that your passwords meet security criteria.
- **Export Passwords:** Backup your passwords to a text file.
- **User-Friendly Interface:** A clean, modern UI designed for ease of use.

## Installation

### Prerequisites

- Python 3.x
- MongoDB (running locally or on a server) used MongoDB Compass

## Usage

1. **Set a Master Password:**
   On first run, you'll be prompted to set a master password. This password will be required to access the app in the future.

2. **Manage Passwords:**
   Add, view, search, update, or delete your passwords through the interface.

3. **Export Passwords:**
   Backup your passwords to a text file for safekeeping.

## Project Structure

password-manager/
│
├── database.py # MongoDB connection and operations
├── encryption.py # Encryption and decryption logic
├── gui.py # Main GUI application
├── app.py # Application entry point
├── requirements.txt # Python dependencies
└── assets/
└── # Company chosen application icon

## Technologies Used

- **Python 3.x**
- **Tkinter:** For the GUI.
- **MongoDB:** For secure password storage.
- **cryptography:** For encrypting and decrypting passwords.

