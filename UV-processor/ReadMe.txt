Author: Ryan Neville Hansen | Stellenbosch University
Email: 25088521@sun.ac.za
Created with assistance from Claude AI
---------------------------------------------------------------------------------------------------

UV Data Processing Tool
=====================

This tool helps process and normalize UV absorbance data from CSV files.

Requirements
-----------
- Python 3.x
- pandas
- numpy
- matplotlib
- scipy (for signal processing and curve fitting)

Installation
-----------
Method 1 - Automatic Installation (Recommended):
1. Double-click the `installer.bat` file
2. The installer will:
   - Check if Python is installed
   - Install required packages (pandas, numpy, matplotlib, scipy)
   - Create necessary directories
3. Wait for the installation to complete

Method 2 - Manual Installation:
1. Install Python 3.x from https://www.python.org/downloads/
   - Make sure to check "Add Python to PATH" during installation
2. Install required packages using pip:
   ```
   pip install pandas numpy matplotlib scipy
   ```

Usage
-----
1. Prepare your data:
   - Your CSV file should contain UV absorbance data
   - Each sample should have wavelength and absorbance columns
   - Sample names should be in the format: sample1, sample2, etc.
   - IMPORTANT: The CSV filename should not contain spaces. Use underscores instead (e.g., "uv_data_2024.csv" not "uv data 2024.csv")
   - When sample names repeat in the CSV, they should be suffixed with "_Cn" where n is an integer (e.g., "sample1", "sample1_C1", "sample1_C2", etc.)

2. Running the script:
   - Double-click `UV-organiser.py` or run from command line
   - You will be prompted for the following inputs:
     * Path to your CSV file (if it is in the same folder as the python script, then simply write its name)
     * Total run time in seconds
     * Time interval between readings in seconds
     * Whether to show the equation on rate plots (yes/no)
     * Type of curve fit to use:
       - Exponential (recommended for most cases)
       - Polynomial
       - Logarithmic

3. Output:
   The script creates several directories:
   - `processed_uv_data/`: Individual CSV files for each sample
   - `normalised_uv_data/`: Normalized versions of the data (includes correction values)
   - `normalised_plots/`: Normalized wavelength vs absorbance plots
   - `rate_plots/`: Time vs absorbance plots with:
     * Scatter plot of data points
     * Best fit line (exponential/polynomial/logarithmic)
     * R² value (measure of fit quality)
     * Initial rate
     * Optional equation of the fit
   - `initial_rates/`: Contains:
     * CSV file with initial rates for each sample
     * Image file showing the rates in a table format

   Each output file will have:
   - Wavelength values as the index
   - Absorbance values as columns
   - Time-based column headers (e.g., "0s", "30s", etc.)

How it Works
-----------
1. Data Processing:
   - Reads the input CSV file
   - Separates data for each sample
   - Creates individual dataframes for each sample
   - Saves processed data to separate CSV files

2. Data Normalization:
   - Finds the row with the smallest range of values
   - Calculates correction values
   - Subtracts correction values from corresponding columns
   - Saves normalized data to separate CSV files
   - Includes correction values in the CSV for reference

3. Rate Analysis:
   - Allows user to specify wavelength of maximum absorbance or automatically detects it
   - Creates time series plots
   - Fits selected curve type to data:
     * Exponential: y = a*exp(-b*x) + y0 (recommended for most cases)
     * Polynomial: y = ax³ + bx² + cx + d
     * Logarithmic: y = a*ln(x) + b
   - Calculates initial rate (derivative at t=0)
   - Saves rates to CSV file
   - Creates plots with statistical information

For any issues or questions, please contact the developer.
