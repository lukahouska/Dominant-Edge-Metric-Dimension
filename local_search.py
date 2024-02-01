import itertools
from sage.graphs.distances_all_pairs import distances_all_pairs
from sage.graphs.graph import Graph
import random
from sage.graphs.trees import TreeIterator





def is_vertex_cover(g, vertex_set):
    for e in g.edges():
        if e[0]  not in vertex_set and e[1] not in vertex_set:
            return False
    return True

def shortest_distance(g, vertex, edge):
    razdalja = min(g.distance(vertex, edge[0]), g.distance(vertex, edge[1]))
    return razdalja



def is_edge_resolving(g, vertex_set):
    for e in g.edges():
        for f in g.edges():
            if e != f:
                s_exist = any([shortest_distance(g, s, e) != shortest_distance(g, s, f) for s in vertex_set])
                if s_exist is False:
                    return False
    return True


def is_dominant_edge_resolving_set(g, vertex_set):
    if is_vertex_cover(g, vertex_set) is True and is_edge_resolving(g, vertex_set) is True:
        return True
    return False

def initial_solution_dedim(g):
    vertices = g.vertices()
    if len(vertices) == Integer(1):
        return g
    if len(vertices) == Integer(2):
        return {vertices[0], vertices[1]}
    else:
        zacetna_resitev = set(random.sample(vertices, len(vertices) - 2 ))
        while is_dominant_edge_resolving_set(g, zacetna_resitev) is False:
            zacetna_resitev = set(random.sample(vertices, len(vertices) - 2 ))
        return zacetna_resitev
    
def initial_solution_edim(g):
    Vertices = g.vertices()
    if len(Vertices) == Integer(1):
        return g
    if len(Vertices) == Integer(2):
        return g
    else:
        Zacetna_resitev = set(random.sample(Vertices, len(Vertices) - 2))
        while is_edge_resolving(g, Zacetna_resitev) is False:
            Zacetna_resitev = set(random.sample(Vertices, len(Vertices) - 2))
        return Zacetna_resitev
    
def local_search_dedim(g):
    zacetna_resitev = initial_solution_dedim(g)
    zacetna_resitev_list = list(zacetna_resitev)
    for vertex in range(0, len(zacetna_resitev_list)):
        nova_resitev = zacetna_resitev.copy()
        nova_resitev.remove(zacetna_resitev_list[vertex])
        if is_dominant_edge_resolving_set(g, nova_resitev) is False:
            nova_resitev.add(zacetna_resitev_list[vertex])
        else:
            zacetna_resitev.remove(zacetna_resitev_list[vertex])
            vertex -= 1
    return nova_resitev

def local_search_edim(g):
    zac_resitev = initial_solution_edim(g)
    zac_resitev_list = list(zac_resitev)
    for vertex in range(0, len(zac_resitev_list)):
        nova_res = zac_resitev.copy()
        nova_res.remove(zac_resitev_list[vertex])
        if is_edge_resolving(g, nova_res) is False:
            nova_res.add(zac_resitev_list[vertex])
        else:
            zac_resitev.remove(zac_resitev_list[vertex])
            vertex -= 1
    return nova_res

def Edim(g, N):
    edim = g
    for i in range(0, N):
        resitev_i = local_search_edim(g)
        if len(resitev_i) < len(edim):
            edim = resitev_i
    if is_edge_resolving(g, edim):
        return edim
        
        
def Dedim(g, N):
    dedim = g
    for i in range(0, N):
        Resitev_i = local_search_dedim(g)
        if len(Resitev_i) < len(dedim):
            dedim = Resitev_i
    if is_dominant_edge_resolving_set(g, dedim):
        return dedim