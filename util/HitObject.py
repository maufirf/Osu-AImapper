# -*- coding: utf-8 -*-

import copy
import util.TimingPoint as tp
import util.Difficulty as di
import util.Beatmap as bm

class HitObjectInputError(Exception):
    def __str__(self):
        return "Not a valid binary number"

class HitObject:
    """Primary constructor of generic Hit_object class
    
    Type 1::
        Hit_object(raw_string)
    To initialize Hit_object object, just shove in the string of the
    ONE Hit Object string straight like the ones you'd see inside an
    .OSU file. example::
        >>> Hit_object("390,227,178322,2,0,L|362:348,1,89,2|0,1:2|1:2,0:0:0:0:")

    Type 2::
        Hit_object(x,y,time,type,hitSound)
    or::
        Hit_object(x=..,y=..,time=..,type=..,hitSound=..)
    The relevant input parameter must be int in type. for example::
        >>> Hit_object(390,227,178322,2,0,'L|362:348',1,89,'2|0','1:2|1:2','0:0:0:0:')
    
    Parameters
    ----------
    x : str or int
        if str, then the whole hit object raw string. else, the x attribute of an hit object
    *args : int
        only if x is int, series of parameter y, time, type, and hitSound
    **kwargs : int
        (alternative of using *args,)
    
    """
    DEBUG = False

    class Type:
        """Subclass of `HitObject` that represents the `HitObject`'s
        object type and combo properties.

        There are three types to initialize this object:

        1. One param, binary `string`
        \texample: Type('00010101') -> Circle, new combo, skipping 2 colours.
        2. One param, decimal `integer`
        \texample: Type(6) -> Slider, new combo, skipping 1 colour.
        3. Six params, starting from the left is the least significant digit (bit 0) as `integer`s or `bool`s.
        \tType(circleBit,sliderBit,newComboBit,spinnerBit,threeBitsOfColorSkip,maniaHoldBit)
        \texample: Type(False,True,False,False,3,False) -> Slider, newCombo is false so color skip of 4 is ignored
        """
        # Note from the wiki:
        # "Circles, sliders, spinners, and hold notes can be OR'd with
        # new combos and the combo skip value, but not with each other."
        # Therefore i create this constant:
        OBJECT_TYPE = ['circle','slider','spinner','maniaHold']
        OBJECT_TYPE_VALUE = [1,2,6,128]

        def __init__(self,intval,*args):
            # If intval is the only value inserted, then it is assumed
            # that the input is the decimal int. I have prepared the case
            # when it is a decimal string and when it is a binary string.
            # intval will be binary string in the end.
            if len(args)==0:
                if type(intval) is int: intval = format(intval,'08b')[-8:]
                elif type(intval) is str:
                    # Checks if intval string is binary or not.
                    # if binary.... else...
                    if all(set(intval)==sets for sets in [{'0'},{'1'},{'0','1'}]):
                        # failsafe if length is less or more than 8 bits:
                        # it adds zeros to the missing significant bits
                        # or it truncates the excessing bits
                        intval = intval.zfill(8)[-8:]
                    elif intval.isnumeric(): intval = format(int(intval),'08b')[-8:]
                    else:
                        print("01 Format invalid! must be either of dec int, dec string, or binary string")
                        return # TODO implement exception
                else:
                    print("02 Format invalid! must be either of dec int, dec string, or binary string")
                    return # TODO implement exception
                obj = [intval[7],intval[6],intval[4],intval[0]]
                if obj.count('1')!=1:
                    print ("03 Circle, slider, spinner, and mania hold CANNOT be OR'd together and only one option is possible")
                    print(obj)
                    return # TODO implement exception
                self.objectType = self.OBJECT_TYPE[obj.index('1')]
                self.newCombo = bool(int(intval[5]))
                self.colorSkip = (1+int(intval[1:4]))*self.newCombo
            # If the input uses *args, then there must be 3 or 6 parameters input
            # case 3 parameters input
            # All inputs must follow this format
            # objectType:int -> {0,1,2,3}, newCombo:bool or :int -> {0,1}, colorSkip:int -> {x, x >= 1 and x <=8}
            # objectType is ordered: circle, slider, spinner, maniaHold
            # colorSkip will be 0 if newCombo is false. Otherwise, limited between 2 and 7.
            elif len(args)==2:
                self.objectType = self.OBJECT_TYPE[intval]
                self.newCombo = bool(args[0])
                self.colorSkip = min(8,max(1,args[1]))*args[0]
            # case 6 parameters input
            # Bit 0 (circle) STARTS FROM LEFT. The input must be int. Format as follows:
            # 0=circle, 1=slider, 2=newCombo, 3=spinner, 4:6=colorSkip, 7=maniaHold
            elif len(args)==5:
                if intval+args[0]+args[2]+args[4]!=1:
                    print ("04 Circle, slider, spinner, and mania hold CANNOT be OR'd together and only one option is possible")
                    return # TODO implement exception
                else:
                    self.objectType = self.OBJECT_TYPE[args[0]+args[2]*2+args[4]*3]
                    self.newCombo = bool(args[1])
                    # colorSkip is ignored if newCombo is false
                    # also from wiki: "The new combo flag always advances to the next combo."
                    self.colorSkip = (1+args[3])*args[1]
        
        def __str__(self):
            if self.newCombo: return '<'+self.objectType+';newCombo+='+str(self.colorSkip)+'>'
            else: return '<'+self.objectType+'>'

        def to_decint(self):
            """Returns the decimal `integer` value of this object"""
            objval = self.OBJECT_TYPE_VALUE[self.OBJECT_TYPE.index(self.objectType)]
            if self.newCombo: return objval + 4 + int(format(self.colorSkip-1,'03b')+'0000',2)
            else: return objval
        
        def to_binstr(self):
            """Returns the binary `string` value of this object"""
            return format(self.to_decint(),'08b')

    class HitSound:
        """Subclass of `HitObject` that represents its `HitSound`s, either a
        combination of `'normal'`, `'whistle'`, `'finish'`, or `'clap'`.
        
        There are two ways to initialize this object:
        
        One - One param
        \tHitSound(decimal_value)
        \tdecimal_value can be either `int` or `str`
        Two - Four params
        \tHitSound(normal,whistle,finish,clap)
        \teach of the params is `boolean` or {0,1} `int`s
        """
        SOUND_TYPE=['normal','whistle','finish','clap']

        def __init__(self,intval,*args):
            # case *args is not used
            if len(args)==0:
                # case intval is decimal integer, convert to binary string if true
                if type(intval) is int:
                    intval = format(intval,'04b')[-4:]
                # case intval is string, either binary or decimal
                elif type(intval) is str:
                    # check if it is binary. Let it be if true
                    if all(set(intval)==x for x in [{0},{1},{0,1}]): pass
                    # check if it is decimal. Convert to binary string if true
                    elif intval.isnumeric(): intval = format(int(intval),'04b')[-4:]
                    # else throw exception
                    else:
                        print('01 if string, input must be either decimal or binary')
                        return # TODO implement exception
                # else throw exception
                else:
                    print('02 input must be either string or integer')
                    return # TODO implement exception
            # case *args is used, total 4 params used and consisted of 0s and/or 1s
            # and are integerss
            elif len(args)==3:
                if all(set([intval,args[0],args[1],args[2]])==x for x in [{0},{1},{0,1}]):
                    intval = ''.join([args[2],args[1],args[0],intval])
                else:
                    print('03 input must be either integers of 1s and/or 0s')
                    return # TODO implement exception
            else:
                print('04 this method takes exactly 1 or 4 parameters')
                return # TODO implement exception
            # Different from HitObject.Type, HitObject.HitSound saves the binary
            # value as attribute. This was caused by a note on the wiki:
            #   "The normal sound is always played, so bit 0 is irrelevant today.
            #   The only exception is for osu!mania, with the skin's LayeredHitSounds
            #   property."
            # Therefore, though bit 0 is ignored, but it can produce different integer
            # value when reverse engineered. For example <normal,whistle,finish>
            # can be either 6 or 7. Therefore, in order to reverse engineer it, i'll
            # just simply convert binval to intval.
            self.binval = intval
            self.activeSounds = [self.SOUND_TYPE[0]]
            for i in [2,1,0]:
                if int(self.binval[i])==1: self.activeSounds.append(self.SOUND_TYPE[-i-1])
        
        def __str__(self):
            return '<{0}>'.format(','.join(self.activeSounds))

    def __init__(self, x,*args,**kwargs):
        """Actual constructor of `HitObject`. Read `HitObject()` documentation for the info."""
        if HitObject.DEBUG: print('x =',x,'\n*args',args,'\n**kwargs',kwargs)
        if 'next_ho' in kwargs: self.next_ho = kwargs['next_ho']
        else: self.next_ho = None
        if 'prev_ho' in kwargs: self.prev_ho = kwargs['prev_ho']
        else: self.prev_ho = None
        if 'parent_map' in kwargs: self.parent_map = kwargs['parent_map']
        else: self.parent_map = None
        if len(args)==0 and type(x) is str:
            x = [int(i) for i in x.split(',')[:5]]
            if len(x) < 5:
                print('The string must contain only comma-separated integers and must be exactly or more than 5 ints')
                return # TODO implement exception
            self.x = x[0]
            self.y = x[1]
            self.time = x[2]
            self.type = HitObject.Type(int(x[3]))
            self.hitSound = HitObject.HitSound(int(x[4]))
        elif type(x) is int:
            if len(args)>=4:
                if not all(type(entry) is int for entry in args[:4]):
                    print('all arguments should be int')
                    return # TODO implement exception
                self.x = x
                self.y = args[0]
                self.time = args[1]
                self.type = HitObject.Type(args[2])
                self.hitSound = HitObject.HitSound(args[3])
            elif all(k in kwargs for k in ['y','time','type','hitSound']):
                if not all(kwargs[entry] is int for entry in args[:4]):
                    print('all keyword arguments should be int')
                    return # TODO implement exception
                self.x = x
                self.y = kwargs['y']
                self.time = kwargs['time']
                self.type = HitObject.Type(kwargs['type'])
                self.hitSound = HitObject.HitSound(kwargs['hitSound'])
        else:
            print('error, bangke')
            return # TODO implement 
        if HitObject.DEBUG: print('x =',self.x,'\ny =',self.y,'\ntime =',self.time,'\ntype =',self.type,'\nhitSound =',self.hitSound)
        
    def __str__(self):
        return '[{0};({1},{2})->{3}ms;{4}]'.format(self.type,self.x,self.y,self.time,self.hitSound)

    def get_startTime(self):
        return self.time
        
    def get_endTime(self):
        return self.time

    @staticmethod
    def wrap(literal,prev_ho=None,next_ho=None,parent_map=None):
        """Returns an objectType-specific object, not a generic HitObject
        from an literal string input

        \twrap(literal,[prev_ho],[next_ho],[parent_map])
        
        Parameters
        ----------
        literal : `str`
        The literal value of the object, for example '411,218,205850,2,0,L|385:111,1,89,10|0,0:2|0:0,0:0:0:0:'

        prev_ho : `HitObject`
        Previous `HitObject` instance on the chainlink. Default is `None`

        next_ho : `HitObject`
        Next `HitObject` instance on the chainlink. Default is `None`

        parent_map : `Beatmap`
        The parent `Beatmap` of current instance. Default is `None`
        
        Return
        ------
        `HitObject` derivates, either `Circle`, `Slider`, `Spinner`,
        or `ManiaHold` depends on the `Type` derived from literal param."""
        objType = HitObject.Type(literal.split(',')[3]).objectType
        if objType=='circle':
            return Circle(literal,prev_ho=prev_ho,next_ho=next_ho,parent_map=parent_map)
        elif objType=='slider':
            return Slider(literal,prev_ho=prev_ho,next_ho=next_ho,parent_map=parent_map)
        elif objType=='spinner':
            return Spinner(literal,prev_ho=prev_ho,next_ho=next_ho,parent_map=parent_map)
        elif objType=='maniaHold':
            return ManiaHold(literal,prev_ho=prev_ho,next_ho=next_ho,parent_map=parent_map)
        else:
            print('01 Type error!')
            return # TODO implement exception
    
    @staticmethod
    def cast(x):
        """returns a new, generic `HitObject`-casted instance of either `Circle`,
        `Slider`, `Spinner`, or `ManiaHold`.
        
        Parameter
        ---------
        x : `HitObject`
        The `HitObject` variety that you want to cast to Either of `Circle`, `Slider`, `Spinner`, or `ManiaHold` works as well.
        
        Return
        ------
        A new, generic `HitObject` instance with the old parameters from
        its derivative preserved. Recastable to their old class."""
        if type(x) in [Circle,Slider,Spinner,ManiaHold]:
            out = copy.deepcopy(x)
            out.__class__ = HitObject
            return out
        else:
            print('01 Input parameter type error!')
            return # TODO implment exception

    
class Circle(HitObject):
    """An `HitObject` derivate variant that fits to describe a classic
    Osu! circle. There are two ways of using this, though only one is
    supported for now:
    ``Circle(literal,[extras],[prev_ho],[next_ho],[parent_map])``

    and (the unsupported one):
    ``Circle(x,y,timing,objType,hitSound,[extras],[prev_ho],[next_ho],[parent_map])``
    """
    def __init__(self, x, y=None, timing=None, objType=None, hitSound=None, extras='0:0:0:0',\
        prev_ho=None, next_ho=None, parent_map=None):
        # case if the input is literal string of the object.
        # Not putting either of y, timing, objType, and hitSound will
        # assumed as this case.
        if {None}==set([y,timing,objType,hitSound]) and type(x) is str:
            x = x.split(',')
            if len(x)!=6:
                print('01 literal input: it has only {0} attributes while 6 is required'.format(len(x)))
                return # TODO implement exception
            super().__init__(','.join([x[0],x[1],x[2],x[3],x[4]]),prev_ho=prev_ho,next_ho=next_ho,parent_map=parent_map)
            self.extras = extras
        else:
            print("02 parameter formt error")
            return # TODO implement exception
        
    def __str__(self):
        return '[{0}~{1}]'.format(super().__str__(),self.extras)

class Slider(HitObject):
    """An `HitObject` derivate variant that fits to describe a classic
    Osu! slider. There are two ways of using this, though only one is
    supported for now:
    ``Slider(literal,[extras],[prev_ho],[next_ho],[parent_map])``

    and (the unsupported one):
    ``Slider(x,y,timing,objType,hitSound,path,repeat,pixelLength,[edgeHitSounds],[edgeAdditions],[extras],[prev_ho],[next_ho],[parent_map])``
    """
    def __init__(self,x=None,y=None,timing=None,objtype=None,hitSound=None,\
        path=None,repeat=None,pixelLength=None,edgeHitSounds=None,\
            edgeAdditions=None,extras='0:0:0:0:',prev_ho=None,next_ho=None,parent_map=None):
        if type(x) is str and {None}==set([y,timing,objtype,hitSound,path,repeat,pixelLength]):
            super().__init__(x,prev_ho=prev_ho,next_ho=next_ho,parent_map=parent_map)
            x = x.split(',')
            self.path = x[5]
            self.repeat = int(x[6])
            self.pixelLength = float(x[7])
            if len(x) == 11:
                self.edgeHitSounds = x[8]
                self.edgeAdditions = x[9]
                self.extras = x[10]
            elif len(x) == 8:
                self.edgeHitSounds = None
                self.edgeAdditions = None
                self.extras = extras
        elif None not in [x,y,timing,objtype,hitSound,path,repeat,pixelLength]:
            super().__init__(x,y,timing,objtype,hitSound,prev_ho=prev_ho,next_ho=next_ho,parent_map=parent_map)
            self.path = path
            self.repeat = repeat
            self.pixelLength = pixelLength
            self.edgeHitSounds = edgeHitSounds
            self.edgeAdditions = edgeAdditions
            self.extras = extras
        else:
            print('01 Parameter format error!')
            return # TODO implement exception
    
    def __str__(self):
        return '[{0}=>{1};(rep={2},pxLen={3})~(edHS={4},edAd={5});{6}]'.format(super().__str__(),self.path,self.repeat,self.pixelLength,self.edgeHitSounds,self.edgeAdditions,self.extras)
    
    def get_duration(self,timingPoint=None,difficulty=None):
        """Finds the slider duration of current slider by this formula:
        
        ``pixelLength / (100.0 * slider_multiplier) * milisecs_per_beats``

        usage:
        ``get_duration([timingPoint],[difficulty])``
        Parameters
        ----------
        timingPoint : `TimingPoint` or `float` |
        A `TimingPoint` instance in which the slider's time laid the region on.
        REQUIRED IF the `Slider` instance don't have parent_map (or `None`).

        difficulty : `Difficulty` or `float` |
        A `Difficulty` instance in which the slider relies its slider multiplier.
        REQUIRED IF the `Slider` instance  don't have parent_map (or `None`)
        Return
        ------
        `float` value of the slider duration in miliseconds. Recommended to ceil to
        the nearest next integral value.
        """
        if {None}==set([timingPoint,difficulty]) and isinstance(self.parent_map,bm.Beatmap):
            mpb = tp.TimingPoint.find_region(self.parent_map.timingPoints,self.time).inherited_mpb()
            SM = self.parent_map.difficulty.SM
            return (self.pixelLength * mpb) / (100.0 * SM)
        elif isinstance(timingPoint,(tp.TimingPoint,float)) and\
            isinstance(difficulty,(list,float)):
            return self.pixelLength / \
                (100.0 * difficulty if type(difficulty)==float else \
                    (difficulty.get_slider_values()[1] if type(difficulty)==di.Difficulty else None)\
                ) * \
                timingPoint if type(timingPoint)==float else \
                    (timingPoint.inherited_mpb() if type(timingPoint)==tp.TimingPoint else None)
        else :
            print('FORMAT ERROR BANGKe!')
            return # TODO implement exception

    def get_endTime(self,timingPoint=None,difficulty=None):
        if {None}==set([timingPoint,difficulty]) and isinstance(self.parent_map,bm.Beatmap):
            return self.get_duration() + self.time
        else:
            print('Parameter input is not supported yet') # TODO implement parameter support
            return # TODO implement exception


class Spinner(HitObject):
    """An `HitObject` derivate variant that fits to describe a Osu! spinner.
    There are two ways of using this, though only one is
    supported for now:
    ``Spinner(literal,[extras],[prev_ho],[next_ho],[parent_map])``

    and (the unsupported one):
    ``Spinner(x,y,timing,objType,hitSound,endTime,[extras],[prev_ho],[next_ho],[parent_map])``
    """
    def __init__(self,x=None,y=None,timing=None,objtype=None,hitSound=None,\
        endTime=None,extras='0:0:0:0:',prev_ho=None,next_ho=None,parent_map=None):
        if type(x) is str and {None}==set([y,timing,objtype,hitSound,endTime]):
            super().__init__(x,prev_ho=prev_ho,next_ho=next_ho,parent_map=parent_map)
            x = x.split(',')
            self.endTime = int(x[5])
            self.extras = x[6]
        elif None not in [x,y,timing,objtype,hitSound,endTime]:
            super().__init__(x,y,timing,objtype,hitSound,prev_ho=prev_ho,next_ho=next_ho,parent_map=parent_map)
            self.endTime = endTime
            self.extras = extras
        else:
            print('01 Parameter format error!')
            return # TODO implement exception

    def __str__(self):
        return '[{0},end={1}ms~{2}]'.format(super().__str__(),self.endTime,self.extras)

    def get_endTime(self):
        return self.endTime

class ManiaHold(HitObject):
    """An `HitObject` derivate variant that fits to describe a Osu!Mania hold key.
    There are two ways of using this, though only one is
    supported for now:
    ``ManiaHold(literal,[extras],[prev_ho],[next_ho],[parent_map])``
    
    and (the unsupported one):
    ``ManiaHold(x,y,timing,objType,hitSound,endTime,[extras],[prev_ho],[next_ho],[parent_map])``
    """
    def __init__(self,x=None,y=None,timing=None,objtype=None,hitSound=None,\
        endTime=None,extras='0:0:0:0:',prev_ho=None,next_ho=None,parent_map=None):
        if type(x) is str and {None}==set([y,timing,objtype,hitSound,endTime]):
            super().__init__(x,prev_ho=prev_ho,next_ho=next_ho,parent_map=parent_map)
            x = x.split(',')[-1].split(':',1)
            self.endTime = int(x[0])
            self.extras = x[1]
        elif None not in [x,y,timing,objtype,hitSound,endTime]:
            super().__init__(x,y,timing,objtype,hitSound,prev_ho=prev_ho,next_ho=next_ho,parent_map=parent_map)
            self.endTime = endTime
            self.extras = extras
        else:
            print('01 Parameter format error!')
            return # TODO implement exception

    def __str__(self):
        return '[{0},end={1}ms~{2}]'.format(super().__init__(),self.endTime,self.extras)
    
    def get_endTime(self):
        return self.endTime

    """OWO
    class Circle:
    def __init__(self, x, y=None, timing=None, objType=None, hitSound=None, extras='0:0:0:0'):
        # case if the input is (HitObject object, [str extras])
        if type(x) is HitObject:
            self.base = x
            if y is None: self.extras=extras
            else: self.extras=y
        # case if the input is literal string of the object.
        # Not putting either of y, timing, objType, and hitSound will
        # assumed as this case.
        elif None in [y,timing,objType,hitSound] and type(x) is str:
            x = x.split(',')
            if len(x)!=6:
                print('01 literal input: it has only {0} attributes while 6 is required'.format(len(x)))
                return # TODO implement exception
            self.basic = HitObject(','.join([x[0],x[1],x[2],x[3],x[4]]))
        else:
            print("02 parameter formt error")
            return # TODO implement exception
        
    def __str__(self):
        return '[{0}~{1}]'.format(self.base,self.extras)
    """