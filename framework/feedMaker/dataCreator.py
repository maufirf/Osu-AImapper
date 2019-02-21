# Internal libraries
from subprocess import call, PIPE

# Third-party libraries
import numpy as np
from PIL import Image

# Local modules
import io_custom.mapRead as mr
import framework.feedMaker.nnInput as nip
import framework.feedMaker.nnOutput as nop

def create_dataset(songPath,beatmapPath,interval,contexted=0,makeCSV=False,CSVname=None):
    # Input data
    song_npa = nip.createSpectrogramImage(songPath, nip.get_duration_ms(songPath))
    song_npa_spliced = nip.spectrogramSplicer(song_npa,interval,contexted)
    # Output data
    beatmap_npa = nop.timeliner_std(mr.readObjects(beatmapPath,returnAsBeatmap=True))
    beatmap_npa_spliced = nop.timelineSplicer(beatmap_npa,interval)
    # Syncing data
    maxparts = np.min((len(song_npa_spliced),len(beatmap_npa_spliced)))

    # Handles the makeCSV flag, TODO complete
    if makeCSV:
        if CSVname is None: CSVname = songPath.replace('mp3','wav')
        pass

    # returns two tuples: (spliced-synced data), (unspliced data)
    return (song_npa_spliced[:maxparts], beatmap_npa_spliced[:maxparts]), (song_npa, beatmap_npa)