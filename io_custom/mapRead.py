"""This is the module that responsible to aid the input and output
process of this whole program"""

# Local modules
import util.HitObject as ho
import util.TimingPoint as tp
import util.Difficulty as di
import util.Beatmap as bm

# Built-in library modules
import math

def readObjects(filepath='dump/Dan Salvato - Your Reality (Nozhomi) [Just You].osu', grouped=False, returnAsBeatmap=False):
    """Reads the given .OSU file from `filepath`, then imports them
    into the program to be processed. If `parent_map` is given, it will
    assign each of the objects to unite on the given map reference.
    Parameters
    ----------
    filepath : `str`
    \tThe .OSU file path that is going to be rendered
    grouped : `bool`
    \tIf True, the returned HitObjects list will be cached to appropriate sublist synced to their TimingPoint region
    parent_map : `Beatmap`
    \tThe beatmap that is going to be reference as uniform"""
    parent_map = bm.Beatmap(None,None,None,None)
    fo = open(filepath,'r',encoding='utf-8')
    flist = [x.replace('\n','') for x in fo.readlines()]
    mapName = fo.name
    fo.close()
    # == DIFFICULTY : Difficulty ==
    difficultyHeaderIdx = flist.index('[Difficulty]')
    eventsHeaderIdx = flist.index('[Events]')
    difQueries = [float(x.split(':')[1]) for x in flist[difficultyHeaderIdx+1:eventsHeaderIdx-1]]
    difficulty = di.Difficulty(difQueries,parent_map=parent_map)
    # == TIMING POINTS : List[TimingPoint] ==
    timingPointsHeaderIdx = flist.index('[TimingPoints]')
    coloursHeaderIdx = flist.index('[Colours]')
    prev = None; timingPoints = []
    for i in range(timingPointsHeaderIdx+1,coloursHeaderIdx-2):
        obj = tp.TimingPoint(flist[i],prev_tp=prev,parent_map=parent_map)
        if type(prev) is tp.TimingPoint: prev.next_tp=obj
        prev = obj
        timingPoints.append(obj)
    # == HIT OBJECTS : List[HitObject(Circle, Slider, Spinner, or ManiaHold)] ==
    hitObjectHeaderIdx = flist.index('[HitObjects]')
    hitObjects = [ho.HitObject.wrap(x,parent_map=parent_map) for x in flist[hitObjectHeaderIdx+1:]]        
    prev = None
    for obj in hitObjects:
        obj.prev_ho = prev
        if prev is not None: prev.next_ho = obj
    # == 'grouped' parameter ==
    if grouped:
        hitObjectsGroups = [[] for i in range(len(timingPoints))]
        for hitObject in hitObjects:
            hitObjectsGroups[timingPoints.index(\
                tp.TimingPoint.find_region(timingPoints,hitObject.time)\
            )].append(hitObject)
        parent_map.setAttrib(mapName, difficulty, timingPoints, hitObjectsGroups)
        if returnAsBeatmap: return parent_map
        else :return mapName, difficulty, timingPoints, hitObjectsGroups
    else:
        parent_map.setAttrib(mapName, difficulty, timingPoints, hitObjects)
        if returnAsBeatmap: return parent_map
        else: return mapName, difficulty, timingPoints, hitObjects
    
def printObjects(filepath='dump/Dan Salvato - Your Reality (Nozhomi) [Just You].osu',parent_map=None):
    """It simply prints what it renders from the given .OSU file to console.
    Parameters
    ----------
    filepath : `str`
    \tThe .OSU file path that is going to be rendered
    parent_map : `Beatmap`
    \tThe beatmap that is going to be reference as uniform"""
    mapName, difficulty, timingPoints, hitObjects = readObjects(filepath)
    timingPoints[0].offset=0
    hitObjectsGroups = [[] for i in range(len(timingPoints))]
    smallestInterval = hitObjects[-1].time
    prevTime = -hitObjects[-1].time
    print(smallestInterval,prevTime)
    objectCount=[0,0,0,0]
    for hitObject in hitObjects:
        objectCount[ho.HitObject.Type.OBJECT_TYPE.index(hitObject.type.objectType)]+=1
        hitObjectsGroups[\
            timingPoints.index(\
                tp.TimingPoint.find_region(timingPoints,hitObject.time)
        )].append(hitObject)
    print(mapName)
    for timingPoint, hitObjectGroup in zip(timingPoints, hitObjectsGroups):
        print('TP at {0}ms; {1}ms per beat{2} {3} object(s)'.format(\
            timingPoint.offset, timingPoint.inherited_mpb(),\
            [';',' (INHERITABLE);'][timingPoint.inherited], len(hitObjectGroup)\
        ))
        for hitObject in hitObjectGroup:
            obType = hitObject.type.objectType
            if obType == ho.HitObject.Type.OBJECT_TYPE[0]:
                smallestInterval = min(smallestInterval, hitObject.time-prevTime)
                prevTime = hitObject.time
                print('\tCircle at {0}ms | SI now = {1}'.format(hitObject.time,smallestInterval))
            elif obType == ho.HitObject.Type.OBJECT_TYPE[1]:
                dur = math.ceil(hitObject.get_duration())
                smallestInterval = min(smallestInterval, hitObject.time-prevTime)
                prevTime = hitObject.time + dur
                print('\tSlider at {0}ms -> {1}ms (for {2}ms) | SI now -> {3}'.format(\
                    hitObject.time, hitObject.time+dur, dur, smallestInterval))
            elif obType == ho.HitObject.Type.OBJECT_TYPE[2]:
                smallestInterval = min(smallestInterval, hitObject.time-prevTime)
                prevTime = hitObject.endTime
                print('\tSpinner at {0}ms -> {1}ms (for {2}ms) | SI now = {3}'.format(\
                    hitObject.time, hitObject.endTime, hitObject.endTime-hitObject.time,smallestInterval))
            elif obType == ho.HitObject.Type.OBJECT_TYPE[3]:
                smallestInterval = min(smallestInterval, hitObject.time-prevTime)
                prevTime = hitObject.endTime
                print('\tMania Hold at {0}ms -> {1}ms (for {2}ms) | SI now = {3}'.format(\
                    hitObject.time, hitObject.endTime, hitObject.endTime-hitObject.time,smallestInterval))
            else:
                print('01 UNPARSEABLE!')
                return # TODO implement exception
            if smallestInterval < 0:
                print("\t\t\t\t\t\tINTERVAL IS NIGGATIVE! {0}ms!".format(smallestInterval))
                return
    print('Total objects = {0}\n\tCircles = {1}\n\tSliders = {2}\n\tSpinners = {3}\n\tMania Hold = {4}'\
        .format(sum(objectCount),objectCount[0],objectCount[1],objectCount[2],objectCount[3]))
    print('Shortest interval time between objects : {0}ms'.format(smallestInterval))
