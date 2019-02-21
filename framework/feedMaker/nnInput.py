import subprocess
from subprocess import call, Popen, PIPE, STDOUT
from PIL import Image
import numpy as np

def createSpectrogramImage(songPath,songDuration,picHeight=256,bw=True):
    """Produces a spectrogram of given song, saved as .PNG next to the audio file, also returns the numpy.ndarray version of it.
    This function implements FFmpeg that is installed separately and run via cmd.
    
    Parameters
    ----------
    songPath : `str`
    \tThe relative or full path of the song
    songDuration : `int`
    \tThe duration of the song in miliseconds, determines horizontal (width, left-right) shape size. One milisecond is one vertical line of pixels.
    picHeight : `int` ; default = `256`
    \tThe desired height (vertical, up-down) of output
    bw : `bool ; default = `True`
    \tDetermines the color output of the spectograph, grayscale if true.
    
    Return
    ------
    `numpy.ndarray` in the shape of ``(picHeight, songDuration+1)`` representing the image."""
    
    # Determines the output file name
    if '.mp3' in songPath: outname = songPath[:songPath.rindex('.mp3')] + '.png'
    else: outname = songPath + '.png'

    # Producing the spectrogram image based on the audio file
    call("ffmpeg -y -loglevel panic -hide_banner -nostats -i {0} -lavfi showspectrumpic=s={1}x{2} {3}".format(songPath,songDuration,picHeight,outname), stdout=PIPE)
    print("Spectrogram created, now cropping") # Confirms image production is finished

    # Image post-processing
    spectrogram = Image.open(outname).crop((141,64,141+songDuration,64+256))  # Cropping, because FFmpeg's spectrogram gives border, texts, and other fancy stuff we don't need
    if bw: spectrogram = spectrogram.convert('L') # If b/w colormap is desired, the image will be converted so.
    spectrogram.save(outname) # saving the image as .PNG next to the audio file
    print("Spectrogram is finished! saved as {0}".format(outname)) # Confirms the image procesing is finished

    return np.array(spectrogram)

def get_duration_ms(songPath):
    """Get the ceiling-tuned milisecond duration of a video or song using FFprobe that comes with FFmpeg installation.
    
    Parameters
    ----------
    songPath : str
    \tThe relative or full path of the song

    Return
    ------
    `int`, the milisecond duration of the song passed as parameter.
    """
    cmd = 'ffprobe -i {} -show_entries format=duration -v quiet -of csv="p=0"'.format(songPath)
    output = subprocess.check_output(
        cmd,
        shell=True, # Let this run in the shell
        stderr=STDOUT
    )
    # return round(float(output))  # ugly, but rounds your seconds up or down
    return int(np.ceil(float(output)*1000))

def spectrogramSplicer(spectrogram,interval,contexted=0,exportSplices=False):
    #print('interval = {0} :: {1}'.format(interval,type(interval)))
    height, width = spectrogram.shape
    diff = interval - (width % interval)
    padwidth = interval * contexted
    print ('diff = {0}\nwidth = {1}\npadwidth = {2}'.format(diff,width,padwidth))
    if contexted > 0:
        print('context multiplier :',contexted)
        print('before :',spectrogram.shape)
        leftpad = np.zeros((height,padwidth))
        rightpad = np.zeros((height,padwidth+diff))
        padded = np.concatenate((leftpad,spectrogram,rightpad),axis = 1)
        print('after :',padded.shape)
    elif diff > 0:
        print('nocontext but has diff')
        print('before :',spectrogram.shape)
        rightpad = np.zeros((height,diff))
        padded = np.concatenate((spectrogram,rightpad),axis = 1)
        print('after :',padded.shape)
    else:
        padded = spectrogram
    export = []
    #print(interval,contexted)
    for i in range(padwidth, padded.shape[1]-padwidth, interval):
        res = padded[:,i-padwidth:i+(interval*(contexted+1))].flatten().reshape((height*((2*padwidth)+interval),1))
        export.append(res)
    return export

def heatColorsetQuantizer(R,G,B):
    # Pivot points:
    # 1 -> Black
    # 2 -> R & B peaked (Purple)
    # 3 -> Red
    # 4 -> R & G peaked (Yellow)
    # 5 -> White
    
    if R < 256: # case 1->2
        return np.round(R/4)
    elif B == 0: # case 2->3 or 4->5
        if G == 0: # case 2->3
            return 64 + np.round((256-B)/4)
        else: # case 4->5
            return 192 + np.round(B/4)
    else: # case 3->4
        return 128 + np.round(G/4)