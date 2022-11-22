# EMGFiltering
This is the sample code for EMG filtering. Kindly note this codebase is get the concept correct first. IT IS NOT OPTIMIZED FOR SPEED. That may be done on later stages.


-> ⭐️ bandpassFilterAndMerge(data): This fucntion takes the data (list of array); and applied band-pass filter on it. Then, it merges 2 channel
paramenters into one, and returns it.
EG:
shortData = [
    [5, 6, 7, 3],
    [6, 6, 7, 8],
    [8, 2, 7, 7],
    [9, 5, 7, 3],
    [3, 4, 7, 4]
]
lowerLimit = 3; upperLimit = 7;
After Step 1:
shortData = [
    [5, 6, 7, 3],
    [6, 6, 7, 0],
    [0, 0, 7, 7],
    [0, 5, 7, 3],
    [3, 4, 7, 4]
]

After Step 2, 3 and 4: 
shortData = [
    [5.5, 5],
    [6, 7],
    [0, 7],
    [5, 5],
    [3.5, 5.5]
]

Step 5: How do we wanna minimize the channel value from the array with n-datasets? (which is equal to windowLength)
EG: How to return one data in each window length for each channel ? Should we average all the values of each channel and return that,
or, should we do some other algotithm? (need discussion with teacher / team).

Here, I have just did a common simple average. (not recommended. We have to modify his part)

Taking the last example and feeding that value here, this fucntion just makes an average of all Channel 1 and Channel 2 values, and returns it
EG: 
Input Data = [
    [5.5, 5],
    [6, 7],
    [0, 7],
    [5, 5],
    [3.5, 5.5]
]

Channel 1 = [5.5 + 6 + 0 + 5 + 3.5] / 5; Channel 2 = [5 + 7 + 7 + 5 + 5.5] / 5;
