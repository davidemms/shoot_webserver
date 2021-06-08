import re
import sys
import ete3
import random
import string
import subprocess

py_path = ":".join(["/lv01/home/emms/anaconda3/lib/python3.6/site-packages"])

shoot_exe = "/lv01/home/emms/anaconda3/bin/python3 /lv01/data/emms/shoot/shoot_prototype/shoot.py"
shoot_db = "/lv01/data/emms/shoot/DATA/Results_Mar16/"
shoot_opt = "-m -p"

def validate_data(text):
    error = None
    if text.startswith(">"):
        name, seq = text.split("\n", 1)
        if name.startswith(">"):
            name = name[1:]
        name = name.rstrip()
        seq = seq.rstrip()
        # clean up name
        print("-" + name + "-")
        print("-" + seq + "-")
        name = re.sub('[^a-zA-Z0-9\.-]', '_', name)
    else:
        name = "QUERY_GENE"
        seq = text
    seq = seq.split(">")[0] # only use first sequence
    seq = ''.join(seq.split()) # squeeze to a single string
    # check protein sequence
    bad_chars = re.sub('[a-zA-Z\-]', "", seq)
    if len(bad_chars) > 0:
        error = "Error, bad characters in sequence data: %s" % bad_chars
        return False, None, None, error
    return True, name, seq, error
   
def flow_text(text, n=60):
    """Split text onto lines of no more that n characters long
    """
    lines = r""
    while len(text) > 0:
        if len(lines) > 0: lines += "\n"
        if len(text) > n:
            # split at no more than 60
            iEnd = n
            while iEnd > 0 and text[iEnd] != " ": iEnd-=1
            if iEnd == 0:
                # there was nowhere to split it at a blank, just have to split at 60
                lines += text[:n]
                text = text[n:]
            else:
                # split at blank
                lines += text[:iEnd]
                text = text[iEnd+1:]  # skip blank
        else:
            lines += text
            text = ""
    return lines    

def flow_text_raw_string(text, n=60):
    """Split text onto lines of no more that n characters long
    """
    lines = r""
    while len(text) > 0:
        if len(lines) > 0: lines += r"\n"
        if len(text) > n:
            # split at no more than 60
            iEnd = n
            while iEnd > 0 and text[iEnd] != " ": iEnd-=1
            if iEnd == 0:
                # there was nowhere to split it at a blank, just have to split at 60
                lines += text[:n]
                text = text[n:]
            else:
                # split at blank
                lines += text[:iEnd]
                text = text[iEnd+1:]  # skip blank
        else:
            lines += text
            text = ""
    return lines   


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
        outfile.write(flow_text(seq))
    sys.path.append("/home/emms/workspace/git/shoot_prototype")
    import shoot
    fn_tree = shoot.main("/data/SHOOT/Results_Mar16/", fn_seq, True)
    with open(fn_tree, 'r') as infile:
        newick_str = next(infile).strip()
        newick_str = newick_str[:-1] # remove semi-colon
    # newick_str = "((%s:1.0,a:1.0):1.0,(b:1.0,c:1.0):1.0)" % name
    return newick_str, err_string

def run_shoot_remote(name, seq):
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
    letters = string.ascii_lowercase
    fn_seq = "/tmp/shoot_%s.fa" % ''.join(random.choice(letters) for i in range(16))
    fasta_lines = [">" + name,] + get_lines(seq)
    fasta_conts = r"\n".join(fasta_lines)
    cmd = """ssh emms@dps008.plants.ox.ac.uk 'echo -en "%s" > %s ; export PYTHONPATH=%s ; %s %s %s %s'""" % (fasta_conts, fn_seq, py_path, shoot_exe, fn_seq, shoot_db, shoot_opt)
    print(cmd)
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
    # print(err)
    # print(stdout)
    try:
        newick_str = stdout[-1].rstrip()
        t = ete3.Tree(newick_str)
        newick_str = newick_str[:-1] # remove semi-colon
    except Exception as e:
        print(str(e))
        err_string = "No hit was found"
        newick_str = "()myroot"
    return newick_str, err_string