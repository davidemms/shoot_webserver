from flask import Flask, url_for, render_template, request

import shoot_wrapper

app = Flask(__name__)



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
        success, seq_name, seq, error = shoot_wrapper.validate_data(submitted_data)
        if success:
            newick_str = shoot_wrapper.run_shoot(seq_name, seq)
    return render_template("result.html", newick_str=newick_str, highlight=seq_name, error=error)

