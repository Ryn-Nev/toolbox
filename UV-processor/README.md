# UV Absorbance Data Processor

A Python script for processing and analyzing raw UV absorbance data from a CSV file. This tool works by separating data the raw data into their respective samples, normalizing it, and generating various plots and performing rate analyses.

## Installation

1. Download and run the `UV_python_installer.bat` script
2. The installer will:
   - Install Python and required libraries
   - Download this script from GitHub
   - Add necessary files to your system PATH
   - Create a convenient command-line shortcut

## Usage

1. Navigate to the folder containing your UV absorbance data CSV file
2. Open Command Prompt in that folder
3. Type `UVP` and press Enter
4. Follow the prompts to:
   - Enter the path to your CSV file
   - Specify the total run time (in seconds)
   - Enter the time interval between readings (in seconds)
   - Specify the number of samples (or enter 0 for automatic detection)
   - Choose whether to show equations on rate plots
   - Select the type of curve fit (exponential, polynomial, or logarithmic)

## Output

The script will create several output directories containing:
- Processed UV data (CSV files)
- Normalized data
- Wavelength vs absorbance plots
- Interactive HTML plots
- Rate analysis plots
- Initial rates data

All outputs will be organized in the `output` folder within your working directory.

## Requirements

- Windows operating system
- Internet connection (for initial installation)
- CSV files containing UV absorbance data

## Support

For questions or issues, please contact:
- Author: Ryan Neville Hansen
- Email: 25088521@sun.ac.za
- Institution: Stellenbosch University 