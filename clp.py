import itertools
from sage.graphs.distances_all_pairs import distances_all_pairs
from sage.numerical.mip import MixedIntegerLinearProgram

def razdalje_povezave_vozlisca(g):
    razdalje = distances_all_pairs(g)
    razdalje_povezave = {}

    for i,j in g.edges(labels=False):
        razdalje_povezave[i,j] = {}
        for v in g:
            razdalje_povezave[i,j][v] = min(razdalje[i][v], razdalje[j][v])

    return razdalje_povezave

def CLP_Dedim(g):

    razdalje = razdalje_povezave_vozlisca(g)

    p = MixedIntegerLinearProgram(maximization = False)
    x = p.new_variable(binary = True)
    p.set_objective( sum([x[v] for v in g]) )

    for u,v in g.edges(labels = False):
        p.add_constraint(x[u] + x[v] >= 1)


    edges = list(g.edges(labels=False))
    for (i,j),(u,v) in itertools.combinations(edges, 2):
        vsota = sum(abs(razdalje[(i,j)][k] - razdalje[(u,v)][k])*x[k] for k in g.vertices())
        p.add_constraint(vsota >= 1)


    optimalna_resitev = p.solve()
    vrednosti_za_S = p.get_values(x)

    return optimalna_resitev, vrednosti_za_S

#edge metric dimension

def CLP_edim(g):

    razdalje = razdalje_povezave_vozlisca(g)

    p = MixedIntegerLinearProgram(maximization = False)
    x = p.new_variable(binary = True)
    p.set_objective( sum([x[v] for v in g]) )

    edges = list(g.edges(labels=False))
    for (i,j),(u,v) in itertools.combinations(edges, 2):
        vsota = sum(abs(razdalje[(i,j)][k] - razdalje[(u,v)][k])*x[k] for k in g.vertices())
        p.add_constraint(vsota >= 1)


    optimalna_resitev = p.solve()
    vrednosti_za_S = p.get_values(x)

    return optimalna_resitev, vrednosti_za_S

#funkcija, ki poišče drevo na n vozliščih z min Dedim
from sage.graphs.trees import TreeIterator
def drevesa_min(i,j):
    for k in range(i,j+1):
        vrednost = 100
        min_tree=[]
        for t in TreeIterator(k):
            v = CLP_Dedim(t)
            if v[0]<= vrednost:
                vrednost = v[0]
                min_tree.append(t)
        show(min_tree[-1])
        print(f"{vrednost}")


#funkcija, ki poišče drevo na n vozliščih z max Dedim
def drevesa_max(i,j):
    for k in range(i,j+1):
        vrednost = 0
        max_tree=[]
        for t in TreeIterator(k):
            v = CLP_Dedim(t)
            if v[0]>= vrednost:
                vrednost = v[0]
                max_tree.append(t)
        show(max_tree[-1])
        print(f"{vrednost}")


#funkcija, ki poišče drevo na n vozliščih z min Dedim-edim

def drevesa_min_razlika(i,j):
    for k in range(i,j+1):
        vrednost = 100
        min_tree=[]
        for t in TreeIterator(k):
            v = CLP_Dedim(t)
            l = CLP_edim(t)
            if v[0]-l[0] <= vrednost:
                vrednost = v[0]-l[0]
                min_tree.append(t)
        show(min_tree[-1])
        print(f"{vrednost}")

#funkcija, ki poišče drevo na n vozliščih z max Dedim-edim

def drevesa_max_razlika(i,j):
    for k in range(i,j+1):
        vrednost = 0
        max_tree=[]
        for t in TreeIterator(k):
            v = CLP_Dedim(t)
            l = CLP_edim(t)
            if v[0]-l[0] >= vrednost:
                vrednost = v[0]-l[0]
                max_tree.append(t)
        show(max_tree[-1])
        print(f"{vrednost}")


#funkcija, ki poišče drevo na n vozliščih z min Dedim/edim

def drevesa_min_ulomek(i,j):
    for k in range(i,j+1):
        vrednost = 100
        min_tree=[]
        for t in TreeIterator(k):
            v = CLP_Dedim(t)
            l = CLP_edim(t)
            if v[0]/l[0] <= vrednost:
                vrednost = v[0]/l[0]
                min_tree.append(t)
        show(min_tree[-1])
        print(f"{vrednost}")

#funkcija, ki poišče drevo na n vozliščih z max Dedim/edim

def drevesa_max_ulomek(i,j):
    for k in range(i,j+1):
        vrednost = 0
        max_tree=[]
        for t in TreeIterator(k):
            v = CLP_Dedim(t)
            l = CLP_edim(t)
            if v[0]/l[0] >= vrednost:
                vrednost = v[0]/l[0]
                max_tree.append(t)
        show(max_tree[-1])
        print(f"{vrednost}")


#funkcija za dedim kartezičnega produkta grafa

#predpostavimo, da je i<=j(simetrija)
def grid_graph(i,j):
    for k in range(1,i+1):
        for l in range(k,j+1):
            p1 =graphs.PathGraph(k)
            p2 =graphs.PathGraph(l)
            g = p1.cartesian_product(p2)
            g.show()
            a = CLP_Dedim(g)
            print(f"{a[0]}")