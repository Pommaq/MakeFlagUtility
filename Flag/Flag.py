def ThrowAway():
    return False

class cFlag(object):
    def __init__(self, flag="", o1=False, o2=False, o3=False, oS=False):
        self.a_flag = flag
        self.a_o1 = o1
        self.a_o2 = o2
        self.a_o3 = o3
        self.a_os = oS
    
    def __str__(self):
        #Controls how this class is represented by e.g. print()
        return self.a_flag
    


    def __eq__(self, other):
        if self.a_flag == other.a_flag and self.a_o1 == other.a_o1 and self.a_o2 == other.a_o2 and self.a_o3 == other.a_o3 and self.a_os == other.a_os:
            return True
        else:
            return False