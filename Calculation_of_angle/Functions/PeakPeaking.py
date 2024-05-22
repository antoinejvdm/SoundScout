import numpy as np

def finde_max(array, window_size, ang):
    # Find the index of the maximum value in the array
    max_index = np.argmax(array)

    # Ensure the window does not go out of bounds
    start_index = max(max_index - window_size, 0)
    end_index = min(max_index + window_size + 1, len(array))

    # Extract the sub-array excluding the window around the maximum value
    sub_array = np.concatenate((array[:start_index], array[end_index:]))
    
    # Find the index of the maximum value in the sub-array
    second_max_index = np.argmax(sub_array)

    # Adjust the second max index if needed
    if second_max_index >= start_index:
        second_max_index += (end_index - start_index)


    return [max_index, second_max_index]