# -*- coding: iso-8859-1 -*-

import os, uuid, json, re

from MoinMoin import wikiutil
from MoinMoin.ngowikiutil import NgoWikiUtil

def execute(pagename, request):
    ngowikiutil = NgoWikiUtil(request)
    ngowikiutil.open_database()
    try:
        form = request.values
        tags = form.get('tags').split(",")
        favorite = None
        if 'favorite' in form and form['favorite'] != "false" and request.user != None and request.user.valid:
            favorite = request.user.id;

        relatedtags = ngowikiutil.select_related_tags(tags, favorite)
        for tag in tags:
            for relatedtag in relatedtags:
                if relatedtag["tag"] == tag:
                    relatedtags.remove(relatedtag)
                    break
        request.write(json.dumps(relatedtags))
    finally:
        ngowikiutil.close_database(True)
