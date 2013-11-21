graphtojson
===========

Creates D3 compatible JSON documents from a graph generated from all trees in Phylografter and the NCBI taxonomy. Designed as a piece of [Phylografter](https://github.com/OpenTreeOfLife/phylografter), but might serve other uses.


<H3><STRONG>Prerequisites:</H3></STRONG> 
In order for this script to work, you'll need to have [Graph-tool](http://graph-tool.skewed.de/) and [IVY](https://github.com/rhr/ivy) installed and working. You'll also need an active Internet connection to pull from Phylografter and access the NCBI servers to grab the latest [taxonomy](tp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/). 


<H3><STRONG>Example Use:</H3></STRONG>


1. Run fetch-taxonomy.sh to retreive the latest copy of the NCBI taxonomy.
2. Run make-taxonomy-graph.py to create a compressed GML file ncbi/ncbi.xml.gz
3. Use the query in phylografter-datalist-query.sql on your phylografter database of choice. 
      If you use phpmyadmin you can export the needed CSV file directly from the web interface.
4. Make sure the stree.csv file is in the /trees directory.
5. Run tree-cache.py to pull all the trees from phylografter and make a local repository to work with.
      This may take quite a long time since it is downloading all 6000+ trees from Phylografter. 
6. Run graph-to-json.py
      This also may take quite awhile as it has to build the visualizations for all 6k+ working trees.
7. Copy the JSON directory to your /phylografter/static/ directory.
8. That should be it, when browsing the Phylografter study viewer, if a tree has a JSON file, 
   you should see an option to view the taxonomy graph next to the tree name.

</H3></STRONG>Alternative Use:</H3></STRONG>

7. Complete steps 1 through 6 above.
8. Copy the single line of JSON for your tree file of choice. 
8. Paste the copied text into the graphtojson.html file included in the repo to display it locally replacing the line:
<pre>
var data = //PASTE JSON STRING HERE;
with
var data = YOURJSONSTRINGHERE;
</pre>
9. Open the file in a modern D3 compatible browser. [Google Chrome](http://www.google.com/chrome) works well. 
