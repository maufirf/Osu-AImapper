import framework.basic as bas

class TimingPoint:
    def __init__(self,offset,mpb=None,meter=None,sampleSet=None,\
        sampleIndex=None,volume=None,inherited=None,kiai=None,\
        inherit_parent=None,prev_tp=None,next_tp=None,parent_map=None):
        self.prev_tp = prev_tp; self.next_tp = next_tp; self.parent_map = parent_map
        self.inherit_parent = inherit_parent
        if type(offset) is int and None not in [mpb,meter,sampleSet,\
            sampleIndex,volume,inherited,kiai]:
            self.offset = offset
            self.mpb = mpb
            self.meter = meter
            self.sampleSet = sampleSet
            self.sampleIndex = sampleIndex
            self.volume = volume
            self.inherited = inherited
            self.kiai = kiai
        elif type(offset) is str:
            offset = offset.split(',')
            self.offset = int(offset[0])
            self.mpb = float(offset[1])
            self.meter = int(offset[2])
            self.sampleSet = int(offset[3])
            self.sampleIndex = int(offset[4])
            self.volume = int(offset[5])
            self.inherited = bool(int(offset[6]))
            self.kiai = bool(int(offset[7]))
        else:
            print('01 parameter format error!')
            return # TODO implement exception
    
    def __str__(self):
        return '[TP@{0}ms;mpb={1}({2}meter={3})vol={4}%~{5}:{6}{7}]'.format(\
            self.offset,self.mpb,['','inheritable,'][self.inherited],\
            self.meter,self.volume,self.sampleSet,self.sampleIndex,['','~KIAI!'][self.kiai])
    
    def findInheritable(self):
        """Finds the first `TimePoint` object that is inheritable by traversing
        through recursive progress on object calling via `prev_tp` attribute.

        If the object itself is inheritable, it sets `inherit_parent` attribute
        to `None` and returns itself.
        
        If the object is not inheritable and found an inheritble `TimePoint`
        object, it sets `inherit_parent` to the previously mentioned object and
        returns said object.
        
        If neither case found, it returns (and sets `inherit_parent` to) None."""
        if self.inherited:
            self.inherit_parent = None
            return self
        elif type(self.prev_tp) is TimingPoint:
            self.inherit_parent = self.prev_tp.findInheritable()
            return self.inherit_parent
        else:
            self.inherit_parent = None
            return None

    @staticmethod
    def mpb_to_bpm(mpb) -> float: return float(60000.0/mpb)
    @staticmethod
    def bpm_to_mpb(bpm) -> float: return float(60000.0/bpm)

    def inherited_mpb(self):
        if self.inherited: return self.mpb
        else: return self.findInheritable().mpb*(abs(self.mpb)/100.0)
    def inherited_bpm(self):
        return TimingPoint.mpb_to_bpm(self.inherited_mpb)
    
    @staticmethod
    def find_region(timingPoints,currentOffset):
        return timingPoints[bas.list_rindex([currentOffset<x.offset for x in timingPoints],False)]
        #return min(timingPoints, key=lambda x:\
        #    abs(x.offset-currentOffset)