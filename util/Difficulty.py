class Difficulty:
    def __init__(self,HP,CS=None,OD=None,AR=None,SM=1.4,ST=1.0,parent_map=None):
        if {None}==set([CS,OD,AR]):
            if type(HP) is list and all(type(x)==float for x in HP):
                if len(HP)>=4:
                    # Map Difficulty
                    self.HP=HP[0];self.CS=HP[1];self.OD=HP[2];self.AR=HP[3]
                    # Slider Settings
                    self.SM = HP[4] if len(HP)>=5 else SM
                    self.ST = HP[5] if len(HP)>=6 else ST
                else:
                    print('Constructor takes at least four argument for list, your list is only {0}'.format(len(HP)))
            elif type(HP) is str:
                print('Literal Input is not supported yet!')
                return # TODO implement exception
            else:
                print('Yourt argument list is invalid')
                return # TODO implement exception
        elif None not in [HP,CS,OD,AR]:
            # Map Difficulty
            self.HP = HP; self.CS = CS; self.OD = OD; self.AR = AR
            # Slider Settings
            self.SM = SM; self.ST = ST
        else:
            print('Input format or type error!')
            return # TODO implement exception
        self.parent_map = parent_map
    
    def __str__(self):
        return '[<HP={0},CS={1},OD={2},AR={3}>;<SM={4},ST={5}>]'.format(\
            self.HP, self.CS, self.OD, self.AR, self.SM, self.ST\
        )

    def get_map_values(self): return [self.HP,self.CS,self.OD,self.AR]
    def get_slider_values(self): return [self.SM,self.ST]
    def get_values(self): self.get_map_values ,self.get_slider_values
    

