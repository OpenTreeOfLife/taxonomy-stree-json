import sys
import requests
import ivy
import time
import csv
import os



## METHOD TO FETCH TREES FROM PHYLOGRAFTER

def fetch_stree(stree_id, taxid_field):
    print 'fetching stree', stree_id, '...',
    u = 'http://reelab.net/phylografter/stree/newick.txt/%s' % stree_id
    lfmt='snode.id,ottol_name.{},otu.label'.format(taxid_field)
    p = dict(lfmt=lfmt, ifmt='snode.id')
    resp = requests.get(u, params=p)
    newick = tree + ":" + resp.content
    return newick

## METHOD TO FETCH TREES FROM PHYLOGRAFTER

choice = raw_input("Generate an a Tree Cache for (1)OTT or (2)NCBI:")

if choice == "1":

    datafile = open('trees/stree.csv', 'r') #read in the stree.csv file
    datareader = csv.reader(datafile) # process the csv file into a list of 2 element lists
    data = []
    treelist = []
    errors = []
    rowcount = 0
    count = 0

    for row in datareader:
        data.append(row)

    for row in data:
        stree = data[rowcount][1]
        treelist.append(stree)
        rowcount += 1

    print ("A total of %s trees included." % rowcount)

    ### Cache all the trees in a file to reduce server requests and streamline the workflow ###

    taxid_field = 'accepted_uid' # OTT taxon id
    print "Set to work with OTT taxa labels:"

    ## Check if the tree file exists
    try:
        with open('trees/ott-treecache.txt'):

            filecreation = os.path.getmtime('trees/ott-treecache.txt')
            now = time.time()
            week_ago = now - 60*60*24*3 # Number of seconds in three days
            
            if week_ago >= filecreation: #Check if the file is more than 3 days old
                print "Tree cache is more than three days old. Generating a fresh cache now..."
                
                f = open('trees/ott-treecache.txt', 'r+')

                for tree in treelist: ## If tree cache is more than 3 days old, automatically update the file.
                    newick = fetch_stree(tree, taxid_field)
                    f.write(newick)
                    print "Tree " + str(count) + " out of " + str(rowcount) + " trees successfully updated."
                    count += 1
                print ("Tree cache successuflly updated with %s new trees" % count)
            
            else:
                
                print "Tree cache is less than three days old." ## If tree cache is less than 3 days old, ask user if they want to update it anyway.
                
                Choice = raw_input("Do you still want to generate a new cache? (Yes / No):")
                
                if Choice == "Yes":
                    
                    f = open('trees/ott-treecache.txt', 'r+')

                    for tree in treelist:
                        newick = fetch_stree(tree, taxid_field)
                        f.write(newick)
                        print "Tree " + str(count) + " out of " + str(rowcount) + " trees successfully updated."
                        count += 1
                    
                    print ("Tree Cache successuflly updated with %s new trees." % count)
                    f.close()       
                
                elif Choice == "No":
                    print "Tree cache left alone."

                else:
                    print "Invalid choice, Tree cache left alone."
    
    ### If no tree cache is found, automatically generate a new one.
    except IOError:
        print "No tree cache found. Generating a new tree cache now..."
        
        # Generate Tree Cache file code here

        f = open('trees/ott-treecache.txt', 'wr+')

        for tree in treelist:
            
            newick = fetch_stree(tree, taxid_field)
            f.write(newick)
            
            print "Tree " + str(count) + " out of " + str(rowcount) + " trees successfully cached."
            count += 1
        
        f.close()    
        
        print ("Tree cache successfully generated with %s trees." % count)
        


elif choice == "2":


    datafile = open('trees/stree.csv', 'r') #read in the stree.csv file
    datareader = csv.reader(datafile) # process the csv file into a list of 2 element lists
    data = []
    treelist = []
    errors = []
    rowcount = 0
    count = 0

    for row in datareader:
        data.append(row)

    for row in data:
        stree = data[rowcount][1]
        treelist.append(stree)
        rowcount += 1

    print ("A total of %s trees included." % rowcount)

    ### Cache all the trees in a file to reduce server requests and streamline the workflow ###

    taxid_field = 'ncbi_taxid' # NCBI taxon id
    
    print "Set to work with NCBI taxa labels:"
    ## Check if the tree file exists
    try:
        with open('trees/ncbi-treecache.txt'):

            filecreation = os.path.getmtime('ncbi-treecache.txt')
            now = time.time()
            week_ago = now - 60*60*24*3 # Number of seconds in three days
            
            if week_ago >= filecreation: #Check if the file is more than 3 days old
                print "Tree cache is more than three days old. Generating a fresh cache now..."
                
                f = open('trees/ncbi-treecache.txt', 'r+')

                for tree in treelist: ## If tree cache is more than 3 days old, automatically update the file.
                    newick = fetch_stree(tree, taxid_field)
                    f.write(newick)
                    print "Tree " + str(count) + " out of " + str(rowcount) + " trees successfully updated."
                    count += 1
                print ("Tree cache successuflly updated with %s new trees" % count)
            else:
                
                print "Tree cache is less than three days old." ## If tree cache is less than 3 days old, ask user if they want to update it anyway.
                
                Choice = raw_input("Do you still want to generate a new cache? (Yes / No):")
                
                if Choice == "Yes":
                    
                    f = open('trees/ncbi-treecache.txt', 'r+')

                    for tree in treelist:
                        newick = fetch_stree(tree, taxid_field)
                        f.write(newick)
                        print "Tree " + str(count) + " out of " + str(rowcount) + " trees successfully updated."
                        count += 1
                    
                    print ("Tree Cache successuflly updated with %s new trees." % count)
                    f.close()       
                
                elif Choice == "No":
                    print "Tree cache left alone."

                else:
                    print "Invalid choice, Tree cache left alone."
    
    ### If no tree cache is found, automatically generate a new one.
    except IOError:
        print "No tree cache found. Generating a new tree cache now..."
        
        # Generate Tree Cache file code here

        f = open('trees/ncbi-treecache.txt', 'wr+')

        for tree in treelist:
            
            newick = fetch_stree(tree, taxid_field)
            f.write(newick)
            
            print "Tree " + str(count) + " out of " + str(rowcount) + " trees successfully cached."
            count += 1
        
        f.close()    
        
        print ("Tree cache successfully generated with %s trees." % count)


else:
    print "Not a valid choice. Please try again."