from ivy import treegraph as tg

choice = raw_input("Build a taxonomy graph for (1)NCBI, (2)OTT or (3)BOTH:")

if choice == "1":

    ## Builds a graph with the NCBI taxonomy
    print "Loading NCBI taxonomy into graph..."
    # save the graph to a GraphML file
    g = tg.create_ncbi_taxonomy_graph(basepath='taxonomy/ncbi')
    # save the graph to a GraphML file
    g.save('taxonomy/ncbi/ncbi.xml.gz')
    print "NCBI taxonomy Graph Complete."


elif choice == "2":

    ## Builds a graph with the OTT taxonomy
    print "Loading OTT taxonomy into graph..."
    g = tg.create_opentree_taxonomy_graph(basepath='taxonomy/ott2.2')
    # save the graph to a GraphML file
    g.save('taxonomy/ott2.2/ott2.2.xml.gz')
    print "OTT taxonomy Graph Complete."

elif choice == "3":

    ## Builds a graph with the NCBI taxonomy
    print "Loading NCBI taxonomy into graph..."
    # save the graph to a GraphML file
    g = tg.create_ncbi_taxonomy_graph(basepath='taxonomy/ncbi')
    g.save('taxonomy//ncbi//ncbi.xml.gz')
    print "NCBI taxonomy Graph Complete."

    ## Builds a graph with the NCBI taxonomy
    print "Loading OTT taxonomy into graph..."
    g = tg.create_opentree_taxonomy_graph(basepath='taxonomy/ott2.2')
    # save the graph to a GraphML file
    g.save('taxonomy/ott2.2/ott2.2.xml.gz')
    print "OTT taxonomy Graph Complete."

else:

    # Catch all for an invalid menu choice
    print "Not a valid choice. Please try again"