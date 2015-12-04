Here is our final project for [INLS 620](https://aeshin.org/teaching/inls-620/2015/fa/). We were tasked with creating a basic information system, using Flask, that archives web pages.

To run it:

1. Install required dependencies:
   ```
   $ pip install -r requirements.txt
   ``` 
   [Flask](http://flask.pocoo.org/docs/0.10/installation/#installation)
   and
   [Flask-RESTful](http://flask-restful.readthedocs.org/en/latest/installation.html) to run `server.py`.

2. Run the webarchive server:
   ```
   $ python server.py
   ```
   
Readme requirements:
1. The attribute values used to describe our application flow
   Cut and paste from Wanchun's.
2. The types and properties used to describe our data:
   A. Metadata for the archived pages and the archiving criteria are stored in .json files in the "database" folder.
   B. Pages (under the page.html template) and rules (under the rule.html template) are described with HTML microdata. ADD      DETAILS ONCE ALEX IS DONE.
   
