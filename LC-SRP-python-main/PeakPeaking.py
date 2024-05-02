import numpy as np

def finde_max(array, window_size, ang):
    # Find the index of the maximum value in the array
    max_index = np.argmax(array)
    
    # Extract the sub-array excluding the window around the maximum value
    sub_array = np.concatenate((array[0:max_index - window_size],
                                 array[max_index + window_size + 1:len(array)]))
    
    # Find the index of the maximum value in the sub-array
    second_max_index = np.argmax(sub_array)
    
    # If the index of the second maximum value is greater than or equal to max_index,
    # adjust it to account for the excluded window
    if second_max_index + window_size >= max_index:
        second_max_index += 2*window_size + 1
    
    x_max = array[max_index] * np.cos(ang[max_index])
    y_max = array[max_index] * np.sin(ang[max_index])

    x_max2 = array[second_max_index] * np.cos(ang[second_max_index])
    y_max2 = array[second_max_index] * np.sin(ang[second_max_index])
    # Return the index of the second maximum value

    return [x_max,y_max,x_max2,y_max2]