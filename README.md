# Sound Localisation

This project aims to build a simple sound localisation system using Python. The goal is to visually represent the direction of arrival (DOA) of real-time sound.

## Table of Content

- **Functions:** Contains all the algorithms (STFT, FD GCC, SRP, ...) used to calculate the direction of arrival (DOA). It is an edited version of the work and research cited below.
- **Visualization:** Contains all the code for plotting our simulations and other data.
  - 'one_source_in_time.py' and 'one_source_in_time_overlap.py' show an example of sound moving around the microphone's array. An arrow points to the sound source's location in real-time (= when the .wav file is playing). The files showcase a non-overlapping and overlapping window for the STFT respectively.
  - 'two_sources_in_time.py' and 'two_sources_in_time_overlap.py' show the localization of sound produced by 2 speakers in a room. Non-overlapping and overlapping window for the STFT respectively.
- **Sound_simulation:** Contains the code for simulating the room environment. 
  - 'simulation_moving_continuous_sound.py' plots the room setup of the example where sound is moving around the microphone array.
  - 'simulation_two_sources.py' plots the room setup of the example where 2 speakers at different angles are localized.
- **Videos_for_presentation:** Contains the videos that were used in the final presentation of our XR project.

## Standing on the Shoulders of Giants

Our project is based on the work and research of:

-       The beamforming algorithms:
        [1] T. Dietzen, E. De Sena, and T. van Waterschoot, "Low-Complexity
        Steered Response Power Mapping based on Nyquist-Shannon Sampling," in
        Proc. 2021 IEEE Workshop Appl. Signal Process. Audio, Acoust. (WASPAA 2021), New Paltz, NY, USA, Oct. 2021.
        https://github.com/bilgesu13/LC-SRP-python/blob/main/main.py
