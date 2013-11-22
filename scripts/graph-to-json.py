import sys
import os
import requests
import pickle
import ivy
from ivy import treegraph as tg
import graph_tool.all as gt
import time
import csv

errorstring = ""
color20 = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
           '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
           '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5',
           '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5']



def build_json(choice):


    
    if choice == "1":
        ## Loads a graph with the OTT taxonomy
        taxonomy="ott"
        print "Loading OTT taxonomy into graph..."
        g = tg.load_taxonomy_graph('taxonomy/ott2.2/ott2.2.xml.gz')
        print "OTT taxonomy Graph loaded successfully."
        print "Loading ott-treecache file..."
        datafile = open('trees/ott-treecache-test.txt', 'r') #read in the treecache file
        print "Loaded."

    elif choice == "2":
        taxonomy="ncbi"
        print "Loading NCBI taxonomy into graph..."
        g = tg.load_taxonomy_graph('taxonomy/ncbi/ncbi.xml.gz')
        print "NCBI taxonomy Graph loaded successfully."
        print "Loading ncbi-treecache file..."
        datafile = open('trees/ncbi-treecache-test.txt', 'r') #read in the treecache file
        print "Loaded."
    
    data = []
    errors = []
    blacklist = []

    ## Loop all of the entries in the treecache.txt file and assign them to data.
    for row in datafile:
        data.append(row)
        #print row


    ## Creates a Tree Blacklist that will ignore problematic trees that cause crashes based on strange formatting issues until then can be resolved.   
    print "Loading tree blacklist..."
    tree_blacklist = open('trees/tree_blacklist.txt', 'r') #read in the tree blacklist file
    print "Loaded."

    ## Loop all of the entries in the tree_blacklist.txt file and assign them to blacklist.
    for tree in tree_blacklist:
        blacklist.append(tree.strip())

    rowcount = 0

    for row in data: #iterate through each unique stree id in the file allowing the code below to generate the graph, write the JSON and save the file

        active_tree = row.split(":") #split the row from treecache into tree id and newick string tree
        
        if active_tree[0] in blacklist: ## if a tree is in the blacklist, ignore it.
            print ("Tree %s is being ignored as it is black listed." % active_tree[0])
            
        else:
            stree = int(active_tree[0]) # convert tree id string into int
            r = ivy.tree.read(active_tree[1].replace("?", "")) #read the tree, also replacing an extraneous ? characters
            leafcount = 0
            r.ladderize()
            ivy.tree.index(r)
            for n in r:
                if n.isleaf:
                    leafcount = leafcount + 1
                    v = n.label.split('_')
                    n.snode_id = int(v[0])
                    n.taxid = int(v[1]) if (len(v)>1 and
                                            v[1] and v[1] != 'None') else None
                else:
                    n.snode_id = int(n.label)
            if leafcount <= 5000: #check to prune trees that have more than 5000 leaves. They will not display correctly in graph form.
                try: #used to catch all errors from incorrectly formatted trees (ie: ? characters, and other issues)

                    r.stree = stree
                    ### ADD CODE HERE TO SKIP TREES WITH MORE THAN 5000 leaves
                    tg.map_stree(g, r)
                    taxids = set()
                    for lf in r.leaves():
                        taxids.update(lf.taxid_rootpath)
                    taxg = tg.taxid_new_subgraph(g, taxids)
                    # taxg is a new graph containing only the taxids in stree

                    # these properties will store the vertices and edges that are traced
                    # by r
                    verts = taxg.new_vertex_property('bool')
                    edges = taxg.new_edge_property('bool')

                    # add stree's nodes and branches into taxonomy graph
                    tg.merge_stree(taxg, r, stree, verts, edges)
                    # verts and edges now filter the paths traced by r in taxg

                    # next, add taxonomy edges to taxg connecting 'incertae sedis'
                    # leaves in stree to their containing taxa
                    for lf in r.leaves():
                        if lf.taxid and lf.incertae_sedis:
                            taxv = taxg.taxid_vertex[lf.taxid]
                            ev = taxg.edge(taxv, lf.v, True)
                            if ev:
                                assert len(ev)==1
                                e = ev[0]
                            else:
                                e = taxg.add_edge(taxv, lf.v)
                            taxg.edge_in_taxonomy[e] = 1

                    # make a view of taxg that keeps only the vertices and edges traced by
                    # the source tree
                    gv = tg.graph_view(taxg, vfilt=verts, efilt=edges)
                    gv.vertex_strees = taxg.vertex_strees
                    gv.edge_strees = taxg.edge_strees
                    # the following code sets up the visualization
                    ecolor = taxg.new_edge_property('string')
                    for e in taxg.edges():
                        est = taxg.edge_strees[e]
                        eit = taxg.edge_in_taxonomy[e]
                        if len(est) and not eit: ecolor[e] = 'blue'
                        elif len(est) and eit: ecolor[e] = 'green'
                        else: ecolor[e] = 'yellow'

                    ewidth = taxg.new_edge_property('int')
                    for e in taxg.edges():
                        est = taxg.edge_strees[e]
                        if len(est): ewidth[e] = 3
                        else: ewidth[e] = 1

                    vcolor = taxg.new_vertex_property('string')
                    for v in taxg.vertices():
                        if not taxg.vertex_in_taxonomy[v]: vcolor[v] = 'blue'
                        else: vcolor[v] = 'green'

                    vsize = taxg.new_vertex_property('int')
                    for v in taxg.vertices():
                        if taxg.vertex_in_taxonomy[v] or v.out_degree()==0:
                            vsize[v] = 8
                        else: vsize[v] = 2

                    pos, pin = tg.layout(taxg, gv, gv.root, sfdp=True, deg0=195.0,
                                         degspan=150.0, radius=400) 

                    for v in gv.vertices(): pin[v] = 1

                    for e in taxg.edges():
                        src = e.source()
                        tgt = e.target()
                        if not verts[src]:
                            verts[src] = 1
                            pos[src] = [0.0, 0.0]
                            vcolor[src] = 'red'
                        if not verts[tgt]:
                            verts[tgt] = 1
                            pos[tgt] = [0.0, 0.0]
                            vcolor[tgt] = 'red'
                        if not edges[e]:
                            edges[e] = 1
                            ecolor[e] = 'red'
                            ewidth[e] = 1.0
                            gv.wt[e] = 1.0

                    pos = gt.sfdp_layout(gv, pos=pos, pin=pin, eweight=gv.wt, multilevel=False)
                    ### Use function in TreeGraph.py to parse Graph(gv) into JSON
                    print "Generating JSON..."
                    result = tg.graph_json(gv, pos=pos, ecolor=ecolor, ewidth=ewidth, vcolor=vcolor, vsize=vsize)
                    result = result[1:] #strip the original { from the json so we can insert the time stamp
                    date = time.strftime("%Y%m%d%I%M%S") # grab the system date for the filename and convert it to a string
                    treeid = str(stree) # convert stree int into a string
                    timestamp = "{\"timestamp\": \"%s\", " %date
                    final_result = timestamp+result # add date to first line of json file for later parsing
                    path = str(os.path.dirname(os.path.realpath(__file__)))
                    path = path[:-8]
                    path = "%s//%s/" % (path, taxonomy) # build the full path to write the file too
                    filename = "%stree_%s.JSON" % (path, treeid)  # build the full file_name for writing
                    if not os.path.exists(path): ## if directory doesn't exist, create it.
                        os.makedirs(path)
                    
                    f = open(filename, 'w')
                    f.write(final_result)
                    f.close
                    print "Done."
                    rowcount = rowcount + 1

                except: # catch *all* exceptions
                    e = sys.exc_info()[0]
                    e = str(e)
                    treeid = str(stree)
                    print ("Error: %s</p>" % e)
                    errorstring = "Error: " + e + " on Tree: " + treeid # rough hack to store trees with errors and the general error
                    errors.append(errorstring) # store all of the error strings
                    rowcount = rowcount + 1
                    continue ## continue converting the rest of the trees into JSON even if a specific tree has errors
            else:
                print "Tree has more than 5000 leaves. No graph will be generated."

    print "JSON Generation Complete."    
    ## write the error strings to a log file for review later

    if errors:
        with open("error_log.txt", "w+") as error_log:
            pickle.dump(errors, error_log)




## Ask for choice

choice = raw_input("Build JSON files for (1)OTT Taxonomy or (2)NCBI Taxonomy:")

## Build the JSONS for the OTT Taxonomy

if choice == "1":

  build_json(choice)

## Build the JSONS for the NCBI Taxonomy

elif choice == "2":

    build_json(choice)
  
else:

    print "Invalid choice. Please try again."

