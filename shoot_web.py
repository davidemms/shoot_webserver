from flask import Flask, url_for, render_template, request

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
            newick_str, err_string = shoot_wrapper.run_shoot_remote(seq_name, seq)
    return render_template("result.html", newick_str=newick_str, highlight=seq_name, error=err_string)

