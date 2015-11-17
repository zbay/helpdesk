from flask import Flask, render_template, make_response, redirect
from flask.ext.restful import Api, Resource, reqparse, abort

import json
import string
import random
from datetime import datetime

FREQUENCIES = ('daily', 'weekly', 'monthly')

# Load data from disk.
# This simply loads the data from our "database," which is just a pair of JSON files.
with open('database/archiveRules.json') as rules_data:
    rules_data = json.load(rules_data)
with open('database/archivedPages.json') as page_data:
    page_data = json.load(page_data)


# Generate a unique ID for a new help request.
# By default this will consist of six lowercase numbers and letters.
def generate_id(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# Respond with 404 Not Found if no rule with the specified ID exists.
def error_if_rule_not_found(rule_id):
    if rule_id not in rules_data['id']:
        message = "No rule with ID: {}".format(rule_id)
        abort(404, message=message)

# Respond with 404 Not Found if no page with the specified ID exists.
def error_if_page_not_found(page_id):
    if page_id not in page_data['id']:
        message = "No rule with ID: {}".format(rule_id)
        abort(404, message=message)


# Filter and sort a list of rules.
def filter_and_sort_rules(query='', sort_by='time'):

    # Returns True if the query string appears in the help request's
    # title or description.
    def matches_query(item):
        (rule_id, rule) = item
        text = rule['title'] + rule['description']
        return query.lower() in text

    # Returns the help request's value for the sort property (which by
    # default is the "time" property).
    def get_sort_value(item):
        (rule_id, rule) = item
        return rule[sort_by]

    filtered_rules = filter(matches_query, data['archivingRules'].items())

    return sorted(filtered_rules, key=get_sort_value, reverse=True)


# Given the data for a rule, generate an HTML representation
# of that help request.
def render_rule_as_html(rule):
    return null # figure out the template logic
    return render_template(
        'rule.html',
         rule=rule,
         frequencies=reversed(list(enumerate(FREQUENCIES))))


# Given the data for a list of rules, generate an HTML representation
# of that list.
def render_rule_list_as_html(rules):
    return render_template(
        'rules+microdata+rdfa.html', #make this file
        rules=rules,
        frequencies=FREQUENCIES)


# Raises an error if the string x is empty (has zero length).
def nonempty_string(x):
    s = str(x)
    if len(x) == 0:
        raise ValueError('string is empty')
    return s


# Specify the data necessary to create a new help request.
# "from", "title", and "description" are all required values.
new_rule_parser = reqparse.RequestParser()
for arg in ['url', 'frequency', 'description']: #fix the stuff in this for loop
    new_rule_parser.add_argument(
        arg, type=nonempty_string, required=True,
        help="'{}' is a required value".format(arg))


# Specify the data necessary to update an existing rule.
# Only the frequency and comments can be updated.
update_rule_parser = reqparse.RequestParser()
update_rule_parser.add_argument(
    'frequency', type=int, default=FREQUENCIES.index('daily'))
update_rule_parser.add_argument(
    'description', type=str, default='')


# Specify the parameters for filtering and sorting help requests.
# See `filter_and_sort_helprequests` above.
query_parser = reqparse.RequestParser()
query_parser.add_argument(
    'query', type=str, default='')
query_parser.add_argument(
    'sort_by', type=str, choices=('frequency', 'time'), default='time')


# Define our help request resource.
class Rule(Resource):

    # If a help request with the specified ID does not exist,
    # respond with a 404, otherwise respond with an HTML representation.
    def get(self, rule_id):
        error_if_rule_not_found(rule_id)
        return make_response(
            render_rule_as_html(
                data['archivingRules'][rule_id]), 200)

    # If a help request with the specified ID does not exist,
    # respond with a 404, otherwise update the help request and respond
    # with the updated HTML representation.
    def patch(self, rule_id):
        error_if_rule_not_found(rule_id)
        rule = data['archivingRules'][rule_id]
        update = update_rule_parser.parse_args()
        rule['frequency'] = update['frequency']
        if len(update['comment'].strip()) > 0:
           rule.setdefault('comments', []).append(update['comment'])
        return make_response(
            render_rule_as_html(rule), 200)


# Define a resource for getting a JSON representation of a help request.
class RuleAsJSON(Resource):

    # If a help request with the specified ID does not exist,
    # respond with a 404, otherwise respond with a JSON representation.
    def get(self, rule_id):
        error_if_rule_not_found(rule_id)
        rule = data['archivingRules'][rule_id]
        #helprequest['@context'] = data['@context']
        return rule


# Define our rule list resource.
class RuleList(Resource):

    # Respond with an HTML representation of the rule list, after
    # applying any filtering and sorting parameters.
    def get(self):
        query = query_parser.parse_args()
        return make_response(
            render_rule_list_as_html(
                filter_and_sort_rules(**query)), 200)

    # Add a new rule to the list, and respond with an HTML
    # representation of the updated list.
    def post(self):
        rule = new_rule_parser.parse_args()
        rule['startDate'] = datetime.isoformat(datetime.now())
        data['archivingRules'][generate_id()] = rule
        return make_response(
            render_rule_list_as_html(
                filter_and_sort_rules()), 201)


# Define a resource for getting a JSON representation of the rule list.
class RuleListAsJSON(Resource):
    def get(self):
        return data


# Assign URL paths to our resources.
app = Flask(__name__)
api = Api(app)
api.add_resource(RuleList, '/rules')
api.add_resource(RuleListAsJSON, '/database/archiveRules.json')
api.add_resource(Rule, '/rule/<string:rule_id>')
api.add_resource(RuleAsJSON, '/rule/<string:rule_id>.json')


# Redirect from the index to the list of rules.
@app.route('/')
def index():
    return redirect(api.url_for(RuleList), code=303)


# Start the server.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)
