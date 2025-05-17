Author: Ryan Neville Hansen | Stellenbosch University
Email: 25088521@sun.ac.za
Created with assistance from Claude AI
---------------------------------------------------------------------------------------------------
# Unzipper
==========
A simple Python script to extract ZIP files to folders with the same name.

## Features
-----------

- Extract ZIP files to folders with matching names
- Option to delete original ZIP files after extraction
- Can be run from any directory after installation
- Works on both Windows and macOS
- Windows: Right-click context menu integration for ZIP files

## Prerequisites

- Windows or macOS operating system
- Administrator privileges (for installation)
- Internet connection (for Python installation if needed)
- No administrator privileges required

## Installation

### Windows

1. Download or clone this repository
2. Double-click `installation/Windows/install.bat`
3. The installer will:
   - Install Python 3.11.7 if not already installed
   - Set up pip if needed
   - Install required packages (pandas, numpy, matplotlib, scipy)
   - Add the Unzipper to your PATH
4. You can now run the Unzipper from any directory by typing `Unzipper.py` in the command line

To uninstall:
1. Double-click `installation/Windows/remove_from_path.bat`
2. Follow the on-screen instructions

### macOS

1. Download or clone this repository
2. Open Terminal and navigate to the repository directory
3. Make the installer executable:
   ```bash
   chmod +x installation/macOS/macOS_installer.sh
   ```
4. Run the installer:
   ```bash
   ./installation/macOS/macOS_installer.sh
   ```
5. The installer will:
   - Install Python 3.11.7 if not already installed
   - Set up pip if needed
   - Install required packages (pandas, numpy, matplotlib, scipy)
   - Add the Unzipper to your PATH
6. You may need to restart your terminal or run `source ~/.zshrc` (or `source ~/.bash_profile` for bash) for changes to take effect
7. You can now run the Unzipper from any directory by typing `python3 Unzipper.py` in the terminal

To uninstall:
1. Run the uninstallation script:
   ```bash
   ./installation/macOS/remove_from_path.sh
   ```
2. Restart your terminal or run `source ~/.zshrc` (or `source ~/.bash_profile` for bash) for changes to take effect

## Usage
--------

### Command Line

1. Navigate to the directory containing your ZIP files
2. Run the script:
   - Windows: `Unzipper.py`
   - macOS: `python3 Unzipper.py`
3. Follow the prompts to:
   - Enter the directory path (or '0' for current directory)
   - Choose whether to delete original ZIP files after extraction

### Direct File Extraction

You can also extract a specific ZIP file by providing its path as an argument:
- Windows: `Unzipper.py path/to/file.zip`
- macOS: `python3 Unzipper.py path/to/file.zip`

### Windows Context Menu

After installation, you can:
1. Right-click on any ZIP file in Windows Explorer
2. Select "Extract with Unzipper"
3. A command prompt will open and automatically extract the ZIP file

## Troubleshooting

### Windows
- If you get "Python is not recognized", try restarting your command prompt
- If the context menu doesn't appear, run `installation/Windows/add_context_menu.bat`

### macOS
- If you get "command not found", try restarting your terminal
- If Python installation fails, you can install it manually from python.org
- If Homebrew installation fails, visit https://brew.sh/ for manual installation

## License

This project is open source and available under the MIT License.

