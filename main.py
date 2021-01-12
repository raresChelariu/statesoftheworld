import flask
from flask import request, jsonify
import json

import dbinit
from wikicrawling import WikiCrawler

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    routes = ('/', '/countries/all', '/countries/?id=Spain', '/gettopten/?column=population',
              '/getallmatching/?column=language&info=english')
    route_html_list = [f'<li><a href=\'{link}\'>{link}</a></li>' for link in routes]

    return f'''<h1>Country API Home Page</h1>
<p>A prototype API for discovering facts about countries.</p>
<h1>Routes</h1>
<ul>
    {''.join(route_html_list)}
</ul>
'''


@app.route('/gettopten/', methods=['GET'])
def get_top_ten():
    if 'column' in request.args:
        column = request.args['column']
    else:
        return "Error: No column field provided. Please specify a column."
    result = dbinit.top_10(column)
    return jsonify(result)


@app.route('/getallmatching/', methods=['GET'])
def get_all_matching():
    if 'column' in request.args:
        column = request.args['column']
    else:
        return "Error: No column field provided. Please specify a column."
    if 'info' in request.args:
        info = request.args['info']
    else:
        return "Error: No info field provided. Please specify a info."

    result = dbinit.all_match_info(column, info)
    return jsonify(result)


@app.route('/countries/all', methods=['GET'])
def api_all():
    return jsonify(WikiCrawler.get_link_for_every_countries())


@app.route('/countries/', methods=['GET'])
def api_by_id():
    if 'id' in request.args:
        country_name = request.args['id']
    else:
        return "Error: No id field provided. Please specify an id."
    # print(WikiCrawler.get_info_all_by_id(country_name))
    return json.dumps(WikiCrawler.get_info_all_by_id(country_name))


app.run()
