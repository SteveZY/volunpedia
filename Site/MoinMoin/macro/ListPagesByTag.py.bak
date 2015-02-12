# -*- coding: utf-8 -*-

from MoinMoin import wikiutil, search
from MoinMoin.ngowikiutil import NgoWikiUtil 
from MoinMoin.Page import Page
from MoinMoin.action.AttachFile import exists
from MoinMoin.action.AttachFile import getAttachUrl
import re, json

Dependencies = ["pages"]

class ListPagesByTag:

    def __init__(self, macro, filterByTags):
        self.macro = macro
        self.request = macro.request
        self.formatter = macro.formatter
        self.page = macro.request.page
        self.filterByTags = filterByTags.split(",")

    def execute(self):
        ngowikiutil = NgoWikiUtil(self.request)
        ngowikiutil.open_database()
        try:
            offset = 0
            length = 10
            sortby = "lastmodified"
            order = "DESC"
            filterByTags = self.filterByTags

            form = self.request.values
            if 'from' in form:
                offset = int(form['from'])
            if 'length' in form:
                length = int(form['length'])
            if 'sortby' in form:
                sortby = form['sortby']
                if sortby == 'title':
                    order = "ASC"
            if 'order' in form:
                order = form['order']
            if 'filterByTags' in form:
                filterByTags = form['filterByTags'].split(",")

            results = ngowikiutil.select_pages_by_tag(filterByTags, sortby, order, offset, length)
            total = ngowikiutil.count_pages_by_tag(filterByTags)

            buffer = []
            buffer.append('''
                <script language="javascript">window.__ListPagesByTag_filterByTag = %(filterByTags)s;window.__ListPagesByTag_filterByTag_default = %(filterByTagsDefault)s;</script>
                <div id="listpagesbytag_sorter"></div>
                <div id="listpagesbytag_filter"></div>
            ''' % {"filterByTagsDefault": json.dumps(self.filterByTags), "filterByTags": json.dumps(",".join(filterByTags))})

            template = '''
                <table class="listitem_with_logosummary">
                    <tr>
                        <!--
                        <td class="logo">
                            %(logo)s
                        </td>
                        -->
                        <td>
                           <div class="title">
                              <a href="%(link)s">%(title)s</a>
                           </div>
                           <div class="meta">
                               <span>%(lastmodified)s</span>
                               <span>%(tags)s</span>
                               <span><span class="metaitem">%(likecount)s<span></span>
                               <span><span class="metaitem">%(commentcount)s<span></span>
                               <span><span class="metaitem">%(hitcount)s<span></span>
                           </div>
                           <div class="summary">%(summary)s</div>
                        </td>
                     </tr>
                 </table>
                '''
            for result in results:
                page = Page(self.request, result["path"]) 
                logo = '<div class="logo defaultLogo">&nbsp;</div>'
                if len(result["logo"]) > 0 and exists(self.request, result["path"], result["logo"]):
                    logo = '<img class="logo" src="' + getAttachUrl(result["path"], result["logo"], self.request) + '">'
                link = page.url(self.request)
                title = result["title"]
                lastmodified = page.mtime_printable(self.request)
                summary = result["summary"].replace("'''", "").replace(u"【请在此插入图片】", "").replace(u"【请在此插入图片，最多可插入9张】", "")

                tags = (", ".join(
                          map(lambda x: '<a href=\'javascript:add_filter_by_tag(' + json.dumps(x["tag"]) + ')\' >' + x["tag"] + '</a>', 
                              filter(lambda x: x["type"] == 1, ngowikiutil.select_page_tags_by_id(result["id"]))
                          )))

                if len(tags) > 0:
                    tags = '<span class="metaitem">' + tags + '</span>'

                buffer.append(template % {"logo":logo, "title": title, "link": link, "lastmodified": lastmodified, "tags": tags, "summary": summary, "likecount": u'\u559c\u6b22\uff1a' + str(result["likecount"]), "commentcount": u'\u8bc4\u8bba\u6570\uff1a' + str(result["commentcount"]), "hitcount": u'\u8bbf\u95ee\u91cf\uff1a' + str(result["hitcount"])})

            buffer.append("<script language='javascript'>render_pagingbar(" + str(total) + ', ' + str(length)  + ');</script>')
            ret = ''.join(buffer)
            return ret
        finally:
            ngowikiutil.close_database(True)

def macro_ListPagesByTag(macro, filterByTags):
    return ListPagesByTag(macro, filterByTags).execute()
