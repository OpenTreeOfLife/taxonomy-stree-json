<h2>taxonomy-stree-json</h2>
===================

JSON files for visualizing source trees aligned to taxonomies in [Phylografter](https://github.com/OpenTreeOfLife/phylografter).


<H3><STRONG>Example Setup 1:</H3></STRONG>

Quick and easy method to grab the JSON files and put them into the correct location with Git.

1. Download the taxonomy-stree-json project. The easiest way to do this is change directories to your /path/to/phylografter/static directory, and do a `git clone https://github.com/OpenTreeOfLife/taxonomy-stree-json`. This will clone the entire repository where it needs to be in Phylografter.
2. Add this directory to your .gitignore IF you are using git to manage Phylografter, so that you can manage this repo independently.

<H3><STRONG>Example Setup 2:</H3></STRONG>

This method shows how to create a sym-link in the phylografter/static directory so that you can keep the JSON files in whatever location you would like.

1. [Download](https://github.com/OpenTreeOfLife/taxonomy-stree-json/archive/master.zip) the entire repository.
2. Open up terminal: `Ctl-Alt-T`
2. Unzip the repo into a directory of your choice: `unzip taxonomy-stree-json-master.zip -d destination_folder`
3. Switch into the phylografter static directory: `cd /path/to/phylografter/static` directory.</li> 
4. Create a symbolic link to your taxonomy-stree-json directory: `ln -s /full/path/to/taxonomy-stree-json .`.


<H3><STRONG>From Scratch:</H3></STRONG>

If you prefer, you can use the pipeline in the [scripts](https://github.com/OpenTreeOfLife/taxonomy-stree-json/tree/master/scripts) folder to generate your own, more recently updated versions of the JSON files. As a warning though, generating the treecache files and the JSON documents can take quite a bit of time.  


You can also use any combination of these approaches, such as as `git clone` the repo into your home directory, and then creating the sym-link to that directory as described in Example Setup 2. Ultimately, as long as the directory is named `taxonomy-stree-json`, and it is in or linked to from the `phylografter/static` directory it should all work.  
