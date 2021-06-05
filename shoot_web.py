from flask import Flask, url_for, render_template, request

app = Flask(__name__)

import re
import sys
import random
import string
# import subprocess

def validate_data(text):
    error = None
    if text.startswith(">"):
        name, seq = text.split("\n", 1)
        # clean up name
        name = re.sub('[^a-zA-Z0-9\./-]', '_', name)
    else:
        name = "query_gene"
        seq = text
    seq = seq.split(">")[0] # only use first sequence
    seq = ''.join(seq.split()) # squeeze to a single string
    # check protein sequence
    bad_chars = re.sub('[a-zA-Z\-]', "", seq)
    if len(bad_chars) > 0:
        error = "Error, bad characters in sequence data ---%s---" % bad_chars
        return False, None, None, error
    return True, name, seq, error
    
def flow_text(text, n=60):
    """Split text onto lines of no more that n characters long
    """
    lines = ""
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

def run_shoot(name, seq):
    newick_str = "((Still:0.150276,not:0.213019):0.230956,(quite:0.263487,successful:0.202633):0.2)myroot"
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
    return newick_str

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/result', methods=['POST', ])
def result():
    error = None
    newick_str = "((Data:0.150276,Was:0.213019):0.230956,(Not:0.263487,Correct:0.202633):0.2)myroot"
    seq_name = ""
    if request.method == 'POST':
        newick_str = "((Data:0.150276,Was:0.213019):0.230956,(Posted:0.263487,Yes:0.202633):0.2)myroot"
        submitted_data = request.form["seq_data"]
        newick_str = newick_str.replace("Data", submitted_data[1:5])
        success, seq_name, seq, error = validate_data(submitted_data)
        if success:
            newick_str = run_shoot(seq_name, seq)
    return render_template("result.html", newick_str=newick_str, highlight=seq_name, error=error)

