import flask
from flask import request, jsonify

from wikicrawling import WikiCrawler

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    routes = ('/', '/countries/all', '/countries/?id=Spain')
    route_html_list = [f'<li><a href=\'{link}\'>{link}</a></li>' for link in routes]

    return f'''<h1>Country API Home Page</h1>
<p>A prototype API for discovering facts about countries.</p>
<h1>Routes</h1>
<ul>
    {''.join(route_html_list)}
</ul>
'''


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
    return jsonify(WikiCrawler.get_info_all_by_id(country_name))


app.run()
