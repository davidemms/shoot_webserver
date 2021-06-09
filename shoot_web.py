from flask import Flask, url_for, render_template, request
from flask.helpers import make_response

import shoot_wrapper

app = Flask(__name__)



@app.route('/')
def index():
    return render_template("index.html")

@app.route('/result', methods=['POST', ])
def result():
    error = None
    newick_str = "()1.0:myroot"
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
    resp.set_cookie('db', "default", samesite=atr_samesite)
    resp.set_cookie('subid', submission_id, samesite=atr_samesite)
    return resp

