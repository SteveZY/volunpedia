# -*- coding: utf-8 -*-

import tenjin, os, time, re
from tenjin.helpers import *
from MoinMoin.Page import Page
from MoinMoin.ngowikiutil import NgoWikiUtil
from MoinMoin.action.AttachFile import exists
from MoinMoin.action.AttachFile import getAttachUrl

class FrontpageMacro:

    lastupdated = None

    totalcount_activities = None
    totalcount_ngos = None
    totalcount_enterprises = None
    featured_activities = None
    featured_ngos = None
    recently_added = None
    news_items = None

    def __init__(self, macro):
        self.macro = macro
        self.request = macro.request
        self.formatter = macro.formatter

    def execute(self):

        if FrontpageMacro.lastupdated == None or long(time.time()) - FrontpageMacro.lastupdated > 3600L:
            ngowikiutil = NgoWikiUtil(self.request)
            try:
                ngowikiutil.open_database()
                FrontpageMacro.totalcount_activities = ngowikiutil.count_pages_by_tag([u'服务产品类']) + ngowikiutil.count_pages_by_tag([u'视听产品类']) + ngowikiutil.count_pages_by_tag([u'实体产品类'])
                FrontpageMacro.totalcount_ngos = ngowikiutil.count_pages_by_tag([u'公益机构类'])
                FrontpageMacro.totalcount_enterprises = ngowikiutil.count_pages_by_tag([u'企业志愿组织类'])
                FrontpageMacro.featured_activities = ngowikiutil.select_pages_with_one_of_tags([u'服务产品类', u'视听产品类', u'实体产品类'], 'featured', 'DESC', 0, 20)
                for record in FrontpageMacro.featured_activities[0:2]:
                    record["summary"] = record["summary"].replace("'''", "")
                    record["summary"] = filter_summary(record["summary"], 50);
                    pagename = record["path"]
                    page = Page(self.request, pagename)
                    record["link"] = page.url(self.request)
                    if len(record["logo"]) > 0 and exists(self.request, record["path"], record["logo"]):
                        record["logo_link"] = getAttachUrl(record["path"], record["logo"], self.request)
                    else:
                        findLogo = False
                        text = page.getPageText()
                        match = re.search('\\{\\{attachment:([^\\|]+)\\|\\|.*}}', text)
                        if match != None:
                            logo = match.group(1)
                            if exists(self.request, record["path"], logo):
                                record["logo_link"] = getAttachUrl(record["path"], logo, self.request)
                                findLogo = True
                        if not findLogo:
                            record["logo_link"] = self.request.cfg.url_prefix_static + "/ngowiki/img/no-logo.png"
                FrontpageMacro.featured_ngos = ngowikiutil.select_pages_by_tag([u'公益机构类'], 'featured', 'DESC', 0, 2)
                for record in FrontpageMacro.featured_ngos:
                    pagename = record["path"]
                    record["summary"] = filter_summary(record["summary"], 50)
                    page = Page(self.request, pagename)
                    record["link"] = page.url(self.request)
                    if len(record["logo"]) > 0 and exists(self.request, record["path"], record["logo"]):
                        record["logo_link"] = getAttachUrl(record["path"], record["logo"], self.request)
                    else:
                        record["logo_link"] = self.request.cfg.url_prefix_static + "/ngowiki/img/no-logo.png"
                FrontpageMacro.recently_added = ngowikiutil.select_latest_created_pages([u'服务产品类', u'视听产品类', u'实体产品类', u'公益机构类', u'企业志愿组织类'], 0, 5)
                for record in FrontpageMacro.recently_added:
                    pagename = record["path"]
                    page = Page(self.request, pagename)
                    record["link"] = page.url(self.request)
                    if len(record["logo"]) > 0 and exists(self.request, record["path"], record["logo"]):
                        record["logo_link"] = getAttachUrl(record["path"], record["logo"], self.request)
                    else:
                        record["logo_link"] = self.request.cfg.url_prefix_static + "/ngowiki/img/no-logo.png"
                    if u'服务产品类' in ngowikiutil.parse_page(page)["categories"] or u'视听产品类' in ngowikiutil.parse_page(page)["categories"] or u'实体产品类' in ngowikiutil.parse_page(page)["categories"]:
                        record["recently_added_type"] = "activity"
                    elif u'公益机构类' in ngowikiutil.parse_page(page)["categories"]:
                        record["recently_added_type"] = "ngo"
                    else:
                        record["recently_added_type"] = "enterprise"
                FrontpageMacro.news_items = ngowikiutil.select_pages_by_tag([u'新闻动态类'], 'featured', 'DESC', 0, 100)
                for record in FrontpageMacro.news_items:
                    pagename = record["path"]
                    page = Page(self.request, pagename)
                    record["link"] = page.url(self.request)
                    if len(record["logo"]) > 0 and exists(self.request, record["path"], record["logo"]):
                        record["logo_link"] = getAttachUrl(record["path"], record["logo"], self.request)
                    else:
                        record["logo_link"] = self.request.cfg.url_prefix_static + "/ngowiki/img/no-logo.png"
            finally:
                ngowikiutil.close_database(True)
            FrontpageMacro.lastupdated = long(time.time())

        context = {
            'totalcount_activities': FrontpageMacro.totalcount_activities,
            'totalcount_ngos': FrontpageMacro.totalcount_ngos,
            'totalcount_enterprises': FrontpageMacro.totalcount_enterprises,
            'featured_activities': FrontpageMacro.featured_activities,
            'featured_ngos': FrontpageMacro.featured_ngos,
            'recently_added': FrontpageMacro.recently_added,
            'news_items': FrontpageMacro.news_items,
            'logo_url': self.request.cfg.url_prefix_static + "/ngowiki/img/sitelogo.png",
            'slogan_url': self.request.cfg.url_prefix_static + "/ngowiki/img/slogan2.png"
        }

        engine = tenjin.Engine(path=[os.path.dirname(__file__) + '/views'])
        html = engine.render('Frontpage.pyhtml', context)

        return self.formatter.rawHTML(html)


def macro_FrontpageMacro(macro):
    return FrontpageMacro(macro).execute()

def filter_summary(summary, length):
    if len(summary) < length:
        return summary
    else:
        return summary[0:length] + "..."

