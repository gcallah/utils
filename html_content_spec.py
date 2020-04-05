#!/usr/bin/python
"""
External variable file for html_checker.py

Primarily used to hold content_spec, which represents a dictionary of 
expected or legal content of various html tags. 

The spec is based on the HTML spec: https://html.spec.whatwg.org/#content-models

The current version is based on the idea that tags are grouped into 
different categories as listed by the HTML spec. Each tag has their own list of 
legal content called the content model

Note: "_EXCEPTIONS" is a custom list of tags to ignore that otherwise might
        not have a clear category in the spec
"""

'''
Generic Structure of a tag content spec
    "<tag>":
        {
            "categories" : [],
            "content_model" : []
        },
'''

'''
    categories can be seen as groups that the tag belong to and/or as list of valid parent tags
    content_model: what the tag expect its descendant tags to be, you can be specific or general
'''
_ANY_CONTENT = "_ANY_CONTENT"
_NO_CONTENT = "_NO_CONTENT"
_NONE_GROUP = "_NONE_GROUP"

content_spec = {"p": 
                    { 
                        "categories" : ["flow", "palpable"], 
                        "content_model" : ["phrasing"]
                    },
                "h1": 
                    { 
                        "categories" : ["flow", "heading", "palpable"], 
                        "content_model" : ["phrasing"]
                    },
                "h2": 
                    { 
                        "categories" : ["flow", "heading", "palpable"], 
                        "content_model" : ["phrasing"]
                    },
                "h3": 
                    { 
                        "categories" : ["flow", "heading", "palpable"], 
                        "content_model" : ["phrasing"]
                    },
                "h4": 
                    { 
                        "categories" : ["flow", "heading", "palpable"], 
                        "content_model" : ["phrasing"]
                    },
                "h5": 
                    { 
                        "categories" : ["flow", "heading", "palpable"], 
                        "content_model" : ["phrasing"]
                    },
                "h6": 
                    { 
                        "categories" : ["flow", "heading", "palpable"], 
                        "content_model" : ["phrasing"]
                    },
                "a":
                    {
                        "categories" : ["flow", "phrasing", "palpable"],
                        "content_model" : ["transparent"]
                    },
                "ol":
                    {
                        "categories" : ["flow"],
                        "content_model" : ["li", "script-supporting"]
                    },
                "ul":
                    {
                        "categories" : ["flow"],
                        "content_model" : ["li", "script-supporting"]
                    },
                "li":
                    {
                        "categories" : [_NONE_GROUP],
                        "content_model" : ["flow"]
                    },
                "script":
                    {
                        "categories" : ["metadata", "flow","phrasing","script-supporting"],
                        "content_model" : [_ANY_CONTENT]
                    },
                "template":
                    {
                        "categories" : ["metadata", "flow","phrasing","script-supporting"],
                        "content_model" : [_ANY_CONTENT]
                    },
                "img":
                    {
                        "categories" : ["flow","phrasing","embedded","form-associated","palpable","interactive"],
                        "content_model" : [_NO_CONTENT]
                    },
                "table":
                    {
                        "categories" : ["flow","palpable"],
                        "content_model" : ["caption","thead","tbody","tfoot"]
                    },
                "thead":
                    {
                        "categories" : [_NONE_GROUP],
                        "content_model" : ["tr"]
                    },
                "tbody":
                    {
                        "categories" : [_NONE_GROUP],
                        "content_model" : ["tr","script-supporting"]
                    },
                "tfoot":
                    {
                        "categories" : [_NONE_GROUP],
                        "content_model" : ["tr"]   
                    },
                "tr":
                    {
                        "categories" : [_NONE_GROUP],
                        "content_model" : ["td", "th", "script-supporting"]
                    },
                "td":
                    {
                        "categories" : [_NONE_GROUP],
                        "content_model" : ["flow"]
                    },
                "th":
                    {
                        "categories" : [_NONE_GROUP],
                        "content_model" : ["flow"]
                    },
                "_EXCEPTIONS":
                    { "html" , "body", "title", "head"}
                }