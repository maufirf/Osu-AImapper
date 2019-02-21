class Beatmap:
    """The class that describes the whole Osu! `Beatmap` from .OSU file
    (apart from the `Storyboard` from .OSB file). Currently only works
    to render the beatmaps that are already made, not to make a new
    beatmap.
    Parameters
    ----------
    filepath:`str`
    \tThe .OSU file path to be parsed from."""
    def __init__(self, mapName, difficulty, timingPoints, hitObjects):
        self.mapName, self.difficulty, self.timingPoints, self.hitObjects =\
        (mapName, difficulty, timingPoints, hitObjects)

    def setAttrib(self, mapName, difficulty, timingPoints, hitObjects):
        self.mapName, self.difficulty, self.timingPoints, self.hitObjects =\
        (mapName, difficulty, timingPoints, hitObjects)