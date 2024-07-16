from src.data_processing import download_and_preprocess_data
from src.plot_generation import generate_plot

def main():
    # Example station ID for Kuwait; replace with desired station ID
    station_id = '40582'

    # Download and preprocess data
    download_and_preprocess_data(station_id)

    # Generate and display plot
    generate_plot()

if __name__ == '__main__':
    main()
