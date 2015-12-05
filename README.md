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

**A. The attribute values used to describe our application flow**

class and rel attributes:

1. rule.html

   class attributes:

      (1) rule_id: Describes unique identifier for each rule

      (2) func_des: Describes the function of contents below

      (3) rule-editor: Indicates the form to edit one specific rule

      (4) rule_des: Description of one specific url

      (5) update: Indicates the function of button


   rel attributes:

      (1) alternate: alternate resource 

      (2) collection: link to a collection of rules


2. page.html

   class attributes:

      (1) page_id:Unique identifier for each archived page

      (2) func_des:Describes the function of contents below

      (3) metadata-changer: Indicates the form to change metadata-changer

      (4) url: Describes page url

      (5) date: Describes date to archive the page

      (6) rule: Describes associated rule

      (7) tag_collection: includes all tags for certain page

      (8) tag: indicates each tag for certain page

      (9) update: indicates action to update tags or page description


   rel attributes:

      (1) alternate: alternate resource 

      (2) collection: link to a collection of pages


3. rule-list.html

   class attributes:

      (1) title: Describes title of this page

      (2) rule_collection: Describes the container of rule list

      (3) rule: Indicates each rule in rule list

      (4) date: Describes the date of archiving rule

      (5) func_des: Describes the function of contents below

      (6) rule-maker: Indicates the form to create a new resource(rule)

      (7) create: Describes the action to create a new rule


   rel attributes:

      (1) alternate: alternate resource 

      (2) page_collection: link to a collection of archived pages


4. page-list.html

   class attributes:

      (1) title: title: Describes title of this page

      (2) page_collection: Describes the container of page list

      (3) page: Indicates each page in the page list

      (4) date: Describes the date of archiving page
      
      (5) func_des: Describes the function of the contents below
      
      (6) search_field: Indicates an input field for searching


   rel attributes:

      (1) alternate: alternate resource



**B. The types and properties used to describe our data:**

   1. Metadata for the archived pages and the archiving criteria are stored in .json files in the "database" folder.
   
   2. Pages (under the page.html template) and rules (under the rule.html template) are described with HTML microdata. ADD      DETAILS ONCE ALEX IS DONE.
   
