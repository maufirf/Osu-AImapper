import framework.basic as bas

class TimingPoint:
    """The class that can describe `TimePoint`s in an Osu! `Beatmap`.
    The `TimePoint`s that can be found in an Osu! `Beatmap` is consisted
    of 8 attributes, plus 4 from this python script to maintain connectivity
    between Osu! objects
    
    Main Attributes:
    \toffset = The offset (in ms) where this TimePoint begin its region. 0 if it is the first TimePoint.
    \tmilisecs per beat = a duration of a beat
    \tmeter = basic musical meter, 3/4 or 4/4
    \tsample set = the default sample sets index
    \tsample set index = default custom index
    \tvolume = you know what it is. 0:100
    \tInherited = boolean values that states if this TimePoint is inheritable
    \tkiai mode = OwO HANABI DESU MITTE TE MINNA SUGOI NEE!? *boom*
    
    You can initialize this object by passing the literal only or put them
    one by one
    
    Parameters
    ----------
    offset:`int`
    \tThe point this TimingPoint should begin its region
    mpb:`float`
    \tThe duraton of one beat for this region. if negative, it is the percent of previous inheritable mpb
    meter:`int`
    \tMusical meter, 3 for 3/4, 4 for 4/4
    sampleSet:`int`
    \tDefault sample set
    sampleIndex:`int`
    \tDefault custom sample set index
    volume:`int`
    \tPercent value of the volume
    inherited:`bool`
    \tStates if this instance is inheritable. usually 1 if mpb is positive.
    kiai:`bool`
    \tStates if this instance's region is in Kiai Mode or not.
    inherit_parent:`TimingPoint`
    \tThe inheritable `TimingPoint` instance if inherited = 1 and/or mpb is negative. Default is `None`
    prev_tp:`TimingPoint`
    \tPrevious `TimingPoint` instance in the chainlink. Default is `None`
    next_tp:`Timingpoint`
    \tNext `TimingPoint` instance in the chainlink. Default is `None`
    parent_map:`Beatmap`
    \tThe `Beatmap` instance this instance belong to. Default is `None`
    """
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
        
        If neither case found, it returns (and sets `inherit_parent` to) None.
        Return
        ------
        The inheritable `TimingPoint` instance for current instance. `None` if not found."""
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
    def mpb_to_bpm(mpb) -> float:
        """Converts Miliseconds per Beat to Beats per Minute
        by simply divisng itself from 60,000.0

        ``60000.0 / mpb``
        Return
        ------
        `float` BPM value"""
        return float(60000.0/mpb)
    @staticmethod
    def bpm_to_mpb(bpm) -> float:
        """Converts Beats per Minute to Miliseconds per Beat
        by simply divisng itself from 60,000.0

        ``60000.0 / mpb``
        Return
        ------
        `float` MPB value"""
        return float(60000.0/bpm)

    def inherited_mpb(self):
        """Returns the `float` inherited mpb value. if current instance is the
        IS the inheritable object, it will return its own mpb
        Return
        ------
        `float` MPB value that is derived from the closest previous inheritable object"""
        if self.inherited: return self.mpb
        else: return self.findInheritable().mpb*(abs(self.mpb)/100.0)
    def inherited_bpm(self):
        """Returns the `float` inherited bpm value. if current instance is the
        IS the inheritable object, it will return its own bpm
        Return
        ------
        `float` BPM value that is derived from the closest previous inheritable object"""
        return TimingPoint.mpb_to_bpm(self.inherited_mpb)
    
    @staticmethod
    def find_region(timingPoints,currentOffset):
        """Returns the `TimingPoint` object from a `list` of `TimingPoint` (`timingPoints`)
        where `currentOffset` belongs to the object's region of timing.
        Return
        ------
        `TimingPoint` instance where the `currentOffset` belongs to among the given
        `TimingPoint`s in the `timingPoints` `list`."""
        return timingPoints[bas.list_rindex([currentOffset<x.offset for x in timingPoints],False)]
        #return min(timingPoints, key=lambda x:\
        #    abs(x.offset-currentOffset)