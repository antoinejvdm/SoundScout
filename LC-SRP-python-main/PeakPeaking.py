import numpy as np

def finde_max(array, window_size, ang):
    # Find the index of the maximum value in the array
    max_index = np.argmax(array)
    print(f"Max Index: {max_index}, Max Value: {array[max_index]}")

    # Ensure the window does not go out of bounds
    start_index = max(max_index - window_size, 0)
    end_index = min(max_index + window_size + 1, len(array))

    # Extract the sub-array excluding the window around the maximum value
    sub_array = np.concatenate((array[:start_index], array[end_index:]))
    
    # Find the index of the maximum value in the sub-array
    second_max_index = np.argmax(sub_array)
    print(f"Second Max Index in Sub-array: {second_max_index}, Value: {sub_array[second_max_index]}")

    # Adjust the second max index if needed
    if second_max_index >= start_index:
        second_max_index += (end_index - start_index)
    print(f"Second Max Index Adjusted: {second_max_index}, Value: {array[second_max_index]}")

    # Convert indices to Cartesian coordinates
    x_max = array[max_index] * np.cos(ang[max_index])
    y_max = array[max_index] * np.sin(ang[max_index])

    x_max2 = array[second_max_index] * np.cos(ang[second_max_index])
    y_max2 = array[second_max_index] * np.sin(ang[second_max_index])

    return [x_max, y_max, x_max2, y_max2]