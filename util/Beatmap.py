import io_custom.mapRead as mr

class Beatmap:
    """The class that describes the whole Osu! `Beatmap` from .OSU file
    (apart from the `Storyboard` from .OSB file). Currently only works
    to render the beatmaps that are already made, not to make a new
    beatmap.
    Parameters
    ----------
    filepath:`str`
    \tThe .OSU file path to be parsed from."""
    def __init__(self, filepath='dump/Dan Salvato - Your Reality (Nozhomi) [Just You].osu'):
        self.mapName, self.difficulty, self.timingPoints, self.hitObjects = mr.readObjects(filepath,parent_map=self)