import numpy as np

TIMELINE_CHANNEL_STD = ['circle','slider','spinner']

def timeliner_std(beatmap):
    oblst = beatmap.hitObjects
    maxDuration = int(np.ceil(oblst[-1].get_endTime()))
    # The timeline with the detail down to 1 milisec
    timeline = np.zeros((maxDuration+1,3))
    for ob in oblst:
        timeline[ob.get_startTime():int(np.ceil(ob.get_endTime()))+1,TIMELINE_CHANNEL_STD.index(ob.type.objectType)]=1
    return timeline

def timelineSplicer(timeline,interval):
    parts = int(np.ceil((timeline.shape[0]-1) / interval))
    nutimeline = np.zeros((parts+1,3))
    for i in range(0,timeline.shape[0],interval):
        nutimidx = int(i/interval)
        if ((timeline[i:i+interval,0]==1).any()): nutimeline[nutimidx,0]=1
        if ((timeline[i:i+interval,1]==1).any()): nutimeline[nutimidx,1]=1
        if ((timeline[i:i+interval,2]==1).any()): nutimeline[nutimidx,2]=1
    return [x.reshape((3,1)) for x in nutimeline]