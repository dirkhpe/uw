from gui.lib import elastic
from flask import flash, render_template
from . import main


el = elastic.Elastic()


@main.route('/')
@main.route('/index')
def index():
    return render_template("index.html")


@main.route('/indices')
def indices():
    res = el.get_indices()
    flash("Ready to show indices", "info")
    return render_template("indices.html", reslist=res.json())
