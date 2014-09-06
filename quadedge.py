class QuadEdge(object):

    def __init__(self):
        self.Onext = None
        self.Rot = None
        self.Org = None

    def __str__(self):
        return "QEdge(" + str(self.Org) + " " + str(self.Dest) + ")"

    def __repr__(self):
        return repr((self.Org, self.Dest))

    @property
    def Onext(self):
        return self._Onext

    @Onext.setter
    def Onext(self, value):
        self._Onext = value

    @property
    def Rot(self):
        return self._Rot

    @Rot.setter
    def Rot(self, value):
        self._Rot = value

    @property
    def Org(self):
        return self._Org

    @Org.setter
    def Org(self, value):
        self._Org = value

    @property
    def Dest(self):
        return self.Sym.Org

    @Dest.setter
    def Dest(self, value):
        self.Sym.Org = value

    @property
    def Sym(self):
        return self.Rot.Rot

    @property
    def Oprev(self):
        return self.Rot.Onext.Rot

    @property
    def Rprev(self):
        return self.Sym.Onext

    @property
    def Rnext(self):
        return self.Rot.Onext.Rot.Sym

    @property
    def Lnext(self):
        return self.Rot.Sym.Onext.Rot

    @property
    def Lprev(self):
        return self.Onext.Sym

def MakeEdge():
    q = []
    for i in range(0, 4):
        q.append(QuadEdge())

    q[0].Onext = q[0]
    q[2].Onext = q[2]
    q[1].Onext = q[3]
    q[3].Onext = q[1]

    q[0].Rot = q[1]
    q[1].Rot = q[2]
    q[2].Rot = q[3]
    q[3].Rot = q[0]

    return q[0]

def Splice(a, b):
    alpha = a.Onext.Rot
    beta  = b.Onext.Rot

    a.Onext, b.Onext = b.Onext, a.Onext
    alpha.Onext, beta.Onext = beta.Onext, alpha.Onext

def Connect(a, b):
    e = MakeEdge()
    e.Org = a.Dest
    e.Dest = b.Org
    Splice(e, a.Lnext)
    Splice(e.Sym, b)
    return e

def DeleteEdge(e):
    Splice(e, e.Oprev)
    Splice(e.Sym, e.Sym.Oprev)
