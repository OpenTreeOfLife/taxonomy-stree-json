import sys
import requests
import ivy
import time
import csv
import os



datafile = open('stree.csv', 'r') #read in the stree.csv file
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

## Check if the tree file exists
try:
    with open('treecache.txt'):

        filecreation = os.path.getmtime('treecache.txt')
        now = time.time()
        week_ago = now - 60*60*24*3 # Number of seconds in three days
        
        if week_ago >= filecreation: #Check if the file is more than 3 days old
            print "Tree cache is more than three days old. Generating a fresh cache now..."
            
            f = open('treecache.txt', 'r+')

            for tree in treelist: ## If tree cache is more than 3 days old, automatically update the file.
                url = 'http://reelab.net/phylografter/stree/newick.txt/%s' % tree
                lfmt='snode.id,ottol_name.ncbi_taxid,otu.label'
                p = dict(lfmt=lfmt, ifmt='snode.id')
                resp = requests.get(url, params=p)
                newick = tree + ":" + resp.content
                f.write(newick)
                print "Tree " + str(count) + " out of " + str(rowcount) + " trees successfully updated."
                count += 1
            print ("Tree cache successuflly updated with %s new trees" % count)
        else:
            print "Tree cache is less than three days old." ## If tree cache is less than 3 days old, ask user if they want to update it anyway.
            Choice = raw_input("Do you still want to generate a new cache? (Yes / No):")
            if Choice == 'Yes':
                f = open('treecache.txt', 'r+')

                for tree in treelist:
                    url = 'http://reelab.net/phylografter/stree/newick.txt/%s' % tree
                    lfmt='snode.id,ottol_name.ncbi_taxid,otu.label'
                    p = dict(lfmt=lfmt, ifmt='snode.id')
                    resp = requests.get(url, params=p)
                    newick = tree + ":" + resp.content
                    f.write(newick)
                    print "Tree " + str(count) + " out of " + str(rowcount) + " trees successfully updated."
                    count += 1
                print ("Tree Cache successuflly updated with %s new trees." % count)
                f.close()       
            elif Choice == 'No':
                print "Tree cache left alone."

            else:
                print "Invalid choice, Tree cache left alone."
### If no tree cache is found, automatically generate a new one.
except IOError:
    print "No tree cache found. Generating a new tree cache now..."
    # Generate Tree Cache file code here

    f = open('treecache.txt', 'wr+')

    for tree in treelist:
        url = 'http://reelab.net/phylografter/stree/newick.txt/%s' % tree
        lfmt='snode.id,ottol_name.ncbi_taxid,otu.label'
        p = dict(lfmt=lfmt, ifmt='snode.id')
        resp = requests.get(url, params=p)
        newick = tree + ":" + resp.content
        f.write(newick)
        print "Tree " + str(count) + " out of " + str(rowcount) + " trees successfully cached."
        count += 1
    f.close()    
    print ("Tree cache successfully generated with %s trees." % count)

