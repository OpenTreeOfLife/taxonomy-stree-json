graphtojson
===========

Creates D3 compatible JSON documents from a graph generated from all trees in Phylografter and the NCBI and OTT taxonomies. Designed as a piece of [Phylografter](https://github.com/OpenTreeOfLife/phylografter), but might serve other uses, and can be used locally.


<H3><STRONG>Prerequisites:</H3></STRONG> 
In order for this script to work, you'll need to have [Graph-tool](http://graph-tool.skewed.de/) and [IVY](https://github.com/rhr/ivy) installed and working. You'll also need an active Internet connection to pull from Phylografter and access the [NCBI](ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/) and [OTT](http://files.opentreeoflife.org/ott/) servers. 


<H3><STRONG>Example Use:</H3></STRONG>


1. Run `sh fetch-(ncbi/ott)-taxonomy.sh` to retreive the latest copy of your preffered taxonomy.
2. Run `python make-taxonomy-graph.py` to create a compressed GML of the taxonomy in /taxonomy.
3. Use the query in phylografter-datalist-query.sql on your phylografter database of choice. 
      If you use [phpmyadmin](http://www.phpmyadmin.net/home_page/index.php) you can export the needed CSV file directly from the web interface.
4. Save the stree.csv file in the /trees directory.
5. Run `python tree-cache.py` to pull all the trees from phylografter and make a local repository to work with.
      This may take quite a long time since it is downloading all 6000+ trees from Phylografter. It is done as a separate, single step in order to reduce queries to the Phylografter server.
6. Run `python graph-to-json.py`
      This also may take quite awhile as it has to build the visualizations for all 6k+ working trees.
7. Copy the JSON directory to your /phylografter/static/ directory.
8. That should be it, when browsing the Phylografter study viewer, if a tree has a JSON file, 
   you should see an option to view the taxonomy graph next to the tree name.

<H3><STRONG>Alternative Use:</H3></STRONG>

7. Complete steps 1 through 6 above.
8. Copy the single line of JSON for your tree file of choice. 
8. Paste the copied text into the static-graph.html file included in the repo to display it locally replacing the line:
<pre>
var data = //PASTE JSON STRING HERE;
with
var data = YOURJSONSTRINGHERE;
</pre>
9. Open the file in a modern D3 compatible browser. [Google Chrome](http://www.google.com/chrome) works well. 
