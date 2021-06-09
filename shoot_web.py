from flask import Flask, url_for, render_template, request, send_file
from flask.helpers import make_response

import shoot_wrapper

app = Flask(__name__)

default_newick_str = "()myroot"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/result', methods=['POST', ])
def result():
    error = None
    newick_str = default_newick_str
    seq_name = ""
    if request.method == 'POST':
        submitted_data = request.form["seq_data"]
        success, seq_name, seq, err_string = shoot_wrapper.validate_data(submitted_data)
        if success:
            newick_str, err_string, submission_id, iog_str = shoot_wrapper.run_shoot_remote(seq_name, seq)
        else:
            newick_str = "()myroot"
            err_string = "ERROR: Submitted sequence was invalid"
            submission_id = "0"*16
            iog_str = "-1"
    resp = make_response(render_template("result.html", 
                                    newick_str=newick_str, 
                                    query_gene_name=seq_name, 
                                    error=err_string))
    atr_samesite = 'Strict'
    resp.set_cookie('iog', iog_str, samesite=atr_samesite)
    resp.set_cookie('db', "Results_Mar16", samesite=atr_samesite)
    resp.set_cookie('subid', submission_id, samesite=atr_samesite)
    resp.set_cookie('name', seq_name, samesite=atr_samesite)
    return resp

@app.route('/result2')
def result_test():
    newick_str="((a,b),(c,d))"
    seq_name = "a"
    err_string = ""
    iog_str = "-1"
    resp = make_response(render_template("result.html", 
                                newick_str=newick_str, 
                                query_gene_name=seq_name, 
                                error=err_string))
    atr_samesite = 'Strict'
    resp.set_cookie('iog', iog_str, samesite=atr_samesite)
    resp.set_cookie('db', "Results_Mar16", samesite=atr_samesite)
    resp.set_cookie('subid', "a"*16, samesite=atr_samesite)
    resp.set_cookie('QUERY_GENE', seq_name, samesite=atr_samesite)
    return resp

@app.route('/download_fasta')
def download_sequences():
    try:
        err_string = "Data is no longer available, please resubmit your search"
        fn = None
        download_name = None

        iog = request.cookies.get('iog')
        db = request.cookies.get('db')
        subid = request.cookies.get('subid')
        gene_name = request.cookies.get('name')
        if db not in shoot_wrapper.available_databases:
            err_string = "Unrecognised SHOOT database"
        elif not shoot_wrapper.valid_iog_format(iog):
            err_string = "Unrecognised tree"
        elif not shoot_wrapper.valid_subid_format(subid):
            err_string = "Data is no longer available, please resubmit your search"
        elif not shoot_wrapper.valid_gene_name(gene_name):
            err_string = "Invalid gene name"
        else:
            fn = shoot_wrapper.create_fasta_file(db, iog, subid)
            download_name = "shoot_tree_%s_sequences.fa" % gene_name
        if fn is None:
            resp = make_response(render_template("result.html", 
                            newick_str=default_newick_str, 
                            query_gene_name="", 
                            error=err_string))
            return resp
        else:
            return send_file(fn, download_name=download_name)
    except Exception as e:
        return str(e)

