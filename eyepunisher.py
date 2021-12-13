import numpy as np
import os

'''Convert .eye files into numpy arrays - making them ready for analysis.'''

def eye2array(file, debug=False):
    '''Converts the .eye file to numpy array.'''
    #Open file and split into trials.
    with open(file, 'r') as f:
        string = f.read()
    strings = string.split('[Eye Sample Data (')[1:]

    #Remove metadata from each trial.
    for i in range(len(strings)):

        #Print trial number if debug is on.
        if debug:
            num_end = strings[i].find('of 101)]')-1
            num = int(strings[i][:num_end])
            print(num)

        #Split at the exact place. And seperate x,y,z coordinates.
        strings[i] = strings[i].split('.iml')
        strings[i] = strings[i][1][5:]
        strings[i] = strings[i].split('\n[Task Data]\n')[0]
        strings[i] = strings[i].split('\n')
        strings[i] = strings[i][1:] #Remove first entry, empty for some reason that I cannot be bothered to fix.

        #Convert each reading into numpy array
        for x in range(len(strings[i])):
            strings[i][x] = np.array(strings[i][x].split(), dtype=float)
        
        strings[i] = np.array(strings[i])
        #strings[i][:,2] = pupil diameter - Normalize between 0 and 1.
        strings[i][:,2] = (strings[i][:,2] - np.min(strings[i][:,2]))/np.ptp(strings[i][:,2])
        
    return np.array(strings)
            
def punish_all_eyes(folder, debug=False):
    '''Saves all files as numpy arrays in a dictionary, participant ID as key.'''
    all_eyes = {}
    files = os.listdir(folder)
    files = [x for x in files if x[0] != '.']

    #Loop through files in folder and convert
    for file in files:
        print(f'Converting {file}...')
        all_eyes[file[:-4]] = eye2array(os.path.join(folder, file), debug=debug)
        
        if debug:
            print(len(all_eyes[file[:-4]]), 'recordings.')
            

    return all_eyes
    

f = punish_all_eyes('Doves/RawData', debug=False)
