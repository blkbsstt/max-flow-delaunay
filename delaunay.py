from quadedge import MakeEdge, Splice, Connect, DeleteEdge

def det(m):
    return m[0][0] * m[1][1] * m[2][2] + m[0][1] * m[1][2] * m[2][0] + m[0][2] * m[1][0] * m[2][1] - m[0][0] * m[1][2] * m[2][1] - m[0][1] * m[1][0] * m[2][2] - m[0][2] * m[1][1] * m[2][0]

def CCW(a, b, c):
    a = [a.x, a.y, 1]
    b = [b.x, b.y, 1]
    c = [c.x, c.y, 1]

    return det([a, b, c]) > 0


def InCircle(a, b, c, d):
    a = [a.x, a.y, a.x * a.x + a.y * a.y]
    b = [b.x, b.y, b.x * b.x + b.y * b.y]
    c = [c.x, c.y, c.x * c.x + c.y * c.y]
    d = [d.x, d.y, d.x * d.x + d.y * d.y]

    return det([a, b, c]) - det([a, b, d]) + det([a, c, d]) - det([b, c, d]) >= 0

def RightOf(x, e):
    return CCW(x, e.Dest, e.Org)

def LeftOf(x, e):
    return CCW(x, e.Org, e.Dest)

def Delaunay(S):
    if len(S) == 2:
        a = MakeEdge()
        a.Org = S[0]
        a.Dest = S[1]
        return [a, a.Sym]
    elif len(S) == 3:
        a = MakeEdge()
        b = MakeEdge()
        Splice(a.Sym, b)
        a.Org = S[0]
        a.Dest = b.Org = S[1]
        b.Dest = S[2]
        if CCW(S[0], S[1], S[2]):
            c = Connect(b, a)
            return [a, b.Sym]
        elif CCW(S[0], S[2], S[1]):
            c = Connect(b, a)
            return [c.Sym, c]
        else:
            return [a, b.Sym]
    else:
        l = len(S) / 2
        ldo, ldi = Delaunay(S[:l])
        rdi, rdo = Delaunay(S[l:])

        #LOWER COMMON TANGENT
        while True:
            if LeftOf(rdi.Org, ldi):
                ldi = ldi.Lnext
            elif RightOf(ldi.Org, rdi):
                rdi = rdi.Rprev
            else:
                break

        basel = Connect(rdi.Sym, ldi)
        if ldi.Org == ldo.Org:
            ldo = basel.Sym
        if rdi.Org == rdo.Org:
            rdo = basel

        #MERGE
        delete = []
        while True:
            lcand = basel.Sym.Onext
            if RightOf(lcand.Dest, basel):
                while (InCircle(basel.Dest, basel.Org, lcand.Dest, lcand.Onext.Dest) and 
                    lcand.Onext.Dest not in [basel.Dest, basel.Org, lcand.Dest] and RightOf(lcand.Onext.Dest, basel)):
                        t = lcand.Onext
                        DeleteEdge(lcand)
                        lcand = t

            rcand = basel.Oprev
            if RightOf(rcand.Dest, basel):
                while (InCircle(basel.Dest, basel.Org, rcand.Dest, rcand.Oprev.Dest) and 
                    rcand.Oprev.Dest not in [basel.Dest, basel.Org, rcand.Dest] and RightOf(rcand.Oprev.Dest, basel)):
                        t = rcand.Oprev
                        DeleteEdge(rcand)
                        rcand = t

            if not RightOf(lcand.Dest, basel) and not RightOf(rcand.Dest, basel):
                break

            if not RightOf(lcand.Dest, basel):
                if (InCircle(basel.Dest, basel.Org, rcand.Dest, rcand.Lnext.Dest) and 
                    rcand.Lnext.Dest not in [basel.Dest, basel.Org, rcand.Dest]):
                        basel = Connect(rcand, basel.Sym)
                        delete.append(basel)
                else:
                    basel = Connect(rcand, basel.Sym)
            elif not RightOf(rcand.Dest, basel):
                if (InCircle(lcand.Dest, basel.Dest, basel.Org, lcand.Rprev.Dest) and 
                    lcand.Rprev.Dest not in [lcand.Dest, basel.Dest, basel.Org]):
                        basel = Connect(basel.Sym, lcand.Sym)
                        delete.append(basel)
                else:
                    basel = Connect(basel.Sym, lcand.Sym)
            elif InCircle(rcand.Dest, basel.Dest, basel.Org, lcand.Dest):
                #if lcand.Dest within basel, rcand circle
                if (InCircle(lcand.Dest, basel.Dest, basel.Org, rcand.Dest) or 
                    (InCircle(lcand.Dest, basel.Dest, basel.Org, lcand.Rprev.Dest) and 
                            lcand.Rprev.Dest not in [lcand.Dest, basel.Dest, basel.Org])):
                    basel = Connect(basel.Sym, lcand.Sym)
                    delete.append(basel)
                else:
                    basel = Connect(basel.Sym, lcand.Sym)
            else:
                if (InCircle(basel.Dest, basel.Org, rcand.Dest, rcand.Lnext.Dest) and 
                    rcand.Lnext.Dest not in [basel.Dest, basel.Org, rcand.Dest]):
                    basel = Connect(rcand, basel.Sym)
                    delete.append(basel)
                else:
                    basel = Connect(rcand, basel.Sym)

        for edge in delete:
            DeleteEdge(edge)

        return [ldo, rdo]

def from_points(points):
    return [(edge.Org, edge.Dest) for edge in get_delaunay(Delaunay(points)[0], set()) if edge.Org.index < edge.Dest.index]

def print_delaunay(d):
    delaunay = get_delaunay(d, set())
    for org, dest in sorted([(e.Org.index, e.Dest.index) for e in delaunay]):
        print (org, dest)

def get_delaunay(d, visited = set()):
    if not d in visited:
        visited.add(d)
        get_delaunay(d.Onext, visited)
        get_delaunay(d.Lnext, visited)
    return visited

