'''
exfor_network_analysis.py

Authors: J Hirdt, D.A. Brown

This module is for making undirected graphs using the networkx and or graph_tool package.

'''
from x4i3 import abundance, endl_Z, fullMonitoredFileName, fullCoupledFileName, fullReactionCountFileName
from x4i3.exfor_utilities import timeit # unique, formatExceptionInfo, 
import math, cPickle, scipy # copy, numpy.linalg, sys, os

'''Use this flag to make networkx be the default graph package'''
FORCENETWORKX = False

# Try to import graph_tool, if it fails then we have to use only networkx
try:
    import graph_tool as gt
except ImportError:
    print "Warning: graph-tool import failed, using networkx only.  Don't expect anything that needs lots of dictionary access to work."
    FORCENETWORKX = True
import networkx as nx


# ------------ plotting functions -------------

def make_histogram( list1, bincount ,title, xlabel, ylabel, xmin, xmax, ymin, ymax ):
    '''
    This function is for plotting histograms using pylabs built in function. Pass in a list of values and pylab converts to a 
    histogram. A bincount must also be added. One can control the title, xlabel, ylabel, xmin, xmax, ymin, ymax.
    '''
    import matplotlib.pyplot as plt
    from pylab import hist
    hist(list1, bins = bincount)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)     
    plt.axis([xmin,xmax,ymin,ymax])
    plt.show()
    plt.clf()

def make_barGraph( listA , title , xlabel, ylabel, xlog = False, ylog = False, xmin = None, xmax = None, ymin = None, ymax = None ):
    '''
    This function for making bargraphs
    '''
    import matplotlib.pyplot as plt
    tupleList = []
    listA = sorted(listA)
    for k in listA:
        count = 0
        for p in listA:
            if k == p:count = count + 1
            else: pass
        p = (k,count)
        if p not in tupleList:tupleList.append(p)
        else: pass
    left = []
    height = []
    for x in tupleList:
        left.append(x[0]-.5)
        height.append(x[-1])
    plt.bar(left, height, width = 1)
    if xlog != False and ylog != False: plt.loglog()
    elif xlog!= False: plt.semilogx()
    elif ylog!= False: plt.semilogy()
    elif xlog == False and ylog == False: plt.axis([xmin,xmax,ymin,ymax])
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)     
    plt.show()
 
def plot_multiple_lineGraphs(listOFlists, title, xlabel, ylabel, xlog = False, ylog = False, xaxislength = (None, None), yaxislength = (None, None), outFilePrefix = None, Legend = None, Legend1 = None, Legend2 = None, Legend3 = None, Legend4 = None):
    import matplotlib.pyplot as plt
    for dataset in listOFlists:
        tupleList = []
        dataset = sorted(dataset)
        for k in dataset:
            count = 0
            for p in dataset:
                if k == p:count = count + 1
                else: pass
            p = (k,count)
            if p not in tupleList:tupleList.append(p)
            else: pass

        x = []
        y = []
        for r in tupleList:
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
    plt.legend((Legend, Legend1, Legend2, Legend3, Legend4),'upper right', shadow = True)
    plt.show()

def get_x_y_column_data( datalist, Type = 'Degree' ):
    tupleList = []
    datalist = sorted(datalist)
    for k in datalist:
        count = 0
        for p in datalist:
            if k == p:count = count + 1
            else: pass
        p = (k,count)
        if p not in tupleList:tupleList.append(p)
        else: pass
    ft = open('XYColumnData'+str(Type)+'.txt','w+')
    for r in tupleList:
        p = ' '.join(map(str,r))
        ft.write(p+'\n')
    ft.close()
        
def plot_lineGraph( datalist, title, xlabel, ylabel, xlog = False, ylog = False, xaxislength = (None, None), yaxislength = (None, None)):
    import matplotlib.pyplot as plt
    tupleList = []
    datalist = sorted(datalist)
    for k in datalist:
        count = 0
        for p in datalist:
            if k == p:count = count + 1
            else: pass
        p = (k,count)
        if p not in tupleList:tupleList.append(p)
        else: pass

    x = []
    y = []
    for r in tupleList:
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
    plt.show()

def plot_x_y_graph( datalist, title, xlabel, ylabel, xlog = False, ylog = False, xaxislength = (None, None), yaxislength = (None, None)):
    '''
    plot_x_y_graph takes a datalist of tupes of (x,y) coordinates to plot. One also has the option of adding a graph title, xlabel,
    ylabel, having the xaxis take the shape of an xlog scale, having the yaxis take the shape of an ylog scale, and finally setting 
    the bounds of the xaxis and yaxis manually by hand.
    '''
    import matplotlib.pyplot as plt
    x = []
    y = []
    for r in datalist:            
        x.append(r[0])
        y.append(r[1])
    plt.plot(x,y,marker='o')
    if xlog != False and ylog != False: plt.loglog()
    elif xlog!= False: plt.semilogx()
    elif ylog!= False: plt.semilogy()
    if xaxislength != (None, None) and yaxislength != (None, None): plt.axis([xaxislength[0] , xaxislength[1], yaxislength[0], yaxislength[1] ]) 
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel) 
    plt.show(  )
    plt.clf()



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

'''CIELO isotopes are the isotopes in the ENDF neutron sublibrary that are being evaluated as part of the CIELO project'''
cieloIsotopes = [ 'H-1' , 'U-238' , 'U-235' , 'PU-239' , 'FE-56', 'O-16']
cieloTargetProjectiles = [ 'H-1(N' , 'U-238(N' , 'U-235(N' , 'PU-239(N' , 'FE-56(N', 'O-16(N']

'''Neutron Reaction Standards, as defined by the CSEWG Standards Committee'''
standardsReactions = [
                      ('H-1(N,EL)','SIG') , ('HE-3(N,P)','SIG') , 
                      ('LI-6(N,T)','SIG') , ('B-10(N,A+G)','SIG') , 
                      ('C-0(N,EL)','SIG') , ('AU-197(N,G)','SIG') , 
                      ('U-235(N,F)','SIG') , ('B-10(N,A)','SIG'), 
                      ('U-238(N,F)','SIG'), ("B-10(N,A+G)", "PAR,SIG") ]

'''Reactions that the CSEWG Standards Committee determined that needed to be evaluated in conjunction with the Neutron Reaction Standards'''
almostStandardReactions = [('LI-6(N,EL)','SIG') , ('B-10(N,EL)','SIG'),  ('PU-239(N,F)','SIG'), ('U-238(N,G)','SIG'), ("B-10(N,A)", "PAR,SIG")]

'''Reactions that the CSEWG Standards Committee are considering as standards in the next major revision of the standards evaluation project'''
soontobeStandards = [("CF-252(0,F)", "NU"), ("CF-252(0,F)", "NU/DE"), ("CF-252(0,F)", "DE"), ('AL-27(N,A)','SIG'),  ('BI-209(N,F)','SIG')]

'''Reactions designated as standards by in the "Atlas of Neutron Resonances"'''
atlasStandards = [
                  ('AU-197(N,G)','RI'),('AU-197(N,G)','SIG'),
                  ('CO-59(N,G)','SIG'),('CO-59(N,G)','RI'),
                  ('MN-55(N,G)','SIG'),('MN-55(N,G)','RI'),
                  ('CL-35(N,G)','SIG'),('B-10(N,G)','SIG'),
                  ('B-0(N,ABS)','SIG'),('LI-6(N,A)','SIG'),
                  ('LI-0(N,ABS)','SIG'),('H-1(N,G)','SIG')]

'''IAEA Charged Particle Monitor Reactions, effectively standards level reactions for charged particle incident data'''
dosimiterReactions= [
                     ('AL-27(P,X+11-NA-22)','SIG'), 
                     ('AL-27(P,X+11-NA-24)','SIG'), 
                     ('TI-0(P,X+23-V-48)', 'SIG'), 
                     ('NI-0(P,X+28-NI-57)','SIG'),
                     ('CU-0(P,X+27-CO-56)','SIG'),
                     ('CU-0(P,X+30-ZN-62)','SIG'),
                     ('CU-0(P,X+30-ZN-63)','SIG'),
                     ('CU-0(P,X+30-ZN-65)','SIG'),
                     ('AL-27(D,X+11-NA-22)','SIG'), 
                     ('AL-27(D,X+11-NA-24)','SIG'),
                     ('TI-0(D,X+23-V-48)', 'SIG'),
                     ('FE-0(D,X+27-CO-56)','SIG'),
                     ('NI-0(D,X+29-CU-61)','SIG'), 
                     ('AL-27(3HE,X+11-NA-22)','SIG'), 
                     ('AL-27(3HE,X+11-NA-24)','SIG'),
                     ('TI-0(3HE,X+23-V-48)', 'SIG'),
                     ('AL-27(A,X+11-NA-22)','SIG'), 
                     ('AL-27(A,X+11-NA-24)','SIG'),
                     ('TI-0(A,X+23-V-48)', 'SIG'),
                     ('CU-0(A,X+31-GA-66)','SIG'),
                     ('CU-0(A,X+31-GA-67)','SIG'),
                     ('CU-0(A,X+30-ZN-65)','SIG'), 
                     ('N-15(P,N+9-0-15)','SIG'), 
                     ('O-18(P,N+9-F-18)','SIG'),
                     ('ZN-67(P,N+31-GA-67)','SIG'),
                     ('ZN-68(P,2N+31-GA-67)','SIG'),
                     ('CD-111(P,N+49-IN-111)','SIG'), 
                     ('CD-112(P,2N+49-IN-111)','SIG'), 
                     ('TE-123(P,N+53-I-123)','SIG'),
                     ('TE-124(P,2N+53-I-123)','SIG'),
                     ('TE-124(P,N+53-I-124)','SIG'), 
                     ('I-127(P,5N+54-XE-123)','SIG'),
                     ('I-127(P,3N+54-XE-125)','SIG'),
                     ('KR-0(P,X+37-RB-81)','SIG'),
                     ('K4-82(P,2N+37-RB-82)','SIG'),
                     ('XE-124(P,2N+55-CS-123)','SIG'),
                     ('XE-124(P,P+N+54-XE-123)','SIG'),
                     ('TL-203(P,2N+82-PB-201)','SIG'),
                     ('TL-203(P,2N+82-PB-202-M)','SIG'),
                     ('TL-203(P,4N+82-PB-200)','SIG'),
                     ('N-14(P,A+6-C-11)','SIG'),
                     ('GA-69(P,2N+32-GE-68)','SIG'),
                     ('GA-0(P,X+32-GE-68)','SIG'),
                     ('O-16(P,A+7-N-13)','SIG'), 
                     ('RB-85(P,4N+38-SR-82)','SIG'), 
                     ('PB-0(P,X+38-SR-82)','SIG'),
                     ('N-14(D,N+8-0-15)','SIG'),
                     ('NE-0(D,X+9-F-19)','SIG')]


'''International Reactor Dosimetry and Fusion File IRDFF v.1.02, June 14, 2012'''
irdffReactions= [ 
    ('LI-6(N,T)','SIG'),
    ('B-10(N,A)','SIG'),
    ('F-19(N,2N)','SIG'),
    ('NA-23(N,2N)','SIG'),
    ('NA-23(N,G)','SIG'),
    ('MG-24(N,P)','SIG'),
    ('AL-27(N,P)','SIG'),
    ('AL-27(N,A)','SIG'),
    ('P-31(N,P)','SIG'),
    ('S-32(N,P)','SIG'),
    ('SC-45(N,G)','SIG'),
    ('TI-46(N,2N)','SIG'),
    ('TI-46(N,P)','SIG'),
    ('TI-47(N,X)','SIG'),
    ('TI-47(N,P)','SIG'),
    ('TI-48(N,X)','SIG'),
    ('TI-48(N,P)','SIG'),
    ('TI-49(N,X)','SIG'),
    ('V-51(N,A)','SIG'),
    ('CR-52(N,2N)','SIG'),
    ('MN-55(N,G)','SIG'),
    ('MN-55(N,2N)','SIG'),
    ('FE-54(N,2N)','SIG'),
    ('FE-54(N,P)','SIG'),
    ('FE-54(N,A)','SIG'),
    ('FE-56(N,P)','SIG'),
    ('FE-58(N,G)','SIG'),
    ('CO-59(N,2N)','SIG'),
    ('CO-59(N,3N)','SIG'),
    ('CO-59(N,G)','SIG'),
    ('CO-59(N,P)','SIG'),
    ('CO-59(N,A)','SIG'),
    ('NI-58(N,2N)','SIG'),
    ('NI-58(N,P)','SIG'),
    ('NI-60(N,P)','SIG'),
    ('CU-63(N,2N)','SIG'),
    ('CU-63(N,G)','SIG'),
    ('CU-63(N,A)','SIG'),
    ('CU-65(N,2N)','SIG'),
    ('ZN-64(N,P)','SIG'),
    ('ZA-67(N,P)','SIG'),
    ('AS-75(N,2N)','SIG'),
    ('Y-89(N,2N)','SIG'),
    ('ZR-90(N,2N)','SIG'),
    ('MO-92(N,P)','SIG'),
    ('NB-93(N,2N)','SIG'),
    ('NB-93(N,2N+41-NB-92-M)','SIG'),
    ('NB-93(N,INL)','SIG'),
    ('NB-93(N,G)','SIG'),
    ('RH-103(N,INL+45-RH-103-M)','SIG'),
    ('AG-109(N,G+47-AG-110-M)','SIG'),
    ('IN-113(N,INL+49-IN-113-M)','SIG'),
    ('IN-115(N,2N+49-IN-114-M)','SIG'),
    ('IN-115(N,INL+49-IN-115-M)','SIG'),
    ('IN-115(N,INL)','SIG'),
    ('IN-115(N,G+49-IN-116-M)','SIG'),
    ('I-127(N,2N)','SIG'),
    ('LA-139(N,G)','SIG'),
    ('PR-141(N,2N)','SIG'),
    ('TM-169(N,2N)','SIG'),
    ('TM-169(N,3N)','SIG'),
    ('TA-181(N,G)','SIG'),
    ('W-186(N,G)','SIG'),
    ('AU-197(N,2N)','SIG'),
    ('AU-197(N,G)','SIG'),
    ('HG-199(N,INL+80-HG-199-M)','SIG'),
    ('PB-204(N,INL+82-PB-204-M)','SIG'),
    ('BI-209(N,3N)','SIG'),
    ('TH-232(N,F+ELEM/MASS)', 'FY'),
    ('TH-232(N,G)','SIG'),
    ('U-235(N,F+ELEM/MASS)', 'FY'),
    ('U-238(N,F+ELEM/MASS)', 'FY'),
    ('U-238(N,G)','SIG'),
    ('NP-237(N,F+ELEM/MASS)', 'FY'),
    ('PU-239(N,F+ELEM/MASS)', 'FY'),
    ('AM-241(N,F+ELEM/MASS)', 'FY'),
]


'''Things our analysis has identified as being good candidates for evaluating and making into standards'''
ourProposed = [
    ('MO-0(P,X+43-TC-96)', 'SIG'), 
    ('MO-0(A,X+44-RU-97)', 'SIG'), 
    ('AL-27(P,X+11-NA-22)','SIG'),
    ('AL-27(P,X+11-NA-24)','SIG'),
    ('AL-27(P,N+3P)','SIG'),
    ('AL-27(6-C-12,X+11-NA-24)', 'SIG'), 
    ('AL-27(N,P)12-MG-27','SIG') ]                          


tier1Standards = standardsReactions + almostStandardReactions + atlasStandards
tier2Standards = dosimiterReactions + irdffReactions
allThingsProposed = soontobeStandards + ourProposed
proposedStandards = allThingsProposed

'''
Cumulative Lists for Multiple x_y_graphs function 
'''
cumulative1 = standardsReactions + atlasStandards
cumulative2 = standardsReactions + atlasStandards + dosimiterReactions
cumulative3 = standardsReactions + atlasStandards + dosimiterReactions + allThingsProposed


# -----------------------------------------------------------------------
#    Graph classes and helpers
# -----------------------------------------------------------------------
def create_graph():
    '''Factory function that knows what kind of graph to make based on whether networkx or graph_tool is imported'''
    if not FORCENETWORKX: return X4iGraphGT()
    return X4iGraphNX()


def load_graph( filename, returnBothGraphs=False, useGraphToolIO=False ):
    '''
    Because of a bug in versions 2.2.25-2.2.26 of graph_tool, graph_tool cannot load node or edge properties.
    
    So, to load a graph, we need to load it in networkx, then copy to graph_tool.  
    Since we already have the graph in networkx, you can optionally return it with the "returnBothGraphs" provided graph_tool is available.
    ''' 
 
    if returnBothGraphs and not FORCENETWORKX:
        graph = nx.read_graphml( filename ) 
        self_loop_list = graph.nodes_with_selfloops()
        for k in self_loop_list:
            graph.remove_edge(k,k)
        nxVersion = X4iGraphNX( nx.read_graphml( filename ) )
        if useGraphToolIO: 
            print "Warning: using graph-tool I/O.  Node and edge metadata will be lost."
            import graph_tool.stats
            graph = gt.load_graph( filename ) 
            graph_tool.stats.remove_self_loops(graph)
            gtVersion = X4iGraphGT( graph )
        else:              gtVersion = nxVersion.toGraphTool()
        return { 'graph_tool':gtVersion, 'networkx':nxVersion }

    if FORCENETWORKX: 
        graph = nx.read_graphml( filename ) 
        self_loop_list = graph.nodes_with_selfloops()
        for k in self_loop_list:
            graph.remove_edge(k,k)
        return X4iGraphNX( graph ) 
 
    if useGraphToolIO:
        import graph_tool.stats
        graph = gt.load_graph( filename ) 
        graph_tool.stats.remove_self_loops(graph)
        return X4iGraphGT( graph )
    
    return X4iGraphNX( nx.read_graphml( filename ) ).toGraphTool()


class X4iGraphBase:
    '''
    Base class of all graph classes, defines common interface
    
    In this and all derived classes, the graph is composed of nodes (a.k.a. vertices) and 
    edges (a.k.a. links).  Depending on the backend, the nodes and edges may be stored in 
    different ways.  For our purpose, both our nodes and edges are Python dicts containing 
    the node/edge attributes.
          
    As this is an undirected graph, ( node0, node1 ) == ( node1, node0 ).
      
    Node Attributes ::
    
        name (str): something like 'U-238(N,F)SIG', derived from EXFOR REACTION field
        reaction (str): something like '(N,F)' or '(A,P+A)'
        observable (str): something like 'SIG' or 'DA'
        projectile (str): something like 'N' or 'G'
        target (str): something like 'AU-197'
        weight (int): number of times this node "added"
        is_elemental_target (bool)
        is_isomer_target (bool)
        is_cielo_projectile_target (bool)
        is_neutron_standard (bool)
        is_cp_standard (bool)
        is_atlas_standard (bool)
        is_soon_tobe_standard (bool)   
        is_almost_standard (bool)
        is_our_proposed_standard (bool)
 
    Edge Attributes ::
    
        is_same_target (bool)
        weight_neutron_standard (int)
        weight_cp_standard (int)
        weight_almost_standard (int)
        weight_soon_to_be_standard (int)
        weight_cielo (int)
        weight_coupled (int)
        weight_monitor (int)
        weight_element (int)
        weight_sumrule (int)
        weight_specialquant (int)
    '''

    def __init__( self, graph_instance=None ): pass
    
    def save( self, filename ): 
        '''
        Save current graph in a file
        '''
        raise NotImplementedError( "Override this in derived classes" )
    
    def copy( self, return_type='graph_tool' ):
        # make the correct target class instance
        if return_type == 'graph_tool': target = X4iGraphGT()
        elif return_type == 'networkx': target = X4iGraphNX()
        else: raise ValueError( "return_type must be either 'graph_tool' or 'networkx'")
        
        # if self and target are already same type, return a deep copy
        if isinstance( self, target.__class__ ):
            import copy
            return copy.deepcopy( self )
        
        # copy the nodes and the node attributes
        for node in self.get_nodes():
            node_name = node['name']
            target.add_node(node_name)
            # add_node puts in the default attributes.  we need the actual ones from disk
            for a in node: 
                if not target.has_node_attribute(a): continue
                target.set_node_attribute(node_name,a,node[a])
        
        # copy the edges and the edge_attributes
        for edge in self.get_edges():
            node_name0 = edge['node0_name']
            node_name1 = edge['node1_name']
            target.add_edge(node_name0,node_name1)
            # add_edge puts in the default attributes.  we need the actual ones from disk
            for a in edge: 
                if not target.has_edge_attribute(a): continue
                target.set_edge_attribute(node_name0,node_name1,a,edge[a])
        
        return target
    
    # ------------ nodes ------------
    
    def __contains__( self, item ): 
        if type( item ) == str: return self.has_node( item )
        elif type( item ) == tuple: return self.has_edge( *item )
        else: raise TypeError( "Must be a string (for a node) or a tuple (for an edge)" )
    
    def num_nodes( self ):raise NotImplementedError( "Override this in derived classes" )
    
    def add_node( self, node_name ): raise NotImplementedError( "Override this in derived classes" )
    
    def add_nodes( self, node_list, maxCount=None, do_weight_update=True ):
        '''
        Add an unconnected bunch of nodes to the graph.
        @type cluster_node_list list
        @param cluster_node_list This list is a list of nodes that are to be connected by this routine.
        @type maxCount int
        @param maxCount Limit the number of EXFOR subentries to process when adding to graph.  "None" means there is no limit.
        @rtype int
        @return Number of EXFOR subentries processed and added to graph 
        '''
        count = 0
        for node_name in node_list:
            if do_weight_update and self.has_node( node_name ): self.update_node_weight( node_name )
            else: 
                self.add_node( node_name ) 
                count += 1   
            if maxCount is not None and self.num_nodes() >= maxCount: return count
        return count

    def has_node( self, node_name ): raise NotImplementedError( "Override this in derived classes" )

    def get_node( self, node_name ): 
        '''Gets the node attribute map associated with node_name'''
        raise NotImplementedError( "Override this in derived classes" )

    def get_nodes( self ): 
        '''Gets the list of node attribute dicts'''
        raise NotImplementedError( "Override this in derived classes" )

    def update_node_weight( self, node_name, amount=1 ): 
        new_amount = self.get_node_attribute( node_name, 'weight' ) + amount
        self.set_node_attribute( node_name, 'weight', new_amount )

    def get_node_weight( self, node_name ): return self.get_node_attribute( node_name, 'weight' )
        
    def get_node_attribute( self, node_name, key ): raise NotImplementedError( "Override this in derived classes" )

    def set_node_attribute( self, node_name, key, value ): raise NotImplementedError( "Override this in derived classes" )
    
    def has_node_attribute(self, key):raise NotImplementedError( "Override this in derived classes" )

    # ------------ edges ------------
    
    def num_edges( self ): raise NotImplementedError( "Override this in derived classes" )
        
    def add_edge( self, node0_name, node1_name, edge_weight_key=None ): 
        raise NotImplementedError( "Override this in derived classes" )

    def has_edge( self, node0_name, node1_name ): raise NotImplementedError( "Override this in derived classes" )

    def get_edge( self, node0_name, node1_name ): 
        '''Gets the edge attribute dict associated with ( node0_name, node1_name )'''
        raise NotImplementedError( "Override this in derived classes" )

    def get_edges( self ): 
        '''Gets the list of edge attribute dicts'''
        raise NotImplementedError( "Override this in derived classes" )

    def update_edge_weight( self, node0_name, node1_name, weight_key, amount=1 ): 
        new_amount = amount + self.get_edge_attribute( node0_name, node1_name, weight_key )
        self.set_edge_attribute( node0_name, node1_name, weight_key, new_amount )
    
    def get_edge_weight( self, node0_name, node1_name, weight_key ): 
        return self.get_edge_attribute( node0_name, node1_name, weight_key )
        
    def get_edge_attribute( self, node0_name, node1_name, key ): raise NotImplementedError( "Override this in derived classes" )

    def set_edge_attribute( self, node0_name, node1_name, key, value ): raise NotImplementedError( "Override this in derived classes" )
    
    def has_edge_attribute(self, key):raise NotImplementedError( "Override this in derived classes" )
    
    def remove_self_loops(self):raise NotImplementedError( "Override this in derived classes" )

        

    # ------------ connected cluster ------------
    
    def add_connected_cluster( self, cluster_node_list, cluster_name=None, maxCount=None, \
        edge_weight_key=None, do_weight_update=True ):
        '''
        Add a cluster nodes and edges to a graph.  
        All nodes in cluster will be connnected to one another.

        If a node and/or edge already is in the graph, only the weights get updated.

        @type cluster_node_list list
        @param cluster_node_list This list is a list of nodes that are to be connected by this routine.
        @type maxCount int
        @param maxCount Limit the number of EXFOR subentries to process when adding to graph.  "None" means there is no limit.
        @type edge_weight_key str, maps to weights in the edge attribute list
        @param edge_weight_key key to tell the edge instance what weight counter to update
        @type do_weight_update bool
        @param do_weight_update flag to tell code to update weights (very expensive calculation)
        @rtype tuple
        @return tuple with number of nodes and edges added to graph 
        '''

        '''
        Node Count is Reseting back to zero somewhere in the code, must find out where this is
        '''
        node_count=0
        edge_count=0
        for ik0, k0 in enumerate(cluster_node_list):
            if ( not maxCount is None ) and ( max( self.num_nodes(), node_count ) >= maxCount ): return node_count, edge_count
            if do_weight_update and self.has_node( k0 ):  self.update_node_weight( k0 )
            else:                 
                self.add_node( k0 )  
                node_count = node_count + 1         
            if ( not maxCount is None ) and ( max( self.num_nodes(), node_count ) >= maxCount ): return node_count, edge_count
            for k1 in cluster_node_list[ ik0+1: len( cluster_node_list ) ]: 
                if self.has_node( k1 ):  self.update_node_weight( k1 )
                else:            
                    self.add_node( k1 )  
                    node_count = node_count + 1             
                if not self.has_edge( k0, k1 ): 
                    self.add_edge( k0, k1, edge_weight_key )
                    edge_count += 1   
                if do_weight_update and edge_weight_key!= None: self.update_edge_weight( k0, k1, edge_weight_key )
                if ( not maxCount is None ) and ( max( self.num_nodes(), node_count ) >= maxCount ): return node_count, edge_count
        return node_count, edge_count

    # ------------ queries ------------
    
    def get_matching_target_projectile( self, target, projectile ):
        '''
        Get list of reaction node names which have a target and projectile matching the function arguments
        '''
        results=[]
        for k in self.get_nodes():
            if k['target']==target and k['projectile']==projectile: results.append( k )
        return results
            
    def get_elemental_targets( self ):
        '''
        Gets the list of reaction nodes that have an elemental target
        '''
        return [ x for x in self.get_nodes() if x['is_elemental_target'] ]

    def get_matching_processes( self, ProcString ):
        '''
        Get list of reaction node names which have a process matching "ProcString", e.g. 'EL' or 'SCT' or '2N'
        '''
        ProcStringList=[]
        for k in self.get_nodes():
            if ProcString in k['reaction']: ProcStringList.append( k )
        return ProcStringList
            
    def get_matching_quantities( self, QuantString ):
        '''
        Get list of reaction node names which have a quantity matching "QuantString", e.g. 'SIG' or 'DA'
        '''
        QuantStringList=[]
        for k in self.get_nodes():
            if k['observable'] == QuantString: QuantStringList.append( k )
        return QuantStringList

    # ------------ node statistics ------------
    
    def get_degree( self, node_name ):  raise NotImplementedError( "Override this in derived classes" )

    def get_weights_list( self ): 
        weightsList = []
        for k in self.get_nodes():
            weightsList.append(k['weight'])
        return weightsList
    
    # ------------ graph statistics ------------
    
    def get_top_N_lists( self,  N = -1 , SortBy = 'degree', Speed = 'slow' ):
        '''
        The following function is to be used in order to find the top N lists of the data in the graph, in the following different ways, 
        degree, eigen centrality, clustering coefficients, betweeness, closeness
        '''
        SortOptions = ['degree','eigenvalue', 'cluster', 'betweenness', 'closeness', 'weight', 'pagerank']
        if SortBy not in SortOptions:   raise KeyError( "Warning, You are not sorting by an acceptable method" )
        
        MyNodes = self.get_nodes()
        
        # Compute requested data
        everything = {}
        everything['degree'] = {k['name']:self.get_degree(k['name']) for k in MyNodes}
        everything['pagerank'] = self.get_page_rank( )
        if Speed == 'slow':
            everything['eigenvalue'] = self.get_eigenvector_centrality()
            everything['cluster'] = self.get_clustering_coefficients()
            everything['betweenness'] = self.get_betweenness_centrality()
            if FORCENETWORKX == True:
                everything['closeness'] = self.get_closeness_centrality_nx()
            elif FORCENETWORKX == False:
                everything['closeness'] = self.get_closeness_centrality_gt()

        # Load up everything into the nodes
        for k in MyNodes:
            for so in SortOptions:
                if so in everything:
                    k[so] = everything[so][k['name']]

        # Sort and return
        MyNodes = sorted(MyNodes, cmp=lambda y,x:cmp(x[SortBy], y[SortBy]))
        return MyNodes[0:N]
 
    def is_connected( self ): raise NotImplementedError( "Override this in derived classes" )
    
    def num_isolates( self ): raise NotImplementedError( "Override this in derived classes" )
    
    def get_connection_probability( self ): raise NotImplementedError( "Override this in derived classes" )

    def get_ave_degree( self ): raise NotImplementedError( "Override this in derived classes" )

    def get_ave_degree_sqr( self ): raise NotImplementedError( "Override this in derived classes" )
    
    def get_diameter( self ): raise NotImplementedError( "Override this in derived classes" )
    
    def get_radius( self ): raise NotImplementedError( "Override this in derived classes" )

    def get_ave_path_length( self ): raise NotImplementedError( "Override this in derived classes" )
    
    def get_ave_cluster_coefficient( self ): raise NotImplementedError( "Override this in derived classes" )

    def get_betweenness_centrality( self ): raise NotImplementedError( "Override this in derived classes" )
    
    def get_eigenvector_centrality( self ): raise NotImplementedError( "Override this in derived classes" )

    def get_distance_between_nodes( self ): raise NotImplementedError( "Override this in derived classes" )

    def get_nodes_matching_CIELO( self ): raise NotImplementedError( "Override this in derived classes" )

    def get_spectral_density( self ): raise NotImplementedError( "Override this in derived classes" )
    
    def get_info( self ):  
        graphInfo = { \
            "# of Nodes" : self.num_nodes(),\
            "# of Edges" : self.num_edges(), \
            "Is connected" : self.is_connected(), \
            "# of Isolates" : self.num_isolates(), \
            "Probability of Connection" : self.get_connection_probability(), \
            "<k>" : self.get_ave_degree(), \
            "<k^2>" : self.get_ave_degree_sqr(), \
            "<C>" : self.get_ave_cluster_coefficient() }
        if self.is_connected(  ) :
            graphInfo["Diameter"] = self.get_diameter()
            graphInfo["Radius"] = self.get_radius()
            graphInfo["Average path length"] = self.get_ave_path_length()
        return graphInfo


    # ------------ filtering ------------
    
    def filter( self, node_filter=None, edge_filter=None ):  raise NotImplementedError( "Override this in derived classes" )

    def keep_only_cross( self ): raise NotImplementedError( "Write me" )
        
    def keep_only_neutron( self ):  raise NotImplementedError( "Write me" )
        
    def keep_only_proton( self ): raise NotImplementedError( "Write me" )
        
    def keep_only_deuteron( self ): raise NotImplementedError( "Write me" )
        
    def keep_only_alpha( self ): raise NotImplementedError( "Write me" )
        
    def keep_only_gamma( self ): raise NotImplementedError( "Write me" )
        
    def keep_only_HE3( self ): raise NotImplementedError( "Write me" )
        
    def keep_only_triton( self ): raise NotImplementedError( "Write me" )
        
    def keep_only_carbon( self ): raise NotImplementedError( "Write me" )
        
    def keep_only_target( self, target ): raise NotImplementedError( "Write me" )
        
    def keep_only_target_projectile( self, target, projectile ): raise NotImplementedError( "Write me" )
    

class X4iGraphGT( X4iGraphBase ):
    '''
    Graph, using graph_tool classes
    
    In this class, the graph is composed of nodes (a.k.a. vertices) and 
    edges (a.k.a. links).  Depending on the backend, the nodes and edges may be stored in 
    different ways.  For our purpose, we will assume that each node is given by a key-value 
    pair ::
    
        * node_name: the key derived from the EXFOR reaction string, like  'B-10(N,A+G)SIG'
        * node_instance: the value, an instance of a Reaction_Node.  
          This contains all the functions, weights and data associated with the node.
        
    Similarly, an edge is given by a key-value pair ::
    
        * ( node0's node_name, node1's node_name ): the key is a tuple of node_names denoting the beginning and end of an edge
        * edge_instance: the value, an instance of a Correlation_Edge.  
          This contains all the functions, weights and data associated with the edge.
          
    As this is an undirected graph, ( node0, node1 ) == ( node1, node0 ).
    '''

    def __init__( self, graph_instance=None ):
        X4iGraphBase.__init__( self )
        if graph_instance!=None:
            if not isinstance( graph_instance, gt.Graph ): raise TypeError( "Must be graph_tool.Graph instance" )
            self.graph=graph_instance
        else: self.graph = gt.Graph(directed = False)
        
        # Set up node attributes
        self.graph.vertex_properties["name"]        = self.graph.new_vertex_property("string")
        self.graph.vertex_properties["reaction"]    = self.graph.new_vertex_property("string")
        self.graph.vertex_properties["observable"]  = self.graph.new_vertex_property("string")
        self.graph.vertex_properties["projectile"]  = self.graph.new_vertex_property("string")
        self.graph.vertex_properties["target"]      = self.graph.new_vertex_property("string")
        self.graph.vertex_properties["weight"]      = self.graph.new_vertex_property("int")
        self.graph.vertex_properties["is_elemental_target"]         = self.graph.new_vertex_property("bool")
        self.graph.vertex_properties["is_isomer_target"]            = self.graph.new_vertex_property("bool")
        self.graph.vertex_properties["is_cielo_projectile_target"]  = self.graph.new_vertex_property("bool")
        self.graph.vertex_properties["is_neutron_standard"]         = self.graph.new_vertex_property("bool")
        self.graph.vertex_properties["is_cp_standard"]              = self.graph.new_vertex_property("bool")
        self.graph.vertex_properties["is_atlas_standard"]           = self.graph.new_vertex_property("bool")
        self.graph.vertex_properties["is_soon_tobe_standard"]       = self.graph.new_vertex_property("bool")
        self.graph.vertex_properties["is_almost_standard"]          = self.graph.new_vertex_property("bool")
        self.graph.vertex_properties["is_our_proposed_standard"]    = self.graph.new_vertex_property("bool")
        #self.graph_vertex_properties["vertex_color"]                = self.graph.new_vertex_property("string")

        # Set up edge attributes
        self.graph.edge_properties["node0_name"]                = self.graph.new_edge_property("string")
        self.graph.edge_properties["node1_name"]                = self.graph.new_edge_property("string")
        self.graph.edge_properties["is_same_target"]            = self.graph.new_edge_property("bool")
        self.graph.edge_properties["weight_neutron_standard"]   = self.graph.new_edge_property("int")
        self.graph.edge_properties["weight_cp_standard"]        = self.graph.new_edge_property("int")
        self.graph.edge_properties["weight_almost_standard"]    = self.graph.new_edge_property("int")
        self.graph.edge_properties["weight_soon_to_be_standard"]= self.graph.new_edge_property("int")
        self.graph.edge_properties["weight_cielo"]              = self.graph.new_edge_property("int")
        self.graph.edge_properties["weight_coupled"]            = self.graph.new_edge_property("int")
        self.graph.edge_properties["weight_monitor"]            = self.graph.new_edge_property("int")
        self.graph.edge_properties["weight_element"]            = self.graph.new_edge_property("int")
        self.graph.edge_properties["weight_sumrule"]            = self.graph.new_edge_property("int")
        self.graph.edge_properties["weight_specialquant"]       = self.graph.new_edge_property("int")
        #self.graph.edge_properties["edge_color"]                = self.graph.new_edge_property("string")
        
    def save( self, filename ): 
        '''Save current graph in a GraphML file'''
        self.graph.save( filename )

    def toNetworkX(self): return self.copy( return_type = 'networkx')

    # ------------ nodes ------------
    
    def num_nodes( self ):return self.graph.num_vertices()
    
    def add_node( self, node_name ):
        target, reaction = node_name.split('(')
        reaction, observable = reaction.split(')')
        projectile = reaction.split(',')[0]
        reaction = '('+reaction+')'
        iterator = self.graph.add_vertex( )
        self.graph.vertex_properties["name"][iterator]          = node_name
        self.graph.vertex_properties["reaction"][iterator]      = reaction
        self.graph.vertex_properties["observable"][iterator]    = observable
        self.graph.vertex_properties["projectile"][iterator]    = projectile
        self.graph.vertex_properties["target"][iterator]        = target
        self.graph.vertex_properties["weight"][iterator]        = 1
        self.graph.vertex_properties["is_elemental_target"][iterator]         = is_element( target )
        self.graph.vertex_properties["is_isomer_target"][iterator]            = 'M' in target[-2:]
        self.graph.vertex_properties["is_cielo_projectile_target"][iterator]  = node_name.split(',')[0] in cieloTargetProjectiles
        self.graph.vertex_properties["is_neutron_standard"][iterator]         = node_name in standardsReactions
        self.graph.vertex_properties["is_cp_standard"][iterator]              = node_name in dosimiterReactions
        self.graph.vertex_properties["is_atlas_standard"][iterator]           = node_name in atlasStandards
        self.graph.vertex_properties["is_soon_tobe_standard"][iterator]       = node_name in soontobeStandards
        self.graph.vertex_properties["is_almost_standard"][iterator]          = node_name in almostStandardReactions
        self.graph.vertex_properties["is_our_proposed_standard"][iterator]    = node_name in proposedStandards
        return iterator
 
    def has_node( self, node_name ): 
        for v in self.graph.vertices():
            if self.graph.vertex_properties["name"][v] == node_name: return True
        return False
    
    def __get_raw_node( self, node_name ):
        '''
        Returns the graph-tool iterator, pointing to the node requested.  For internal use only.
        '''
        for v in self.graph.vertices():
            if self.graph.vertex_properties["name"][v] == node_name: return v
        raise KeyError( "Node named '"+node_name+"' not found!" )

    def get_node( self, node_name ):
        '''Gets the Reaction_Node associated with node_name'''
        result = {}
        for k in self.graph.vertex_properties:
            result[k] = self.graph.vertex_properties[k][ self.__get_raw_node( node_name ) ]
        return result
        
    def get_nodes( self ): 
        ListOfResults = []
        for v in self.graph.vertices():
            result = {}
            for k in self.graph.vertex_properties:
                result[k] = self.graph.vertex_properties[k][v]
            ListOfResults.append(result)
        return ListOfResults

    def get_node_attribute( self, node_name, key ): 
        return self.graph.vertex_properties[key][ self.__get_raw_node( node_name ) ]

    def set_node_attribute( self, node_name, key, value ): 
        self.graph.vertex_properties[key][ self.__get_raw_node( node_name ) ] = value

    def has_node_attribute(self, key): return key in self.graph.vertex_properties
        
    # ------------ edges ------------
    
    def num_edges( self ):return self.graph.num_edges()
        
    def add_edge( self, node0_name, node1_name, edge_weight_key=None ): 
        n0 = self.__get_raw_node( node0_name )
        n1 = self.__get_raw_node( node1_name )
        e = self.graph.add_edge( n0, n1 )
        self.graph.edge_properties["node0_name"][e]                = node0_name
        self.graph.edge_properties["node1_name"][e]                = node1_name
        self.graph.edge_properties["is_same_target"][e]            = node0_name.split('(')[0] == node1_name.split('(')[0]
        self.graph.edge_properties["weight_neutron_standard"][e]   = 0
        self.graph.edge_properties["weight_cp_standard"][e]        = 0
        self.graph.edge_properties["weight_almost_standard"][e]    = 0
        self.graph.edge_properties["weight_soon_to_be_standard"][e]= 0
        self.graph.edge_properties["weight_cielo"][e]              = 0
        self.graph.edge_properties["weight_coupled"][e]            = 0
        self.graph.edge_properties["weight_monitor"][e]            = 0
        self.graph.edge_properties["weight_element"][e]          = 0
        self.graph.edge_properties["weight_sumrule"][e]            = 0
        self.graph.edge_properties["weight_specialquant"][e]       = 0
        if edge_weight_key!=None:
            self.graph.edge_properties[edge_weight_key][e]         = 1
        return e
    
    def has_edge( self, node0_name, node1_name ): 
        for e in self.graph.edges():
            et = ( self.graph.edge_properties["node0_name"][e], self.graph.edge_properties["node1_name"][e] ) 
            if node0_name in et and node1_name in et: return True
        return False
                
    def __get_raw_edge( self, node0_name, node1_name ): 
        for e in self.graph.edges():
            et = ( self.graph.edge_properties["node0_name"][e], self.graph.edge_properties["node1_name"][e] ) 
            if node0_name in et and node1_name in et: return e
        raise KeyError( "Edge connecting '"+node0_name+"' and '"+node1_name+"' not found!" )

    def get_edge( self, node0_name, node1_name ): 
        '''Gets the Correlation_Edge associated with ( node0_name, node1_name )'''
        result = {}
        for k in self.graph.edge_properties:
            result[k] = self.graph.edge_properties[k][ self.__get_raw_edge( node0_name, node1_name ) ]
        return result

    def get_edges( self ): 
        ListOfEdgesResults = []
        for e in self.graph.edges():
            result = {}
            for p in self.graph.edge_properties:
                result[p] = self.graph.edge_properties[p][e]
            ListOfEdgesResults.append(result)
        return ListOfEdgesResults

    def get_edge_attribute( self, node0_name, node1_name, key ): 
        return self.graph.edge_properties[key][ self.__get_raw_edge( node0_name, node1_name ) ]

    def set_edge_attribute( self, node0_name, node1_name, key, value ): 
        self.graph.edge_properties[key][ self.__get_raw_edge( node0_name, node1_name ) ] = value

    # ------------ node statistics ------------
    
    def has_edge_attribute(self,key): return key in self.graph.edge_properties
    
    def remove_self_loops(self):
        import graph_tool.stats
        graph_tool.stats.remove_self_loops(self.graph)
    
    def get_degree( self, node_name ):
        return self.__get_raw_node( node_name ).out_degree()  

    def get_degree_list( self ):
        degree_list = []
        for k in self.graph.vertices():
            degree_list.append( k.out_degree())
        return degree_list
    
    # ------------ Node & Edge Coloring ------------ 

    def get_node_colors( self ):
        nodeColor = self.graph.new_vertex_property('string')
        nodeFillcolor = self.graph.new_vertex_property('string')
        for node in self.graph.vertices():
            if self.graph.vertex_properties["is_elemental_target"][node] == True:
                nodeColor[node] = '#000000'
                nodeFillcolor[node] = '#0cf232'
            elif self.graph.vertex_properties["is_isomer_target"][node] == True:
                nodeColor[node] = '#000000'
                nodeFillcolor[node] = '#f90000'
            elif self.graph.vertex_properties["is_cielo_projectile_target"][node] == True:
                nodeColor[node] = '#000000'
                nodeFillcolor[node] = '#00f8c1'
            elif self.graph.vertex_properties["is_neutron_standard"][node] == True:
                nodeColor[node] = '#505655'
                nodeFillcolor[node] = '#000000'
            elif self.graph.vertex_properties["is_cp_standard"][node] == True:
                nodeColor[node] = '#000000'
                nodeFillcolor[node] = '#a9257c'
            elif self.graph.vertex_properties["is_atlas_standard"][node] == True:
                nodeColor[node] = '#fbff00'
                nodeFillcolor[node] = '#064f15'
            elif self.graph.vertex_properties["is_soon_tobe_standard"][node] == True:
                nodeColor[node] = '#085de5'
                nodeFillcolor[node] = '#085de5'
            elif self.graph.vertex_properties["is_almost_standard"][node] == True:
                nodeColor[node] = '#000000'
                nodeFillcolor[node] = '#f95800'
            elif self.graph.vertex_properties["is_our_proposed_standard"][node] == True:
                nodeColor[node] = '#000000'
                nodeFillcolor[node] = '#0007f9'
            else:
                nodeColor[node] = '#000000'
                nodeFillcolor[node] = '#ffffff'
        self.graph.vertex_properties["nodeColor"] = nodeColor
        self.graph.vertex_properties["nodeFillcolor"] = nodeFillcolor

    def get_edge_colors( self ):
        edgeColor = self.graph.new_edge_property('string')
        self.graph.edge_properties["edgeColor"] = edgeColor
        for edge in self.graph.edges():
            if self.graph.edge_properties["weight_element"][edge] != 0.0:
                edgeColor[edge] = '#0cf232'
            elif self.graph.edge_properties["weight_monitor"][edge] != 0.0:
                edgeColor[edge] = '#000000'
            elif self.graph.edge_properties["weight_cielo"][edge] != 0.0:
                edgeColor[edge] = '#00f8c1'
            elif self.graph.edge_properties["weight_neutron_standard"][edge] != 0.0:
                edgeColor[edge] = '#00f8c1'
            else:   
                edgeColor[edge] = '#f90000'
        self.graph.edge_properties["edgeColor"] = edgeColor
                
    # ------------ Graph Drawing ------------ 
    
    def drawGraph( self, output_size=(200,200), outFile=None ):
        import graph_tool.draw
        self.get_edge_colors()
        self.get_node_colors()
        k = graph_tool.draw.arf_layout(self.graph)
        graph_tool.draw.graph_draw(
                                   self.graph, 
                                   pos = k, 
                                   vertex_color = self.graph.vertex_properties["nodeColor"], 
                                   vertex_fill_color = self.graph.vertex_properties["nodeFillcolor"], 
                                   vertex_size = self.graph.vertex_properties["weight"], 
                                   vertex_text_position = 1, 
                                   vertex_text = self.graph.vertex_properties["name"], 
                                   edge_color = self.graph.edge_properties["edgeColor"], 
                                   display_props=['name'],
                                   output_size=output_size, 
                                   output=outFile)


    
    # ------------ graph statistics ------------   
    
    def is_connected( self ): 
        connected = True
        for x in self.graph.vertices():
            dgr = x.out_degree()
            if dgr == 0:
                connected = False
            else: pass
        return connected
    
    def num_isolates( self ): 
        isolateNUMB = 0
        for rr in self.graph.vertices():
            count = 0
            zz = gt.Vertex.all_neighbours(rr)
            for y in zz:
                count = count + 1
            if count == 0:
                isolateNUMB = isolateNUMB + 1 
        return isolateNUMB
    
    def get_connection_probability( self ): 
        '''
        connection probability is equal to the total number of edges divided by the total number of edges possible
        '''
        tnoe = self.graph.num_edges()
        tnon = self.graph.num_vertices()
        tnoep = (tnon*(tnon-1))/2.0
        cp = tnoe/tnoep
        return cp

    def get_ave_degree( self ): 
        avgDgrTot = 0
        for x in self.graph.vertices():
            dgr = x.out_degree()
            avgDgrTot = dgr + avgDgrTot
        avgDgr = avgDgrTot/(self.graph.num_vertices())
        return avgDgr

    def get_ave_degree_sqr( self ): 
        avgDgrTot = 0
        for x in self.graph.vertices():
            dgr = x.out_degree()
            avgDgrTot = dgr + avgDgrTot
        numnodes = self.graph.num_vertices()
        denominator = numnodes*(numnodes-1)
        avgDgrsqr = math.pow(avgDgrTot,2.0)/denominator 
        return avgDgrsqr
    
    def get_diameter( self ): 
        '''
        pseudo_diameter outputs a tuple of info with diameter being the first element of the tuple
        & the two nodes iterators that are part of the diameter as the second part of the tuple
        '''
        import graph_tool.topology
        dist, ends = graph_tool.topology.pseudo_diameter(self.graph)
        return dist

    def get_closeness_centrality_gt( self, Node = None ): 

        '''
        Attention Closeness Issue! Graph-Tool and NetworkX perform the Closeness Centrality differently. Calculating the 
        closeness       centrality for networkx using n = number of nodes in the graph. Whereas calculating the closeness 
        centrality in  graph tool uses n = number of nodes in the cluster. To combat this two seperate unique functions were 
        written which will provide different output for any graph with cluster count greater than or equal to 2
        '''
        close_dict = {}
        import graph_tool.centrality
        cc = graph_tool.centrality.closeness(self.graph)
        for c in self.graph.vertices():
            close_dict[self.graph.vertex_properties["name"][c]]=cc[c]
        if Node == None:
            return close_dict
        else: 
            for p in close_dict:
                if p == Node:
                    return close_dict[Node]
        
    def get_betweenness_centrality( self, Node = None ): 
        between_dict = {}
        import graph_tool.centrality
        bc, fg = graph_tool.centrality.betweenness(self.graph)
        for g in self.graph.vertices():
            between_dict[self.graph.vertex_properties["name"][g]]=bc[g]
        if Node == None:
            return between_dict
        else:
            for p in between_dict:
                if p == Node:
                    return between_dict[Node]

    def get_eigenvector_centrality( self , Node = None ):
        eigen_dict = {} 
        import graph_tool.centrality
        he,el = graph_tool.centrality.eigenvector(self.graph)
        for k in self.graph.vertices():
            eigen_dict[self.graph.vertex_properties["name"][k]]=el[k]
        if Node == None:
            return eigen_dict
        else: 
            for p in eigen_dict:
                if p == Node:
                    return eigen_dict[Node]

    def get_page_rank( self, Node = None ):
        pageRank_dict = {}
        import graph_tool.centrality
        pr = graph_tool.centrality.pagerank(self.graph)
        for k in self.graph.vertices():
            pageRank_dict[self.graph.vertex_properties['name'][k]] = pr[k]
        if Node == None:
            return pageRank_dict
        else:
            for p in pageRank_dict:
                if p == Node:
                    return pageRank_dict[Node]
        
    def get_clustering_coefficients( self, Node = None ):
        '''
        get_clustering_coefficients is for returning a list of clusetering coefficients
        '''
        import graph_tool.clustering
        cc_dict = {}
        cc = graph_tool.clustering.local_clustering( self.graph )
        for h in self.graph.vertices():
            cc_dict[self.graph.vertex_properties['name'][h]]=cc[h]
        if Node == None:
            return cc_dict
        else: 
            for h in cc_dict:
                if h == Node:
                    return cc_dict[Node]

    def get_clustering_distribution( self ):
        '''
        get_clustering_distribution returns a list of tuples of form (clustering coefficient, # of occurances)
        '''
        import graph_tool.clustering 
        clustering_occur_list = []
        cluster_occur = {}
        clustering_list = []
        count = 1
        cc = graph_tool.clustering.local_clustering( self.graph )
        for node in self.graph.vertices():clustering_occur_list.append(cc[node])
        for v in clustering_occur_list:
            if v not in cluster_occur:cluster_occur[v] = 1  
            elif v in cluster_occur:cluster_occur[v] = cluster_occur[v] + 1    
        cluster_occur_list = sorted(cluster_occur.items())
        return cluster_occur_list

    def get_nodes_matching_CIELO( self ):
        '''
        This function can be used for the gathering the list of all CIELO nodes as tuples for use in distance functions 
        '''
        CIELOlist = []
        for node in self.graph.vertices():
            for k in cieloTargetProjectiles:
                if k in self.graph.vertex_properties['name'][node]: 
                    CIELOlist.append( self.graph.vertex_properties['name'][node] )
                else: pass
        return CIELOlist    

    def get_radius( self ): raise NotImplementedError( "Until we possibly code up a function for taking the eccentricity of the graph we cannot code up a radius function" )

    def get_distance_between_nodes( self, TargetList = standardsReactions):
        TargetList = [''.join(x) for x in TargetList]
        import graph_tool.topology
        DistancetoTargetList = []
        for x in self.graph.vertices():
            TempDistanceList = []
            for p in TargetList:
                try: TempDistanceList.append( graph_tool.topology.shortest_distance(self.graph, source = x, target = self.__get_raw_node(p)) )
                except ( nx.NetworkXNoPath, nx.NetworkXError ): pass
            if TempDistanceList == []:
                pass
            else:
                DistancetoTargetList.append( min(TempDistanceList) )
        return DistancetoTargetList   
        
    def get_spectral_density( self ):
        import graph_tool.spectral
        A = graph_tool.spectral.adjacency( self.graph )
        ew, ev= scipy.sparse.linalg.eigsh( A.todense() )
        return ew, ev
        


    # ------------ filtering ------------
    
    def filter( self, node_filter=None, edge_filter=None ): 
        return X4iGraphGT( graph_instance=gt.GraphView( self.graph, vfilt=node_filter, efilt=edge_filter ) )

       
class X4iGraphNX( X4iGraphBase ):
    '''
    Graph, using networkx classes
    
    In this class, the graph is composed of nodes (a.k.a. vertices) and 
    edges (a.k.a. links).  Depending on the backend, the nodes and edges may be stored in 
    different ways.  For our purpose, we will assume that each node is given by a key-value 
    pair ::
    
        * node_name: the key derived from the EXFOR reaction string, like  'B-10(N,A+G)SIG'
        * node_instance: the value, an instance of a Reaction_Node.  
          This contains all the functions, weights and data associated with the node.
        
    Similarly, an edge is given by a key-value pair ::
    
        * ( node0's node_name, node1's node_name ): the key is a tuple of node_names denoting the beginning and end of an edge
        * edge_instance: the value, an instance of a Correlation_Edge.  
          This contains all the functions, weights and data associated with the edge.
          
    As this is an undirected graph, ( node0, node1 ) == ( node1, node0 ).
    '''

    def __init__( self, graph_instance=None ):
        X4iGraphBase.__init__( self )
        if graph_instance!=None:
            if not isinstance( graph_instance, nx.Graph ): raise TypeError( "Must be networkx.Graph instance" )
            self.graph=graph_instance
        else: self.graph = nx.Graph()
        
    def save( self, filename ): 
        '''Save current graph in a GraphML file'''
        nx.write_graphml( self.graph, filename )

    def toGraphTool(self): 
        target = X4iGraphGT()
        
        # copy the nodes and the node attributes
        for node in self.get_nodes():
            node_name = node['name']
            iNode = target.add_node(node_name)
            # add_node puts in the default attributes.  we need the actual ones from disk
            for a in node: 
                if not target.has_node_attribute(a): continue
                target.graph.vertex_properties[a][iNode] = node[a]
        
        # copy the edges and the edge_attributes
        for edge in self.get_edges():
            node_name0 = edge['node0_name']
            node_name1 = edge['node1_name']
            iEdge = target.add_edge(node_name0,node_name1)
            # add_edge puts in the default attributes.  we need the actual ones from disk
            for a in edge: 
                if not target.has_edge_attribute(a): continue
                target.graph.edge_properties[a][iEdge] = edge[a]
        
        return target
        
#        return self.copy(return_type='graph_tool')

    # ------------ nodes ------------
    
    def num_nodes( self ): return self.graph.number_of_nodes()
    
    def add_node( self, node_name ):
        target, reaction = node_name.split('(')
        reaction, observable = reaction.split(')')
        projectile = reaction.split(',')[0]
        reaction = '('+reaction+')'
        self.graph.add_node( \
            node_name, \
            name = node_name,\
            reaction = reaction,\
            observable = observable,\
            projectile = projectile,\
            target = target,\
            weight = 1,\
            is_elemental_target = is_element( target ),\
            is_isomer_target = 'M' in target[-2:],\
            is_cielo_projectile_target = node_name.split(',')[0] in cieloTargetProjectiles,\
            is_neutron_standard = node_name in standardsReactions,\
            is_cp_standard = node_name in dosimiterReactions,\
            is_atlas_standard = node_name in atlasStandards,\
            is_soon_tobe_standard = node_name in soontobeStandards,\
            is_almost_standard = node_name in almostStandardReactions,\
            is_our_proposed_standard = node_name in proposedStandards )
        return self.graph.node[node_name]
    
    def has_node( self, node_name ): return self.graph.has_node( node_name )
    
    def get_node( self, node_name ): 
        '''Gets the node associated with node_name'''
        return self.graph.node[node_name]
                
    def get_nodes( self ): 
        '''Gets the list of nodes as Reaction_Node instances'''
        return [x[1] for x in self.graph.nodes( data=True )]

    def get_node_attribute( self, node_name, key ): return self.graph.node[node_name][key]

    def set_node_attribute( self, node_name, key, value ): self.graph.node[node_name][key]=value
          
    def has_node_attribute(self,key): 
        if len(self.graph.node) == 0: return False
        n = self.graph.nodes()[0]
        return key in self.graph.node[n]      
          
    # ------------ edges ------------
    
    def num_edges( self ): return self.graph.number_of_edges()
        
    def add_edge( self, node0_name, node1_name, edge_weight_key=None ): 
        self.graph.add_edge( \
            node0_name, \
            node1_name, \
            node0_name = node0_name, \
            node1_name = node1_name, \
            is_same_target = node0_name.split('(')[0] == node1_name.split('(')[0], \
            weight_neutron_standard = 0, \
            weight_cp_standard = 0, \
            weight_almost_standard = 0, \
            weight_soon_to_be_standard = 0, \
            weight_cielo = 0, \
            weight_coupled = 0, \
            weight_monitor = 0, \
            weight_element = 0, \
            weight_sumrule = 0, \
            weight_specialquant = 0 )
        if edge_weight_key!=None:
            self.graph[ node0_name ][ node1_name ][edge_weight_key] = 1
        return self.graph[ node0_name ][ node1_name ]
        
    def has_edge( self, node0_name, node1_name ): 
        return ( node0_name, node1_name ) in self.graph.edges() or ( node1_name, node0_name ) in self.graph.edges()

    def get_edge( self, node0_name, node1_name ):
        '''Gets the Correlation_Edge associated with ( node0_name, node1_name )'''
        return self.graph[ node0_name ][ node1_name ]
            
    def get_edges( self ): 
        return [ x[2] for x in self.graph.edges( data=True ) ]

    def get_edge_attribute( self, node0_name, node1_name, key ): 
        return self.get_edge( node0_name, node1_name )[key]

    def set_edge_attribute( self, node0_name, node1_name, key, value ): 
        self.get_edge( node0_name, node1_name )[key] = value

    def has_edge_attribute(self,key): 
        if len(self.graph.edges) == 0: return False
        n = self.graph.edges()[0]
        return key in self.graph[ n[0] ][ n[1] ]

    # ------------ node statistics ------------
    
    def get_degree( self, node_name ):  return self.graph.degree( node_name )

    def get_degree_list( self ):
        degree_list = []
        for k in self.graph.nodes():
            degree_list.append( self.get_degree( k ))
        return degree_list

    def get_nodes_with_degree( self, degree ): 
        dgr = degree
        listOfTuples = []
        for k in self.graph.nodes():
            listOfTuples.append( (k , self.get_degree( k )) )
        for lp in listOfTuples:
            if dgr == lp[-1]:
                print lp[0]
            else:
                pass
            
            
   
        
    # ------------ graph statistics ------------
    
    def is_connected( self ): return nx.is_connected( self.graph )
    
    def num_isolates( self ): 
        count = 0
        for x in self.graph.nodes():
            q = self.graph.neighbors(x)
            if q == []: count = count + 1
            else: pass
        return count             
    
    def get_connection_probability( self ): 
        '''
        connection probability is equal to the total number of edges divided by the total number of edges possible
        '''
        tnoe = self.graph.number_of_edges()
        tnon = self.graph.number_of_nodes()
        tnoep = (tnon*(tnon-1))/2.0 
        cp = tnoe/tnoep
        return cp

    def get_distance_between_nodes( self, TargetList = standardsReactions ):
        TargetList = [''.join(x) for x in TargetList]
        DistancetoTargetList = []
        for x in self.graph.nodes():
            TempDistanceList = []
            for p in TargetList:
                try: TempDistanceList.append( nx.shortest_path_length(self.graph,source = x, target = p) )
                except ( nx.NetworkXNoPath, nx.NetworkXError ): pass
            if TempDistanceList == []:
                pass
            else:
                DistancetoTargetList.append( min(TempDistanceList) )
        return DistancetoTargetList

    def get_ave_degree( self ):
        summation = 0.0 
        for x in self.graph.nodes():
            deg = self.graph.degree( x )
            summation = deg + summation
        aveDeg = summation/(self.graph.number_of_nodes())
        return aveDeg

    def get_ave_degree_sqr( self ): 
        summation = 0.0 
        for x in self.graph.nodes():
            deg = self.graph.degree( x )
            summation = deg + summation
        numnodes = 0.0
        numnodes = self.graph.number_of_nodes()
        denominator = (numnodes)*(numnodes-1.0)
        aveDegSqr = (math.pow(summation,2))/denominator
        return aveDegSqr
    
    def get_diameter( self ): return nx.diameter( self.graph )
    
    def get_radius( self ): return nx.radius( self.graph )

    def get_ave_path_length( self ): return nx.average_shortest_path_length( self.graph )
    
    def get_ave_cluster_coefficient( self ): return nx.average_clustering( self.graph )

    def get_nodes_matching_CIELO( self ):
        '''
        This function can be used for the gathering the list of all CIELO nodes as tuples for use in distance functions 
        '''
        CIELOlist = []
        for node in self.graph.nodes():
            for k in cieloTargetProjectiles:
                if k in node: 
                    CIELOlist.append( node )
                else: pass
        return CIELOlist    

    def get_page_rank( self, Node = None, max_iter=100, tol=1.e-8 ):
        pr = nx.pagerank(self.graph, max_iter=max_iter, tol=tol)
        if Node == None: return pr
        else: return pr[Node]

    def get_pagerank_list( self, max_iter = 100, tol=1.e-8 ):
        pageranklist = []
        pr = nx.pagerank(self.graph, max_iter=max_iter, tol=tol)
        for xx in self.graph.nodes():
            pageranklist.append(pr[xx])
        return pageranklist
            
    def get_closeness_centrality_nx( self, Node = None):
        '''
        Attention Closeness Issue! Graph-Tool and NetworkX perform the Closeness Centrality differently. Calculating the 
        closeness       centrality for networkx using n = number of nodes in the graph. Whereas calculating the closeness 
        centrality in  graph tool uses n = number of nodes in the cluster. To combat this two seperate unique functions were 
        written which will provide different output for any graph with cluster count greater than or equal to 2
        '''
        close_dict = {}
        close_dict = nx.closeness_centrality( self.graph )
        if Node == None: 
            return close_dict
        else: 
            for p in close_dict:
                if p == Node:
                    return close_dict[Node]

    def get_betweenness_centrality( self, Node = None):
        between_dict = {}
        between_dict = nx.betweenness_centrality( self.graph ) 
        if Node == None: 
            return between_dict
        else: 
            for p in between_dict:
                if p == Node:
                    return between_dict[Node]
    
    def get_eigenvector_centrality( self, Node = None ): 
        eigen_dict = {}
        eigen_dict = nx.eigenvector_centrality( self.graph )
        if Node == None:
            return eigen_dict
        else: 
            for p in eigen_dict:
                if p == Node:
                    return eigen_dict[Node]

    def get_subgraphs( self , minDegree = 100):
        import matplotlib.pyplot as plt
        count = 0
        for k in nx.connected_component_subgraphs( self.graph ):
            if len(k.nodes()) >= minDegree:
                H = k
                nx.write_graphml(H,'Graphs'+str(count)+'.xml') 
                count = count + 1
                fk = open('GraphsList'+str(count)+'.txt', 'w+')
                for k in H.nodes():
                    fk.write(str(k)+'\n')
                fk.close()   

    def get_N_TOT_Errors( self ):
        SubgraphNodeCounts = []
        for k in nx.connected_component_subgraphs( self.graph ):
            SubgraphNodeCounts.append(len(k.nodes()))
            if len(k.nodes()) == 1:
                for p in k.nodes():
                    if '(N,TOT)' in p:
                        print str(p)  
        return SubgraphNodeCounts

    def get_subgraph_counts( self ):
        SubgraphNodeCounts = []
        IsolatesList = open('IsolatesList.txt', 'w+')
        for k in nx.connected_component_subgraphs( self.graph ):
            SubgraphNodeCounts.append(len(k.nodes()))
            if len(k.nodes()) == 1:
                for p in k.nodes():
                    IsolatesList.write(str(p)+'\n') 
        IsolatesList.close()
        return SubgraphNodeCounts

    def get_clustering_coefficients( self, Node = None ):
        '''
        get_clustering_coefficients returns a list of the clustering coefficinents for the nodes in the graph
        '''
        cc_dict = {}
        cc_dict = nx.clustering( self.graph )
        if Node == None:
            return cc_dict
        else:
            for p in cc_dict:
                if p == Node:
                    return cc_dict[Node]

    def get_clustering_distribution( self ):
        '''
        get_clustering_distribution returns a list of tuples of form (clustering coefficient, # of occurances)
        '''
        clustering_occur_list = []
        cluster_occur = {}
        clustering_list = []
        count = 1
        for node in self.graph.nodes():clustering_occur_list.append(nx.clustering(self.graph,[node]).items()[0][1])
        for v in clustering_occur_list:
            if v not in cluster_occur:cluster_occur[v] = 1  
            elif v in cluster_occur:cluster_occur[v] = cluster_occur[v] + 1    
        cluster_occur_list = sorted(cluster_occur.items())
        return cluster_occur_list

    def get_clustering_coefficient_list( self ):
        '''
        get_clustering_distribution returns a list of tuples of form (clustering coefficient, # of occurances)
        '''
        clustering_occur_list = []
        cluster_occur = {}
        clustering_list = []
        count = 1
        for node in self.graph.nodes():clustering_occur_list.append(nx.clustering(self.graph,[node]).items()[0][1])
        return clustering_occur_list


    def get_average_cluster_coefficient( self ):
        clustering_occur_list = []
        ccTotal = 0.0
        for node in self.graph.nodes():clustering_occur_list.append(nx.clustering(self.graph,[node]).items()[0][1])
        for k in clustering_occur_list:
            ccTotal = ccTotal + k
        Ave_Clust_Coef = ccTotal/self.graph.number_of_nodes()
        return Ave_Clust_Coef

    # ------------ filtering ------------
    
    def filter( self, node_filter=None, edge_filter=None ):  raise NotImplementedError( "Override this in derived classes" )

        
# -----------------------------------------------------------------------
#    Add cluster functions
# -----------------------------------------------------------------------

# ---- following add nodes/edges from external sources, call these first ----

def add_neutron_standards_cluster( theGraph, maxCount=None, do_weight_update=True, verbose=True ):
    '''Get the Standards data (+ everything done with standards) and couple together'''
    nn,ne = theGraph.add_connected_cluster( \
        [ ''.join(x) for x in standardsReactions ], \
        cluster_name="standardsReactions", \
        maxCount=maxCount, \
        edge_weight_key='weight_neutron_standard',\
        do_weight_update=do_weight_update )
    if verbose: print "Neutron standards: added %i nodes and %i edges" % (nn,ne)
    
@timeit
def add_monitor_clusters( theGraph, maxCount=None, do_weight_update=True, verbose=False ): 
    '''
    Get all reactions that have reaction monitors and couple those reactions to those monitors
    '''
    nn=0
    ne=0
    f = cPickle.load( open( fullMonitoredFileName, mode='r' ) )
    for k in f: 
        iin,iie = theGraph.add_connected_cluster( \
            [ ''.join(x) for x in f[k] ], \
            cluster_name=k, \
            maxCount=maxCount, \
            edge_weight_key='weight_monitor',\
            do_weight_update=do_weight_update )
        nn+=iin
        ne+=iie
    if verbose: print "Monitor data: added %i nodes and %i edges" % (nn,ne) 

@timeit
def add_coupled_clusters( theGraph, maxCount=None, do_weight_update=True, verbose=False ):
    '''
    Get all reactions that are coupled via EXFOR reaction field math, then make clusters
    '''
    nn=0
    ne=0
    f = cPickle.load( open( fullCoupledFileName, mode='r' ) )
    for k in f: 
        iin,iie = theGraph.add_connected_cluster( \
            [ ''.join(x) for x in f[k] ], \
            cluster_name=k, \
            maxCount=maxCount, \
            edge_weight_key='weight_coupled', \
            do_weight_update=do_weight_update )
        nn+=iin
        ne+=iie
    if verbose: print "Coupled data: added %i nodes and %i edges" % (nn,ne) 

def add_atlas_nodes( theGraph, maxCount=None, do_weight_update=True, verbose=False ): 
    '''Show all Atlas Standards Reactions'''
    n = theGraph.add_nodes( [''.join(x) for x in atlasStandards], maxCount, do_weight_update=do_weight_update )
    if verbose: print "Add all Atlas Standards reaction data: %i nodes" % n 

@timeit
def add_reaction_nodes( theGraph, maxCount=None, do_weight_update=True, verbose=False ): 
    '''Show all Reaction Data'''
    r = cPickle.load( open( fullReactionCountFileName, mode='r') ) 
    n = theGraph.add_nodes( [''.join(x) for x in r], maxCount, do_weight_update=do_weight_update )
    if verbose: print "Add all Reaction data: %i nodes" % n 

def add_expanded_neutron_standards_clusters( theGraph, maxCount=None, do_weight_update=True, verbose=False ): 
    '''Get the Standards data + everything done with standards + new standards and couple together'''
    nn,ne = theGraph.add_connected_cluster( \
        [ ''.join(x) for x in standardsReactions+almostStandardReactions+soontobeStandards ], \
        cluster_name="supersetOfStandardsReactions", \
        maxCount=maxCount, \
        edge_weight_key='weight_soon_to_be_standard', \
        do_weight_update=do_weight_update )
    if verbose: print "Expanded neutron standards: added %i nodes and %i edges" % (nn,ne)

# ---- following add nodes/edges using nodes already in the graph, call these second, and in the correct order ----
# ----    since it is hard to figure out the right order, use the catch-all function add_rest_of_clusters()    ----
# ----  these also have additional edge_weight_key argument to allow you to turn off weighting from these guys ----

@timeit
def _add_inclusive_clusters( theGraph, maxCount=None, edge_weight_key='weight_sumrule', do_weight_update=True, verbose=False ): 
    '''
    Unpacks (==expands a reaction into a cluster) the inclusive reactions 'ABS', 'SCT', and 'NON' using EXFOR sum rules.  
    The sum rules are ::
    
        * (N,ABS) = (N,TOT) - (N,SCT)
        * (N,ABS) = (N,NON) - (N,INL)
        * (N,NON) = (N,TOT) - (N,EL)
        * (N,SCT) = (N,INL) + (N,EL)
    '''
    nn=0
    ne=0
    for o in theGraph.get_matching_processes( 'ABS' ) :
        if 'SIG' in o['name'] and 'N,' in o['name']:
            iin,iie = theGraph.add_connected_cluster( \
                [ o['name'], o['name'].replace('ABS', 'TOT'), o['name'].replace('ABS', 'SCT') ], cluster_name=o['name'], \
                    maxCount=maxCount, edge_weight_key=edge_weight_key, do_weight_update=do_weight_update )
            nn+=iin
            ne+=iie
            iin,iie = theGraph.add_connected_cluster( \
                [ o['name'], o['name'].replace('ABS', 'NON'), o['name'].replace('ABS', 'INL') ], cluster_name=o['name'], \
                    maxCount=maxCount, edge_weight_key=edge_weight_key, do_weight_update=do_weight_update )
            nn+=iin
            ne+=iie
    for o in theGraph.get_matching_processes( 'NON' ) :
        if 'SIG' in o['name'] and 'N,' in o['name']:
            iin,iie = theGraph.add_connected_cluster( \
                [ o['name'], o['name'].replace('NON', 'TOT'), o['name'].replace('NON', 'EL') ], cluster_name=o['name'], \
                    maxCount=maxCount, edge_weight_key=edge_weight_key, do_weight_update=do_weight_update )
            nn+=iin
            ne+=iie
    for o in theGraph.get_matching_processes( 'SCT' ) :
        if 'SIG' in o['name'] and 'N,' in o['name']:
            iin,iie = theGraph.add_connected_cluster( \
                [ o['name'], o['name'].replace('SCT', 'INL'), o['name'].replace('SCT', 'EL') ], cluster_name=o['name'], \
                    maxCount=maxCount, edge_weight_key=edge_weight_key, do_weight_update=do_weight_update )
            nn+=iin
            ne+=iie
    if verbose: print "Inclusive/Sumrule data: added %i nodes and %i edges" % (nn,ne) 
              
@timeit
def _add_special_quants_clusters( theGraph, maxCount=None, edge_weight_key='weight_specialquant', do_weight_update=True, verbose=False ):    
    '''
    Unpacks (==expands a reaction into a cluster) quantities 'ETA', 'ALF' and 'RI', using their definitions.
    Specifically, 
    
        * ETA = $\bar{\nu}\sigma_f/(\sigma_\gamma/+\sigma_f)$
        * ALF = $\sigma_\gamma/\sigma_f$ or $\sigma_\gamma/\sigma_{abs}$
        * RI = $\int_0^\infty dE \sigma(E)/E$
    '''
    nn=0
    ne=0
    for o in theGraph.get_matching_quantities( 'ETA' ):
        if "(N,F)" in o['name']: 
            oo=o['name'].replace('ETA', 'SIG')
            iin,iie = theGraph.add_connected_cluster( \
                [ o['name'], o['name'].replace('ETA', 'NU' ), oo, oo.replace('N,F', 'N,G') ], cluster_name=o, \
                    maxCount=maxCount, edge_weight_key=edge_weight_key, do_weight_update=do_weight_update )
            nn+=iin
            ne+=iie
    for o in theGraph.get_matching_quantities( 'ALF' ):
        if "(N,G)" in o['name']: 
            oo=o['name'].replace('ALF', 'SIG' )
            iin,iie = theGraph.add_connected_cluster( \
                [ o['name'], oo, oo.replace('(N,G)', '(N,F)') ], cluster_name=o, \
                    maxCount=maxCount, edge_weight_key=edge_weight_key, do_weight_update=do_weight_update )
            nn+=iin
            ne+=iie
        if "(N,ABS)" in o['name']:
            oo=o['name'].replace('ALF', 'SIG')
            iin,iie = theGraph.add_connected_cluster( \
                [ o['name'], oo, oo.replace('(N,ABS)', '(N,F)'), oo.replace('(N,ABS)', '(N,G)') ], cluster_name=o, \
                    maxCount=maxCount, edge_weight_key=edge_weight_key, do_weight_update=do_weight_update )
            nn+=iin
            ne+=iie
    for o in theGraph.get_matching_quantities( 'RI' ) :
        if "(N,G)" in o['name'] or "N,F)" in o['name'] or "(N,TOT)" in o['name'] or "(N,EL)" in o['name']: 
            iin,iie = theGraph.add_connected_cluster( \
                [ o['name'], o['name'].replace('RI', 'SIG' ) ], cluster_name=o['name'], \
                    maxCount=maxCount, edge_weight_key=edge_weight_key, do_weight_update=do_weight_update )
            nn+=iin
            ne+=iie
    if verbose: print "Special quantities data: added %i nodes and %i edges" % (nn,ne) 
 
@timeit
def _add_elemental_clusters( theGraph, maxCount=None, edge_weight_key='weight_element', do_weight_update=True, verbose=False ): 
    '''
    Unpacks (==expands a reaction into a cluster) a reaction on an elemental target into reactions 
    on the isotopic targets composing the element.
    '''
    nn=0
    ne=0
    for o in theGraph.get_elemental_targets() :
        isotope_list= get_isotopes_from_element( o['target'] )
        iin,iie = theGraph.add_connected_cluster( \
            [ o['name'] ] + [ o['name'].replace( o['target'], i ) for i in isotope_list ], cluster_name=o['name'], \
                maxCount=maxCount, edge_weight_key=edge_weight_key, do_weight_update=do_weight_update )
        nn+=iin
        ne+=iie
    if verbose: print "Elemental data: added %i nodes and %i edges" % (nn,ne) 
        
@timeit
def _add_CIELO_clusters( theGraph, maxCount=None, edge_weight_key='weight_cielo', do_weight_update=True, verbose=False ): 
    '''
    Add connections between any two neutron incident reactions on isotopes that are part of the CIELO set.
    Note: This only works on EXISTING nodes, so no new nodes will be added here, just edges.  
          We rely on the graph.add_connected_cluster()'s updating logic here.
    '''
    nn=0
    ne=0
    cielo_nodes=[ n['name'] for n in theGraph.get_nodes() if n['is_cielo_projectile_target'] ]
    for targ in cieloIsotopes:
        iin,iie = theGraph.add_connected_cluster( \
            [ x for x in cielo_nodes if x.startswith(targ) ], cluster_name=targ, \
                maxCount=maxCount, edge_weight_key=edge_weight_key, do_weight_update=do_weight_update )
        nn+=iin
        ne+=iie
    if verbose: print "CIELO data: added %i nodes and %i edges" % (nn,ne) 

@timeit
def add_rest_of_clusters( theGraph, \
    addInclusiveClusters=True, addSpecialQuantsClusters=True, addElementalClusters=True, addCIELOClusters=True, \
    maxCount=None, do_weight_update=True, verbose=False ):

    if addInclusiveClusters: 
        _add_inclusive_clusters( theGraph, maxCount, do_weight_update=do_weight_update, verbose=verbose )

    if addSpecialQuantsClusters: 
        _add_special_quants_clusters( theGraph, maxCount, do_weight_update=do_weight_update, verbose=verbose )

    if addElementalClusters: 
        _add_elemental_clusters( theGraph, maxCount, do_weight_update=do_weight_update, verbose=verbose )

    if addSpecialQuantsClusters and addElementalClusters:
        # need second call to one with newly added guys, 
        # setting edge_weight_key to None turns off double weighting of edges.
        _add_special_quants_clusters( theGraph, maxCount, edge_weight_key=None, do_weight_update=do_weight_update, verbose=verbose ) 

    if addCIELOClusters:            
        _add_CIELO_clusters( theGraph, maxCount, do_weight_update=do_weight_update, verbose=verbose )

# -----------------------------------------------------------------------
#    Main routine
# -----------------------------------------------------------------------

if __name__ == "__main__":
    import unittest


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
       
        def test_num_nodes( self ):
            self.graph.add_nodes( [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', 'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', 'U-235(N,F)SIG', 'AU-197(N,G)SIG' ] )
            self.assertEqual( self.graph.num_nodes(), 10 )
        
        def test_add_node( self ):
            self.assertIsNotNone( self.graph.add_node( 'B-10(N,A+G)SIG' ) )
        
        def test_add_nodes( self ):
            self.assertEqual( self.graph.add_nodes( [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', 'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', 'U-235(N,F)SIG', 'AU-197(N,G)SIG' ] ), 10 )
         
        def test_has_node( self ): 
            self.graph.add_nodes( [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', 'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', 'U-235(N,F)SIG', 'AU-197(N,G)SIG' ] )
            self.assertTrue( self.graph.has_node( 'C-0(N,EL)SIG' ) )
        
        def test___contains__( self ): 
            self.graph.add_nodes( [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', 'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', 'U-235(N,F)SIG', 'AU-197(N,G)SIG' ] )
            self.assertTrue( 'C-0(N,EL)SIG' in self.graph )
       
        def test_update_node_weight( self ): 
            self.graph.add_nodes( [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', 'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', 'U-235(N,F)SIG', 'AU-197(N,G)SIG' ] )
            self.graph.update_node_weight( 'U-238(N,F)SIG', 13 ) 
            self.assertEqual( self.graph.get_node_weight( 'U-238(N,F)SIG' ), 14 )
        
        def test_get_node_weight( self ): 
            self.graph.add_nodes( [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', 'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', 'U-235(N,F)SIG', 'AU-197(N,G)SIG' ] )
            self.assertEqual( self.graph.get_node_weight( 'U-238(N,F)SIG' ), 1 )
        
        def test_get_node( self ): 
            self.graph.add_nodes( [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', 'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', 'U-235(N,F)SIG', 'AU-197(N,G)SIG' ] )
            self.assertEqual( str( self.graph.get_node( 'H-1(N,EL)SIG' )['name'] ), 'H-1(N,EL)SIG' )
            self.assertEqual( self.graph.get_node( 'H-1(N,EL)SIG' )['target'],  'H-1' )
            self.assertEqual( self.graph.get_node( 'H-1(N,EL)SIG' )['observable'],  'SIG' )
            self.assertEqual( self.graph.get_node( 'H-1(N,EL)SIG' )['reaction'],  '(N,EL)' )
            self.assertEqual( self.graph.get_node( 'H-1(N,EL)SIG' )['weight'], 1 )

        def test_get_nodes( self ): 
            self.graph.add_connected_cluster( 
                [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', \
                    'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', \
                    'U-235(N,F)SIG', 'AU-197(N,G)SIG' ], \
                cluster_name='Neutron Standards', maxCount=None )
            self.assertEqual( set([ x['name'] for x in self.graph.get_nodes() ]), \
                set([ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', \
                    'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', \
                    'U-235(N,F)SIG', 'AU-197(N,G)SIG' ]) )
        
        def test_get_node_attribute( self ):  
            self.graph.add_connected_cluster( 
                [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', \
                    'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', \
                    'U-235(N,F)SIG', 'AU-197(N,G)SIG' ], \
                cluster_name='Neutron Standards', maxCount=None )
            self.graph.set_node_attribute( 'AU-197(N,G)SIG', 'weight', 14 )
            self.assertEqual( self.graph.get_node_attribute( 'AU-197(N,G)SIG', 'weight' ), 14 )
        
        def test_set_node_attribute( self ):
            self.graph.add_connected_cluster( 
                [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', \
                    'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', \
                    'U-235(N,F)SIG', 'AU-197(N,G)SIG' ], \
                cluster_name='Neutron Standards', maxCount=None )
            self.graph.set_node_attribute( 'AU-197(N,G)SIG', 'weight', 14 )
            self.assertEqual( self.graph.get_node_attribute( 'AU-197(N,G)SIG', 'weight' ), 14 )

        # ------------ edges ------------ 
    
        def test_num_edges( self ):
            self.graph.add_nodes( [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', 'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', 'U-235(N,F)SIG', 'AU-197(N,G)SIG' ] )
            self.graph.add_edge( 'B-10(N,A+G)SIG', 'U-238(N,F)SIG' )
            self.graph.add_edge( 'B-10(N,A+G)SIG', 'AU-197(N,G)SIG' )
            self.assertEqual( self.graph.num_edges(), 2 )
    
        def test_add_edge( self ):
            self.graph.add_nodes( [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', 'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', 'U-235(N,F)SIG', 'AU-197(N,G)SIG' ] )
            self.graph.add_edge( 'B-10(N,A+G)SIG', 'U-238(N,F)SIG' )
            self.graph.add_edge( 'B-10(N,A+G)SIG', 'AU-197(N,G)SIG' )
            self.assertEqual( self.graph.num_edges(), 2 )
      
        def test_has_edge( self ): 
            self.graph.add_nodes( [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', 'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', 'U-235(N,F)SIG', 'AU-197(N,G)SIG' ] )
            self.graph.add_edge( 'B-10(N,A+G)SIG', 'U-238(N,F)SIG' )
            self.graph.add_edge( 'B-10(N,A+G)SIG', 'AU-197(N,G)SIG' )
            self.assertTrue( self.graph.has_edge('B-10(N,A+G)SIG', 'AU-197(N,G)SIG') )
            self.assertTrue( self.graph.has_edge('AU-197(N,G)SIG', 'B-10(N,A+G)SIG' ) )
            self.assertFalse( self.graph.has_edge('B-10(N,A+G)SIG', 'C-0(N,EL)SIG',) )
      
        def test_update_edge_weight( self ): 
            self.graph.add_nodes( [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', 'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', 'U-235(N,F)SIG', 'AU-197(N,G)SIG' ] )
            self.graph.add_edge( 'B-10(N,A+G)SIG', 'U-238(N,F)SIG' )
            self.graph.add_edge( 'B-10(N,A+G)SIG', 'AU-197(N,G)SIG' )
            self.graph.update_edge_weight( 'B-10(N,A+G)SIG', 'AU-197(N,G)SIG', 'weight_neutron_standard', 2 )
            self.graph.update_edge_weight( 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'weight_neutron_standard', 50 )
            self.assertEqual( self.graph.get_edge_weight( 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'weight_neutron_standard' ), 50 )
     
        def test_get_edge_weight( self ): 
            self.graph.add_nodes( [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', 'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', 'U-235(N,F)SIG', 'AU-197(N,G)SIG' ] )
            self.graph.add_edge( 'B-10(N,A+G)SIG', 'U-238(N,F)SIG' )
            self.graph.add_edge( 'B-10(N,A+G)SIG', 'AU-197(N,G)SIG' )
            self.graph.update_edge_weight( 'B-10(N,A+G)SIG', 'AU-197(N,G)SIG', 'weight_neutron_standard', 2 )
            self.graph.update_edge_weight( 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'weight_neutron_standard', 50 )
            self.assertEqual( self.graph.get_edge_weight( 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'weight_neutron_standard' ), 50 )
            self.assertEqual( self.graph.get_edge_weight( 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'weight_cielo' ), 0 )
            self.assertEqual( self.graph.get_edge_weight( 'B-10(N,A+G)SIG', 'AU-197(N,G)SIG', 'weight_neutron_standard' ), 2 )
        
        def test_get_edge( self ): 
            self.graph.add_nodes( [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', 'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', 'U-235(N,F)SIG', 'AU-197(N,G)SIG' ] )
            self.graph.add_edge( 'B-10(N,A+G)SIG', 'U-238(N,F)SIG' )
            self.graph.add_edge( 'B-10(N,A+G)SIG', 'AU-197(N,G)SIG' )
            e = self.graph.get_edge( 'B-10(N,A+G)SIG', 'U-238(N,F)SIG' )
            self.assertEqual( ( e['node0_name'], e['node1_name'] ), ('B-10(N,A+G)SIG', 'U-238(N,F)SIG') )

        def test_get_edges( self ): 
            self.graph.add_connected_cluster( 
                [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', \
                    'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', \
                    'U-235(N,F)SIG', 'AU-197(N,G)SIG' ], \
                cluster_name='Neutron Standards', maxCount=None )
            self.assertEqual( set( [ ( x['node0_name'], x['node1_name'] ) for x in self.graph.get_edges() ] ), \
                set( [ ('B-10(N,A)SIG', 'H-1(N,EL)SIG'), \
                    ('HE-3(N,P)SIG', 'AU-197(N,G)SIG'), \
                    ('B-10(N,A+G)SIG', 'AU-197(N,G)SIG'), \
                    ('C-0(N,EL)SIG', 'HE-3(N,P)SIG'), \
                    ('C-0(N,EL)SIG', 'U-235(N,F)SIG'), \
                    ('B-10(N,A+G)SIG', 'B-10(N,A+G)PAR,SIG'), \
                    ('LI-6(N,T)SIG', 'U-235(N,F)SIG'), \
                    ('H-1(N,EL)SIG', 'AU-197(N,G)SIG'), \
                    ('B-10(N,A)SIG', 'AU-197(N,G)SIG'), \
                    ('C-0(N,EL)SIG', 'B-10(N,A+G)PAR,SIG'), \
                    ('U-238(N,F)SIG', 'H-1(N,EL)SIG'), \
                    ('B-10(N,A+G)SIG', 'H-1(N,EL)SIG'), \
                    ('HE-3(N,P)SIG', 'U-235(N,F)SIG'), \
                    ('U-238(N,F)SIG', 'HE-3(N,P)SIG'), \
                    ('B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG'), \
                    ('U-238(N,F)SIG', 'LI-6(N,T)SIG'), \
                    ('U-238(N,F)SIG', 'C-0(N,EL)SIG'), \
                    ('HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG'), \
                    ('LI-6(N,T)SIG', 'B-10(N,A+G)PAR,SIG'), \
                    ('B-10(N,A)SIG', 'HE-3(N,P)SIG'), \
                    ('LI-6(N,T)SIG', 'AU-197(N,G)SIG'), \
                    ('B-10(N,A+G)SIG', 'B-10(N,A)SIG'), \
                    ('B-10(N,A)SIG', 'C-0(N,EL)SIG'), \
                    ('B-10(N,A+G)SIG', 'U-238(N,F)SIG'), \
                    ('H-1(N,EL)SIG', 'U-235(N,F)SIG'), \
                    ('U-238(N,F)SIG', 'AU-197(N,G)SIG'), \
                    ('B-10(N,A)SIG', 'U-235(N,F)SIG'), \
                    ('C-0(N,EL)SIG', 'LI-6(N,T)SIG'), \
                    ('U-235(N,F)SIG', 'AU-197(N,G)SIG'), \
                    ('B-10(N,A+G)PAR,SIG', 'AU-197(N,G)SIG'), \
                    ('C-0(N,EL)SIG', 'H-1(N,EL)SIG'), \
                    ('U-238(N,F)SIG', 'B-10(N,A+G)PAR,SIG'), \
                    ('LI-6(N,T)SIG', 'HE-3(N,P)SIG'), \
                    ('LI-6(N,T)SIG', 'H-1(N,EL)SIG'), \
                    ('HE-3(N,P)SIG', 'H-1(N,EL)SIG'), \
                    ('B-10(N,A)SIG', 'B-10(N,A+G)PAR,SIG'), \
                    ('U-238(N,F)SIG', 'U-235(N,F)SIG'), \
                    ('B-10(N,A+G)SIG', 'LI-6(N,T)SIG'), \
                    ('B-10(N,A+G)SIG', 'U-235(N,F)SIG'), \
                    ('B-10(N,A+G)SIG', 'HE-3(N,P)SIG'), \
                    ('C-0(N,EL)SIG', 'AU-197(N,G)SIG'), \
                    ('B-10(N,A)SIG', 'LI-6(N,T)SIG'), \
                    ('B-10(N,A+G)SIG', 'C-0(N,EL)SIG'), \
                    ('U-238(N,F)SIG', 'B-10(N,A)SIG'), \
                    ('B-10(N,A+G)PAR,SIG', 'U-235(N,F)SIG') ] ) )

        def test_get_edge_attribute( self ):  
            self.graph.add_nodes( [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', 'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', 'U-235(N,F)SIG', 'AU-197(N,G)SIG' ] )
            self.graph.add_edge( 'B-10(N,A+G)SIG', 'U-238(N,F)SIG' )
            self.graph.add_edge( 'B-10(N,A+G)SIG', 'AU-197(N,G)SIG' )
            self.graph.set_edge_attribute( 'B-10(N,A+G)SIG', 'AU-197(N,G)SIG', 'weight_element', 4 )
            self.assertEqual( self.graph.get_edge_attribute( 'B-10(N,A+G)SIG', 'AU-197(N,G)SIG', 'weight_element' ), 4 )

        def test_set_edge_attribute( self ): 
            self.graph.add_nodes( [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', 'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', 'U-235(N,F)SIG', 'AU-197(N,G)SIG' ] )
            self.graph.add_edge( 'B-10(N,A+G)SIG', 'U-238(N,F)SIG' )
            self.graph.add_edge( 'B-10(N,A+G)SIG', 'AU-197(N,G)SIG' )
            self.graph.set_edge_attribute( 'B-10(N,A+G)SIG', 'AU-197(N,G)SIG', 'weight_element', 4 )
            self.assertEqual( self.graph.get_edge_attribute( 'B-10(N,A+G)SIG', 'AU-197(N,G)SIG', 'weight_element' ), 4 )

        # ------------ connected cluster ------------
        
        def test_add_connected_cluster( self ):
            self.graph.add_connected_cluster( 
                [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', \
                    'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', \
                    'U-235(N,F)SIG', 'AU-197(N,G)SIG' ], \
                cluster_name='Neutron Standards', maxCount=None )
            self.assertEqual( self.graph.num_edges(), 45 )
               
        # ------------ queries ------------
        
        def test_get_matching_target_projectile( self ):
            self.graph.add_connected_cluster( 
                [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', \
                    'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', \
                    'U-235(N,F)SIG', 'AU-197(N,G)SIG' , 'AU-197(A,G)SIG' ], \
                cluster_name='Junk for testing', maxCount=None )
            self.assertEqual( \
                self.graph.get_matching_target_projectile( target='AU-197', projectile='N' )[0]['name'], 'AU-197(N,G)SIG' )
            self.assertEqual( \
                self.graph.get_matching_target_projectile( target='AU-197', projectile='A' )[0]['name'], 'AU-197(A,G)SIG' )
            self.assertEqual( \
                self.graph.get_matching_target_projectile( target='LI-6', projectile='N' )[0]['name'], 'LI-6(N,T)SIG' )
        
        def test_get_elemental_targets( self ):
            self.graph.add_connected_cluster( 
                [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', \
                    'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', \
                    'U-235(N,F)SIG', 'AU-197(N,G)SIG' ], \
                cluster_name='Neutron Standards', maxCount=None )
            self.assertEqual( [ x['name'] for x in self.graph.get_elemental_targets() ], ['C-0(N,EL)SIG'] )

        def test_get_matching_processes( self ):
            self.graph.add_connected_cluster( 
                [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', \
                    'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', \
                    'U-235(N,F)SIG', 'AU-197(N,G)SIG' ], \
                cluster_name='Neutron Standards', maxCount=None )
            self.assertEqual( [x['name'] for x in self.graph.get_matching_processes( 'A+G' ) ], \
                ['B-10(N,A+G)SIG', 'B-10(N,A+G)PAR,SIG'] )
 
        def test_get_matching_quantities( self ):
            self.graph.add_connected_cluster( 
                [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', \
                    'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', \
                    'U-235(N,F)SIG', 'AU-197(N,G)SIG' ], \
                cluster_name='Neutron Standards', maxCount=None )
            self.assertItemsEqual( [ x['name'] for x in self.graph.get_matching_quantities( 'SIG' ) ], \
                [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', \
                    'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'H-1(N,EL)SIG','U-235(N,F)SIG', 'AU-197(N,G)SIG' ] )

        # ------------ node statistics ------------
        
        def test_get_degree( self ): 
            self.graph.add_connected_cluster( 
                [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', \
                    'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', \
                    'U-235(N,F)SIG', 'AU-197(N,G)SIG' ], \
                cluster_name='Neutron Standards', maxCount=None )
            self.assertEqual( self.graph.get_degree( 'AU-197(N,G)SIG' ), 9 )
    
        # ------------ graph statistics ------------


        def test_is_connected( self ): 
            self.graph.add_connected_cluster( 
                [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', \
                    'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', \
                    'U-235(N,F)SIG', 'AU-197(N,G)SIG' ], \
                cluster_name='Neutron Standards', maxCount=None )
            self.assertEqual( self.graph.is_connected( ), True )
    
        def test_num_isolates( self ): 
            self.graph.add_connected_cluster( 
                [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', \
                    'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', \
                    'U-235(N,F)SIG', 'AU-197(N,G)SIG' ], \
                cluster_name='Neutron Standards', maxCount=None )
            self.assertEqual( self.graph.num_isolates( ), 0 )

        def test_get_connection_probability( self ): 
            self.graph.add_connected_cluster( 
                [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', \
                    'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', \
                    'U-235(N,F)SIG', 'AU-197(N,G)SIG' ], \
                cluster_name='Neutron Standards', maxCount=None )
            self.assertEqual( self.graph.get_connection_probability( ), 1.0 )

        def test_get_ave_degree( self ): 
            self.graph.add_connected_cluster( 
                [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', \
                    'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', \
                    'U-235(N,F)SIG', 'AU-197(N,G)SIG' ], \
                cluster_name='Neutron Standards', maxCount=None )
            self.assertEqual( self.graph.get_ave_degree( ), 9.0 )

        def test_get_ave_degree_sqr( self ):
            self.graph.add_connected_cluster( 
                [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', \
                    'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', \
                    'U-235(N,F)SIG', 'AU-197(N,G)SIG' ], \
                cluster_name='Neutron Standards', maxCount=None )
            self.assertEqual( self.graph.get_ave_degree_sqr( ), 90.0 ) 
    
        def test_get_diameter( self ): 
            self.graph.add_connected_cluster( 
                [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', \
                    'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', \
                    'U-235(N,F)SIG', 'AU-197(N,G)SIG' ], \
                cluster_name='Neutron Standards', maxCount=None )
            self.assertEqual( self.graph.get_diameter( ), 1 )

        @unittest.skipIf( FORCENETWORKX == False, 'coding for NetworkX only' )
        def test_get_radius( self ): 
            self.graph.add_connected_cluster( 
                [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', \
                    'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', \
                    'U-235(N,F)SIG', 'AU-197(N,G)SIG' ], \
                cluster_name='Neutron Standards', maxCount=None )
            self.assertEqual( self.graph.get_radius(), 1 )

        def test_get_distance_between_nodes( self ):
            self.graph.add_connected_cluster(
                [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', \
                    'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', \
                    'U-235(N,F)SIG', 'AU-197(N,G)SIG' ], \
                cluster_name='Neutron Standards', maxCount=None )    
            TestList = [ 'B-10(N,A+G)SIG' ]
            self.assertEqual( self.graph.get_distance_between_nodes( TargetList = TestList ), [0, 1, 1, 1, 1, 1, 1, 1, 1, 1] )
   
        def test_get_nodes_matching_CIELO( self ):
            '''
            This function can be used for the gathering the list of all CIELO nodes as tuples for use in distance functions 
            '''
            self.graph.add_connected_cluster( [ 'H-1(N,F)SIG' , 'U-238(N,F)SIG' , 'U-238(N,G)SIG', 'H-1(N,G)SIG', 'LI-6(N,A+G)SIG'], cluster_name = 'CIELO Examples' , maxCount = None )
            self.assertItemsEqual( self.graph.get_nodes_matching_CIELO( ), [ 'H-1(N,F)SIG' , 'U-238(N,F)SIG' , 'U-238(N,G)SIG', 'H-1(N,G)SIG' ])       

        def test_get_info( self ): 
            self.graph.add_connected_cluster( 
                [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', \
                    'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', \
                    'U-235(N,F)SIG', 'AU-197(N,G)SIG' ], \
                cluster_name='Neutron Standards', maxCount=None )
            self.assertEqual( self.graph.get_info(), { '# of Edges': 45, '# of Nodes': 10, '# of Isolates': 0, '<k>': 9.0, '<k^2>': 90.0, 'Probability of Connection': 1.0, 'Diameter': 1 , 'Is connected' : True})

        @unittest.skipIf(FORCENETWORKX == False,  'This function only to be used with NetworkX' )
        def test_get_closeness_centrality_nx( self ):
            self.maxDiff = None 
            self.graph.add_connected_cluster( 
                [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG' ], \
                cluster_name='Neutron Standards', maxCount=None )
            self.graph.add_connected_cluster(
                ['LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', \
                    'U-235(N,F)SIG', 'AU-197(N,G)SIG' ], \
                cluster_name='Additional Neutron Standards', maxCount = None)
            self.assertEqual( self.graph.get_closeness_centrality_nx(), {'AU-197(N,G)SIG': 0.625,'B-10(N,A)SIG': 0.25,'B-10(N,A+G)PAR,SIG': 0.625,'B-10(N,A+G)SIG': 0.25,'H-1(N,EL)SIG': 0.625,'HE-3(N,P)SIG': 0.625,'LI-6(N,T)SIG': 0.625,'U-235(N,F)SIG': 0.625,'U-238(N,F)SIG': 0.25} )
            self.assertEqual( self.graph.get_closeness_centrality_nx(Node = 'U-235(N,F)SIG'), 0.625)

        @unittest.skipIf(FORCENETWORKX == True,  'This function only to be used with Graph Tool' )
        def test_get_closeness_centrality_gt( self ):
            self.maxDiff = None 
            self.graph.add_connected_cluster( 
                [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG' ], \
                cluster_name='Neutron Standards', maxCount=None )
            self.graph.add_connected_cluster(
                ['LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', \
                    'U-235(N,F)SIG', 'AU-197(N,G)SIG' ], \
                cluster_name='Additional Neutron Standards', maxCount = None)
            self.assertEqual( self.graph.get_closeness_centrality_gt(), {'AU-197(N,G)SIG': 1.0,'B-10(N,A)SIG': 1.0,'B-10(N,A+G)PAR,SIG': 1.0,'B-10(N,A+G)SIG': 1.0,'H-1(N,EL)SIG': 1.0,'HE-3(N,P)SIG': 1.0,'LI-6(N,T)SIG': 1.0,'U-235(N,F)SIG': 1.0,'U-238(N,F)SIG': 1.0} )
            self.assertEqual( self.graph.get_closeness_centrality_gt(Node = 'U-235(N,F)SIG'), 1.0)

        def test_get_betweenness_centrality( self ): 
            self.graph.add_connected_cluster( 
                [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', \
                    'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', \
                    'U-235(N,F)SIG', 'AU-197(N,G)SIG' ], \
                cluster_name='Neutron Standards', maxCount=None )
            self.assertEqual( self.graph.get_betweenness_centrality(), {'B-10(N,A+G)SIG': 0.0, 'U-238(N,F)SIG': 0.0, 'B-10(N,A)SIG': 0.0, 'C-0(N,EL)SIG': 0.0, 'LI-6(N,T)SIG': 0.0, 'HE-3(N,P)SIG': 0.0, 'B-10(N,A+G)PAR,SIG': 0.0, 'H-1(N,EL)SIG': 0.0, 'U-235(N,F)SIG': 0.0, 'AU-197(N,G)SIG': 0.0} )
            self.assertEqual( self.graph.get_betweenness_centrality(Node = 'H-1(N,EL)SIG'), 0.0)
   
        def test_get_eigenvector_centrality( self ): 
            self.graph.add_connected_cluster( 
                [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', \
                    'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', \
                    'U-235(N,F)SIG', 'AU-197(N,G)SIG' ], \
                cluster_name='Neutron Standards', maxCount=None )
            self.assertEqual( self.graph.get_eigenvector_centrality(), {'U-238(N,F)SIG': 0.31622776601683794, 'H-1(N,EL)SIG': 0.31622776601683794, 'B-10(N,A)SIG': 0.31622776601683794, 'C-0(N,EL)SIG': 0.31622776601683794, 'LI-6(N,T)SIG': 0.31622776601683794, 'HE-3(N,P)SIG': 0.31622776601683794, 'B-10(N,A+G)PAR,SIG': 0.31622776601683794, 'B-10(N,A+G)SIG': 0.31622776601683794, 'U-235(N,F)SIG': 0.31622776601683794, 'AU-197(N,G)SIG': 0.31622776601683794} )
            self.assertEqual( self.graph.get_eigenvector_centrality(Node = 'U-238(N,F)SIG' ),0.31622776601683794)

        @unittest.skipIf(FORCENETWORKX == True,  'This function only to be used with Graph Tool' )
        def test_get_page_rank( self):
            self.graph.add_connected_cluster( 
                [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', \
                    'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', \
                    'U-235(N,F)SIG', 'AU-197(N,G)SIG' ], \
                cluster_name='Neutron Standards', maxCount=None )
            self.assertEqual( self.graph.get_page_rank(), {'U-238(N,F)SIG': 0.1, 'H-1(N,EL)SIG': 0.1, 'B-10(N,A)SIG': 0.1, 'C-0(N,EL)SIG': 0.1, 'LI-6(N,T)SIG': 0.1, 'HE-3(N,P)SIG': 0.1, 'B-10(N,A+G)PAR,SIG': 0.1, 'B-10(N,A+G)SIG': 0.1, 'U-235(N,F)SIG': 0.1, 'AU-197(N,G)SIG': 0.1} )
            self.assertEqual( self.graph.get_page_rank(Node = 'U-238(N,F)SIG' ), 0.1 )

        def test_get_clustering_coefficient( self ):
            self.graph.add_connected_cluster( 
                [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', \
                    'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', \
                    'U-235(N,F)SIG', 'AU-197(N,G)SIG' ], \
                cluster_name='Neutron Standards', maxCount=None )
            answer = {'B-10(N,A+G)SIG':1.0,'B-10(N,A+G)SIG':1.0,'B-10(N,A)SIG':1.0,'C-0(N,EL)SIG':1.0,'LI-6(N,T)SIG':1.0,'HE-3(N,P)SIG':1.0,'B-10(N,A+G)PAR,SIG':1.0,'H-1(N,EL)SIG':1.0,'U-235(N,F)SIG':1.0,'AU-197(N,G)SIG':1.0}
            result = self.graph.get_clustering_coefficients()
            result1 = self.graph.get_clustering_coefficients( Node = 'C-0(N,EL)SIG' )
            for i in answer:
                self.assertAlmostEqual(answer[i], result[i])
                self.assertAlmostEqual(answer[i], result[i])
            self.assertAlmostEqual(result1, 1.0 )
            

        def test_get_clustering_distribution( self ):
            self.graph.add_connected_cluster( 
                [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG', 'C-0(N,EL)SIG', \
                    'LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', \
                    'U-235(N,F)SIG', 'AU-197(N,G)SIG' ], \
                cluster_name='Neutron Standards', maxCount=None )
            answer = [(1.0,10)]
            result = self.graph.get_clustering_distribution()
            self.assertEqual(len(result), len(answer))
            for i in range(len(answer)):
                self.assertAlmostEqual(answer[i][0], result[i][0])
                self.assertAlmostEqual(answer[i][1], result[i][1])

        def test_get_top_N_lists( self ):
            check_list = ['betweenness', 'cluster','degree', 'eigenvalue']
            self.graph.add_connected_cluster( 
                [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG', 'B-10(N,A)SIG' ], \
                cluster_name='Neutron Standards', maxCount=None )
            self.graph.add_connected_cluster(
                ['LI-6(N,T)SIG', 'HE-3(N,P)SIG', 'B-10(N,A+G)PAR,SIG', 'H-1(N,EL)SIG', \
                    'U-235(N,F)SIG', 'AU-197(N,G)SIG' ], \
                cluster_name='Additional Neutron Standards', maxCount = None)
            self.maxDiff = None

            answer1 = [{'betweenness': 0.0,'closeness': 0.625,'cluster': 1.0000000000000002,'degree': 5,'eigenvalue': 0.40824829046384414,'is_almost_standard': 0,'is_cielo_projectile_target': 0,'is_cp_standard': 0,'is_elemental_target': 0,'is_isomer_target': 0,'is_neutron_standard': 0,'is_our_proposed_standard': 0,'is_soon_tobe_standard': 0,'name': 'LI-6(N,T)SIG','observable': 'SIG','projectile': 'N','reaction': '(N,T)','target': 'LI-6','weight': 1},{'betweenness': 0.0,'closeness': 0.625,'cluster': 1.0000000000000002,'degree': 5,'eigenvalue': 0.40824829046384414,'is_almost_standard': 0,'is_cielo_projectile_target': 0,'is_cp_standard': 0,'is_elemental_target': 0,'is_isomer_target': 0,'is_neutron_standard': 0,'is_our_proposed_standard': 0,'is_soon_tobe_standard': 0,'name': 'HE-3(N,P)SIG','observable': 'SIG','projectile': 'N','reaction': '(N,P)','target': 'HE-3','weight': 2},{'betweenness': 0.0,'closeness': 0.625,'cluster': 1.0000000000000002,'degree': 5,'eigenvalue': 0.40824829046384414,'is_almost_standard': 0,'is_cielo_projectile_target': 0,'is_cp_standard': 0,'is_elemental_target': 0,'is_isomer_target': 0,'is_neutron_standard': 0,'is_our_proposed_standard': 0,'is_soon_tobe_standard': 0,'name': 'B-10(N,A+G)PAR,SIG','observable': 'PAR,SIG','projectile': 'N','reaction': '(N,A+G)','target': 'B-10','weight': 3}]
            results1 = self.graph.get_top_N_lists(N = 3, SortBy = 'degree' )
            for i,p in enumerate(results1):
                for x in check_list:
                    self.assertAlmostEqual( results1[i][x], answer1[i][x] , 5)

            answer2 = [{'betweenness': 0.0,'closeness': .25,'cluster': 1.0,'degree': 2,'eigenvalue': 1.095883160116901e-06,'is_almost_standard': 0,'is_cielo_projectile_target': 0,'is_cp_standard': 0,'is_elemental_target': 0,'is_isomer_target': 0,'is_neutron_standard': 0,'is_our_proposed_standard': 0,'is_soon_tobe_standard': 0,'name': 'B-10(N,A+G)SIG','observable': 'SIG','projectile': 'N','reaction': '(N,A+G)','target': 'B-10','weight': 1},{'betweenness': 0.0,'closeness': .25,'cluster': 1.0,'degree': 2,'eigenvalue': 1.095883160116901e-06,'is_almost_standard': 0,'is_cielo_projectile_target': 1,'is_cp_standard': 0,'is_elemental_target': 0,'is_isomer_target': 0,'is_neutron_standard': 0,'is_our_proposed_standard': 0,'is_soon_tobe_standard': 0,'name': 'U-238(N,F)SIG','observable': 'SIG','projectile': 'N','reaction': '(N,F)','target': 'U-238','weight': 2},{'betweenness': 0.0,'closeness': .25,'cluster': 1.0,'degree': 2,'eigenvalue': 1.095883160116901e-06,'is_almost_standard': 0,'is_cielo_projectile_target': 0,'is_cp_standard': 0,'is_elemental_target': 0,'is_isomer_target': 0,'is_neutron_standard': 0,'is_our_proposed_standard': 0,'is_soon_tobe_standard': 0,'name': 'B-10(N,A)SIG','observable': 'SIG','projectile': 'N','reaction': '(N,A)','target': 'B-10','weight': 3}]
            results2 = self.graph.get_top_N_lists( N = 3, SortBy = 'betweenness' )
            for i,p in enumerate(results2):
                for x in check_list:
                    self.assertAlmostEqual( results2[i][x], answer2[i][x] ,5)
            
            '''
            answer3 = [{'is_cp_standard': False, 'reaction': '(N,T)', 'is_soon_tobe_standard': False, 'target': 'LI-6', 'weight': 1, 'observable': 'SIG', 'eigenvalue': 0.4082482904631276, 'closeness': 0.625, 'is_almost_standard': False, 'is_isomer_target': False, 'is_cielo_projectile_target': False, 'cluster': 1.0, 'betweenness': 0.0, 'is_our_proposed_standard': False, 'is_elemental_target': False, 'projectile': 'N', 'degree': 5, 'is_neutron_standard': False, 'name': 'LI-6(N,T)SIG'}, {'is_cp_standard': False, 'reaction': '(N,P)', 'is_soon_tobe_standard': False, 'target': 'HE-3', 'weight': 2, 'observable': 'SIG', 'eigenvalue': 0.4082482904631276, 'closeness': 0.625, 'is_almost_standard': False, 'is_isomer_target': False, 'is_cielo_projectile_target': False, 'cluster': 1.0, 'betweenness': 0.0, 'is_our_proposed_standard': False, 'is_elemental_target': False, 'projectile': 'N', 'degree': 5, 'is_neutron_standard': False, 'name': 'HE-3(N,P)SIG'}, {'is_cp_standard': False, 'reaction': '(N,A+G)', 'is_soon_tobe_standard': False, 'target': 'B-10', 'weight': 3, 'observable': 'PAR,SIG', 'eigenvalue': 0.4082482904631276, 'closeness': 0.625, 'is_almost_standard': False, 'is_isomer_target': False, 'is_cielo_projectile_target': False, 'cluster': 1.0, 'betweenness': 0.0, 'is_our_proposed_standard': False, 'is_elemental_target': False, 'projectile': 'N', 'degree': 5, 'is_neutron_standard': False, 'name': 'B-10(N,A+G)PAR,SIG'}, {'is_cp_standard': False, 'reaction': '(N,G)', 'is_soon_tobe_standard': False, 'target': 'AU-197', 'weight': 6, 'observable': 'SIG', 'eigenvalue': 0.4082482904631276, 'closeness': 0.625, 'is_almost_standard': False, 'is_isomer_target': False, 'is_cielo_projectile_target': False, 'cluster': 1.0, 'betweenness': 0.0, 'is_our_proposed_standard': False, 'is_elemental_target': False, 'projectile': 'N', 'degree': 5, 'is_neutron_standard': False, 'name': 'AU-197(N,G)SIG'}, {'is_cp_standard': False, 'reaction': '(N,F)', 'is_soon_tobe_standard': False, 'target': 'U-235', 'weight': 5, 'observable': 'SIG', 'eigenvalue': 0.4082482904631276, 'closeness': 0.625, 'is_almost_standard': False, 'is_isomer_target': False, 'is_cielo_projectile_target': True, 'cluster': 1.0, 'betweenness': 0.0, 'is_our_proposed_standard': False, 'is_elemental_target': False, 'projectile': 'N', 'degree': 5, 'is_neutron_standard': False, 'name': 'U-235(N,F)SIG'}, {'is_cp_standard': False, 'reaction': '(N,EL)', 'is_soon_tobe_standard': False, 'target': 'H-1', 'weight': 4, 'observable': 'SIG', 'eigenvalue': 0.4082482904631276, 'closeness': 0.625, 'is_almost_standard': False, 'is_isomer_target': False, 'is_cielo_projectile_target': True, 'cluster': 1.0, 'betweenness': 0.0, 'is_our_proposed_standard': False, 'is_elemental_target': False, 'projectile': 'N', 'degree': 5, 'is_neutron_standard': False, 'name': 'H-1(N,EL)SIG'}, {'is_cp_standard': False, 'reaction': '(N,A+G)', 'is_soon_tobe_standard': False, 'target': 'B-10', 'weight': 1, 'observable': 'SIG', 'eigenvalue': 1.095883160116901e-06, 'closeness': 0.25, 'is_almost_standard': False, 'is_isomer_target': False, 'is_cielo_projectile_target': False, 'cluster': 1.0, 'betweenness': 0.0, 'is_our_proposed_standard': False, 'is_elemental_target': False, 'projectile': 'N', 'degree': 2, 'is_neutron_standard': False, 'name': 'B-10(N,A+G)SIG'}, {'is_cp_standard': False, 'reaction': '(N,F)', 'is_soon_tobe_standard': False, 'target': 'U-238', 'weight': 2, 'observable': 'SIG', 'eigenvalue': 1.095883160116901e-06, 'closeness': 0.25, 'is_almost_standard': False, 'is_isomer_target': False, 'is_cielo_projectile_target': True, 'cluster': 1.0, 'betweenness': 0.0, 'is_our_proposed_standard': False, 'is_elemental_target': False, 'projectile': 'N', 'degree': 2, 'is_neutron_standard': False, 'name': 'U-238(N,F)SIG'}, {'is_cp_standard': False, 'reaction': '(N,A)', 'is_soon_tobe_standard': False, 'target': 'B-10', 'weight': 3, 'observable': 'SIG', 'eigenvalue': 1.095883160116901e-06, 'closeness': 0.25, 'is_almost_standard': False, 'is_isomer_target': False, 'is_cielo_projectile_target': False, 'cluster': 1.0, 'betweenness': 0.0, 'is_our_proposed_standard': False, 'is_elemental_target': False, 'projectile': 'N', 'degree': 2, 'is_neutron_standard': False, 'name': 'B-10(N,A)SIG'}]
            results3 = self.graph.get_top_N_lists( N = 9, SortBy = 'closeness')
            print results3
            for i,p in enumerate(results3):
                for x in check_list:
                    self.assertAlmostEqual( results3[i][x], answer3[i][x] ,5)

            '''

            answer4 = [{'betweenness': 0.0,'closeness': 1.0,'cluster': 1.0000000000000002,'degree': 5,'eigenvalue': 0.40824829046384414,'is_almost_standard': 0,'is_cielo_projectile_target': 0,'is_cp_standard': 0,'is_elemental_target': 0,'is_isomer_target': 0,'is_neutron_standard': 0,'is_our_proposed_standard': 0,'is_soon_tobe_standard': 0,'name': 'LI-6(N,T)SIG','observable': 'SIG','projectile': 'N','reaction': '(N,T)','target': 'LI-6','weight': 1},{'betweenness': 0.0,'closeness': 1.0,'cluster': 1.0000000000000002,'degree': 5,'eigenvalue': 0.40824829046384414,'is_almost_standard': 0,'is_cielo_projectile_target': 0,'is_cp_standard': 0,'is_elemental_target': 0,'is_isomer_target': 0,'is_neutron_standard': 0,'is_our_proposed_standard': 0,'is_soon_tobe_standard': 0,'name': 'HE-3(N,P)SIG','observable': 'SIG','projectile': 'N','reaction': '(N,P)','target': 'HE-3','weight': 2}]
            results4 = self.graph.get_top_N_lists( N = 2, SortBy = 'eigenvalue')
            for i,p in enumerate(results4):
                for x in check_list:
                    self.assertAlmostEqual( results4[i][x], answer4[i][x] , 5)

            #self.assertEqual( self.graph.get_top_N_lists( N = 2, SortBy = 'cluster'), [])

        # ------------ filtering ------------
    
        @unittest.skip( 'write me' )
        def test_filter( self, node_filter=None, edge_filter=None ):  raise NotImplementedError( "Write me" )

        @unittest.skip( 'write me' )
        def test_keep_only_cross( self ): raise NotImplementedError( "Write me" )
        
        @unittest.skip( 'write me' )
        def test_keep_only_neutron( self ):  raise NotImplementedError( "Write me" )
        
        @unittest.skip( 'write me' )
        def test_keep_only_proton( self ): raise NotImplementedError( "Write me" )
        
        @unittest.skip( 'write me' )
        def test_keep_only_deuteron( self ): raise NotImplementedError( "Write me" )
        
        @unittest.skip( 'write me' )
        def test_keep_only_alpha( self ): raise NotImplementedError( "Write me" )
        
        @unittest.skip( 'write me' )
        def test_keep_only_gamma( self ): raise NotImplementedError( "Write me" )
        
        @unittest.skip( 'write me' )
        def test_keep_only_HE3( self ): raise NotImplementedError( "Write me" )
        
        @unittest.skip( 'write me' )
        def test_keep_only_triton( self ): raise NotImplementedError( "Write me" )
        
        @unittest.skip( 'write me' )
        def test_keep_only_carbon( self ): raise NotImplementedError( "Write me" )
        
        @unittest.skip( 'write me' )
        def test_keep_only_target( self, target ): raise NotImplementedError( "Write me" )
        
        @unittest.skip( 'write me' )
        def test_keep_only_target_projectile( self, target, projectile ): raise NotImplementedError( "Write me" )
    

    class Test_Graph_Construction_Functions( unittest.TestCase ):
        def test_load_graph( self ):
            self.graph.add_connected_cluster( 
                [ 'B-10(N,A+G)SIG', 'U-238(N,F)SIG'], \
                cluster_name='Random Cluster Pair', maxCount=None )
            self.graph.save( 'testsavegraph.xml' )
            grphs = load_graph( 'testsavegraph.xml', returnBothGraphs=True )
            def smartValueSwap( d ):
                nd = {}
                for k in d:
                    if k.startswith('is'):nd[k]=bool(d[k])
                    elif k.startswith('weight'):nd[k]=d[k]
                    elif k=='id':pass
                    else: nd[k]=str(d[k])
                return nd
            for g in grphs:
                if grphs[g] == None and FORCENETWORKX: continue
                for n in map( smartValueSwap, grphs[g].get_nodes() ):
                    self.assertIn( n , 
                        [{'is_almost_standard': False,
                          'is_atlas_standard': False,
                          'is_cielo_projectile_target': True,
                          'is_cp_standard': False,
                          'is_elemental_target': False,
                          'is_isomer_target': False,
                          'is_neutron_standard': False,
                          'is_our_proposed_standard': False,
                          'is_soon_tobe_standard': False,
                          'name': 'U-238(N,F)SIG',
                          'observable': 'SIG',
                          'projectile': 'N',
                          'reaction': '(N,F)',
                          'target': 'U-238',
                          'weight': 2},
                         {'is_almost_standard': False,
                          'is_atlas_standard': False,
                          'is_cielo_projectile_target': False,
                          'is_cp_standard': False,
                          'is_elemental_target': False,
                          'is_isomer_target': False,
                          'is_neutron_standard': False,
                          'is_our_proposed_standard': False,
                          'is_soon_tobe_standard': False,
                          'name': 'B-10(N,A+G)SIG',
                          'observable': 'SIG',
                          'projectile': 'N',
                          'reaction': '(N,A+G)',
                          'target': 'B-10',
                          'weight': 1}])
                for g in map( smartValueSwap, grphs[g].get_edges() ):
                    self.assertEquals( g,
                         { 'is_same_target': False,
                           'node0_name': 'B-10(N,A+G)SIG',
                           'node1_name': 'U-238(N,F)SIG',
                           'weight_almost_standard': 0,
                           'weight_cielo': 0,
                           'weight_coupled': 0,
                           'weight_cp_standard': 0,
                           'weight_element': 0,
                           'weight_monitor': 0,
                           'weight_neutron_standard': 0,
                           'weight_soon_to_be_standard': 0,
                           'weight_specialquant': 0,
                           'weight_sumrule': 0} )
            import os
            os.remove( 'testsavegraph.xml' )
             
    
        def setUp( self ):
            self.graph = create_graph()
            self.maxDiff = None

        def test_add_neutron_standards_cluster( self ):
            add_neutron_standards_cluster( self.graph )
            self.assertTrue( self.graph.has_edge( 'B-10(N,A+G)SIG', 'U-238(N,F)SIG' ) )

        def test_add_monitor_clusters( self ): 
            add_monitor_clusters( self.graph, maxCount=10, verbose=False )
            self.assertTrue( self.graph.has_edge( 'BI-209(N,X+2-HE-4)DA/DE', 'BI-209(N,X+2-HE-3)DA/DE' ) )

        def test_add_coupled_clusters( self ):
            add_coupled_clusters( self.graph, maxCount=10, verbose=False )
            self.assertTrue( self.graph.has_edge( 'NI-58(N,G)WID', 'NI-58(N,TOT)WID' ) )
        
        def test_add_reaction_nodes( self ): 
            add_reaction_nodes( self.graph, maxCount=10, verbose=False ) 
            self.assertTrue( self.graph.has_node( 'GE-70(N,EL)SIG' ) )
        
        def test_add_expanded_neutron_standards_clusters( self ): 
            add_expanded_neutron_standards_clusters( self.graph ) 
            self.assertTrue( self.graph.has_edge( 'BI-209(N,F)SIG', 'U-238(N,F)SIG' ) )

        def test_add_CIELO_clusters( self ): 
            add_expanded_neutron_standards_clusters( self.graph )
            self.graph.add_node( 'FE-56(N,G)SIG' )
            self.graph.add_node( 'FE-56(N,2N)SIG' )
            self.graph.add_node( 'FE-56(P,A)SIG' ) 
            _add_CIELO_clusters( self.graph )
            self.assertTrue( self.graph.has_edge( 'FE-56(N,G)SIG', 'FE-56(N,2N)SIG' ) )
            self.assertFalse( self.graph.has_edge( 'FE-56(N,G)SIG', 'FE-56(P,A)SIG' ) )
            self.assertFalse( self.graph.has_edge( 'FE-56(N,G)SIG', 'U-238(N,F)SIG' ) )

        def test_add_elemental_clusters( self ):
            self.graph.add_node( 'C-0(N,TOT)SIG' )
            _add_elemental_clusters( self.graph, maxCount=None )
            self.assertItemsEqual( [x['name'] for x in self.graph.get_nodes()] , ['C-0(N,TOT)SIG', 'C-13(N,TOT)SIG','C-12(N,TOT)SIG' ])
            self.assertItemsEqual( [(x['node0_name'], x['node1_name']) for x in self.graph.get_edges()], \
                [('C-0(N,TOT)SIG', 'C-13(N,TOT)SIG'), ('C-0(N,TOT)SIG', 'C-12(N,TOT)SIG'),('C-13(N,TOT)SIG', 'C-12(N,TOT)SIG')] )

        def test_add_inclusive_clusters( self ): 
            self.graph.add_node( 'AL-26(N,SCT)SIG' )
            self.graph.add_node( 'AL-27(N,ABS)SIG' )
            self.graph.add_node( 'AL-28(N,NON)SIG' )
            _add_inclusive_clusters( self.graph, maxCount=None )
            self.assertEqual( set( [ x['name'] for x in self.graph.get_nodes() ] ), \
                set( ['AL-26(N,EL)SIG', 'AL-26(N,INL)SIG', 'AL-26(N,SCT)SIG', \
                    'AL-27(N,ABS)SIG', 'AL-27(N,INL)SIG', 'AL-27(N,TOT)SIG', \
                    'AL-27(N,EL)SIG', 'AL-27(N,SCT)SIG','AL-27(N,NON)SIG',
                    'AL-28(N,TOT)SIG', 'AL-28(N,NON)SIG', 'AL-28(N,EL)SIG'] ) )
            self.assertEqual( set( [ (x['node0_name'], x['node1_name'] ) for x in self.graph.get_edges() ] ), \
                set( [ ('AL-26(N,INL)SIG', 'AL-26(N,EL)SIG'),
                    ('AL-26(N,SCT)SIG', 'AL-26(N,EL)SIG'),\
                    ('AL-26(N,SCT)SIG', 'AL-26(N,INL)SIG'),\
                    ('AL-27(N,ABS)SIG', 'AL-27(N,TOT)SIG'),\
                    ('AL-27(N,ABS)SIG', 'AL-27(N,NON)SIG'),\
                    ('AL-27(N,ABS)SIG', 'AL-27(N,SCT)SIG'),\
                    ('AL-27(N,ABS)SIG', 'AL-27(N,INL)SIG'),\
                    ('AL-27(N,INL)SIG', 'AL-27(N,EL)SIG'),\
                    ('AL-27(N,NON)SIG', 'AL-27(N,INL)SIG'),\
                    ('AL-27(N,SCT)SIG', 'AL-27(N,INL)SIG'),\
                    ('AL-27(N,TOT)SIG', 'AL-27(N,EL)SIG'),\
                    ('AL-27(N,NON)SIG', 'AL-27(N,TOT)SIG'),\
                    ('AL-27(N,TOT)SIG', 'AL-27(N,SCT)SIG'),\
                    ('AL-27(N,NON)SIG', 'AL-27(N,EL)SIG'),\
                    ('AL-27(N,SCT)SIG', 'AL-27(N,EL)SIG'),\
                    ('AL-28(N,TOT)SIG', 'AL-28(N,EL)SIG'),\
                    ('AL-28(N,NON)SIG', 'AL-28(N,TOT)SIG'),\
                    ('AL-28(N,NON)SIG', 'AL-28(N,EL)SIG') ] ) )
             
        def test_add_special_quants_clusters( self ): 
            self.graph.add_node( 'AL-26(N,G)RI' )
            self.graph.add_node( 'U-235(N,F)ETA' )
            self.graph.add_node( 'PU-238(N,ABS)ALF' )
            _add_special_quants_clusters( self.graph, maxCount=None )   
            self.assertEqual( set( [ x['name'] for x in self.graph.get_nodes() ] ), \
                set(['PU-238(N,F)SIG', 'PU-238(N,ABS)SIG', 'AL-26(N,G)SIG', \
                    'AL-26(N,G)RI', 'U-235(N,F)ETA', 'U-235(N,G)SIG', 'U-235(N,F)NU', \
                    'PU-238(N,ABS)ALF', 'U-235(N,F)SIG', 'PU-238(N,G)SIG' ]) )
            self.assertEqual( set( [ (x['node0_name'], x['node1_name'] ) for x in self.graph.get_edges() ] ), \
                set( [ \
                    ('AL-26(N,G)RI', 'AL-26(N,G)SIG'),\
                    ('U-235(N,F)NU', 'U-235(N,G)SIG'),\
                    ('U-235(N,F)ETA', 'U-235(N,F)NU'),\
                    ('U-235(N,F)SIG', 'U-235(N,G)SIG'),\
                    ('U-235(N,F)ETA', 'U-235(N,F)SIG'),\
                    ('U-235(N,F)NU', 'U-235(N,F)SIG'),\
                    ('U-235(N,F)ETA', 'U-235(N,G)SIG'),\
                    ('PU-238(N,ABS)SIG', 'PU-238(N,F)SIG'),\
                    ('PU-238(N,ABS)SIG', 'PU-238(N,G)SIG'),\
                    ('PU-238(N,ABS)ALF', 'PU-238(N,G)SIG'),\
                    ('PU-238(N,ABS)ALF', 'PU-238(N,ABS)SIG'),\
                    ('PU-238(N,F)SIG', 'PU-238(N,G)SIG'),\
                    ('PU-238(N,ABS)ALF', 'PU-238(N,F)SIG') ] ) )
                
    unittest.main()
