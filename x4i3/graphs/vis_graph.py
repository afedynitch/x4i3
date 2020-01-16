'''
vis_graph.py

Authors: J Hirdt, D.A. Brown

This module is for making undirected graphs using the networkx package.

'''
from x4i3 import __path__, abundance, endl_Z, fullMonitoredFileName, fullCoupledFileName, fullReactionCountFileName
from x4i3.exfor_utilities import unique
import copy, math, numpy.linalg, time, traceback, sys, os, cPickle, collections, subprocess

'''
try:
    import graph_tool as gt
    HAVEGRAPHTOOL = True
except ImportError:
    import networkx as nx
    HAVEGRAPHTOOL = False
'''
try:
    import networkx as nx
    HAVEGRAPHTOOL = False
except ImportError:
    import graph_tool as gt
    HAVEGRAPHTOOL = True


# -----------------------------------------------------------------------
#   Utilities
# -----------------------------------------------------------------------

def formatExceptionInfo(maxTBlevel=5):
     cla, exc, trbk = sys.exc_info()
     excName = cla.__name__
     try:
         excArgs = exc.__dict__["args"]
     except KeyError:
         excArgs = "<no args>"
     excTb = traceback.format_tb(trbk, maxTBlevel)
     return (excName, excArgs, excTb)



# -----------------------------------------------------------------------
#   Shortest Path Length Function Tests
# -----------------------------------------------------------------------

def get_distance_between_nodes( graph, node0, node1):
    '''Get the distance from node0 to node1 in graph'''
    distance = nx.shortest_path_length (graph,source = node0, target = node1 )
    return distance



# -----------------------------------------------------------------------
#    Things related to elements
# -----------------------------------------------------------------------

def has_element( target ):
    '''
    Returns true if target is or is part of a naturally occurring element, on Earth.
    '''
    sym = target.split('-')[0]
    if len(sym) != 1: sym = sym.capitalize()
    Z = endl_Z.endl_SymbolZ( sym )
    for za in abundance.abundances:
        if za[0] == Z: return True
    return False

def is_element( target ):
    '''
    Returns true if target is an element symbol.
    '''
    return  target.split('-')[-1] == '0'

def get_isotopes_from_element( element ):
    '''
    Scans the targList for elements (of form "Sym-0")
    and returns all the isotopes for "Sym-0" in the targList.
    This routine does not check if elements encountered are 
    valid, in that they actually occur naturally on Earth.
    '''
    targList =[]
    if element.endswith( '-0' ):
        sym = element.split('-')[0].capitalize()
        Z = endl_Z.endl_SymbolZ( sym )
        for za in abundance.abundances:
            if za[0] == Z: 
                newIso = sym.capitalize()+'-'+str(za[1])
                if newIso not in targList: 
                    targList.append( newIso.upper() )
    return targList

    

# -----------------------------------------------------------------------
#    Special node classifications
# -----------------------------------------------------------------------

cieloIsotopes = [ 'H-1(N' , 'U-238(N' , 'U-235(N' , 'PU-239(N' , 'FE-56(N', 'O-16(N']
standardsReactions = [('H-1(N,EL)','SIG') , ('HE-3(N,P)','SIG') , ('LI-6(N,T)','SIG') , ('B-10(N,A+G)','SIG') , ('C-0(N,EL)','SIG') , ('AU-197(N,G)','SIG') , ('U-235(N,F)','SIG') , ('B-10(N,A)','SIG'), ('U-238(N,F)','SIG'), ("B-10(N,A+G)", "PAR,SIG") ]
almostStandardReactions = [('LI-6(N,EL)','SIG') , ('B-10(N,EL)','SIG'),  ('PU-239(N,F)','SIG'), ('U-238(N,G)','SIG'), ("B-10(N,A)", "PAR,SIG")]
soontobeStandards = [("CF-252(0,F)", "NU"), ("CF-252(0,F)", "NU/DE"), ("CF-252(0,F)", "DE")]
dosimiterReactions= [('AL-27(P,X+11-NA-22)','SIG'), ('AL-27(P,X+11-NA-24)','SIG'), ('TI-0(P,X+23-V-48)', 'SIG'), ('NI-0(P,X+28-NI-57)','SIG'),('CU-0(P,X+27-CO-56)','SIG'),('CU-0(P,X+30-ZN-62)','SIG'),('CU-0(P,X+30-ZN-63)','SIG'),('CU-0(P,X+30-ZN-65)','SIG'),('AL-27(D,X+11-NA-22)','SIG'), ('AL-27(D,X+11-NA-24)','SIG'),('TI-0(D,X+23-V-48)', 'SIG'),('FE-0(D,X+27-CO-56)','SIG'),('NI-0(D,X+29-CU-61)','SIG'), ('AL-27(3HE,X+11-NA-22)','SIG'), ('AL-27(3HE,X+11-NA-24)','SIG'),('TI-0(3HE,X+23-V-48)', 'SIG'),('AL-27(A,X+11-NA-22)','SIG'), ('AL-27(A,X+11-NA-24)','SIG'),('TI-0(A,X+23-V-48)', 'SIG'),('CU-0(A,X+31-GA-66)','SIG'),('CU-0(A,X+31-GA-67)','SIG'),('CU-0(A,X+30-ZN-65)','SIG'), ('N-15(P,N+9-0-15)','SIG'), ('O-18(P,N+9-F-18)','SIG'),('ZN-67(P,N+31-GA-67)','SIG'),('ZN-68(P,2N+31-GA-67)','SIG'),('CD-111(P,N+49-IN-111)','SIG'), ('CD-112(P,2N+49-IN-111)','SIG'), ('TE-123(P,N+53-I-123)','SIG'),('TE-124(P,2N+53-I-123)','SIG'),('TE-124(P,N+53-I-124)','SIG'), ('I-127(P,5N+54-XE-123)','SIG'),('I-127(P,3N+54-XE-125)','SIG'),('KR-0(P,X+37-RB-81)','SIG'),('K4-82(P,2N+37-RB-82)','SIG'),('XE-124(P,2N+55-CS-123)','SIG'),('XE-124(P,P+N+54-XE-123)','SIG'),('TL-203(P,2N+82-PB-201)','SIG'),('TL-203(P,2N+82-PB-202+M)','SIG'),('TL-203(P,4N+82-PB-200)','SIG'),('N-14(P,A+6-C-11)','SIG'),('GA-69(P,2N+32-GE-68)','SIG'),('GA-0(P,X+32-GE-68)','SIG'),('O-16(P,A+7-N-13)','SIG'), ('RB-85(P,4N+38-SR-82)','SIG'), ('PB-0(P,X+38-SR-82)','SIG'),('N-14(D,N+8-0-15)','SIG'),('NE-0(D,X+9-F-19)','SIG')]
proposedStandards = [('MO-0(P,X+43-TC-96)', 'SIG'), ('MO-0(A,X+44-RU-97)', 'SIG'), ('CO-59(N,G)','SIG'), ('AL-27(6-C-12,X+11-NA-24)', 'SIG'), ('AL-27(N,P)12-MG-27','SIG'), ('CO-59(N,G)','RI'), ('NI-58(N,P)', 'SIG'), ('U-235(N,F+ELEM/MASS)', 'FY')]
proposedAndStandards = [('MO-0(P,X+43-TC-96)', 'SIG'), ('MO-0(A,X+44-RU-97)', 'SIG'), ('CO-59(N,G)','SIG'), ('AL-27(6-C-12,X+11-NA-24)', 'SIG'), ('AL-27(N,P)12-MG-27','SIG'), ('CO-59(N,G)','RI'), ('NI-58(N,P)', 'SIG'), ('U-235(N,F+ELEM/MASS)', 'FY'),('H-1(N,EL)','SIG') , ('HE-3(N,P)','SIG') , ('LI-6(N,T)','SIG') , ('B-10(N,A+G)','SIG') , ('C-0(N,EL)','SIG') , ('AU-197(N,G)','SIG') , ('U-235(N,F)','SIG') , ('B-10(N,A)','SIG'), ('U-238(N,F)','SIG'), ("B-10(N,A+G)", "PAR,SIG") ]

        
# -----------------------------------------------------------------------
#    Class Reaction Node
# -----------------------------------------------------------------------

class Reaction_Node:
    '''
    Simple holder for reaction node information.
    '''

    def __init__( self, reaction, observable, weight=1, count=1 ):
		self.reaction = reaction
		self.observable = observable
		self.target = self.reaction.split('(')[0]
		self.weight = weight
		self.count = count # to be removed

    def is_elemental_target(self): return is_element( self.target )

    def is_cielo_target(self): return self.reaction.split(',')[0] in cieloIsotopes

    def is_standard_reaction(self): return self.as_tuple() in standardsReactions

    def is_dosimiter_reaction(self): return self.as_tuple() in dosimiterReactions
    
    def is_soon_tobe_standard(self): return self.as_tuple() in soontobeStandards
    
    def is_almost_standard_reaction(self): return self.as_tuple() in almostStandardReactions

    def is_proposed_standard(self): return self.as_tuple() in proposedStandards

    def is_proposed_and_standard(self): return self.as_tuple() in proposedAndStandards
    
    def is_special(self): return self.as_tuple() in almostStandardReactions+soontobeStandards+dosimiterReactions+standardsReactions or self.is_cielo_target()
    
    def is_special_or_proposed(self): return self.as_tuple() in proposedStandards+almostStandardReactions+soontobeStandards+dosimiterReactions+standardsReactions or self.is_cielo_target()

    def is_proposed_or_dosimiter(self): return self.as_tuple() in dosimiterReactions+proposedStandards
    
    def as_tuple(self): return (self.reaction,self.observable)

    def __str__(self):
		return self.reaction + self.observable
	
    def __hash__(self):
		return hash( self.as_tuple() )


# -----------------------------------------------------------------------
#    Class Correlation Edge
# -----------------------------------------------------------------------

class Correlation_Edge:
    '''
    Simple holder for correlation edge information.
    '''

    def __init__( self, node0, node1, weights={} ):
		self.node0 = node0
		self.node1 = node1
		self.is_part_of_composite_target = False
		self.is_same_target = self.node0.target = self.node1.target
		self.is_inclusive_reaction = False
		self.is_resonance = False
		self.is_coupled_reactions = False
		self.is_monitored_reactions = False
		self.weights = weights 

    def as_tuple(self): return (self.node0,self.node1)

    def __str__(self):
		return str( self.as_tuple() )
	
    def __hash__(self):
		return hash( self.as_tuple() )


 




# -----------------------------------------------------------------------
#    Graph coloration function
# -----------------------------------------------------------------------
def add_vertex(theGraph, iterator, rxnstring ):
    iterator = theGraph.add_vertex( )
    theGraph.vertex_properties["node_name"][iterator]= str(rxnstring)
    theGraph.vertex_properties["node_instance"][iterator]= Reaction_Node(str(rxnstring).split(')')[0]+')', str(rxnstring).split(')')[-1])
    if theGraph.vertex_properties["node_instance"][iterator].is_standard_reaction():
        theGraph.vertex_properties["node_color"][iterator]='#03ee1f'
    if theGraph.vertex_properties["node_instance"][iterator].is_cielo_target():
        theGraph.vertex_properties["node_color"][iterator]='#190ce9'
    if theGraph.vertex_properties["node_instance"][iterator].is_almost_standard_reaction():
        theGraph.vertex_properties["node_color"][iterator]='#03e4ee'
    if theGraph.vertex_properties["node_instance"][iterator].is_soon_tobe_standard():
        theGraph.vertex_properties["node_color"][iterator]='#e90ca8'
    if theGraph.vertex_properties["node_instance"][iterator].is_dosimiter_reaction():
        theGraph.vertex_properties["node_shape"][iterator]='square'
    if not theGraph.vertex_properties["node_instance"][iterator].is_standard_reaction() \
    and not theGraph.vertex_properties["node_instance"][iterator].is_cielo_target() \
    and not theGraph.vertex_properties["node_instance"][iterator].is_soon_tobe_standard() \
    and not theGraph.vertex_properties["node_instance"][iterator].is_dosimiter_reaction(): 
        theGraph.vertex_properties["node_color"][iterator] = '#ee0303'

# -----------------------------------------------------------------------
#    Function to add stuff to the graph
# -----------------------------------------------------------------------

def graph_init():
    # Initialize the Graph
    if HAVEGRAPHTOOL:
        G = gt.Graph(directed = False)
        G.vertex_properties["node_name"] = G.new_vertex_property("string")
        G.vertex_properties["node_color"] = G.new_vertex_property("string")
        G.vertex_properties["node_shape"] = G.new_vertex_property("string")
        G.vertex_properties["node_linestyle"] = G.new_vertex_property("string")
        G.vertex_properties["node_instance"] = G.new_vertex_property("python::object")
        G.edge_properties["edge_color"] = G.new_edge_property("string")
        G.edge_properties["edge_linestyle"] = G.new_edge_property("string")
        return G
    else:
        G = nx.Graph()
        return G

def add_to_graph( theGraph, nodeMap, maxCount=None ):
    '''
    Add nodes and edges to a map.
    @type theGraph networkx.Graph
    @param theGraph The instance of the Graph we are adding stuff to.
    @type nodeMap dict
    @param nodeMap A Python dict whose key is arbitrary (but is usually a tuple of form (ENTRY,SUBENT,pointer), from EXFOR) and whose value is a list.
        This list is a list of nodes that are to be connected by this routine.  The nodes are Reaction_Node instances.
    @type maxCount int
    @param maxCount Limit the number of EXFOR subentries to process when adding to graph.  "None" means there is no limit.
    @rtype int
    @return Number of EXFOR subentries processed and added to graph 
    '''
    if HAVEGRAPHTOOL:   
        count = 0
        node0 = 0
        node1 = 0
        edge_list = []
        for nodeListKey in nodeMap:
            for ik0, k0 in enumerate(nodeMap[nodeListKey]):
                
                if not isinstance(k0,Reaction_Node): raise TypeError( "Nodes must be Reaction_Node instances")            
                if k0 in theGraph.vertices():  pass #(Needs to be changed)   theGraph.node[k0]['nodeInstance'].count += 1
                else:                    
                    add_vertex(theGraph, node0, k0 )
                for k1 in nodeMap[nodeListKey][ ik0+1: len( nodeMap[nodeListKey] ) ]:
                    if not isinstance(k1,Reaction_Node): raise TypeError( "Nodes must be Reaction_Node instances")            
                    if k1 in theGraph.vertices():  pass #(Needs to be changed)    theGraph.node[k1]['nodeInstance'].count += 1
                    else:                    
                        add_vertex(theGraph, node1, k1 )
                    theGraph.add_edge( node0, node1 )
                    edge_list.append( (node0, node1) )
            count = count + 1
            if maxCount is not None and count >= maxCount: break
        return edge_list	 
     
    else:
        count=0
        edge_list = []
        for nodeListKey in nodeMap:
            for ik0, k0 in enumerate(nodeMap[nodeListKey]):
                
                if not isinstance(k0,Reaction_Node): raise TypeError( "Nodes must be Reaction_Node instances")            
                if k0 in theGraph.node:  theGraph.node[k0]['nodeInstance'].count += 1
                else:                    theGraph.add_node( str( k0 ), nodeInstance = k0 )			

                for k1 in nodeMap[nodeListKey][ ik0+1: len( nodeMap[nodeListKey] ) ]:	
                
                    if not isinstance(k1,Reaction_Node): raise TypeError( "Nodes must be Reaction_Node instances")            
                    if k1 in theGraph.node:  theGraph.node[k1]['nodeInstance'].count += 1
                    else:                    theGraph.add_node( str( k1 ), nodeInstance = k1 )
                    
                    theGraph.add_edge( str( k0 ), str( k1 ) )
                    edge_list.append( ( str( k0 ), str( k1 ) ) )

            count = count + 1
            if maxCount is not None and count >= maxCount: break
        return edge_list	

def add_rxn_remaining( theGraph, nodelist, maxCount=None ):

    #Add nodes for the recfile nodes
    if HAVEGRAPHTOOL:
        count = 0
        ele = 0
        for node_element in nodelist:
                    
            if node_element in theGraph.vertices(): pass
            else:
                add_vertex(theGraph, ele, node_element )
                count = count + 1
            if maxCount is not None and count >= maxCount: break
    else: 
        count = 0
        for node_element in nodelist:
            if not isinstance( node_element, Reaction_Node ): raise TypeError( "Nodes must be Reaction_Node instances")         
            if node_element in theGraph.node: pass
            else:
                
                theGraph.add_node( str( node_element ), nodeInstance = node_element )
                count = count + 1
                
            if maxCount is not None and count >= maxCount: break


# -----------------------------------------------------------------------
#   Some handy graph query functions
# -----------------------------------------------------------------------

def get_elemental_nodes( theGraph ):
    '''
    Bug: theGraph[q] gives us {'ZR-91(N,EL)STF': {}} instead of 
{'ZR-91(N,EL)STF': {'nodeInstance': <x4i.vis_graph.Reaction_Node instance at 0xaec398c>}}

    '''
    if HAVEGRAPHTOOL:
        element_list = []    
        for q in theGraph.vertices():
            p = theGraph.vertex_properties["node_name"][q].split('(')[0]
            if p.split('-')[-1] == '0':
                element_list.append(theGraph.vertex_properties["node_name"][q])  
        return element_list

    else: 
        element_list = []    
        for q in theGraph.nodes(data=True):
            p = q[0].split('(')[0]
            if p.split('-')[-1] == '0':
                element_list.append(q[0])  
        return element_list


def get_standard_nodes( theGraph ):
    if HAVEGRAPHTOOL:  
        return [n for n, d in theGraph.vertices() if theGraph.vertex_properties["node_instance"].is_standard_reaction()]
    else: 
        return [n for n, d in theGraph.nodes(data = True) if d['nodeInstance'].is_standard_reaction()]
           
           
def get_cielo_nodes( theGraph ): 
    if HAVEGRAPHTOOL:  
        return [n for n, d in theGraph.vertices() if theGraph.vertex_properties["node_instance"].is_cielo_target()]
    else: 
        return [n for n, d in theGraph.nodes(data = True) if d['nodeInstance'].is_cielo_target()]


def get_dosimiter_nodes( theGraph):
    if HAVEGRAPHTOOL:  
        return [n for n, d in theGraph.vertices() if theGraph.vertex_properties["node_instance"].is_dosimiter_reaction()]
    else:
        return [n for n, d in theGraph.nodes(data = True) if d['nodeInstance'].is_dosimiter_reaction()]


def get_almost_standard_nodes( theGraph ): 
    if HAVEGRAPHTOOL:  
        return [n for n, d in theGraph.vertices() if theGraph.vertex_properties["node_instance"].is_almost_standard_reaction()]
    else:
        return [n for n, d in theGraph.nodes(data = True) if d['nodeInstance'].is_almost_standard_reaction()]


def get_soon_to_be_standard_nodes( theGraph ): 
    if HAVEGRAPHTOOL:  
        return [n for n, d in theGraph.vertices() if theGraph.vertex_properties["node_instance"].is_soon_tobe_standard()]
    else:
        return [n for n, d in theGraph.nodes(data = True) if d['nodeInstance'].is_soon_tobe_standard()]


def get_proposed_standard_nodes( theGraph ):
    if HAVEGRAPHTOOL:  
        return [n for n, d in theGraph.vertices() if theGraph.vertex_properties["node_instance"].is_proposed_standard()]
    else:
        return [n for n, d in theGraph.nodes(data = True) if d['nodeInstance'].is_proposed_standard()]


def get_proposed_and_standard_nodes( theGraph ):
    if HAVEGRAPHTOOL:  
        return [n for n, d in theGraph.vertices() if theGraph.vertex_properties["node_instance"].is_proposed_and_standard()]
    else:    
        return [n for n, d in theGraph.nodes(data = True) if d['nodeInstance'].is_proposed_and_standard()]
    

def get_special_nodes( theGraph ):
    if HAVEGRAPHTOOL:  
        return [n for n, d in theGraph.vertices() if theGraph.vertex_properties["node_instance"].is_special()]
    else:
        return [n for n, d in theGraph.nodes(data = True) if d['nodeInstance'].is_special()]
     
           
def get_special_or_proposed_nodes( theGraph ):
    if HAVEGRAPHTOOL:  
        return [n for n, d in theGraph.vertices() if theGraph.vertex_properties["node_instance"].is_special_or_proposed()]
    else:
        return [n for n, d in theGraph.nodes(data = True) if d['nodeInstance'].is_special_or_proposed()]

           
def get_proposed_or_dosimiter_nodes( theGraph ):
    if HAVEGRAPHTOOL:  
        return [n for n, d in theGraph.vertices() if theGraph.vertex_properties["node_instance"].is_proposed_or_dosimiter()]
    else:
        return [n for n, d in theGraph.nodes(data = True) if d['nodeInstance'].is_proposed_or_dosimiter()]
           
           
def is_matching_process( theGraph, ProcString ):
    if HAVEGRAPHTOOL:  
        ProcStringList=[]
        for k in theGraph.vertices():
            if theGraph.vertex_properties["node_name"][k].split(')')[-1] == ProcString:ProcStringList.append(theGraph.vertex_properties["node_name"][k])
    else:
        ProcStringList=[]
        for k in theGraph.nodes(data = True):
            if k[0].split(')')[0].split(',')[-1] == ProcString:ProcStringList.append(k[0])
        return ProcStringList
            
            
def is_matching_quantity( theGraph, QuantString ):
    if HAVEGRAPHTOOL:
        QuantStringList=[]
        for k in theGraph.vertices():
            if theGraph.vertex_properties["node_name"][k].split(')')[-1] == QuantString: QuantStringList.append(theGraph.vertex_properties["node_name"][k])
    else:
        QuantStringList=[]
        for k in theGraph.nodes(data = True):
            if k[0].split(')')[-1] == QuantString: QuantStringList.append(k[0])
        return QuantStringList
 
 
# -----------------------------------------------------------------------
#   Some handy graph modification functions
# -----------------------------------------------------------------------
def filter_lists_and_graph( theGraph, listOfLists, filterFunc ):
    '''
    Does an inplace filter of all lists in listOfLists and theGraph itself.  

    The function filterFunc is a user provided function that takes a node 
    (really the key of the node in theGraph) as an argument and returns True/False.
    '''
    for edge_list in listOfLists:
        edge_copy = copy.copy( edge_list )
        for e in edge_copy:
        #for e in edge_list:
            if not ( filterFunc( e[0] ) and filterFunc( e[1] ) ) and e in edge_list: edge_list.remove( e )
    for p in filter( lambda x: not filterFunc(x), theGraph.nodes() ): theGraph.remove_node(p)

def add_edges_for_matching_nodes( theGraph, edgeMatchFunc ):
    '''
    Update theGraph by adding edges between all nodes n0, n1 for which the 
    function edgeMatchFunc( n0, n1 ) is True.  
    
    Returns a list of all the added edges.
    '''
    raise NotImplementedError( "This routine is untested, don't use it yet" )
    result = []
    node_list = theGraph.nodes()
    for ik,k in enumerate(node_list):
        for p in node_list[ik+1:]:
            if edgeMatchFunc( k, p ):
                theGraph.add_edge(k,p)
                result.append((k,p))
        else: pass
    return result

    
# -----------------------------------------------------------------------
#    Some handy graph statistics functions
# -----------------------------------------------------------------------
def get_node_degree( theGraph, node0):
    dgre = nx.degree( theGraph, node0 )
    return dgre

'''
Before you can use any of the two* functions below you must first create a list of tuples of format (node, degree) this list is node_list1 for both functions below.This will automatically be done in vis-coupled.py before these two functions are called creating the list for you.
'''

def get_nodes_with_degree( node_list1,  degree ):
    '''
    Function get_nodes_with_degree, takes a node_list1 which is a list of tuples (node, degree) and takes
     an argument of node_list2 which will be returned with a list of nodes that contain the degree you
    are searching for
    '''
    node_list2 = []
    for k in node_list1:
        if k[1] == degree:
            node_list2.append(k[0])
        else: pass
    return node_list2

def get_degree_for_reaction(node0, node_list1):
    '''
    Function takes the input of a node and a node_list1 which is a list of tuples (node, degree)
    Function also takes a degree_list to which it will store the degree value to output
    will search the first element of all the nodes in the nodelist and when the node being searched for 
    matches it will return the degree    
    '''
    
    for k in node_list1:
        if k[0] == node0:
            node_degree = k[1]
        else: pass
    return node_degree

def get_spectral_density( theGraph):
     eigenvalues=numpy.linalg.eigvalsh
     e=eigenvalues(nx.adjacency_matrix(theGraph))
     return e

def get_node_type( node ):
    if (node.split(')')[0]+')',node.split(')')[-1]) in cieloIsotopes:
        nodeType = "CIELO"
    elif (node.split(')')[0]+')',node.split(')')[-1]) in standardsReactions:
        nodeType = "STANDARD"
    elif (node.split(')')[0]+')',node.split(')')[-1]) in almostStandardReactions:
        nodeType = "ALMOST STANDARD"
    elif (node.split(')')[0]+')',node.split(')')[-1]) in soontobeStandards:
        nodeType = "SOON TO BE STANDARD"
    elif (node.split(')')[0]+')',node.split(')')[-1]) in dosimiterReactions:
        nodeType = "DOSIMITER"
    elif (node.split(')')[0]+')',node.split(')')[-1]) in proposedStandards:
        nodeType = "Proposed Standard"
    else:
        nodeType = "REGULAR"
    return nodeType

def get_info( theGraph ):
    dgre_list = []
    for k in theGraph.nodes():
        dgre_list.append( theGraph.degree( k ) )
    summation = 0.0
    for kk in dgre_list:
        summation = kk + summation
    graphInfo = {"# of Nodes" : theGraph.number_of_nodes(),"# of Edges" : theGraph.number_of_edges(), "Is connected" : nx.is_connected( theGraph ), "# of Isolates" : len( nx.isolates( theGraph ) ), "Probability of Connection" : (theGraph.number_of_edges())/((theGraph.number_of_nodes()*(theGraph.number_of_nodes()-1.0))/2.0), "<k>" : summation/theGraph.number_of_nodes(), "k^2" : math.pow(summation/theGraph.number_of_nodes(),2)}
    if nx.is_connected( theGraph ) == True:
        graphInfo["Diameter"] = nx.diameter( theGraph )
        graphInfo["Radius"] = nx.radius( theGraph )
    return graphInfo

def get_node_info( theGraph, node, centralityMeasures={} ):
    p = centralityMeasures.get( 'degree_centrality', {} ) 
    f = centralityMeasures.get( 'load_centrality', {} )
    d = centralityMeasures.get( 'eigenvalue_centrality', {} )
    if d:   eigencentral = d[node]
    else:   eigencentral = None
    if p:   dgrcentral = p[node]
    else:   dgrcentral = None
    if f:   loadcentral = f[node]
    else:   loadcentral = None
    node_info = { \
        "RXN" : node.split(')')[0]+')'  , \
        "Degree Centrality" : dgrcentral ,\
        "Observable" : node.split(')')[-1], \
        "Degree" : theGraph.degree( node ), \
        "Load Centrality" : loadcentral, \
        "Eigenvalue Centrality" : eigencentral, \
        "Clustering Coefficient" : nx.clustering( theGraph, node ),\
        "Closeness" : nx.closeness_centrality( theGraph, node ), \
        "Betweenness" : nx.betweenness_centrality( theGraph )[node], \
        "Node Type" : get_node_type( node )}
    if nx.is_connected( theGraph ) : node_info['Eccentricity'] = nx.eccentricity( theGraph, node )
    return node_info

def get_distance_to_different_nodes( theGraph, nodeList ):
    '''
    Gets the shortest distance of each nodes in theGraph to a node in the nodeList
    
    parameters ::
    
        theGraph : the networkx graph instance 
        nodeList : list of node keys of the nodes you want the distance to 
    '''
    distance_to_goal = {}
    sl = {}
    goal_distance = []
    goal_distance_list = []
    Unconnected_list = []
    if nodeList == []:
        return goal_distance_list, Unconnected_list
    else:
        for t in nodeList: sl[t] = [Reaction_Node(t.split(')')[0]+')', t.split(')')[1])]
        for k in theGraph.nodes():
                sd_list = []
                for z in sl:
                    try: sd_list.append(get_distance_between_nodes(theGraph,k,z)) 
                    except ( nx.NetworkXNoPath,  nx.NetworkXError ): sd_list.append(1e9)
                sl_min = min(sd_list)
                if sl_min > 1e8 and not k in Unconnected_list:
                    Unconnected_list.append(k)
                    sl_min = -10
                goal_distance.append( sl_min )
        distance_to_goal = {}
        for v in goal_distance:
            if v not in distance_to_goal:distance_to_goal[v] = 1  
            elif v in distance_to_goal:distance_to_goal[v] = distance_to_goal[v] + 1    
        goal_distance_list = sorted(distance_to_goal.items())
        return goal_distance_list, Unconnected_list   

def doatopten( e, title, numToShow=20 ):
            print "Top",numToShow,title
            el = sorted(e.items(),cmp=lambda x,y: cmp(x[1], y[1]),reverse=True)
            print '\n'.join(map(str,el[:numToShow]))

def get_independent_cluster_distributions( theGraph, Unconnected_list ):
    no_connections_list = []
    unknown_cluster_list = []
    for p in theGraph.nodes():
        for h in Unconnected_list:
            if p == h:
                if get_node_degree( theGraph, p) == 0:
                    no_connections_list.append(h)
                else:        
                    unknown_cluster_list.append(h)
    count_list = []
    for k in unknown_cluster_list:
        count = 0
        cluster_list = []
        neighbors_list = []
        for c in theGraph.neighbors(k):
            neighbors_list.append(c)
            cluster_list.append(c)
            count = count + 1
        for q in neighbors_list:
            for gg in theGraph.neighbors(q):
                if gg not in neighbors_list:
                    neighbors_list.append(gg)
                    cluster_list.append(gg)
                    count = count + 1  
        if cluster_list == []:  
            pass
        if cluster_list != []:
            count_list.append(count)
        for tt in cluster_list:
            unknown_cluster_list.remove(tt)
    cluster_counts = {}
    cluster_counts_list = []
    for v in count_list:
        if v not in cluster_counts:cluster_counts[v] = 1  
        elif v in cluster_counts:cluster_counts[v] = cluster_counts[v] + 1    
    cluster_counts_list = sorted(cluster_counts.items())
    return cluster_counts_list
    
# -----------------------------------------------------------------------
#    Plotting
# -----------------------------------------------------------------------
def make_histogram( list1, bincount ,title, xlabel, ylabel, outFilePrefix = None):
    import matplotlib.pyplot as plt
    from pylab import hist
    hist(list1, bins = bincount)
    if outFilePrefix == None: 
        plt.title(title)
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)     
        plt.axis([-25,25,0,4000])
        plt.show()
        plt.clf()
    else:
        plt.title(title)
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)                          
        plt.axis([-25, 25, 0, 4000])
        plt.savefig(outFilePrefix+'.png', bbox_inches = 0 )
        plt.clf()

def plot_x_y_histogram( datalist, title, xlabel, ylabel, xlog = False, ylog = False, xaxislength = (None, None), yaxislength = (None, None), outFilePrefix = None, Legend = None, Legend1 = None, Legend2 = None ):
    import matplotlib.pyplot as plt
    for dataset in datalist:
        x = []
        y = []
        for r in dataset:
            count = 0
            for k in r:
                if count == 0:              
                    x.append(k)
                    count = count + 1
                else:y.append(k)
        plt.plot(x,y,marker='o')
    if xlog != False and ylog != False: plt.loglog()
    elif xlog!= False: plt.semilogx()
    elif ylog!= False: plt.semilogy()
    if xaxislength != (None, None) and yaxislength != (None, None): plt.axis([xaxislength[0] , xaxislength[1], yaxislength[0], yaxislength[1] ]) 
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.legend((Legend, Legend1, Legend2),'upper center', shadow = True)
    if outFilePrefix == None:   
        plt.show(  )
        plt.clf()
    else:                       
        plt.savefig(outFilePrefix+'.png', bbox_inches = 0 )
        plt.clf()


# ---- Graph addition operations -----

def add_standards(max_count, G, standard_edges):
    '''Get the Standard data and couple together'''
    sd = {"key":[Reaction_Node(y[0],y[1]) for y in standardsReactions]}
    standard_edges = add_to_graph(G,sd,max_count)
    return standard_edges

def add_almost_standards( max_count, G, almost_standard_edges ):
    '''Show almost standards and couple together'''
    asd = {"key":[Reaction_Node(y[0],y[1]) for y in almostStandardReactions]}
    almost_standard_edges = add_to_graph(G,asd, max_count)
    asd = {"key":[Reaction_Node(y[0],y[1]) for y in soontobeStandards]}
    almost_standard_edges += add_to_graph(G,asd, max_count)
    return almost_standard_edges

def add_standard_almost_standard( max_count, G, standard_edges, almost_standard_edges ):
    '''Get the Standard data and almost standards and both couple together'''
    sd = {"key":[Reaction_Node(y[0],y[1]) for y in standardsReactions]}
    standard_edges = add_to_graph(G,sd,max_count)
    asd = {"key":[Reaction_Node(y[0],y[1]) for y in standardsReactions] + \
        [Reaction_Node(y[0],y[1]) for y in almostStandardReactions] + \
        [Reaction_Node(y[0],y[1]) for y in soontobeStandards]}
    almost_standard_edges = add_to_graph(G,asd, max_count)
    asd = {"key":[Reaction_Node(y[0],y[1]) for y in soontobeStandards]}
    almost_standard_edges += add_to_graph(G,asd, max_count)
    return standard_edges, almost_standard_edges

def add_CIELO(G, cielo_edges):
    cielo_nodes=[n for n, d in G.nodes(data = True) if d['nodeInstance'].is_cielo_target()]
    for p in cielo_nodes:
        for k in cielo_nodes:
            if p == k:
                pass
            else:
                G.add_edge(p,k)
                cielo_edges.append((p,k)) 
    return cielo_edges

def add_Coupled( max_count, inFile, G, coupled_edges):
    # Get the coupled data
    cou_timer=time.clock()
    f = cPickle.load( open( inFile, mode='r' ) )
    ff = {}
    for x in f:
        ff[x] = [Reaction_Node(y[0],y[1]) for y in f[x]]
        if len( ff[x] ) < 2: print 'Warning:',x,map(str,ff[x]), '(Coupled) has less than two nodes'
    coupled_edges = add_to_graph(G,ff, max_count)
    print "Show all Coupled Data", time.clock()-cou_timer, "Seconds" 
    return coupled_edges

def add_Monitor( max_count, monFile, verbose, G, monitored_edges ):
    # Get the monitor data
    mon_timer=time.clock()
    m = cPickle.load( open( monFile, mode='r' ) )
    mm = {}
    for x in m: 
        mm[x] = [Reaction_Node(y[0],y[1]) for y in m[x]]
        if len( mm[x] ) < 2 and verbose: print 'Warning:',x,map(str,mm[x]), '(Monitor) has less than two nodes'
    monitored_edges = add_to_graph(G,mm, max_count)
    if verbose: print monitored_edges
    print "Show all Monitor Data", time.clock()-mon_timer, "Seconds" 
    return monitored_edges

def add_Reaction(max_count, recFile, G):
    '''Show all Reaction Data'''
    rxn_timer=time.clock()
    r = cPickle.load( open( recFile, mode='r') )
    c = []
    for k in r: c.append( Reaction_Node( k[0], k[1], count=r[k] ) )
    add_rxn_remaining(G,c,max_count)
    print "Show all Reaction Data", time.clock()-rxn_timer, "Seconds" 

def add_elemental(max_count, G, element_edges):
    fe = {}
    for o in get_elemental_nodes(G) :
        isotope_lists= get_isotopes_from_element( o.split('(')[0] )
        fe[o] = [Reaction_Node(o.split(')')[0] + ')' , o.split(')')[1])]
        for k in isotope_lists:
            oo = o.replace(o.split('(')[0],k)  
            fe[o].append( Reaction_Node( oo.split(')')[0] + ')', oo.split(')')[1] ) )
    element_edges = add_to_graph(G,fe, max_count)
    return element_edges

def add_inclusive(max_count, G, inclusive_process_edges):
    fe = {}
    for o in is_matching_process( G, 'ABS' ) :
        if 'SIG' in o and 'N,' in o:
            fe[o] = [Reaction_Node(o.split(')')[0] + ')' , o.split(')')[1])]
            oo=o.replace('ABS', 'TOT')
            fe[o].append( Reaction_Node( oo.split(')')[0] + ')', oo.split(')')[1] ) )
            oo=o.replace('ABS', 'SCT')
            fe[o].append( Reaction_Node( oo.split(')')[0] + ')', oo.split(')')[1] ) )
            inclusive_process_edges += add_to_graph(G,fe, max_count)
    fe = {}
    for o in is_matching_process( G, 'ABS' ) :
        if 'SIG' in o and 'N,' in o:
            fe[o] = [Reaction_Node(o.split(')')[0] + ')' , o.split(')')[1])]
            oo=o.replace('ABS', 'NON')
            fe[o].append( Reaction_Node( oo.split(')')[0] + ')', oo.split(')')[1] ) )
            oo=o.replace('ABS', 'INL')
            fe[o].append( Reaction_Node( oo.split(')')[0] + ')', oo.split(')')[1] ) )
            inclusive_process_edges += add_to_graph(G,fe, max_count)
    fe = {}
    for o in is_matching_process( G, 'NON' ) :
        if 'SIG' in o and 'N,' in o:
            fe[o] = [Reaction_Node(o.split(')')[0] + ')' , o.split(')')[1])]
            oo=o.replace('NON', 'TOT')
            fe[o].append( Reaction_Node( oo.split(')')[0] + ')', oo.split(')')[1] ) )
            oo=o.replace('NON', 'EL')
            fe[o].append( Reaction_Node( oo.split(')')[0] + ')', oo.split(')')[1] ) )
            inclusive_process_edges += add_to_graph(G,fe, max_count)
    fe = {}
    for o in is_matching_process( G, 'SCT' ) :
        if 'SIG' in o and 'N,' in o:
            fe[o] = [Reaction_Node(o.split(')')[0] + ')' , o.split(')')[1])]
            oo=o.replace('SCT', 'INL')
            fe[o].append( Reaction_Node( oo.split(')')[0] + ')', oo.split(')')[1] ) )
            oo=o.replace('SCT', 'EL')
            fe[o].append( Reaction_Node( oo.split(')')[0] + ')', oo.split(')')[1] ) )
            inclusive_process_edges += add_to_graph(G,fe, max_count)  
    return inclusive_process_edges

def add_special_quants(max_count, G, special_quants_edges):
    sq={}
    for o in is_matching_quantity( G, 'ETA' ):
        sq[o] = [Reaction_Node(o.split(')')[0]+')', o.split(')')[1])]
        if "(N,F)" in o: 
            oo=o.replace('ETA', 'NU' )
            sq[o].append( Reaction_Node(oo.split(')')[0]+')', oo.split(')')[1]))
        if "(N,F)" in o: 
            oo=o.replace('ETA', 'SIG')
            sq[o].append( Reaction_Node(oo.split(')')[0]+')', oo.split(')')[1]))
        if "(N,F)" in o: 
            oo = oo.replace('N,F', 'N,G')
            [o].append( Reaction_Node(oo.split(')')[0]+')', oo.split(')')[1]))
        special_quants_edges += add_to_graph(G, sq, max_count)
    sq={}
    for o in is_matching_quantity( G, 'ALF' ):
        sq[o] = [Reaction_Node(o.split(')')[0]+')', o.split(')')[1])]
        if "(N,G)" in o: 
            oo=o.replace('ALF', 'SIG' )
            sq[o].append( Reaction_Node(oo.split(')')[0]+')', oo.split(')')[1]))
            oo=o.replace('ALF', 'SIG')
            cc=oo.replace('(N,G)', '(N,F)')    
            sq[o].append( Reaction_Node(cc.split(')')[0]+')', cc.split(')')[1]))
        if "(N,ABS)" in o:
            oo=o.replace('ALF', 'SIG')
            cc=oo.replace('(N,ABS)', '(N,F)')    
            sq[o].append( Reaction_Node(cc.split(')')[0]+')', cc.split(')')[1]))
            cc=oo.replace('(N,ABS)', '(N,G)')    
            sq[o].append( Reaction_Node(cc.split(')')[0]+')', cc.split(')')[1]))
        special_quants_edges += add_to_graph(G, sq, max_count)
        
    for o in is_matching_quantity( G, 'SIG' ):
        sq={}
        sq[o] = [Reaction_Node(o.split(')')[0]+')', o.split(')')[1])]
        if "(N,G)" in o or "N,F)" in o or "(N,TOT)" in o or "(N,EL)" in o: 
            oo=o.replace('SIG', 'RI' )
            sq[o].append( Reaction_Node(oo.split(')')[0]+')', oo.split(')')[1]))
        special_quants_edges += add_to_graph(G, sq, max_count)  
    return special_quants_edges

def add_special_elemental(max_count, G, element_edges):
    fe = {}
    for o in get_elemental_nodes(G) :
        isotope_lists= get_isotopes_from_element( o.split('(')[0] )
        fe[o] = [Reaction_Node(o.split(')')[0] + ')' , o.split(')')[1])]
        for k in isotope_lists:
            oo = o.replace(o.split('(')[0],k)  
            fe[o].append( Reaction_Node( oo.split(')')[0] + ')', oo.split(')')[1] ) )
    element_edges = add_to_graph(G,fe, max_count)
    return element_edges

# -----filter functions here -----

def keep_only_cross(G, standard_edges, almost_standard_edges, cielo_edges, coupled_edges, monitored_edges, element_edges, inclusive_process_edges, special_quants_edges, target_edges, target_proj_link_edges):
    ddd = time.clock( )
    def is_cross_section( xyx ): return 'SIG' in xyx or 'ALF' in xyx
    filter_lists_and_graph( G, [ monitored_edges, coupled_edges, cielo_edges, almost_standard_edges, standard_edges, element_edges, target_edges, inclusive_process_edges, special_quants_edges ], is_cross_section )  
    eee = time.clock( )
    print "Show Cross Only Takes", eee-ddd, "Seconds" 

def keep_only_neutron(G, standard_edges, almost_standard_edges, cielo_edges, coupled_edges, monitored_edges, element_edges, inclusive_process_edges, special_quants_edges, target_edges, target_proj_link_edges):
    ded = time.clock( )
    def is_neutron_projectile( x ): return x.split(',')[0].split('(')[-1] =='N'
    filter_lists_and_graph( G, [ monitored_edges, coupled_edges, cielo_edges, almost_standard_edges, standard_edges, element_edges, target_edges, inclusive_process_edges, special_quants_edges ], is_neutron_projectile )
    fed = time.clock( )
    print "Show Neutron Only Takes", fed-ded, "Seconds"

def keep_only_proton(G, standard_edges, almost_standard_edges, cielo_edges, coupled_edges, monitored_edges, element_edges, inclusive_process_edges, special_quants_edges, target_edges, target_proj_link_edges):
    qqq = time.clock( )
    def is_proton_projectile( x ): return x.split(',')[0].split('(')[-1] =='P'
    filter_lists_and_graph( G, [ monitored_edges, coupled_edges, cielo_edges, almost_standard_edges, standard_edges, element_edges, target_edges, inclusive_process_edges, special_quants_edges ], is_proton_projectile )
    www = time.clock( )
    print "Show Proton Only Takes", www-qqq, "Seconds"

def keep_only_deuteron(G, standard_edges, almost_standard_edges, cielo_edges, coupled_edges, monitored_edges, element_edges, inclusive_process_edges, special_quants_edges, target_edges, target_proj_link_edges):
    trt = time.clock( )
    def is_deuteron_projectile( x ): return x.split(',')[0].split('(')[-1] =='D'
    filter_lists_and_graph( G, [ monitored_edges, coupled_edges, cielo_edges, almost_standard_edges, standard_edges, element_edges, target_edges, inclusive_process_edges, special_quants_edges ], is_deuteron_projectile )
    dee = time.clock( )
    print "Show Deutron Only Takes", dee-trt, "Seconds"

def keep_only_alpha(G, standard_edges, almost_standard_edges, cielo_edges, coupled_edges, monitored_edges, element_edges, inclusive_process_edges, special_quants_edges, target_edges, target_proj_link_edges):
    aaa = time.clock( )
    def is_alpha_projectile( x ): return x.split(',')[0].split('(')[-1] =='A'
    filter_lists_and_graph( G, [ monitored_edges, coupled_edges, cielo_edges, almost_standard_edges, standard_edges, element_edges, target_edges, inclusive_process_edges, special_quants_edges ], is_alpha_projectile )
    bbb = time.clock( )
    print "Show Alpha Only Takes", bbb-aaa, "Seconds"

def keep_only_gamma(G, standard_edges, almost_standard_edges, cielo_edges, coupled_edges, monitored_edges, element_edges, inclusive_process_edges, special_quants_edges, target_edges, target_proj_link_edges):
    ggg = time.clock( )
    def is_gamma_projectile( x ): return x.split(',')[0].split('(')[-1] =='G'
    filter_lists_and_graph( G, [ monitored_edges, coupled_edges, cielo_edges, almost_standard_edges, standard_edges, element_edges, target_edges, inclusive_process_edges, special_quants_edges ], is_gamma_projectile )
    kkk = time.clock( )
    print "Show Gamma Only Takes", kkk-ggg, "Seconds"

def keep_only_HE3(G, standard_edges, almost_standard_edges, cielo_edges, coupled_edges, monitored_edges, element_edges, inclusive_process_edges, special_quants_edges, target_edges, target_proj_link_edges):
    zzz = time.clock( )
    def is_he3_projectile( x ): return x.split(',')[0].split('(')[-1] =='HE3'
    filter_lists_and_graph( G, [ monitored_edges, coupled_edges, cielo_edges, almost_standard_edges, standard_edges, element_edges, target_edges, inclusive_process_edges, special_quants_edges ], is_he3_projectile )
    uuu = time.clock( )
    print "Show HE3 Only Takes", uuu-zzz, "Seconds"

def keep_only_carbon(G, standard_edges, almost_standard_edges, cielo_edges, coupled_edges, monitored_edges, element_edges, inclusive_process_edges, special_quants_edges, target_edges, target_proj_link_edges):
    ccc = time.clock( )
    def is_carbon_projectile( x ): return '-C-' in x.split(',')[0].split('(')[-1]
    filter_lists_and_graph( G, [ monitored_edges, coupled_edges, cielo_edges, almost_standard_edges, standard_edges, element_edges, target_edges, inclusive_process_edges, special_quants_edges ], is_carbon_projectile )
    dfd = time.clock( )
    print "Show Carbon Only Takes", dfd - ccc, "Seconds"

def keep_only_triton(G, standard_edges, almost_standard_edges, cielo_edges, coupled_edges, monitored_edges, element_edges, inclusive_process_edges, special_quants_edges, target_edges, target_proj_link_edges):
    ttt = time.clock( )
    def is_triton_projectile( x ): return x.split(',')[0].split('(')[-1] =='T'
    filter_lists_and_graph( G, [ monitored_edges, coupled_edges, cielo_edges, almost_standard_edges, standard_edges, element_edges, target_edges, inclusive_process_edges, special_quants_edges ], is_triton_projectile )
    rrr = time.clock( )
    print "Show Triton Only Takes", rrr-ttt, "Seconds"

def keep_only_target(G, target_edges):
    bbb = time.clock( )        
    node_list = G.nodes()
    for ik,k in enumerate(node_list):
        for p in node_list[ik+1:]:
            if k.split('(')[0] == p.split('(')[0]:
                G.add_edge(k,p)
                target_edges.append((k,p))
        else: pass
    bcb = time.clock( )
    print "Show Trag Link Takes", bcb-bbb, "Seconds"
    return target_edges

def keep_only_target_proj(G, target_proj_link_edges):
    uku = time.clock( )
    node_list = G.nodes()
    for ik,k in enumerate(node_list):
        for p in node_list[ik+1:]:
            if k.split(',')[0] == p.split(',')[0]:
                G.add_edge(k,p)
                target_proj_link_edges.append((k,p))
        else: pass
    yyy = time.clock( )
    print "Show Targ Proj Link Takes", yyy-uku, "Seconds"
    return target_proj_link_edges

# -----graph function here -----

def generate_graph(outFilePrefix, G, standard_edges, almost_standard_edges, cielo_edges, coupled_edges, monitored_edges, element_edges, inclusive_process_edges, special_quants_edges, target_edges, target_proj_link_edges):
    import matplotlib.pyplot as plt
    try:
        grph = time.clock( )
        try:    GG = nx.connected_component_subgraphs(G)[args.subGraphNumber]
        except: GG = G
        pos = nx.graphviz_layout(GG)#,prog='circo')
        
        # Draw the nodes
        cielo_edges = []
        blue_nodes=[n for n, d in GG.nodes(data = True) if d['nodeInstance'].is_cielo_target()]
        green_nodes = [n for n, d in GG.nodes(data = True) if d['nodeInstance'].is_standard_reaction()]
        yellow_nodes=[n for n, d in GG.nodes(data = True) if d['nodeInstance'].is_almost_standard_reaction()]
        magenta_nodes = [n for n, d in GG.nodes(data = True) if d['nodeInstance'].is_soon_tobe_standard()]
        square_nodes = [n for n, d in GG.nodes(data = True) if d['nodeInstance'].is_dosimiter_reaction()]
        red_nodes = [n for n, d in GG.nodes(data = True) \
            if not d['nodeInstance'].is_standard_reaction() \
            and not d['nodeInstance'].is_cielo_target() \
            and not d['nodeInstance'].is_almost_standard_reaction() \
            and not d['nodeInstance'].is_soon_tobe_standard() \
            and not d['nodeInstance'].is_dosimiter_reaction()]        	
        nx.draw_networkx_nodes(GG, pos, nodelist=blue_nodes, node_color ='b')
        nx.draw_networkx_nodes(GG, pos, nodelist=square_nodes, node_color = 'y', node_shape= 's')
        nx.draw_networkx_nodes(GG, pos, nodelist=green_nodes, node_color = 'g')
        nx.draw_networkx_nodes(GG, pos, nodelist=yellow_nodes, node_color ='y')
        nx.draw_networkx_nodes(GG, pos, nodelist=red_nodes, node_color = 'r')
        nx.draw_networkx_nodes(GG, pos, nodelist=magenta_nodes, node_color = 'm')
        nx.draw_networkx_edges(GG, pos, edgelist=cielo_edges, edge_color = 'g', style= 'dashed')
        grph1 = time.clock( )
        print "Make_Graph part 1 Takes", grph1-grph, "Seconds"
        # Draw the edges
        nx.draw_networkx_edges(GG, pos, edgelist=[e for e in coupled_edges if e in GG.edges()], edge_color = 'g', style = 'dashed')  
        nx.draw_networkx_edges(GG, pos, edgelist=[e for e in standard_edges if e in GG.edges()], edge_color = 'r', style = 'solid')
        nx.draw_networkx_edges(GG, pos, edgelist = [e for e in almost_standard_edges if e in GG.edges()], edge_color = 'g', style = 'dashed')
        nx.draw_networkx_edges(GG, pos, edgelist=[e for e in monitored_edges if e in GG.edges()], edge_color = 'k', style='solid')   
        nx.draw_networkx_edges(GG, pos, edgelist=[e for e in target_edges if e in GG.edges()], edge_color = 'y', style = 'solid')
        nx.draw_networkx_edges(GG, pos, edgelist = [e for e in target_proj_link_edges if e in GG.edges()], edge_color = 'm', style = 'solid')
        nx.draw_networkx_edges(GG, pos, edgelist= [e for e in inclusive_process_edges if e in GG.edges()], edge_color = 'g', style= 'solid')
        nx.draw_networkx_edges(GG, pos, edgelist= [e for e in special_quants_edges if e in GG.edges()], edge_color = 'm', style = 'dashed')
        nx.draw_networkx_edges(GG, pos, edgelist=[e for e in element_edges if e in GG.edges()], edge_color = 'b', style = 'dotted')
         
        # For debugging, turn on every node and edge
        if False: 
            nx.draw_networkx_nodes(GG, pos, node_color = 'r')	
            nx.draw_networkx_edges(GG, pos, edge_color = 'k', style = 'solid')
              
        nx.draw_networkx_labels(GG,pos)
        if outFilePrefix == None:   
            plt.show(  )
            plt.clf()
        else:                       
            plt.savefig(outFilePrefix+'.png', bbox_inches = 0 )
            plt.clf()
        grph2 = time.clock( )
        print "Make_Graph part 2 Takes", grph2-grph1, "Seconds"
    except Exception, e:
        print formatExceptionInfo()

def get_subgraphs(outFilePrefix, G):
    import matplotlib.pyplot as plt
    count = 0
    for k in nx.connected_component_subgraphs(G):
        if len(k.nodes()) >= 30:
            H = k
            nx.draw(H)
             
            count = count + 1
            if outFilePrefix == None: 
                plt.show(  )
                plt.clf()
            else:    
                fk = open(outFilePrefix+'_Subgraph'+str(count)+'.txt', 'w+')
                for k in H.nodes():
                    fk.write(str(k)+'\n')
                fk.close()
                plt.savefig(outFilePrefix+'subgraph'+str(count)+'.png', bbox_inches = 0)
                plt.clf()

def get_eccentricity(G):
    try:
        if nx.is_connected(G) == True:
            make_histogram(nx.eccentricity(G).items(), 100)
        else:
            print "WARNING! ... You cannot do that, the graph is not completely connected"
    except Exception, e:
        print formatExceptionInfo()

def get_top20info(outFilePrefix, G, top20list):
    try:
        centralityMeasures = {}
        centralityMeasures[ 'degree_centrality' ] = nx.degree_centrality( G )
        centralityMeasures[ 'load_centrality' ] = nx.load_centrality( G )
        centralityMeasures[ 'eigenvalue_centrality' ] = {} #nx.eigenvalue_centrality( G )
        if outFilePrefix == None:
            for k in top20list:
                print k[0], '\n',get_node_info( G, k[0], centralityMeasures ),'\n','\n' 
        else:
            fk = open(outFilePrefix+'_Top20Info.txt', 'w+')
            for k in top20list:
                fk.write(str(k[0])+'\n')
                fk.write(str(get_node_info( G, k[0], centralityMeasures ) )+'\n'+'\n'+'\n' )
            fk.close()
    except Exception, e:
        print formatExceptionInfo()

def get_graph_info( outFilePrefix, G ):
    try:
        k = get_info( G )
        p = k.items()
        if outFilePrefix == None:   return k
        else:                       
            fo = open(outFilePrefix+'_Info.txt', "w+")
            for x in p:
                fo.write(x[0]+'    '+str(x[1])+'\n')
            fo.close()
    except Exception, e:
        print e
#    if get_node_info:
#        try: return get_node_info( G, get_node_info )
#        except Exception, e:print formatExceptionInfo()

def get_spectral_density(outFilePrefix, G):
    if outFilePrefix == None:saveas = None
    elif outFilePrefix != None:saveas = outFilePrefix+'_SpectralDensity'
    try:
        if outFilePrefix == None:sdp = open('SpectralDensityData.txt', "w+")
        elif args.outFilePrefix != None:sdp = open(outFilePrefix+'_SpectralDensityData.txt', "w+")
        sdp.write(str(list(get_spectral_density( G ))))
        sdp.close()
        make_histogram(get_spectral_density( G ), 100, "Spectral Density", "Eigenvalue", "Density", outFilePrefix = saveas)
    except Exception, e:
        print formatExceptionInfo()

def get_neighbor():
    try:
        raise DeprecationWarning( 'get_neighbors command line argument' )
        ser = time.clock( )
        print G.neighbors(args.get_neighbors)
        res = time.clock( )
        print "Get Neighbors Takes", res-ser, "Seconds"
    except Exception, e:
        print formatExceptionInfo()

def get_clustering_distribution(outFilePrefix, G):
    if outFilePrefix == None:
        saveas = None
    elif outFilePrefix != None:
        saveas = outFilePrefix+'_ClusteringDistribution'
    try:
        clustering_occur_list = []
        cluster_occur = {}
        clustering_list = []
        count = 1
        gfg = time.clock( )
        for node in G.nodes():
            clustering_occur_list.append(nx.clustering(G,[node]).items()[0][1])
        for v in clustering_occur_list:
            if v not in cluster_occur:cluster_occur[v] = 1  
            elif v in cluster_occur:cluster_occur[v] = cluster_occur[v] + 1    
        cluster_occur_list = sorted(cluster_occur.items())
        plot_x_y_histogram( [cluster_occur_list], "Clustering Coefficient Distribution", "Clustering Coefficient", "Number of Occurences", xlog = False, ylog = True,Legend = "Clustering Distribution", outFilePrefix = saveas )
    except Exception, e:print formatExceptionInfo()

def get_ddf(outFilePrefix, G):
    import matplotlib.pyplot as plt
    try:
        gkg = time.clock( )
        histogram_list = nx.degree_histogram(G)
        plt.loglog(histogram_list,'b-',marker='o')
        plt.title("Degree Distribution for ")
        plt.ylabel("Degree")
        plt.xlabel("Nodes")
        #Command to actually plot graph
        if outFilePrefix == None:   
            plt.show(  )
            plt.clf()
        else:                       
            plt.savefig(outFilePrefix+'_DDF'+'.png', bbox_inches = 0 )
            plt.clf()
        kgk = time.clock( )
        print "DDF Takes", kgk-gkg, "Seconds"
    except Exception, e:print formatExceptionInfo()

def get_degree_tuple(G):
    try:
        sps = time.clock( )
        Node_Degree_Tuple_list = []
        for c in G.nodes():  Node_Degree_Tuple_list.append((c, get_node_degree(G,c)))
        Node_Degree_Tuple_list = sorted(Node_Degree_Tuple_list, cmp=lambda x,y: cmp(x[1], y[1]) )
        Node_Degree_Tuple_list.reverse()
        top20list = Node_Degree_Tuple_list[0:20]
        return top20list  
        #print top20list 
    except Exception, e:print formatExceptionInfo()

def get_node_degree_info(degreeForNodes, nodeForDegree):
    '''
    This must be done to create a list of tuples of format (node, degree) before you can call the two func former 
    '''
    raise DeprecationWarning( "This is for testing only")
    try:
        uyu = time.clock( )
        Degree_list = []
        for c in G.nodes():       
            Degree_list.append((c, get_node_degree(G,c)))
        if degreeForNodes!=None:
            #Getting a list of nodes with degree x
            print get_nodes_with_degree( Degree_list, degreeForNodes)
        if nodeForDegree !=None:
            #Get the degree of a certain node
            print get_degree_for_reaction(nodeForDegree, Degree_list)
        ghg = time.clock( )
        print "Tuple List Creation Takes", ghg-uyu, "Seconds"
    except Exception, e:
        print formatExceptionInfo()

def get_cluster(G):
    try:
        raise DeprecationWarning(  'cluster command line argument, use "show_clustering_distribution"'  )
        hjh = time.clock( )
        for nodes in G.nodes():
            print nx.clustering(G,[nodes])
        fjj = time.clock( )
        print "Print Cluster List Takes", fjj-hjh, "Seconds"
    except Exception, e:
        print formatExceptionInfo()

def get_unconnected_cluster(outFilePrefix, G):
    if outFilePrefix == None:saveas = None
    elif outFilePrefix != None:saveas = outFilePrefix+'_UnconnectedClusterInfo'
    cluster_length_list = []
    cluster_length_quant_list = []
    p = -3
    for k in nx.connected_component_subgraphs(G): cluster_length_list.append(len(k.nodes()))
    for p in cluster_length_list:
        count = 0
        for t in cluster_length_list:
            if p == t:count = count + 1
        if (p,count) in cluster_length_quant_list:pass  
        else:cluster_length_quant_list.append((p,count))   
    plot_x_y_histogram( [cluster_length_quant_list], "Size distribution of disconnected clusters", "Number of Nodes in cluster", "Number of Occurences", xlog = True, ylog = True, xaxislength = (pow(10.0,0.0), pow(10.0,3.0)), yaxislength = (pow(10.0,-1.0), pow(10.0,4.0)), Legend = "Unconnected Nodes",  outFilePrefix = saveas) 

def get_independent_cluster(outFilePrefix, G):
    if outFilePrefix == None:saveas = None
    elif outFilePrefix != None:saveas = outFilePrefix+'_IndependentClusterInfo'
    try:
        junk, special_unconnected_list                 = get_distance_to_different_nodes( G,  get_special_nodes(G) )
        junk, proposed_standard_unconnected_list       = get_distance_to_different_nodes( G,  get_proposed_standard_nodes(G) )
        junk, proposed_and_special_unconnected_list    = get_distance_to_different_nodes( G,  get_special_or_proposed_nodes(G) )
        special_cluster_counts_list                 = get_independent_cluster_distributions( G, special_unconnected_list )
        proposed_standard_cluster_counts_list       = get_independent_cluster_distributions( G, proposed_standard_unconnected_list )
        proposed_and_special_cluster_counts_list    = get_independent_cluster_distributions( G, proposed_and_special_unconnected_list )
        plot_x_y_histogram( [ special_cluster_counts_list, proposed_standard_cluster_counts_list, proposed_and_special_cluster_counts_list ], \
            "Size distribution of disconnected clusters", "Number of Nodes in cluster", "Number of Occurences", xlog = True, ylog = True, xaxislength = (pow(10.0,0.0), pow(10.0,3.0)), yaxislength = (pow(10.0,-1.0), pow(10.0,4.0)), Legend = "Unconnected to Special Nodes", Legend1 = "Unconnected to Proposed Standards" , Legend2 = "Unconnected to Proposed and Special Nodes" , outFilePrefix = saveas)
    except Exception, e:print formatExceptionInfo()

def get_cumulative_histogram(outFilePrefix, G):
    if outFilePrefix == None:saveas = None
    elif outFilePrefix != None:saveas = outFilePrefix+'_CumulativeHistogram'
    try:
        special_distance_list, Unconnected_list = get_distance_to_different_nodes( G,  get_special_nodes(G) )
        proposed_standard_distance_list, Unconnected_list = get_distance_to_different_nodes( G,  get_proposed_standard_nodes(G) )
        proposed_and_special_distance_list, Unconnected_list = get_distance_to_different_nodes( G,  get_special_or_proposed_nodes(G) )
        plot_x_y_histogram( [ special_distance_list, proposed_standard_distance_list, proposed_and_special_distance_list ], \
            "Shortest Path to Standards Comparitive", "Shortest Path Length", "Number of Nodes", xlog = False, ylog = True , Legend = "Special Nodes", Legend1 = "Proposed Standards" , Legend2 = "Proposed and special Nodes" , outFilePrefix = saveas)
    except Exception, e:print formatExceptionInfo()

def get_distance_P_S(outFilePrefix, G):
    if outFilePrefix == None:saveas = None
    elif outFilePrefix != None:saveas = outFilePrefix+'_DistanceToProposedAndStandard'
    try:
        proposed_and_standard_distance_list, Unconnected_list = get_distance_to_different_nodes( G,  get_proposed_and_standard_nodes(G) )
        plot_x_y_histogram( [proposed_and_standard_distance_list], "Shortest Path to Proposed and Standards Histogram", "Shortest Path Length to Proposed and Standard", "Number of nodes",xlog = False, ylog = True, Legend = "Proposed and Standards Nodes", outFilePrefix = saveas)
    except Exception, e:print formatExceptionInfo()

def get_distance_P(outFilePrefix, G):
    if outFilePrefix == None:saveas = None
    elif outFilePrefix != None:saveas = outFilePrefix+'_DistanceToProposedStandard'
    try:
        proposed_standard_distance_list, Unconnected_list = get_distance_to_different_nodes( G, get_proposed_standard_nodes(G) )
        plot_x_y_histogram( [proposed_standard_distance_list], "Shortest Path to Proposed Standards Histogram", "Shortest Path Length to Proposed Standard", "Number of Nodes",xlog = False, ylog = True, Legend = "Proposed Standards Nodes", outFilePrefix = saveas)
    except Exception, e:print formatExceptionInfo()

def get_distance_S(outFilePrefix, G):
    if outFilePrefix == None:saveas = None
    elif outFilePrefix != None:saveas = outFilePrefix+'_DistanceToStandard'
    try:
        standard_distance_list, Unconnected_list = get_distance_to_different_nodes( G,  get_standard_nodes(G) )
        plot_x_y_histogram( [standard_distance_list], "Shortest Path to Standards Histogram", "Shortest Path Length to Standard", "Number of Nodes",xlog = False, ylog = True, Legend = "Standards Nodes", outFilePrefix = saveas)
    except Exception, e:print formatExceptionInfo()

def get_distance_C(outFilePrefix, G):
    if outFilePrefix == None:saveas = None
    elif outFilePrefix != None:saveas = outFilePrefix+'_DistanceToCIELO'
    try:
        CIELO_distance_list, Unconnected_list = get_distance_to_different_nodes( G, get_cielo_nodes(G) )
        plot_x_y_histogram( [CIELO_distance_list], "Shortest Path to CIELO Histogram", "Shortest Path Length to CIELO", "Number of Nodes",xlog = False, ylog = True, Legend = "CIELO Nodes", outFilePrefix = saveas)
    except Exception, e:print formatExceptionInfo()

def get_distance_special_P(outFilePrefix, G):
    if outFilePrefix == None:saveas = None
    elif outFilePrefix != None:saveas = outFilePrefix+'_DistanceToSpecialorProposed'
    try:
        special_or_proposed_nodes_list, Unconnected_list = get_distance_to_different_nodes( G, get_special_or_proposed_nodes(G) )  
        plot_x_y_histogram( [special_or_proposed_nodes_list], "Shortest Path to Special or Proposed Nodes Histogram", "Shortest Path Length to Special or Proposed Nodes", "Number of Nodes",xlog = False, ylog = True, Legend = "Special or Proposed Nodes", outFilePrefix = saveas)  
    except Exception, e:print formatExceptionInfo()

def get_distance_D(outFilePrefix, G):
    if outFilePrefix == None:saveas = None
    elif outFilePrefix != None:saveas = outFilePrefix+'_DistanceToDosimiter'
    try:
        dosimiter_distance_list, Unconnected_list = get_distance_to_different_nodes( G, get_dosimiter_nodes(G) )
        plot_x_y_histogram( [dosimiter_distance_list], "Shortest Path to Dosimiter Histogram", "Shortest Path Length to Dosimiter", "Number of Nodes",xlog = False, ylog = True, Legend = "Dosimiter Nodes", outFilePrefix = saveas)
    except Exception, e:print formatExceptionInfo()

def get_distance_special(outFilePrefix, G):
    if outFilePrefix == None:saveas = None
    elif outFilePrefix != None:saveas = outFilePrefix+'_DistanceToSpecialNodes'
    try:
        special_nodes_list, Unconnected_list = get_distance_to_different_nodes( G, get_special_nodes(G) )
        plot_x_y_histogram( [special_nodes_list], "Shortest Path to Special Nodes Histogram", "Shortest Path Length to Special Nodes", "Number of Nodes",xlog = False, ylog = True, Legend = "Special Nodes", outFilePrefix = saveas)
    except Exception, e:print formatExceptionInfo()

def get_distance_D_P(outFilePrefix, G):
    if outFilePrefix == None:saveas = None
    elif outFilePrefix != None:saveas = outFilePrefix+'_DistanceToDosimiterorProposed'
    try:
        Dosimiter_and_proposed_nodes_list, Unconnected_list = get_distance_to_different_nodes( G, get_proposed_or_dosimiter_nodes(G) )
        plot_x_y_histogram( [Dosimiter_and_proposed_nodes_list], "Shortest Path to Dosimiter or Proposed Nodes Histogram", "Shortest Path Length to Dosimiter or Proposed Nodes", "Number of Nodes",xlog = False, ylog = True, Legend = "Dosimiter or Proposed Nodes", outFilePrefix = saveas)
    except Exception, e:print formatExceptionInfo()

# -----------------------------------------------------------------------
#    Main routine
# -----------------------------------------------------------------------

if __name__ == "__main__":
    import unittest

    class Test_Reaction_Node( unittest.TestCase ):

        def test__init__( self ):
			a = Reaction_Node( 'FE-56(N,G)', 'WID' )
			self.assertEqual( a.reaction, 'FE-56(N,G)' )
			self.assertEqual( a.observable, 'WID' )
			self.assertEqual( a.target, 'FE-56' )
	
        def test_is_cielo_target(self):
			a = Reaction_Node( 'FE-56(N,G)', 'WID' )
			self.assertTrue( a.is_cielo_target() ) 
    
        def test_is_standard_reaction(self):
			a = Reaction_Node( 'FE-56(N,G)', 'WID' )
			self.assertFalse( a.is_standard_reaction() ) 
			b = Reaction_Node( 'AU-197(N,G)', 'SIG' )
			self.assertTrue( b.is_standard_reaction() ) 

        def test_is_dosimiter_reaction(self):
            a = Reaction_Node( 'AL-27(P,X+11-NA-22)','SIG' )
            self.assertTrue( a.is_dosimiter_reaction() )
    
        def test_is_almost_standard_reaction(self):
			a = Reaction_Node( 'FE-56(N,G)', 'WID' )
			self.assertFalse( a.is_almost_standard_reaction() ) 
        
        def test_is_soon_tobe_standard(self):
            a = Reaction_Node( 'FE-56(N,G)', 'WID')
            self.assertFalse(a.is_soon_tobe_standard())
            b = Reaction_Node( "CF-252(0,F)", "NU")
            self.assertTrue(b.is_soon_tobe_standard())

        def test_is_proposed_standard(self):
            a = Reaction_Node( 'CO-59(N,G)', 'SIG' )
            self.assertTrue(a.is_proposed_standard())

        def test_is_proposed_and_standard(self):
            a = Reaction_Node( 'CO-59(N,G)', 'SIG' )
            self.assertTrue(a.is_proposed_standard())

        def test_is_special(self):
            b = Reaction_Node( 'AU-197(N,G)', 'SIG' ) 
            self.assertTrue( b.is_special() )
        
        def test_is_special_or_proposed(self):
            a = Reaction_Node( 'CO-59(N,G)', 'SIG' )
            self.assertTrue(a.is_proposed_standard())

        def test_is_proposed_or_dosimiter(self):
            a = Reaction_Node( 'AL-27(P,X+11-NA-22)','SIG' )
            self.assertTrue( a.is_dosimiter_reaction() )

        def test_as_tuple(self): 
			a = Reaction_Node( 'FE-56(N,G)', 'WID' )
			self.assertEqual( a.as_tuple(), ( 'FE-56(N,G)', 'WID' )  )

        def test__str__( self ):
			a = Reaction_Node( 'FE-56(N,G)', 'WID' )
			self.assertEqual( str(a), 'FE-56(N,G)' + 'WID') 

        def test__hash__(self):
			a = Reaction_Node( 'FE-56(N,G)', 'WID')
			self.assertEqual( hash(a), hash(('FE-56(N,G)','WID')) )


    class Test_Abundance_Functions( unittest.TestCase ):
    
        def test_has_element( self ):
            self.assertTrue( has_element( 'U-233' ) )
            self.assertTrue( has_element( 'Mo-100' ) )
            self.assertTrue( has_element( 'N-0' ) )
            self.assertTrue( has_element( 'Fe-56' ) )
            self.assertFalse( has_element( 'Pu-239' ) )
            self.assertFalse( has_element( 'Cf-252' ) )

        def test_is_element( self ): 
            self.assertFalse( is_element( 'U-233' ) )
            self.assertFalse( is_element( 'Mo-100' ) )
            self.assertTrue( is_element( 'N-0' ) )
            self.assertFalse( is_element( 'Fe-56' ) )

        def test_get_isotopes_from_element( self ):
            self.assertEqual( get_isotopes_from_element( 'U-0' ), ['U-234', 'U-235', 'U-238'] )
            self.assertEqual( get_isotopes_from_element( 'PU-0' ), [] )
            self.assertEqual( get_isotopes_from_element( 'O-0' ), ['O-18', 'O-17', 'O-16'] )
            self.assertEqual( get_isotopes_from_element( 'H-0' ), ['H-1', 'H-2'] )


    class Test_X4i_Graph( unittest.TestCase ):
    
        def setUp( self ):
            self.graph = create_graph()

        # ------------ nodes ------------
    
        def test_add_node( self ):
            self.assertIsNotNone( self.graph.add_node( 'B-10(N,A+G)SIG' ) )
    
        def test_add_nodes( self ):
            self.assertEqual( self.graph.add_nodes( [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', 'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', 'U-235(N,F)SIG', 'AU-197(N,G)SIG' ] ), 10 )
            
        def test___contains__( self ): 
            self.graph.add_nodes( [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', 'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', 'U-235(N,F)SIG', 'AU-197(N,G)SIG' ] )
            self.assertTrue( 'C-0(N,EL)SIG' in self.graph )

        def test_num_nodes( self ):
            self.graph.add_nodes( [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', 'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', 'U-235(N,F)SIG', 'AU-197(N,G)SIG' ] )
            self.assertEqual( self.graph.num_nodes(), 10 )

        def test_num_edges( self ):
            self.graph.add_nodes( [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', 'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', 'U-235(N,F)SIG', 'AU-197(N,G)SIG' ] )
            self.graph.add_edge( 'B-10(N,A+G)SIG', 'U-238(N,F)SIG' )
            self.graph.add_edge( 'B-10(N,A+G)SIG', 'AU-197(N,G)SIG' )
            self.assertEqual( self.graph.num_edges(), 2 )

        def test_has_node( self ): 
            self.graph.add_nodes( [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', 'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', 'U-235(N,F)SIG', 'AU-197(N,G)SIG' ] )
            self.assertTrue( self.graph.has_node( 'C-0(N,EL)SIG' ) )

        def test_update_node_weight( self ): 
            self.graph.add_nodes( [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', 'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', 'U-235(N,F)SIG', 'AU-197(N,G)SIG' ] )
            self.graph.update_node_weight( 'U-238(N,F)SIG', 13 ) 
            self.assertEqual( self.graph.get_node_weight( 'U-238(N,F)SIG' ), 14 )

        def test_get_node( self ): 
            self.graph.add_nodes( [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', 'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', 'U-235(N,F)SIG', 'AU-197(N,G)SIG' ] )
            self.assertEqual( self.graph.get_node( 'H-1(N,EL)SIG', data=True ).target,  'H-1' )
            self.assertEqual( self.graph.get_node( 'H-1(N,EL)SIG', data=True ).observable,  'SIG' )
            self.assertEqual( self.graph.get_node( 'H-1(N,EL)SIG', data=True ).reaction,  'H-1(N,EL)' )
            self.assertEqual( self.graph.get_node( 'H-1(N,EL)SIG', data=True ).weight, 1 )

        def test_get_node_property( self ):
            #get_node_property( self, node, prop_key )
            pass
            
        def test_set_node_property( self ):
            #set_node_property( self, node, prop_key, prop_val )
            pass

        # ------------ edges ------------ 
    
        def test_add_edge( self ):
            self.graph.add_nodes( [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', 'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', 'U-235(N,F)SIG', 'AU-197(N,G)SIG' ] )
            self.graph.add_edge( 'B-10(N,A+G)SIG', 'U-238(N,F)SIG' )
            self.graph.add_edge( 'B-10(N,A+G)SIG', 'U-238(N,F)SIG' ) # double add should do nothing (for now)
            self.graph.add_edge( 'B-10(N,A+G)SIG', 'AU-197(N,G)SIG' )
            self.assertEqual( self.graph.num_edges(), 2 )

        def test_get_edge_property( self ):
            #get_edge_property( edge, prop_key ):
            pass

        def test_set_edge_property( self ):
            #set_edge_property( self, edge, prop_key, prop_val )
            pass
    
        def test_add_connected_cluster( self ):
            self.graph.add_connected_cluster( 
                [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', \
                    'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', \
                    'U-235(N,F)SIG', 'AU-197(N,G)SIG' ], \
                cluster_name='Neutron Standards', maxCount=None )
            self.assertEqual( self.graph.num_edges(), 45 )
               
        # ------------ connected cluster ------------
    
        # ------------ queries ------------
    
        # ------------ statistics ------------


    class Test_Node_Adding( unittest.TestCase ): 
    
        def setUp( self ):
            self.graph=nx.Graph()

        def test_add_to_graph( self ):
            add_to_graph( self.graph, { 'stds':[ Reaction_Node( y[0], y[1] ) for y in standardsReactions ] } )
            self.assertEqual( self.graph.nodes(), [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', 'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', 'U-235(N,F)SIG', 'AU-197(N,G)SIG' ] )
        
        def test_add_to_graph_is_complete( self ):
            maybe_edge_list = add_to_graph( self.graph, { 'stds':[ Reaction_Node( y[0], y[1] ) for y in standardsReactions ] } )
            numNodes = self.graph.order()
            numEdges = self.graph.size()
            self.assertEqual( numNodes, 10 )
            self.assertEqual( len( maybe_edge_list ), numEdges )
            self.assertEqual( numEdges, 45 )
            self.assertTrue( numEdges == numNodes*(numNodes-1)/2)

        def test_add_rxn_remaining( self ):
            add_rxn_remaining( self.graph, [ Reaction_Node( y[0], y[1] ) for y in soontobeStandards ] )
            self.assertEqual( self.graph.nodes(), ['CF-252(0,F)NU', 'CF-252(0,F)NU/DE', 'CF-252(0,F)DE'] )


    class Test_Graph_Modification_Functions( unittest.TestCase ):
        
        def setUp( self ):
            self.graph=nx.Graph()
            self.maxDiff = None
            self.list_of_std_edges = add_to_graph( self.graph, { 'stds':[ Reaction_Node( y[0], y[1] ) for y in standardsReactions+[ ('C-0(N,2N)','SIG')] ] } )
            self.list_of_astd_edges = add_to_graph( self.graph, { 'astds':[ Reaction_Node( y[0], y[1] ) for y in almostStandardReactions ] } )
        
        def test_filter_lists_and_graph( self ):
            def is_not_natC( x ): return not 'C-0' in x
            self.assertEqual( self.graph.nodes(), ['B-10(N,EL)SIG', 'C-0(N,2N)SIG', 'B-10(N,A)PAR,SIG', 'LI-6(N,EL)SIG', 'U-238(N,G)SIG', 'B-10(N,A+G)SIG', \
                'U-238(N,F)SIG', 'PU-239(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', 'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', 'U-235(N,F)SIG', 'AU-197(N,G)SIG'] )
            filter_lists_and_graph( self.graph, [ self.list_of_std_edges, self.list_of_astd_edges ], is_not_natC )
            self.assertEqual( self.graph.nodes(), [ 'B-10(N,EL)SIG', 'B-10(N,A)PAR,SIG', 'LI-6(N,EL)SIG', 'U-238(N,G)SIG', 'B-10(N,A+G)SIG', \
                'U-238(N,F)SIG', 'PU-239(N,F)SIG', 'B-10(N,A)SIG', 'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', 'U-235(N,F)SIG', 'AU-197(N,G)SIG' ] )
            self.assertEqual( self.list_of_std_edges, [ ('H-1(N,EL)SIG', 'HE-3(N,P)SIG'), ('H-1(N,EL)SIG', 'LI-6(N,T)SIG'), ('H-1(N,EL)SIG', 'B-10(N,A+G)SIG'), \
                ('H-1(N,EL)SIG', 'AU-197(N,G)SIG'), ('H-1(N,EL)SIG', 'U-235(N,F)SIG'), ('H-1(N,EL)SIG', 'B-10(N,A)SIG'), ('H-1(N,EL)SIG', 'U-238(N,F)SIG'), \
                ('H-1(N,EL)SIG', 'B-10(N,A+G)PAR,SIG'), ('HE-3(N,P)SIG', 'LI-6(N,T)SIG'), ('HE-3(N,P)SIG', 'B-10(N,A+G)SIG'), ('HE-3(N,P)SIG', 'AU-197(N,G)SIG'), \
                ('HE-3(N,P)SIG', 'U-235(N,F)SIG'), ('HE-3(N,P)SIG', 'B-10(N,A)SIG'), ('HE-3(N,P)SIG', 'U-238(N,F)SIG'), ('HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG'), \
                ('LI-6(N,T)SIG', 'B-10(N,A+G)SIG'), ('LI-6(N,T)SIG', 'AU-197(N,G)SIG'), ('LI-6(N,T)SIG', 'U-235(N,F)SIG'), ('LI-6(N,T)SIG', 'B-10(N,A)SIG'), \
                ('LI-6(N,T)SIG', 'U-238(N,F)SIG'), ('LI-6(N,T)SIG', 'B-10(N,A+G)PAR,SIG'), ('B-10(N,A+G)SIG', 'AU-197(N,G)SIG'), ('B-10(N,A+G)SIG', 'U-235(N,F)SIG'), \
                ('B-10(N,A+G)SIG', 'B-10(N,A)SIG'), ('B-10(N,A+G)SIG', 'U-238(N,F)SIG'),('B-10(N,A+G)SIG', 'B-10(N,A+G)PAR,SIG'), ('AU-197(N,G)SIG', 'U-235(N,F)SIG'), \
                ('AU-197(N,G)SIG', 'B-10(N,A)SIG'), ('AU-197(N,G)SIG', 'U-238(N,F)SIG'), ('AU-197(N,G)SIG', 'B-10(N,A+G)PAR,SIG'), ('U-235(N,F)SIG', 'B-10(N,A)SIG'), \
                ('U-235(N,F)SIG', 'U-238(N,F)SIG'), ('U-235(N,F)SIG', 'B-10(N,A+G)PAR,SIG'), ('B-10(N,A)SIG', 'U-238(N,F)SIG'), ('B-10(N,A)SIG', 'B-10(N,A+G)PAR,SIG'), ('U-238(N,F)SIG', 'B-10(N,A+G)PAR,SIG')] )
            self.assertEqual( self.list_of_astd_edges, [('LI-6(N,EL)SIG', 'B-10(N,EL)SIG'), ('LI-6(N,EL)SIG', 'PU-239(N,F)SIG'), ('LI-6(N,EL)SIG', 'U-238(N,G)SIG'), ('LI-6(N,EL)SIG', 'B-10(N,A)PAR,SIG'), \
                ('B-10(N,EL)SIG', 'PU-239(N,F)SIG'), ('B-10(N,EL)SIG', 'U-238(N,G)SIG'), ('B-10(N,EL)SIG', 'B-10(N,A)PAR,SIG'), ('PU-239(N,F)SIG', 'U-238(N,G)SIG'), ('PU-239(N,F)SIG', 'B-10(N,A)PAR,SIG'), ('U-238(N,G)SIG', 'B-10(N,A)PAR,SIG')] )


    class Test_Graph_Statistics_Functions( unittest.TestCase ):

        def setUp( self ):
            G=nx.Graph()
            add_to_graph( G, { 'fakedata':[ Reaction_Node( y[0], y[1] ) \
                for y in [ ('U-0(N,EL)', 'DA'), ('U-0(N,INL)', 'DA'), ('BI-209(N,X+2-HE-4)', 'DA/DE'), \
                    ('BI-209(N,X+2-HE-3)', 'DA/DE'), ('U-238(N,G)','SIG'), ('U-234(N,F)', 'SIG'), \
                    ('U-235(N,F)', 'SIG'), ('NI-58(N,EL)', 'WID'), ('NI-58(N,G)', 'WID'), ('CF-252(0,F)','NU'),\
                    ('NI-58(N,TOT)', 'WID'), ('LI-7(D,A)', 'SIG'), ('U-238(N,F)','SIG') ] ] } )
            self.graph = G
            
        def test_get_node_degree( self ):
            self.assertEqual( get_node_degree( self.graph, 'U-0(N,EL)DA' ), 12 )

        def test_get_node_type( self ):
            self.assertEqual( get_node_type( 'U-0(N,EL)DA' ), 'REGULAR' )

        def test_get_graph_info( self ):
            self.assertEqual( get_graph_info( None, self.graph ), {"# of Nodes" : 13, "# of Edges" : 78, "Is connected" : True, "# of Isolates" : 0, "Probability of Connection" : 1.0, "<k>" : 12.0, "k^2" : 144.0, "Diameter" : 1, "Radius" : 1})
    
        def test_get_node_info( self ):
            self.assertEqual( get_node_info( self.graph, 'U-0(N,EL)DA' ), {"RXN" : 'U-0(N,EL)', 'Load Centrality':None, 'Degree Centrality':None, "Observable" : 'DA', "Degree" : 12, "Clustering Coefficient" : 1.0, "Closeness" : 1.0, "Eigenvalue Centrality" : None, "Betweenness" : 0.0, "Node Type" : 'REGULAR', "Eccentricity" : 1} )

        def test_get_nodes_with_degree( self ):
            fake_node_tuple_list = [('U-0(N,EL)DA',12) , ('U-0(N,INL)DA', 12 ) ,\
            ('BI-209(N,X+2-HE-4)DA/DE',12) , ('BI-209(N,X+2-HE-3)DA/DE',12) , \
            ('U-238(N,G)SIG',12), ('U-234(N,F)SIG',12), ('U-235(N,F)SIG',12), ('NI-58(N,EL)WID',12),\
            ('NI-58(N,G)WID',12), ('CF-252(0,F)NU',12), ('NI-58(N,TOT)WID',12), ('LI-7(D,A)SIG',12), \
            ('U-238(N,F)SIG',12)]
            self.assertEqual( get_nodes_with_degree( fake_node_tuple_list,  12 ), ['U-0(N,EL)DA','U-0(N,INL)DA', 'BI-209(N,X+2-HE-4)DA/DE', 'BI-209(N,X+2-HE-3)DA/DE', 'U-238(N,G)SIG', 'U-234(N,F)SIG', 'U-235(N,F)SIG', 'NI-58(N,EL)WID', 'NI-58(N,G)WID', 'CF-252(0,F)NU', 'NI-58(N,TOT)WID', 'LI-7(D,A)SIG', 'U-238(N,F)SIG'])   

        def test_degree_for_reaction( self ):
            fake_node_tuple_list = [('U-0(N,EL)DA',12) , ('U-0(N,INL)DA', 12 ) ,\
            ('BI-209(N,X+2-HE-4)DA/DE',12) , ('BI-209(N,X+2-HE-3)DA/DE',12) , \
            ('U-238(N,G)SIG',12), ('U-234(N,F)SIG',12), ('U-235(N,F)SIG',12), ('NI-58(N,EL)WID',12),\
            ('NI-58(N,G)WID',12), ('CF-252(0,F)NU',12), ('NI-58(N,TOT)WID',12), ('LI-7(D,A)SIG',12), \
            ('U-238(N,F)SIG',12)]
            self.assertEqual( get_degree_for_reaction('U-0(N,EL)DA', fake_node_tuple_list), 12)
        
        def test_get_distance_to_different_nodes( self ):
            fake_standard_list = [ ('LI-7(D,A)SIG'), ('U-238(N,F)SIG'), ('U-235(N,F)SIG') ]
            self.assertEqual( get_distance_to_different_nodes( self.graph, fake_standard_list), ( [(0, 3), (1, 10)],[] ) )

        def test_get_independent_cluster_distributions( self ):
            fake_unconnected_list = [('U-0(N,EL)', 'DA'), ('U-0(N,INL)', 'DA'), ('BI-209(N,X+2-HE-4)', 'DA/DE'), \
                    ('BI-209(N,X+2-HE-3)', 'DA/DE'), ('U-238(N,G)','SIG'), ('U-234(N,F)', 'SIG'), \
                     ('U-235(N,F)', 'SIG'), ('NI-58(N,EL)', 'WID'), ('NI-58(N,G)', 'WID'), ('CF-252(0,F)','NU'),\
                    ('NI-58(N,TOT)', 'WID'), ('LI-7(D,A)', 'SIG'), ('U-238(N,F)','SIG')]
            self.assertEqual( get_independent_cluster_distributions( self.graph, fake_unconnected_list ), [] )
        
    class Test_Graph_Query_Functions( unittest.TestCase ):

        def setUp( self ):
            G=nx.Graph()
            add_to_graph( G, { 'fakedata':[ Reaction_Node( y[0], y[1] ) \
                for y in [ ('U-0(N,EL)', 'DA'), ('U-0(N,INL)', 'DA'), ('BI-209(N,X+2-HE-4)', 'DA/DE'), \
                    ('BI-209(N,X+2-HE-3)', 'DA/DE'), ('U-238(N,G)','SIG'), ('U-234(N,F)', 'SIG'), \
                    ('U-235(N,F)', 'SIG'), ('NI-58(N,EL)', 'WID'), ('NI-58(N,G)', 'WID'),('CF-252(0,F)','NU'), \
                    ('NI-58(N,TOT)', 'WID'), ('LI-7(D,A)', 'SIG'), ('U-238(N,F)','SIG'), ('ZR-91(N,NON)','SIG'),\
                    ('U-235(N,F)','ETA'), ('AL-27(P,X+11-NA-22)','SIG'), ('MO-0(P,X+43-TC-96)', 'SIG')] ] } )
            self.graph = G

        def test_get_elemental_nodes( self ): 
            self.assertEqual( get_elemental_nodes( self.graph ), ["U-0(N,INL)DA","MO-0(P,X+43-TC-96)SIG", "U-0(N,EL)DA"] )

        def test_get_standard_nodes( self ):
            self.assertEqual( get_standard_nodes( self.graph ), ["U-238(N,F)SIG", "U-235(N,F)SIG"] )

        def test_get_cielo_nodes( self ): 
            self.assertEqual( get_cielo_nodes( self.graph ), ["U-235(N,F)ETA","U-238(N,G)SIG" ,"U-238(N,F)SIG", "U-235(N,F)SIG"] )

        def test_get_almost_standard_nodes( self ): 
            self.assertEqual( get_almost_standard_nodes( self.graph ), ["U-238(N,G)SIG"] )

        def test_get_dosimiter_nodes( self ):
            self.assertEqual( get_dosimiter_nodes( self.graph ), ["AL-27(P,X+11-NA-22)SIG"])

        def test_get_soon_to_be_standard_nodes( self ): 
            self.assertEqual( get_soon_to_be_standard_nodes( self.graph ), ["CF-252(0,F)NU"] )

        def test_get_proposed_standard_nodes( self ):
            self.assertEqual( get_proposed_standard_nodes( self.graph ), ["MO-0(P,X+43-TC-96)SIG"] )

        def test_get_proposed_and_standard_nodes( self ):
            self.assertEqual( get_proposed_and_standard_nodes( self.graph), ["MO-0(P,X+43-TC-96)SIG", "U-238(N,F)SIG", "U-235(N,F)SIG" ] )

        def test_get_special_nodes( self ):
            self.assertEqual( get_special_nodes( self.graph ), ['U-235(N,F)ETA', 'U-238(N,G)SIG', \
                    'U-238(N,F)SIG','CF-252(0,F)NU', \
                    'U-235(N,F)SIG','AL-27(P,X+11-NA-22)SIG'] )

        def test_get_special_or_proposed_nodes( self ):
            self.assertEqual( get_special_or_proposed_nodes( self.graph ), ['U-235(N,F)ETA', 'U-238(N,G)SIG', \
                    'MO-0(P,X+43-TC-96)SIG','U-238(N,F)SIG','CF-252(0,F)NU', \
                    'U-235(N,F)SIG','AL-27(P,X+11-NA-22)SIG'] )

        def test_get_proposed_or_dosimiter_nodes( self ):
            self.assertEqual( get_proposed_or_dosimiter_nodes( self.graph ), ["MO-0(P,X+43-TC-96)SIG", "AL-27(P,X+11-NA-22)SIG"] )

        def test_is_matching_process( self ):
            self.assertEqual( is_matching_process( self.graph, 'NON'), ["ZR-91(N,NON)SIG"])
          
        def test_is_matching_quantity( self ):
            self.assertEqual( is_matching_quantity( self.graph, 'ETA'), ["U-235(N,F)ETA"])

    unittest.main()
