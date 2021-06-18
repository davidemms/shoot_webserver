from os import POSIX_FADV_SEQUENTIAL
import re
import sys
import random
import string
import subprocess

import ete3

py_path = ":".join(["/lv01/home/emms/anaconda3/lib/python3.6/site-packages"])

shoot_exe = "/lv01/home/emms/anaconda3/bin/python3 /lv01/data/emms/SHOOT/shoot_prototype/shoot.py"
helper_exe = "/lv01/home/emms/anaconda3/bin/python3 /lv01/data/emms/SHOOT/shoot_prototype/helper_shoot.py"
shoot_db_dir = "/lv01/data/emms/SHOOT/DATA/"
shoot_opt = "-m -u 2000 -l 50 -p"
db_default = "UniProt_RefProteomes_homologs"  # note, no forward slash
available_databases = [db_default, "UniProt_RefProteomes"]
gene_name_disallowed_chars_re = '[^A-Za-z0-9_\\-.]'
gene_name_allowed_chars_re = "^[A-Za-z0-9_\\-.]*$"

def get_database(idb):
    """
    Get the name of the i-th database
    Args:
        idb - the required database (the selector in index.html should be kept in sync)
    """
    return available_databases[idb]

def validate_data(text):
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
    else:
        name = "QUERY_GENE"
        seq = text
    seq = seq.split(">")[0] # only use first sequence
    seq = ''.join(seq.split()) # squeeze to a single string
    # check protein sequence
    bad_chars = re.sub('[a-zA-Z\-]', "", seq)
    # eat our own dog food for the valid_gene_name function. It must work here!
    if len(bad_chars) > 0 or not valid_gene_name(name):
        error = "Error, bad characters in sequence data: %s" % bad_chars
        return False, None, None, error
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

def run_shoot_remote(name, seq, db_name):
    """
    There are some limits to how long the ssh command can be. Probably safe with 
    1MB ~ 1 million characters
    
    String escaping:
    We need to command to look like this:
    ssh emms@dps008.plants.ox.ac.uk r'echo ">name\nAFASA\nasfdsf" > file.txt'
    The commands below prepare that
    The file contents need to be prepared as a raw string:
    y = r'>name\nAFASA\nasfdsf'
    then the command is constructed like this:
    "string in triple quotes" % y
    """
    err_string = ""
    name = name[:100]
    seq = seq[:100000]
    submission_id = ''.join(random.choice(string.ascii_letters) for i in range(16))
    fn_seq = "/tmp/shoot_%s.fa" % submission_id
    fasta_lines = [">" + name,] + get_lines(seq)
    fasta_conts = r"\n".join(fasta_lines) + r"\n"
    db = shoot_db_dir + db_name + "/"
    cmd = """ssh emms@dps008.plants.ox.ac.uk 'echo -en "%s" > %s ; export PYTHONPATH=%s ; %s %s %s %s'""" % (fasta_conts, fn_seq, py_path, shoot_exe, fn_seq, db, shoot_opt)
    # print(cmd)
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

def valid_iog_format(iog_str):
    """
    Is the iog_str in the valid format (doesn't check if it exists))
    Args:
        iog_str - str representing the iog integer
    Returns:
        True is valid, otherwise False
    """
    try:
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
        return subid.isalpha()
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

def create_fasta_file(db, iog_str, subid, gene_name = None, i_level=None):
    """
    Create the FASTA file of sequences for a user's results
    Args:
        db - the shoot database name
        iog - the og their sequence was placed in
        i_level - the number of nodes above the query gene to the clade of interest
        subid - the id of their sequence submission
    Returns:
        fn - the full path filename for the file to download
    """
    return_fn = None
    try:
        # create the file on the compute server
        # copy it to here
        # return the filename to download
        db_path = shoot_db_dir + db + "/"
        filename = "/tmp/shoot_%s.tre_seqs.fa" % subid
        if gene_name is not None and i_level is not None:
            fn_og_seqs = "%s/Orthogroup_Sequences/OG%s.fa" % (db_path, iog_str)
            fn_tree = "/tmp/shoot_%s.fa.grafted.msa.tre" % subid
            # cmd: write_fasta infasta intree seq level
            cmd_select_genes = "%s write_fasta %s %s %s %d"  % (helper_exe, fn_og_seqs, fn_tree, gene_name, i_level)
        else:
            # just get all the sequences
            cmd_select_genes = """cat %s/Orthogroup_Sequences/OG%s.fa""" % (db_path, iog_str)
        cmd = """ssh emms@dps008.plants.ox.ac.uk 'cat /tmp/shoot_%s.fa ; %s '""" % (subid, cmd_select_genes)
        with open(filename, 'w') as outfile:
            capture = subprocess.Popen(cmd, shell=True, stdout=outfile, stderr=subprocess.PIPE)
            stderr = [x for x in capture.stderr]
            try:
                stderr = [x.decode() for x in stderr]
            except (UnicodeDecodeError, AttributeError):
                stderr = [x.encode() for x in stderr]
        if any("No such file or directory" in l for l in stderr):
            return return_fn
        return_fn = filename
    except Exception as e:
        print(str(e))
    return return_fn