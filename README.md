# Example webserver for SHOOT.bio - the phylogenetic search engine
SHOOT is a phylogenetic alternative to BLAST. Instead of returning a list of similar sequences to a query sequence it returns a maximum likelihood phylogenetic tree with your query sequence embedded in it. This repository contains an example webserver than can be adapted for use as required.

## Preparing a SHOOT phylogenetic database
Before following the steps for preparing a SHOOT database you will first need to ensure your input proteomes are in the correct format to be properly handled by the webserver's tree viewer:

See: https://github.com/davidemms/SHOOT#preparing-a-shoot-phylogenetic-database

### Database requirements:
- Each species should be descirbed by a binomial (genus_species) with one undescore separating the two words
- In order to enable hyperlinks from the genes on the gene tree to an online page describing the gene:
    - The gene named can contain multiple underscores
    - The first word of the gene name (up to the first underscore) should be the ID used to access its page on the relevant genome resource. E.g. For uniprot genes a suitable gene name would be Q93YU5_SEC8, since the first word can be used to create the valid url: https://www.uniprot.org/uniprot/Q93YU5.

## Server configuration
The website is run using python flask. It has the following python dependencies: flask ete3 six numpy biopython.

In this example webserver there is a server that hosts the website and a compute server than holds the SHOOT databases and performs the calculations. The webserver communicates with the compute server via ssh. You will need to edit the file `shootbio/config_shoot.example.json` to provide the information on the address for the server.
* py_path - the PYTHONPATH environment variable for the libraries required by the shoot command line tool
* py_exe - the full path to the python executable
* d_shoot - the directory containing the shoot databases. Each database specified by the variable `available_databases` should have a matching directory with the same name within the d_shoot directory.
With this configuration you will need to setup ssh keys for the user account that runs your webserver so that it can communicate with the compute server over ssh.


## Running the webserver
You can run a test webserver using flask:
* Export the environment variable `SHOOT_CONFIG` specifying the path to the config_shoot.json file, e.g. `export SHOOT_CONFIG=/home/emms/git/shoot_webserver/shootbio/config_shoot.json`
* export FLASK_APP=shootbio.shoot_web
* flask run

Flask’s built-in server is not suitable for production, the flask project page contains suggested options: https://flask.palletsprojects.com/en/2.0.x/deploying/index.html

## Tree visualisation
The tree visualisation on the SHOOT website is provided by phylotree.js, thanks to the developers of that for a great tool. The citation is:

Shank, S., Weaver, S. & Kosakovsky Pond, S. phylotree.js - a JavaScript library for application development and interactive data visualization in phylogenetics. BMC Bioinformatics 19, 276 (2018). https://doi.org/10.1186/s12859-018-2283-2

I've made some alterations to their code to adjust the functionality for SHOOT. If you see any bugs in the visualisation they are almost certainly due to my ham-fisted alterations rather than the original authors, so please report any issues here.
