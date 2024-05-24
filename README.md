# Sound Localisation

This project aims to build a simple sound localisation system using Python. The goal is to visually represent the direction of arrival (DOA) of real-time sound.

## Table of Content
-       Audio_simulations: Contains all the .wav files used in the project
-       CSV_files: Contains all the files containing the coordinates of the virtual microphone and sound source setup in CSV format
-       Functions: Contains all the algorithms (STFT, FD GCC, SRP, ...) used to calculate the direction of arrival (DOA). It is an edited version of the work and research cited below.
-       Visualization: Contains all the code for plotting our simulations and other data.
-       Videos_for_presentation: Contains the videos that were used in the final presentation of our XR project.

## Standing on the Shoulders of Giants

Our project is based on the work and research of:

-       The beamforming algorithms:
        [1] T. Dietzen, E. De Sena, and T. van Waterschoot, "Low-Complexity
        Steered Response Power Mapping based on Nyquist-Shannon Sampling," in
        Proc. 2021 IEEE Workshop Appl. Signal Process. Audio, Acoust. (WASPAA 2021), New Paltz, NY, USA, Oct. 2021.
        https://github.com/bilgesu13/LC-SRP-python/blob/main/main.py
