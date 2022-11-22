# This is the sample code for EMG filtering.
# Kindly note this codebase is get the concept correct first. IT IS NOT OPTIMIZED FOR SPEED.
# That may be done on later stages.

#Test Data, indexes 0 & 1 are from Muscle Group A - CHANNEL 1; indexes 2 & 3 are from Muscle Group B - CHANNEL 2;
SensorData =  [
    [119.9375, 114.6875, 483.3125, 481.25],
    [110.125, 105.875, 489.75, 493.125],
    [103.9375, 101.5625, 492.625, 485.375],
    [97.125, 90.9375, 487.125, 484.1875],
    [89.875,90.3125,456.625,432.6875],
    [86.6875,85.5,434.4375,418.4375],
    [83.5,78.125,420.8125,440.1875],
    [76.1875,76.75,432.8125,434.625],
    [74.6875,73.0,410.5,407.9375],
    [69.8125,66.5,410.75,400.25],
    [61.4375,56.3125,406.375,398.5625],
    [52.0625,52.375,427.6875,423.4375],
    [52.1875,52.75,416.125,401.0],
    [55.4375,55.9375,367.0,383.3125],
    [74.125,68.125,376.4375,370.6875],
    [55.25,41.8125,364.9375,367.8125],
    [36.6875,34.625,358.1875,353.75],
    [29.375,19.8125,361.5,310.4375],
    [19.4375,14.375,310.5625,312.8125],
    [42.6875,31.75,308.6875,315.6875],
    [47.25,283.75,309.875,294.25],
    [363.6875,306.625,272.375,261.875],
    [253.75,190.75,238.75,281.75],
    [166.625,162.375,318.75,311.125],
    [149.0,141.3125,310.4375,304.4375],
    [141.8125,148.3125,303.25,314.0625],
    [136.6875,161.0,307.1875,300.9375],
    [160.0,134.0625,289.0625,299.75],
    [112.125,103.3125,309.5,309.1875],
    [89.0625,78.3125,309.9375,309.625],
    [64.4375,71.4375,310.4375,318.5625],
    [64.1875,56.5625,314.9375,315.1875],
    [47.875,42.25,306.5625,303.4375],
    [31.875,27.1875,297.875,296.625],
    [28.0,28.3125,288.4375,288.8125],
    [24.625,26.0625,285.5625,278.0625],
    [25.375,17.4375,289.9375,283.0],
    [9.0,9.5,281.9375,271.8125],
    [8.75,9.6875,277.25,269.8125],
    [8.1875,5.4375,265.25,274.9375],
    [4.75,2.625,269.875,259.75],
    [2.75,1.8125,259.3125,257.6875],
    [2.4375,5.4375,259.9375,249.375],
    [2.5,2.0,247.8125,250.8125],
    [2.125,1.6875,247.5625,247.625],
    [2.5625,2.3125,245.625,241.0625],
    [2.5625,6.625,231.9375,223.0],
    [6.9375,7.5,219.25,216.125],
    [6.375,5.375,219.25,221.8125],
    [10.125,10.3125,207.5,199.75],
    [8.875,9.8125,195.125,192.6875],
    [13.75,18.25,196.125,199.75],
    [17.1875,18.0,199.25,203.0625],
    [24.3125,22.8125,189.625,183.75],
    [17.125,13.0,179.8125,180.75],
    [13.0,16.875,167.3125,173.5],
    [19.3125,21.4375,168.875,168.375],
    [20.1875,18.0625,164.1875,166.625],
    [16.5,13.1875,165.9375,165.0625],
    [12.0625,9.5625,154.3125,139.8125],
    [7.375,6.8125,137.5,139.4375],
    [8.75,3.8125,142.8125,145.9375],
    [2.6875,2.4375,150.9375,153.125],
    [10.125,19.1875,147.1875,140.625],
    [37.5625,42.9375,132.5625,100.5],
    [37.1875,60.3125,90.3125,102.1875],
    [44.3125,78.875,100.4375,62.125],
    [132.75,87.1875,49.375,52.0625],
    [144.0625,118.0,59.0625,63.8125],
    [122.3125,66.3125,37.375,27.375],
    [58.0625,60.625,107.5625,70.9375],
]
filteredCollectionData = []

#This is short sample data used in example.
shortData = [
    [5, 6, 7, 3],
    [6, 6, 7, 8],
    [8, 2, 7, 7],
    [9, 5, 7, 3],
    [3, 4, 7, 4]
]

#May be changed later, or alloted dynamically using ~10% and ~45% of the original sample rate.
# 4 and 7 is used for 'shortData'. use '40' and '200' for 'SensorData'
lowerThreshold = 4 #(40) 
upperThreshold = 7 #(200)

#The 'SensorData' here is being passed as an array of arrays. Please modify this as per requirements.
#Kindly call this fucntion once at the end of every window cycle. (if your cycle is 20, call this fucntion everytime after you collect 20 datasets)
def bandpassFilterAndMerge (data):
    counter = 0;
    while(counter < len(data)):
        #Step 1: Simple BandPass Filtering
        #As per documentation, with sample rate of 512, cut off should be around 40 and 200.
        filteredSingleData = [ 0 if (item < lowerThreshold or item > upperThreshold) else item for item in data[counter]]
        tempo = [];

        #Step 2: Merging 2 data into 1 for each channel (AVG)
        # If each item of channel has values after filtering, we take their avegrage. If either item is Zero after aftering, we just take the availble value.
        if (filteredSingleData[0] == 0 or filteredSingleData[1] == 0):
            tempo.append(filteredSingleData[0] + filteredSingleData[1])
        else:
            tempo.append((filteredSingleData[0] + filteredSingleData[1]) / 2)

        if (filteredSingleData[2] == 0 or filteredSingleData[3] == 0):
            tempo.append(filteredSingleData[2] + filteredSingleData[3])
        else:
            tempo.append((filteredSingleData[2] + filteredSingleData[3]) / 2)

        #Step 3: Add this to the main return array
        filteredCollectionData.append(tempo)

        #Step 4: Increment of counter
        counter = counter + 1
    return (filteredCollectionData)


# -> ⭐️ bandpassFilterAndMerge(data): This fucntion takes the data (list of array); and applied band-pass filter on it. Then, it merges 2 channel
# paramenters into one, and returns it.
# EG:
# shortData = [
#     [5, 6, 7, 3],
#     [6, 6, 7, 8],
#     [8, 2, 7, 7],
#     [9, 5, 7, 3],
#     [3, 4, 7, 4]
# ]
# lowerLimit = 3; upperLimit = 7;
# After Step 1:
# shortData = [
#     [5, 6, 7, 3],
#     [6, 6, 7, 0],
#     [0, 0, 7, 7],
#     [0, 5, 7, 3],
#     [3, 4, 7, 4]
# ]
# After Step 2, 3 and 4: 
# shortData = [
#     [5.5, 5],
#     [6, 7],
#     [0, 7],
#     [5, 5],
#     [3.5, 5.5]
# ]

# Step 5: How do we wanna minimize the channel value from the array with n-datasets? (which is equal to windowLength)
# EG: How to return one data in each window length for each channel ? Should we average all the values of each channel and return that,
# or, should we do some other algotithm? (need discussion with teacher / team).

# Here, I have just did a common simple average. (not recommended. We have to modify his part)

def ValuePerWindow (data):
    counter = 0
    channel1 = 0
    channel2 = 0

    while (counter < len(data)):
        channel1 = data[counter][0] + channel1
        channel2 = data[counter][1] + channel2
        counter = counter + 1
    
    channel1 = channel1 / len (data)
    channel2 = channel2 / len (data)

    return (channel1, channel2)

# Taking the last example and feeding that value here, this fucntion just makes an average of all Channel 1 and Channel 2 values, and returns it
# EG: 
# Input Data = [
#     [5.5, 5],
#     [6, 7],
#     [0, 7],
#     [5, 5],
#     [3.5, 5.5]
# ]

# Channel 1 = [5.5 + 6 + 0 + 5 + 3.5] / 5; Channel 2 = [5 + 7 + 7 + 5 + 5.5] / 5;



processedArray = bandpassFilterAndMerge(shortData) #Pass the data array here
finalValue = ValuePerWindow(processedArray)
print (finalValue)
