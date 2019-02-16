import util.HitObject as ho
import util.TimingPoint as tp

def readAllHitObjects(filepath="dump/fhana - Sorairo Picture (Sotarks) [Haruto's Insane].osu"):
    fo = open(filepath,'r',encoding='utf-8')
    print ("Name of the file: ", fo.name)
    flist=[x.replace('\n','') for x in fo.readlines()] 
    hitObjectHeaderIdx = flist.index('[HitObjects]')
    hitObjects = [ho.HitObject(x) for x in flist[hitObjectHeaderIdx+1:]]        
    prev = None
    for obj in hitObjects:
        obj.prev_ho = prev
        if prev is not None: prev.next_ho = obj
    return hitObjects     

def printAllHitObjects(filepath="dump/fhana - Sorairo Picture (Sotarks) [Haruto's Insane].osu"):
    hitObjects = readAllHitObjects(filepath)
    for hitObject in hitObjects:
        print(hitObject)

def readAllWrappedHitObjects(filepath='dump/Dan Salvato - Your Reality (Nozhomi) [Just You].osu'):
    fo = open(filepath,'r',encoding='utf-8')
    print ("Name of the file: ", fo.name)
    flist=[x.replace('\n','') for x in fo.readlines()] 
    hitObjectHeaderIdx = flist.index('[HitObjects]')
    hitObjects = [ho.HitObject.wrap(x) for x in flist[hitObjectHeaderIdx+1:]]        
    prev = None
    for obj in hitObjects:
        obj.prev_ho = prev
        if prev is not None: prev.next_ho = obj
    fo.close()    
    return hitObjects 

def printAllWrappedHitObjects(filepath='dump/Dan Salvato - Your Reality (Nozhomi) [Just You].osu'):
    hitObjects = readAllWrappedHitObjects(filepath)
    count = [0,0,0,0]
    for hitObject in hitObjects:
        count[ho.HitObject.Type.OBJECT_TYPE.index(hitObject.type.objectType)]+=1
        print(hitObject)
    print("Circles={0}; Sliders={1}; Spinners={2}; ManiaHolds={3}".format(count[0],count[1],count[2],count[3]))    

def printAllEssentialHitObjects(filepath='dump/Dan Salvato - Your Reality (Nozhomi) [Just You].osu'):
    hitObjects = readAllWrappedHitObjects(filepath)
    count = [0,0,0,0]; types = ho.HitObject.Type.OBJECT_TYPE
    for hitObject in hitObjects:
        obtype = hitObject.type.objectType
        count[ho.HitObject.Type.OBJECT_TYPE.index(obtype)]+=1
        if obtype is types[0]:
            print('{0} at {1}ms'.format(obtype, hitObject.time))
        elif obtype is types[1]:
            print('{0} from {1}ms for {2}px'.format(obtype, hitObject.time, hitObject.pixelLength))
        elif obtype is types[2]:
            print('{0} from {1}ms->{2}ms (for {3}ms)'.format(\
                    obtype, hitObject.time, hitObject.endTime, hitObject.endTime-hitObject.time\
                    ))
        elif obtype is types[3]:
            pass 
        else:
            print("ERROR!")
            return
    print("Circles={0}; Sliders={1}; Spinners={2}; ManiaHolds={3}".format(count[0],count[1],count[2],count[3]))        

def readAllTimingPoints(filepath='dump/Dan Salvato - Your Reality (Nozhomi) [Just You].osu'):
    fo = open(filepath,'r',encoding='utf-8')
    print ("Name of the file: ", fo.name)
    
    flist=[x.replace('\n','') for x in fo.readlines()]
    timingPointsHeaderIdx = flist.index('[TimingPoints]')
    coloursHeaderIdx = flist.index('[Colours]')
    prev=None; timingPoints = []
    for i in range(timingPointsHeaderIdx+1,coloursHeaderIdx-2):
        obj = tp.TimingPoint(flist[i],prev_tp=prev)
        if type(prev) is tp.TimingPoint: prev.next_tp=obj
        prev = obj
        timingPoints.append(obj)
    fo.close()    
    return timingPoints

def printAllTimingPoints(filepath='dump/Dan Salvato - Your Reality (Nozhomi) [Just You].osu'):
    tplist = readAllTimingPoints(filepath=filepath)
    for timingPoint in tplist: print(timingPoint)

def printAllEssentialTimingPoints(filepath='dump/Dan Salvato - Your Reality (Nozhomi) [Just You].osu'):
    tplist = readAllTimingPoints(filepath=filepath)
    for obj in tplist:
        print("TimingPoint at {0} with {1}ms per beat{2}".format(\
            obj.offset, obj.inherited_mpb(), [', inherited.','.'][int(obj.inherited)]))