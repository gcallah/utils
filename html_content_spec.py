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
Note 2: some tags have special rules that need additional context (attributes, html structure, etc)
        These rules are not captured within the content_spec.
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

_ANY_CONTENT = "_ANY_CONTENT" # Filler for adding tags, but not sure about the content
_NO_CONTENT = "_NO_CONTENT" # For content_models who expect no tags
_NONE_GROUP = "_NONE_GROUP" # Group for tags that don't have a category in the spec

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
                "form":
                    {
                        "categories" : ["flow", "palpable"],
                        "content_model" : ["flow"]
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
                "link":
                    {
                        # has special categories depending on attribute as well (not covered)
                        "categories" : ["metadata"],
                        "content_model" : [_NO_CONTENT]
                    },
                "title":
                    {
                        "categories" : ["metadata"],
                        "content_model" : [_NO_CONTENT]
                    },
                "button":
                    {
                        # This has special rules (not )
                        "categories" : ["flow","phrasing", "palpable","interactive"],
                        "content_model" : ["phrasing"]
                    },
                "br":
                    {
                        "categories" : ["flow","phrasing"],
                        "content_model" : [_NO_CONTENT]
                    },
                "label":
                    {
                        "categories" : ["flow","phrasing","interactive","palpable"],
                        "content_model" : ["phrasing"]
                    },
                "textarea":
                    {
                        "categories" : ["flow","phrasing","interactive", "palpable"],
                        "content_model" : [_NO_CONTENT]
                    },
                "strong":
                    {
                        "categories" : ["flow","phrasing","palpable"],
                        "content_model" : ["phrasing"]
                    },
                "small":
                    {
                        "categories" : ["flow","phrasing","palpable"],
                        "content_model" : ["phrasing"]
                    },
                "i":
                    {
                        "categories" : ["flow","phrasing","palpable"],
                        "content_model" : ["phrasing"]
                    },
                "span":
                    {
                        "categories" : ["flow","phrasing","palpable"],
                        "content_model" : ["phrasing"]
                    },
                "article":
                    {
                        "categories" : ["flow","sectioning","palpable"],
                        "content_model" : ["flow"]
                    },
                "section":
                    {
                        "categories" : ["flow","sectioning","palpable"],
                        "content_model" : ["flow"]
                    },
                "nav":
                    {
                        "categories" : ["flow","sectioning","palpable"],
                        "content_model" : ["flow"]
                    },
                "aside":
                    {
                        "categories" : ["flow","sectioning","palpable"],
                        "content_model" : ["flow"]
                    },
                "iframe":
                    {
                        "categories" : ["flow","phrasing","embedded","interactive","palpable"],
                        "content_model" : [_NO_CONTENT]
                    },
                "code":
                    {
                        "categories" : ["flow", "phrasing", "palpable"],
                        "content_model" : ["phrasing"]
                    },
                "header":
                    {
                        "categories" : ["flow", "palpable"],
                        "content_model" : ["flow"]
                    },
                "em":
                    {
                        "categories" : ["flow","phrasing", "palpable"],
                        "content_model" : ["phrasing"]
                    },
                "_EXCEPTIONS":
                    { "html" , "body", "title", "head"}
                }