"""
6.101 Lab:
Audio Processing
"""

import os
import wave
import struct
# import typing  # optional import
# import pprint  # optional import

# No additional imports allowed!


def backwards(sound):
    """
    Returns a new sound containing the samples of the original in reverse
    order, without modifying the input sound.

    Args:
        sound: a dictionary representing the original mono sound

    Returns:
        A new mono sound dictionary with the samples in reversed order
    """
    
    new_sound = sound.copy()
    new_sound["samples"] = new_sound["samples"][::-1]
    return new_sound     


def mix(sound1, sound2, p):
    """
    mix 2 good sounds
    """
    if ("rate" in sound1) is False or ("rate" in sound2) is False or (sound1["rate"]==sound2["rate"]) is False:

        print("no")
        return

    r=sound1["rate"]# get rate
    sound1=sound1["samples"]
    sound2=sound2["samples"]
    if len(sound1)<len(sound2):l=len(sound1)
    elif len(sound2)<len(sound1):l=len(sound2)
    elif len(sound1)==len(sound2):l=len(sound1)
    else:
        print("whoops")
        

    s  = []
    x  =  0
    while x<=l:
        s2,s1 = p*sound1[x], sound2[x]*(1 - p)
        s.append(s1+s2)# add sounds
        x+= 1
        if x ==l:# end
            break



    return {"rate": r, "samples": s}# return new sound


def echo(sound, num_echoes, delay, scale):
    """
    Compute a new sound consisting of several scaled-down and delayed versions
    of the input sound. Does not modify input sound.

    Args:
        sound: a dictionary representing the original mono sound
        num_echoes: int, the number of additional copies of the sound to add
        delay: float, the amount of seconds each echo should be delayed
        scale: float, the amount by which each echo's samples should be scaled

    Returns:
        A new mono sound dictionary resulting from applying the echo effect.
    """
    sample_delay = round(delay * sound["rate"])
    start_index = 0
    count_echo = 0
    new_sound = sound['samples'][:]
    new_sound.extend([0 for x in range(num_echoes*sample_delay) if True])                     
    while count_echo < num_echoes:
        start_index += sample_delay
        j = 0
        count_echo += 1
       
        
        
        

        for i in range(start_index, start_index + len(sound['samples'])):
            
            new_sound[i] +=  (sound['samples'][j])*(scale**count_echo)
                       
            j += 1
    new_sound_fin = sound.copy()
    new_sound_fin['samples'] = new_sound   
    return new_sound_fin    


def pan(sound):
    left_scale = [1 - (i/(len(sound["left"])-1)) for i in range(len(sound["left"]))]
    right_scale = left_scale[::-1]
    sound_new = sound.copy()
    sound_new["left"] = [left_scale[i]*(sound["left"][i]) for i in range(len(sound["left"]))]
    sound_new["right"] = [right_scale[i]*(sound["right"][i]) for i in range(len(sound["left"]))]              
    return sound_new

def remove_vocals(sound):
    new_sound = {"rate": sound["rate"], "samples" : [sound["left"][i] - sound["right"][i] for i in range(len(sound["left"]))]}
    return new_sound


# below are helper functions for converting back-and-forth between WAV files
# and our internal dictionary representation for sounds


def load_wav(filename, stereo=False):
    """
    Given the filename of a WAV file, load the data from that file and return a
    Python dictionary representing that sound
    """
    file = wave.open(filename, "r")
    chan, bd, sr, count, _, _ = file.getparams()

    assert bd == 2, "only 16-bit WAV files are supported"

    out = {"rate": sr}

    if stereo:
        left = []
        right = []
        for _ in range(count):
            frame = file.readframes(1)
            if chan == 2:
                left.append(struct.unpack("<h", frame[:2])[0])
                right.append(struct.unpack("<h", frame[2:])[0])
            else:
                datum = struct.unpack("<h", frame)[0]
                left.append(datum)
                right.append(datum)

    if stereo:
        out["left"] = [i / (2**15) for i in left]
        out["right"] = [i / (2**15) for i in right]
    else:
        samples = []
        for _ in range(count):
            frame = file.readframes(1)
            if chan == 2:
                left = struct.unpack("<h", frame[:2])[0]
                right = struct.unpack("<h", frame[2:])[0]
                samples.append((left + right) / 2)
            else:
                datum = struct.unpack("<h", frame)[0]
                samples.append(datum)

        out["samples"] = [i / (2**15) for i in samples]

    return out


def write_wav(sound, filename):
    """
    Given a dictionary representing a sound, and a filename, convert the given
    sound into WAV format and save it as a file with the given filename (which
    can then be opened by most audio players)
    """
    # make folders if they do not exist
    directory = os.path.realpath(os.path.dirname(filename))
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    outfile = wave.open(filename, "w")

    if "samples" in sound:
        # mono file
        outfile.setparams((1, 2, sound["rate"], 0, "NONE", "not compressed"))
        out = [int(max(-1, min(1, v)) * (2**15 - 1)) for v in sound["samples"]]
    else:
        # stereo
        outfile.setparams((2, 2, sound["rate"], 0, "NONE", "not compressed"))
        out = []
        for left, right in zip(sound["left"], sound["right"]):
            left = int(max(-1, min(1, left)) * (2**15 - 1))
            right = int(max(-1, min(1, right)) * (2**15 - 1))
            out.append(left)
            out.append(right)

    outfile.writeframes(b"".join(struct.pack("<h", frame) for frame in out))
    outfile.close()


if __name__ == "__main__":
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place to put your
    # code for generating and saving sounds, or any other code you write for
    # testing, etc.

    # here is an example of loading a file (note that this is specified as
    # sounds/hello.wav, rather than just as hello.wav, to account for the
    # sound files being in a different directory than this file)
    mountain = load_wav("sounds/lookout_mountain.wav", stereo = True)
    

    write_wav(remove_vocals(mountain), "mountain.wav")
