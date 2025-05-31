"""
Author: Ryan Neville Hansen | Stellenbosch University
Email: 25088521@sun.ac.za
Created with assistance from Claude AI

This script processes UV absorbance data from CSV files, creating separate dataframes
for each sample and generating plots of the absorbance data.
"""

# ----- Importing libraries -------------------------------------------------------------------------

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
import plotly.graph_objects as go

# ----- Global variables -------------------------------------------------------------------------

global max_abs_row
max_abs_row = 0  # Global variable to store the row index of the maximum absorbance
global num_samples
num_samples = 0

# ----- Utility functions -------------------------------------------------------------------------

def inverse_exponential(x, a, b, y0):
                return -a * np.exp(-b * x) + y0

# ----- Processing functions -------------------------------------------------------------------------

def process_uv_data(input_file, run_time, interval) -> dict:
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Directory used to store the output files
    output_dir = 'output/processed_uv_data'
    
    # Get all column names
    all_columns = df.columns
    
    # Find unique sample names by looking at non-blank columns until we hit a "_c1" suffix
    # Or by getting the first 'num_samples' column names
    sample_names = []
    if (num_samples == 0):
        for col in all_columns:
            if ("Unnamed" not in col) and (col.strip()):  # Check if column name is not empty
                if col.endswith("_C1"):  # Stop when we hit a repeated sample
                    break
                sample_names.append(col)
    elif (num_samples >= 1):
        count = 0
        for col in all_columns:
            if ("Unamed" not in col):
                if (count >= num_samples):
                    break
                sample_names.append(col)

    
    # Calculate number of repeat experiments
    l = len(sample_names)  # number of unique samples
    N = (len(all_columns) // l) - 1  # number of repeat experiments
    
    # Drop the first row of the dataframe as it contains header information
    df = df.iloc[1:]
    
    # Convert all columns to float
    df = df.astype(float)
    
    # Store wavelengths from the first column
    wavelengths = df.iloc[:, 0].astype(int)
    
    # Create time points for column headers
    time_points = [f"{t}s" for t in range(0, int(run_time) + int(interval), int(interval))]
    
    # Dictionary to store all sample dataframes
    sample_dataframes = {}
    
    # Process each sample
    for i, sample_name in enumerate(sample_names):
        # Find all absorbance columns for this sample using the pattern (2i+1)+ln
        absorbance_indices = []
        for n in range(N + 1):  # n goes from 0 to N
            col_idx = (2 * (i+1) - 1) + 2*(l * n)
            if col_idx < len(all_columns):
                absorbance_indices.append(col_idx)
        
        
        if absorbance_indices:
            # Create a dictionary to store the data
            data_dict = {}
            for idx, time_point in zip(absorbance_indices, time_points[:len(absorbance_indices)]):
                data_dict[time_point] = df.iloc[:, idx].values
            
            # Create dataframe with wavelengths as index and absorbance columns
            sample_df = pd.DataFrame(data_dict, index=wavelengths)
            
            # Store in dictionary
            sample_dataframes[sample_name] = sample_df
            
            # Save to CSV
            output_file = os.path.join(output_dir, f'{sample_name}_uv_data.csv')
            sample_df.to_csv(output_file)
            print(f'Processed {sample_name} - saved to {output_file}')
    
    print()
    # Invert the order of the dictionary
    sample_dataframes = dict(reversed(list(sample_dataframes.items())))
    
    return sample_dataframes

def normalize_data(processed_dataframes) -> dict:
    # Directory used to store the output files
    output_dir = 'output/normalised_uv_data'
    
    # Dictionary to store the normalised dataframes
    normalised_dataframes = {}

    # Process each sample
    for sample_name, df in processed_dataframes.items():
        
        # Calculate the baseline correction values
        row_ranges = df.max(axis=1) - df.min(axis=1)
        idx = row_ranges.idxmin()
        min_range_row = df.loc[idx].copy()
        smallest_value = min_range_row.min()
        correction_values = min_range_row - smallest_value

        # Subtract correction values from corresponding columns
        df = df.subtract(correction_values)

        # Store the normalised dataframe
        normalised_dataframes[sample_name] = df

        # Create a copy of the dataframe for saving to CSV
        df_to_save = df.copy()
        # Add correction values as a new row
        df_to_save.loc['corr_values'] = correction_values

        # Save each normalised dataframe with correction values
        output_file = os.path.join(output_dir, f'{sample_name}_normalised.csv')
        df_to_save.to_csv(output_file)
        print(f'Saved normalized data for {sample_name} to {output_file}')

    print()
    return normalised_dataframes


def plot_absorbance_data(dataframes) -> None:
    # Directory used to store the plots
    plot_dir = 'output/normalised_plots'
    interactive_plot_dir = 'output/normalised_plots/interactive_plots'
    
    # Plot each sample
    for sample_name, df in dataframes.items():
        plt.figure(figsize=(10, 6))
        plotly_fig = go.Figure()
        
        # Plot each column (time point) with a different color
        for column in df.columns:
            plt.plot(df.index, df[column])
            plotly_fig.add_trace(go.Scatter(x=df.index, y=df[column], mode='lines', name=column))
        
        plt.xlabel('Wavelength (nm)')
        plt.ylabel('Absorbance')
        plt.title(f'Absorbance vs Wavelength for {sample_name}')
        plt.grid(True)

        plotly_fig.update_layout(title=f'Absorbance vs Wavelength for {sample_name}',
                                 xaxis_title='Wavelength (nm)',
                                 yaxis_title='Absorbance',
                                 showlegend = False)
        
        # Save the plot
        plot_file = os.path.join(plot_dir, f'{sample_name}_absorbance_plot.png')
        plt.savefig(plot_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f'Saved plot for {sample_name} to {plot_file}')

        plotly_fig.write_html(os.path.join(interactive_plot_dir, f'{sample_name}_absorbance_plot.html'))
        print(f'Saved interactive plot for {sample_name} to {os.path.join(interactive_plot_dir, f"{sample_name}_absorbance_plot.html")}')
    print()
    return

def determine_rate(dataframes, show_equation=False, fit_type='exponential') -> dict:
    # Directory used to store the plots
    plot_dir = 'output/rate_plots'
    rate_dir = 'output/initial_rates'
    interactive_plot_dir = 'output/rate_plots/interactive_plots'

    # Getting the max absorbance wavelength from the user
    print("\nYou can either inspect the plots and give the wavelngth of max absorbance, ")
    print("or have the program determine it from the very first sample.")
    print("Enter 0 to have the program determine it")
    max_abs_row = int(input("Enter the wavelength with the maximum absorbance (e.g., 260): "))
    print()

    # Find the wavelength with local maximum absorbance if not user-specified
    if max_abs_row == 0:
        # Get the first dataframe from the dictionary
        first_df = next(iter(dataframes.values()))
        max_values = first_df.max(axis=1)

        # Find local maxima in the absorbance values
        peaks, _ = find_peaks(max_values)

        # If there are multiple peaks, select the second one (local max)
        if len(peaks) > 1:
            max_abs_row = max_values.index[peaks[0]]
        else:
            # Fallback to the global maximum if no local max is found
            max_abs_row = max_values.idxmax()
        
        print(f"\nThe wavelength determined by the programme is:")
        print(f"{max_abs_row} nm")
        print()

    # Dictionary to store initial rates
    initial_rates = {}
    # order = int(input("Enter your choice (0/1/2): "))
    
    # Process each sample
    for sample_name, df in dataframes.items():
        # Find the row index for the wavelength
        row_idx = df.index.get_loc(max_abs_row)
        # Get the time series data (row of absorbance values)
        time_series = df.iloc[row_idx]


        # Convert time points to numeric values (remove 's' and convert to float)
        times = np.array([float(t.replace('s', '')) for t in time_series.index])
        absorbances = np.array(time_series.values)
        
        
        x_fit = np.linspace(min(times), max(times), 100)
        y_pred = None
        y_fit = None
        equation = None
        
        # Fit curve based on selected type
        if fit_type == 'polynomial':
            # Fit a 3rd degree polynomial
            coeffs = np.polyfit(times, absorbances, 3)
            poly = np.poly1d(coeffs)
            y_pred = poly(times)
            
            # Calculate derivative (rate) at t=0
            derivative = np.polyder(poly)
            initial_rate = derivative(0)
            
            # Generate points for smooth curve
            y_fit = poly(x_fit)
            
            # Create equation string
            if show_equation:
                equation = f"y = {coeffs[0]:.2e}x³ + {coeffs[1]:.2e}x² + {coeffs[2]:.2e}x + {coeffs[3]:.2e}"
            
        elif fit_type == 'logarithmic':
            # Fit logarithmic curve: y = a * ln(x) + b
            # Add small constant to times to avoid log(0)
            times_adj = times + 1e-10
            coeffs = np.polyfit(np.log(times_adj), absorbances, 1)
            a, b = coeffs
            
            # Calculate predictions
            y_pred = a * np.log(times_adj) + b
            
            # Calculate derivative (rate) at t=0
            initial_rate = a / 1e-10  # derivative of a*ln(x) is a/x
            
            # Generate points for smooth curve
            y_fit = a * np.log(x_fit + 1e-10) + b
            
            # Create equation string
            if show_equation:
                equation = f"y = {a:.2e}ln(x) + {b:.2e}"
            
        elif fit_type == 'exponential':
            # Calculate better initial parameter guesses
            # y0: estimate as the minimum value
            y0_guess = np.min(absorbances)
            
            # a: estimate as the difference between max and min values
            a_guess = np.max(absorbances) - y0_guess
            
            # b: estimate from the first few points using the slope
            # For y = a*exp(-b*x) + y0, the slope at t=0 is -a*b
            # We can estimate b from the initial slope
            initial_slope = (absorbances[1] - absorbances[0]) / (times[1] - times[0])
            b_guess = abs(initial_slope / a_guess) if a_guess != 0 else 0.1
            
            # Fit exponential curve using scipy's curve_fit with better initial guesses
            coeffs, _ = curve_fit(inverse_exponential, times, absorbances, 
                                p0=(a_guess, b_guess, y0_guess),
                                maxfev=20000)  # Increase max iterations for better fit
            a, b, y0 = coeffs

            # NOTE: This is a hardcoded solution to the fact that the exponential curve is not fitting correctly
            # Check here if there are any future problems
            if (b < 0 or a < 0):
                b = abs(b)
                a = abs(a)
            
            # Calculate predictions
            y_pred = inverse_exponential(times, a, b, y0)
            
            # Calculate derivative (rate) at t=0
            initial_rate = 1 * a * b  # derivative of -a*exp(-b*x) + y0 is a*b*exp(-b*x)
            
            # Generate points for smooth curve
            y_fit = inverse_exponential(x_fit, a, b, y0)
            
            # Create equation string
            if show_equation:
                equation = f"y = -{a:.2e}exp(-{b:.2e}x) + {y0:.2e}"
        
        # Calculate R-squared
        ss_tot = np.sum((absorbances - np.mean(absorbances))**2)
        ss_res = np.sum((absorbances - y_pred)**2)
        r_squared = 1 - (ss_res / ss_tot)
        
        # Store initial rate
        initial_rates[sample_name] = initial_rate
        
        # Create the plot
        plt.figure(figsize=(10, 6))
        plotly_fig = go.Figure()
        
        # Plot scatter points
        plt.scatter(times, absorbances, color='blue', label='Data points')
        plotly_fig.add_trace(go.Scatter(x=times, y=absorbances, mode='markers', name='Data points'))
        
        # Plot best fit line
        plt.plot(x_fit, y_fit, 'r-', label='Best fit line')
        plotly_fig.add_trace(go.Scatter(x=x_fit, y=y_fit, mode='lines', name='Best fit line'))
        
        # Add fit information to plot
        fit_info = f"R² = {r_squared:.4f}\nInitial rate = {initial_rate:.2e} s⁻¹"
        if show_equation:
            fit_info = f"{equation}\n{fit_info}"     

        plt.text(0.02, 0.98, fit_info, 
                transform=plt.gca().transAxes, 
                verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        plt.xlabel('Time (seconds)')
        plt.ylabel('Absorbance')
        plt.title(f'Absorbance vs Time for {sample_name}\nMax absorbance at {max_abs_row} nm')
        plt.grid(True)
        
        plotly_fig.update_layout(title=f'Absorbance vs Time for {sample_name}\nMax absorbance at {max_abs_row} nm',
                                 xaxis_title='Time (seconds)',
                                 yaxis_title='Absorbance',
                                 showlegend = False)
        
        # Save the plot
        plot_file = os.path.join(plot_dir, f'{sample_name}_rate_plot.png')
        plt.savefig(plot_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f'Saved rate plot for {sample_name} to {plot_file}')

        plotly_fig.write_html(os.path.join(interactive_plot_dir, f'{sample_name}_rate_plot.html'))
        print(f'Saved interactive plot for {sample_name} to {os.path.join(interactive_plot_dir, f"{sample_name}_rate_plot.html")}')
    print()
    # Save initial rates to CSV
    rates_df = pd.DataFrame({'K': initial_rates})
    rates_csv_file = os.path.join(rate_dir, 'initial_rates.csv')
    rates_df.to_csv(rates_csv_file)
    print(f'Saved initial rates to {rates_csv_file}')

    # Save the initial rates as an image
    fig, ax = plt.subplots(figsize=(8, len(initial_rates) * 0.4 + 1))  # Reduced height multiplier and base height
    ax.axis('tight')
    ax.axis('off')
    
    # Create table
    table = ax.table(cellText=rates_df.values,
                    rowLabels=rates_df.index,
                    colLabels=rates_df.columns,
                    cellLoc='center',
                    loc='center',
                    bbox=[0, 0, 1, 1])
    
    # Adjust table properties
    table.auto_set_font_size(False)
    table.set_fontsize(12)  # Increased base font size
    table.scale(1.2, 1.2)  # Reduced vertical scaling
    
    # Adjust cell heights
    for cell in table._cells:
        table._cells[cell].set_height(0.3)  # Reduced cell height
    
    # Save figure
    rates_image_file = os.path.join(rate_dir, 'initial_rates.png')
    plt.savefig(rates_image_file, bbox_inches='tight', dpi=300)
    plt.close()


# ----- Main method -------------------------------------------------------------------------------------

    # Get the CSV file path from user
def main():
    csv_file = input("Enter the path to your CSV file: ").strip('"')

    # Validate the path
    if not os.path.isfile(csv_file):
        print("Error: File does not exist.")
        return

    # Set base_dir to the directory containing the CSV file
    base_dir = os.path.dirname(os.path.abspath(csv_file))

    # Optionally change working directory to base_dir (optional)
    os.chdir(base_dir)

    # Create directories relative to the CSV file's location
    os.makedirs(os.path.join(base_dir, 'output'), exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'output/processed_uv_data'), exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'output/normalised_uv_data'), exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'output/normalised_plots'), exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'output/rate_plots'), exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'output/normalised_plots/interactive_plots'), exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'output/rate_plots/interactive_plots'), exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'output/initial_rates'), exist_ok=True)

    print("Directories made successfully in:\n", base_dir)
    print()

    # Get run time and interval from user
    run_time = float(input("Enter the total run time of your UV experiment in seconds: "))
    interval = float(input("Enter the time interval between readings in seconds: "))

    # Get number of samples from the user
    print("\nPlease enter the number of samples that you analyzed,")
    print("Otherwise enter 0, and the programme will determine how many there are.")
    num_samples = int(input("Enter the number of samples:"))
    
    # Get user preference for showing equation
    show_equation = input("Do you want to show the equation on the rate plots? (yes/no): ").lower() == 'yes'
    
    # Get user preference for fit type
    print("\nChoose the type of curve fit:")
    print("1. Inverse exponential (recommended for most cases)")
    print("2. Polynomial")
    print("3. Logarithmic (won't work if neg abs values are present)")
    fit_choice = input("Enter your choice (1/2/3): ")
    print()
    
    fit_type = {
        '1': 'exponential',
        '2': 'polynomial',
        '3': 'logarithmic'
    }.get(fit_choice, 'exponential')  # Default to exponential if invalid choice
    
    # Process the data
    processed_dataframes = process_uv_data(csv_file, run_time, interval)

    # Normalize the data
    normalized_dataframes = normalize_data(processed_dataframes)
    
    # Create plots for normalized data
    plot_absorbance_data(normalized_dataframes)
    
    # Create rate plots for normalized data and determine initial rates
    determine_rate(normalized_dataframes, show_equation=show_equation, fit_type=fit_type)
    
    print("\nProcessing complete! Check the following directories for results:")
    print("- processed_uv_data/: Individual CSV files for each sample")
    print("- normalised_uv_data/: Normalized versions of the data")
    print("- normalised_plots/: Normalized wavelength vs absorbance plots")
    print("- rate_plots/: Time vs absorbance plots with rate analysis")
    print("- initial_rates/: Contains initial rates CSV and image files")

# ----- Running the programme -------------------
if __name__ == "__main__":
    main()
