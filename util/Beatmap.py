import io_custom.mapRead as mr

class Beatmap:
    def __init__(self, filepath='dump/Dan Salvato - Your Reality (Nozhomi) [Just You].osu'):
        self.mapName, self.difficulty, self.timingPoints, self.hitObjects = mr.readObjects(filepath,parent_map=self)