from flask import Flask, render_template, make_response, redirect
from flask.ext.restful import Api, Resource, reqparse, abort

import json
import string
import random
from datetime import datetime

# Define our priority levels.
# These are the values that the "priority" property can take on a help request.
FREQUENCIES = ('daily', 'weekly', 'monthly', 'hourly')

# Load data from disk.
# This simply loads the data from our "database," which is just a JSON file.
with open("database/archiveRules.json") as rules_data:
    rules_data = json.load(rules_data)
with open("database/archivedPages.json") as page_data:
    page_data = json.load(page_data)


# Generate a unique ID for a new help request.
# By default this will consist of six lowercase numbers and letters.
def generate_id(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# Respond with 404 Not Found if no help request with the specified ID exists.
def error_if_rule_not_found(rule_id):
    if rule_id not in rules_data['archivingRules']:
        message = "No rule with ID: {}".format(rule_id)
        abort(404, message=message)

def error_if_page_not_found(page_id):
    if page_id not in page_data['archivedPages']:
        message = "No page with ID: {}".format(page_id)
        abort(404, message=message)


# Filter and sort a list of helprequests.
def filter_and_sort_rules(query='', sort_by='startDate'):

    # Returns True if the query string appears in the help request's
    # title or description.
    def matches_query(item):
        (rule_id, rule) = item
        text = rule['url'] + rule['description']
        return query.lower() in text

    # Returns the help request's value for the sort property (which by
    # default is the "time" property).
    def get_sort_value(item):
        (rule_id, rule) = item
        return rule[sort_by]

    filtered_rules = filter(matches_query, rules_data['archivingRules'].items())

    return sorted(filtered_rules, key=get_sort_value, reverse=True)

def filter_and_sort_pages(query='', sort_by='date'):

    # Returns True if the query string appears in the help request's
    # title or description.
    def matches_query(item):
        (page_id, page) = item
        text = page['url'] + page['date']
        return query.lower() in text

    # Returns the help request's value for the sort property (which by
    # default is the "time" property).
    def get_sort_value(item):
        (page_id, page) = item
        return page[sort_by]

    filtered_pages = filter(matches_query, page_data['archivedPages'].items())

    return sorted(filtered_pages, key=get_sort_value, reverse=True)

# Given the data for a help request, generate an HTML representation
# of that help request.
def render_rule_as_html(rule):
    return render_template(
        'rule.html',
        rule=rule,
        frequencies=reversed(list(enumerate(FREQUENCIES))))

def render_page_as_html(page):
    return render_template(
        'page.html',
        page=page,
        frequencies=reversed(list(enumerate(FREQUENCIES))))


# Given the data for a list of help requests, generate an HTML representation
# of that list.
def render_rule_list_as_html(rules):
    return render_template(
        'rule-list.html',
        rules=rules,
        frequencies=FREQUENCIES)

def render_page_list_as_html(pages):
    return render_template('page-list.html', pages=pages)

# Raises an error if the string x is empty (has zero length).
def nonempty_string(x):
    s = str(x)
    if len(x) == 0:
        raise ValueError('string is empty')
    return s


# Specify the data necessary to create a new rule.
# "url", "frequency", "getLinks" and "description" are all required values.
new_rule_parser = reqparse.RequestParser()
for arg in ['url', 'frequency', 'getLinks', 'description']:
    new_rule_parser.add_argument(
        arg, type=nonempty_string, required=True,
        help="'{}' is a required value".format(arg))


# Specify the data necessary to update an existing help request.
# Only the priority and comments can be updated.
update_rule_parser = reqparse.RequestParser()
update_rule_parser.add_argument(
    'frequency', type=str, default='weekly')
update_rule_parser.add_argument(
    'description', type=str, default='')
update_rule_parser.add_argument(
    'getLinks', type=str, default='false')

update_page_parser = reqparse.RequestParser()
update_page_parser.add_argument('tags', type=str, default="")
update_page_parser.add_argument(
    'description', type=str, default='')


# Specify the parameters for filtering and sorting help requests.
# See `filter_and_sort_helprequests` above.
query_parser = reqparse.RequestParser()
query_parser.add_argument(
    'query', type=str, default='')
query_parser.add_argument(
    'sort_by', type=str, choices=('frequency', 'startDate'), default='startDate')

page_parser = reqparse.RequestParser()
page_parser.add_argument(
    'query', type=str, default='')
page_parser.add_argument(
    'sort_by', type=str, choices=('date'), default='date')

# Define our help request resource.
class Rule(Resource):

    # If a help request with the specified ID does not exist,
    # respond with a 404, otherwise respond with an HTML representation.
    def get(self, rule_id):
        error_if_rule_not_found(rule_id)
        return make_response(
            render_rule_as_html(
                rules_data['archivingRules'][rule_id]), 200)

    # If a help request with the specified ID does not exist,
    # respond with a 404, otherwise update the help request and respond
    # with the updated HTML representation.
    def patch(self, rule_id):
        error_if_rule_not_found(rule_id)
        rule = rules_data['archivingRules'][rule_id]
        update = update_rule_parser.parse_args()
        rule['frequency'] = update['frequency']
        rule['description'] = update['description']
        rule['getLinks'] = update['getLinks']
        return make_response(
            render_rule_as_html(rule), 200)

class Page(Resource):

    # If a help request with the specified ID does not exist,
    # respond with a 404, otherwise respond with an HTML representation.
    def get(self, page_id):
        error_if_page_not_found(page_id)
        print page_data['archivedPages'][page_id]['tags'][0]
        return make_response(
            render_page_as_html(
                page_data['archivedPages'][page_id]), 200)

    # If a help request with the specified ID does not exist,
    # respond with a 404, otherwise update the help request and respond
    # with the updated HTML representation.
    def patch(self, page_id):
        error_if_page_not_found(page_id)
        page = page_data['archivedPages'][page_id]
        update = update_page_parser.parse_args()
        if len(update['tags'].strip()) > 0:
            update['tags'] = update['tags'].split(";")
            for tag in update['tags']:
                page.setdefault('tags', []).append(tag)
        page['description'] = update['description']
        return make_response(
            render_page_as_html(page), 200)


# Define a resource for getting a JSON representation of a help request.
class RuleAsJSON(Resource):

    # If a help request with the specified ID does not exist,
    # respond with a 404, otherwise respond with a JSON representation.
    def get(self, rule_id):
        error_if_rule_not_found(rule_id)
        rule = rules_data['archivingRules'][rule_id]
        #rule['@context'] = rules_data['@context']
        return rule

class PageAsJSON(Resource):

    # If a help request with the specified ID does not exist,
    # respond with a 404, otherwise respond with a JSON representation.
    def get(self, page_id):
        error_if_page_not_found(page_id)
        page = page_data['archivedPages'][page_id]
        #page['@context'] = page_data['@context']
        return page


# Define our help request list resource.
class RuleList(Resource):

    # Respond with an HTML representation of the help request list, after
    # applying any filtering and sorting parameters.
    def get(self):
        query = query_parser.parse_args()
        return make_response(
            render_rule_list_as_html(
                filter_and_sort_rules(**query)), 200)

    # Add a new help request to the list, and respond with an HTML
    # representation of the updated list.
    def post(self):
        rule = new_rule_parser.parse_args()
        rule_id = generate_id()
        rule['@id'] = 'rule/' + rule_id
        rule['@type'] = 'helpdesk:HelpRequest'
        rule['startDate'] = datetime.isoformat(datetime.now())
        rules_data['archivingRules'][rule_id] = rule
        return make_response(
            render_rule_list_as_html(
                filter_and_sort_rules()), 201)

class PageList(Resource):
    def get(self):
        query = page_parser.parse_args()
        return make_response(render_page_list_as_html(filter_and_sort_pages(**query)), 200)


# Define a resource for getting a JSON representation of the help request list.
class RuleListAsJSON(Resource):
    def get(self):
        return rules_data

class PageListAsJSON(Resource):
    def get(self):
        return page_data


# Assign URL paths to our resources.
app = Flask(__name__)
api = Api(app)
api.add_resource(RuleList, '/rules')
api.add_resource(RuleListAsJSON, '/rules.json')
api.add_resource(Rule, '/rule/<string:rule_id>')
api.add_resource(RuleAsJSON, '/rule/<string:rule_id>.json')
api.add_resource(PageList, '/pages')
api.add_resource(PageListAsJSON, '/pages.json')
api.add_resource(Page, '/page/<string:page_id>')
api.add_resource(PageAsJSON, '/page/<string:page_id>.json')

# Redirect from the index to the list of help requests.
@app.route('/')
def index():
    return redirect(api.url_for(RuleList), code=303)


# This is needed to load JSON from Javascript running in the browser.
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response

# Start the server.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)
