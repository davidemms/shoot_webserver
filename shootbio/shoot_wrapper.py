import re
import sys
import json
import random
import string
import subprocess
import os

import numpy as np
import ete3


shoot_opt = "-u 2000 -l 50 -p"
db_default = "UniProt_RefProteomes_homologs"  # note, no forward slash
available_databases = [db_default, "Metazoa", "Plants", "Fungi", "BacteriaArchaea"]
web_db_urls = ["https://www.uniprot.org/uniprot/", 
               "https://www.ensembl.org/Gene/Summary?g=", 
               "https://phytozome.jgi.doe.gov/pz/portal.html#!gene?search=1&detail=1&crown&method=0&searchText=transcriptid:", 
               "https://fungi.ensembl.org/Gene/Summary?g=",
               "https://www.uniprot.org/uniprot/"]
gene_name_disallowed_chars_re = '[^A-Za-z0-9_\\-.]'
gene_name_allowed_chars_re = "^[A-Za-z0-9_\\-.]*$"


class server_config(object):
    def __init__(self):
        if not self.load_json_configuration():
            raise RuntimeError("SHOOT server configurations could not be loaded")

    def specific_config(self, i):
        i = int(i)
        shoot_db_dir = self.d_shoot[i] + "/DATA/"
        shoot_exe = self.py_exe[i] +  " " + self.d_shoot[i] + "shoot"
        helper_exe = self.py_exe[i] +  " " + self.d_shoot[i] +  "/shoot/helper_shoot.py"
        return i, shoot_db_dir, shoot_exe, helper_exe, self.py_path[i], self.ssh_user_hostname[i]

    def random_config(self):
        i = np.random.randint(len(self.py_path))
        return self.specific_config(i)

    def load_json_configuration(self):
        servers_to_use = []
        configs = dict()
        fn_config = os.environ.get('SHOOT_CONFIG')
        if fn_config is None:
            print("ERROR: please set the environment variable 'SHOOT_CONFIG' to the location of the config_shoot.json file")
            return False
        if not os.path.exists(fn_config):
            print("ERROR: SHOOT_CONFIG file does not exist: %s" % fn_config)
            return False
        with open(fn_config, 'r') as infile:
                try:
                    d = json.load(infile)
                except ValueError:
                    print(("WARNING: Incorrectly formatted configuration file %s. Cannot call shoot on external server." % fn_config))
                    print("File is not in .json format.")
                    return False
        for name, v in d.items():
            if name == "__comment": continue
            if " " in name:
                print(("WARNING: Incorrectly formatted configuration file entry: %s" % name))
                print(("No space is allowed in name: '%s'" % name))
                continue
            if name == "servers":
                servers_to_use = v
            else:
                # this is a server config
                if any(x not in v for x in ["py_path", "py_exe", "d_shoot", "ssh_user_hostname"]):
                    print(("WARNING: Incorrectly formatted configuration file entry: %s" % name))
                    print('Entries must be specified for "ssh_user_hostname", "py_path", "py_exe" and "d_shoot"')
                    return False
                configs[name] = v
        if len(servers_to_use) < 1:
            print("ERROR: No servers listed to use")
            return False
        self.py_path = []
        self.py_exe = []
        self.d_shoot = []
        self.ssh_user_hostname = []
        for s in servers_to_use:
            if s not in configs:
                print("ERROR: No config info found for server '%s'")
                return False
            self.py_path.append(configs[s]["py_path"])
            self.py_exe.append(configs[s]["py_exe"])
            self.d_shoot.append(configs[s]["d_shoot"])
            self.ssh_user_hostname.append(configs[s]["ssh_user_hostname"])
        return True

try:
    server
    q_server_loader = True
except:
    q_server_loader = False
if not q_server_loader:
    server = server_config()


def get_database(idb):
    """
    Get the name of the i-th database
    Args:
        idb - the required database (the selector in index.html should be kept in sync)
    """
    return available_databases[idb]


def get_web_url(idb):
    """
    Get the url for gene webpages of the i-th database
    Args:
        idb - the required database (the selector in index.html should be kept in sync)
    """
    return web_db_urls[idb]


def validate_data(text):
    """
    Transform data form formats other than FASTA, e.g. NCBI format. Removes whitespace
    and numbers from the sequence. Any other characters cause an error.
    Args:
        text - text from the sequence data textarea
    Returns:
        success - bool
        name - sequence name
        seq - amino acid sequence
        error - error message
    """
    error = None
    if text.startswith(">"):
        name, seq = text.split("\n", 1)
        if name.startswith(">"):
            name = name[1:]
        name = name.rstrip()
        seq = seq.rstrip()
        # clean up name
        # print("-" + name + "-")
        # print("-" + seq + "-")
        name = re.sub(gene_name_disallowed_chars_re, '_', name)
        if name == "":
            name = "QUERY_GENE"
    else:
        name = "QUERY_GENE"
        seq = text
    # clean up sequence formatting, e.g.  NCBI: remove whitespaces and numbers
    seq = re.sub("[\d\s]", "", seq).upper()
    name = name[:75]
    seq = seq.split(">")[0] # only use first sequence
    seq = ''.join(seq.split()) # squeeze to a single string
    # check protein sequence
    bad_chars = re.sub('[a-zA-Z\-]', "", seq)
    # eat our own dog food for the valid_gene_name function. It must work here!
    if len(bad_chars) > 0 or not valid_gene_name(name):
        error = "Error, bad characters in sequence data: %s" % bad_chars
        return False, "", None, error
    return True, name, seq, error
   

def get_lines(text, n=60):
    """Split text onto lines of no more that n characters long
    """
    lines = []
    while len(text) > 0:
        if len(text) > n:
            # split at no more than 60
            iEnd = n
            while iEnd > 0 and text[iEnd] != " ": iEnd-=1
            if iEnd == 0:
                # there was nowhere to split it at a blank, just have to split at 60
                lines.append(text[:n])
                text = text[n:]
            else:
                # split at blank
                lines.append(text[:iEnd])
                text = text[iEnd+1:]  # skip blank
        else:
            lines.append(text)
            text = ""
    return lines   


def run_shoot_local(name, seq):
    err_string = ""
    newick_str = "()myroot"
    letters = string.ascii_lowercase
    fn_seq = "/tmp/shoot_%s.fa" % ''.join(random.choice(letters) for i in range(16))
    with open(fn_seq, 'w') as outfile:
        outfile.write(">%s\n" % name)
        outfile.write("\n".join(get_lines(seq)) + "\n")
    sys.path.append("/home/emms/workspace/git/shoot_prototype")
    import shoot
    fn_tree = shoot.main("/data/SHOOT/Results_Mar16/", fn_seq, True)
    with open(fn_tree, 'r') as infile:
        newick_str = next(infile).strip()
        newick_str = newick_str[:-1] # remove semi-colon
    # newick_str = "((%s:1.0,a:1.0):1.0,(b:1.0,c:1.0):1.0)" % name
    return newick_str, err_string


def run_shoot_remote(server_id, submission_id, name, seq, db_name, i_dmnd_sens=0, i_dmnd_profiles=0, i_mafft_opts=0):
    """
    Args:
        name - gene name
        seq - gene seqeunce
        db_name - SHOOT DB
        i_dmnd_sens - 0: default SHOOT sensitivity for DIAMOND search
        i_dmnd_profiles - 0: default SHOOT profiles database
        i_mafft_opts - 0: default SHOOT MAFFT options (i.e. accelerated)
    Returns:
        newick_str
        err_string
        submission_id
        iog_str
    
    Implementation:
    There are some limits to how long the ssh command can be. Probably safe with 
    1MB ~ 1 million characters
    
    String escaping:
    We need to command to look like this:
    ssh user@hostname r'echo ">name\nAFASA\nasfdsf" > file.txt'
    The commands below prepare that
    The file contents need to be prepared as a raw string:
    y = r'>name\nAFASA\nasfdsf'
    then the command is constructed like this:
    "string in triple quotes" % y
    """
    server_id, shoot_db_dir, shoot_exe, helper_exe, py_path, ssh_user_hostname = server.specific_config(server_id)
    err_string = ""
    name = name[:100]
    seq = seq[:100000]
    fn_seq = "/tmp/shoot_%s.fa" % submission_id
    fasta_lines = [">" + name,] + get_lines(seq)
    fasta_conts = r"\n".join(fasta_lines) + r"\n"
    db = shoot_db_dir + db_name + "/"
    global shoot_opt
    if i_dmnd_sens != 0:
        shoot_opt += " --high_sens"
    if i_dmnd_profiles != 0:
        shoot_opt += " --profiles_all"
    if i_mafft_opts != 0:
        shoot_opt += " --mafft_defaults"
    cmd = """ssh %s 'echo -en "%s" > %s ; export PYTHONPATH=%s ; %s %s %s %s'""" % (
        ssh_user_hostname, 
        fasta_conts, 
        fn_seq, 
        py_path, 
        shoot_exe,
        fn_seq, 
        db,
        shoot_opt)
    # print(cmd)
    with open(fn_seq + ".started", 'w') as outfile:
        pass
    try:
        capture = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout = [x for x in capture.stdout]
        stderr = [x for x in capture.stderr]
        try:
            stdout = [x.decode() for x in stdout]
            stderr = [x.decode() for x in stderr]
        except (UnicodeDecodeError, AttributeError):
            stdout = [x.encode() for x in stdout]
            stderr = [x.encode() for x in stderr]
        capture.communicate()
        rc = capture.returncode
    finally:
        with open(fn_seq + ".finished", 'w') as outfile:
            pass
    # print(output)
    # print(rc)
    # print(stderr)
    # print(stdout)
    iog_str = "-1"
    for l in stdout:
        if l.startswith("WARNING: "):
            err_string = l.rstrip()
        if l.startswith("Gene assigned to: "):
            iog_str = l.split(": ", 1)[1].rstrip()[2:]   # clip off the 'OG'
    try:
        newick_str = stdout[-1].rstrip()
        t = ete3.Tree(newick_str)
        newick_str = newick_str[:-1] # remove semi-colon
    except Exception as e:
        print(str(e))
        err_string = "No homologs were found for the gene in this database"
        newick_str = "()myroot"
    return newick_str, err_string, submission_id, iog_str
    
    
def exists(submission_id):
    fn = "/tmp/shoot_%s.fa.started" % submission_id
    return os.path.exists(fn)


def is_complete(submission_id):
    fn = "/tmp/shoot_%s.fa.finished" % submission_id
    return os.path.exists(fn)


def mark_complete(submission_id):
    # useful if local apache files have been deleted but remote files still exist
    for x in ["started", "finished"]:
        with open("/tmp/shoot_%s.fa.%s" % (submission_id, x), 'w') as outfile:
            pass
 
 
def remote_file_exists(fn, server_id):
    _, _, _, _, _, ssh_user_hostname = server.specific_config(server_id)
    cmd='ssh -q {} [[ -f {} ]] && echo "Exists" || echo "Does not";'.format(ssh_user_hostname, fn)
    capture = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    stdout = next(capture.stdout, b"")
    if isinstance(stdout, bytes):
        stdout = stdout.decode()
    return stdout.startswith("Exists")
    
 
def exists_and_complete_remote_check(submission_id):
    server_id = int(submission_id[0]) 
    fn_in = "/tmp/shoot_%s.fa" % submission_id
    fn_complete = fn_in + ".sh.log"
    exists = remote_file_exists(fn_in, server_id)
    complete = remote_file_exists(fn_complete, server_id)
    return exists, complete 


def get_result(submission_id):
    fn = "/tmp/shoot_%s.fa.shoot.tre" % submission_id
    server_id = int(submission_id[0])
    _, _, _, _, _, ssh_user_hostname = server.specific_config(server_id)
    cmd = """ssh %s 'cat %s'""" % (ssh_user_hostname, fn)
    capture = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = [x for x in capture.stdout]
    stderr = [x for x in capture.stderr]
    try:
        stdout = [x.decode() for x in stdout]
        stderr = [x.decode() for x in stderr]
    except (UnicodeDecodeError, AttributeError):
        stdout = [x.encode() for x in stdout]
        stderr = [x.encode() for x in stderr]
    capture.communicate()
    rc = capture.returncode    
    err_string = ""
    # for l in stdout:
    #    if l.startswith("WARNING: "):
    #        err_string = l.rstrip()
    success = False
    db_url = ""
    gene_name = ""
    try:
        dbname, _, gene_name = get_dbname_ogpart_gene(submission_id)
        db_url = web_db_urls[available_databases.index(dbname)]
        newick_str = stdout[-1].rstrip()
        t = ete3.Tree(newick_str)
        newick_str = newick_str[:-1] # remove semi-colon
        success = True
    except Exception as e:
        print(str(e))
        err_string = "No homologs were found for the gene in this database"
        newick_str = "()r"
    return success, newick_str, gene_name, db_url, err_string


def get_dbname_ogpart_gene(submission_id):
    fn = "/tmp/shoot_%s.fa.assign.txt" % submission_id
    server_id = int(submission_id[0])
    _, _, _, _, _, ssh_user_hostname = server.specific_config(server_id)
    cmd = """ssh %s 'cat %s'""" % (ssh_user_hostname, fn)
    capture = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = [x for x in capture.stdout]
    stderr = [x for x in capture.stderr]
    try:
        stdout = [x.decode() for x in stdout]
        stderr = [x.decode() for x in stderr]
    except (UnicodeDecodeError, AttributeError):
        stdout = [x.encode() for x in stdout]
        stderr = [x.encode() for x in stderr]
    capture.communicate()
    if len(stdout) > 2:
        db_name = stdout[0].rstrip()
        iog_str = stdout[1].rstrip()
        gene_name = stdout[2].rstrip()
    else: 
        db_name = "None"
        iog_str = "-1"
        gene_name = "query"
    return db_name, iog_str, gene_name
    
    
def valid_iog_format(iog_str):
    """
    Is the iog_str in the valid format (doesn't check if it exists))
    Args:
        iog_str - str representing the iog integer
    Returns:
        True is valid, otherwise False
    """
    try:
        if "." in iog_str:
            sp = iog_str.split(".")
            if len(sp) != 2:
                return False
            iog_str = sp[0]
            ipart_str = sp[1]
            if not ipart_str.isdigit():
                return False
            ipart = int(ipart_str)
            if ipart < 0:
                return False
        if len(iog_str) != 7:
            return False
        if not iog_str.isdigit():
            return False
        iog = int(iog_str)
        if iog < 0:
            return False
        return True
    except:
        return False


def valid_subid_format(subid):
    """
    Is the subid in the valid format (doesn't check if it exists)
    Args:
        subid - str: user submission ID
    Returns:
        True is valid, otherwise False
    """
    try:
        try:
            i = int(subid[0])
        except:
            return False
        return subid[1:].isalpha()
    except:
        return False


def valid_gene_name(gene_name):
    """
    Is the gene_name valid
    Args:
        gene_name - gene name
    Returns:
        True is valid, otherwise False
    """
    try:
        return bool(re.match(gene_name_allowed_chars_re, gene_name))
    except:
        return False


def create_fasta_file(subid, i_level=None):
    """
    Create the FASTA file of sequences for a user's results
    Args:
        i_level - the number of nodes above the query gene to the clade of interest
        subid - the id of their sequence submission
    Returns:
        fn - the full path filename for the file to download
    """
    return_fn = None
    gene_name = "query"
    try:
        # create the file on the compute server
        # copy it to here
        # return the filename to download
        db_name, iog_ipart_str, gene_name = get_dbname_ogpart_gene(subid)
        if "." in iog_ipart_str:
            iog_str = iog_ipart_str.split(".")[0]
        else:
            iog_str = iog_ipart_str
        server_id = subid[0]
        server_id, shoot_db_dir, shoot_exe, helper_exe, py_path, ssh_user_hostname = server.specific_config(server_id)
        db_path = shoot_db_dir + db_name + "/"
        filename = "/tmp/shoot_%s.tre_seqs.fa" % subid
        if gene_name is not None and i_level is not None:
            fn_og_seqs = "%s/Orthogroup_Sequences/OG%s.fa" % (db_path, iog_str)
            fn_tree = "/tmp/shoot_%s.fa.shoot.tre" % subid
            # cmd: write_fasta infasta intree seq level
            cmd_select_genes = "%s write_fasta %s %s %s %d"  % (helper_exe, fn_og_seqs, fn_tree, gene_name, i_level)
        else:
            # just get all the sequences
            cmd_select_genes = """cat %s/Orthogroup_Sequences/OG%s.fa""" % (db_path, iog_str)
        cmd = """ssh %s 'cat /tmp/shoot_%s.fa ; %s '""" % (ssh_user_hostname, subid, cmd_select_genes)
        # print(cmd)
        with open(filename, 'w') as outfile:
            capture = subprocess.Popen(cmd, shell=True, stdout=outfile, stderr=subprocess.PIPE)
            stderr = [x for x in capture.stderr]
            try:
                stderr = [x.decode() for x in stderr]
            except (UnicodeDecodeError, AttributeError):
                stderr = [x.encode() for x in stderr]
        if any("No such file or directory" in l for l in stderr):
            return return_fn, gene_name
        return_fn = filename
    except Exception as e:
        print(str(e))
    return return_fn, gene_name

