# -*- coding: utf-8 -*-

from MoinMoin.theme import rightsidebar
from MoinMoin import user, wikiutil
from MoinMoin.user import User
from MoinMoin.Page import Page
from MoinMoin.ngowikiutil import NgoWikiUtil
import time

class Theme(rightsidebar.Theme):
    name = "ngowiki"

    recommendbarItems = None
    recommendbarItemsLastUpdated = None

    _ = lambda x: x     # We don't have gettext at this moment, so we fake it
    icons = {
        # key         alt                        icon filename      w   h
        # FileAttach
        'attach':     ("%(attach_count)s",       "moin-attach.png", 16, 16),
        'info':     ("[INFO]",       "moin-info.png", 16, 16),
        'attachimg':  (_("[ATTACH]"),            "attach.png",      32, 32),
        # RecentChanges
        'rss':        (_("[RSS]"),               "moin-rss.png",    16, 16),
        'deleted':    (_("[DELETED]"),           "moin-deleted.png",16, 16),
        'updated':    (_("[UPDATED]"),           "moin-updated.png",16, 16),
        'renamed':    (_("[RENAMED]"),           "moin-renamed.png",16, 16),
        'conflict':   (_("[CONFLICT]"),          "moin-conflict.png", 16, 16),
        'new':        (_("[NEW]"),               "moin-new.png",    16, 16),
        'diffrc':     (_("[DIFF]"),              "moin-diff.png",   16, 16),
        # General
        'bottom':     (_("[BOTTOM]"),            "moin-bottom.png", 16, 16),
        'top':        (_("[TOP]"),               "moin-top.png",    16, 16),
        'www':        ("[WWW]",                  "moin-www.png",    16, 16),
        'mailto':     ("[MAILTO]",               "moin-email.png",  16, 16),
        'news':       ("[NEWS]",                 "moin-news.png",   16, 16),
        'telnet':     ("[TELNET]",               "moin-telnet.png", 16, 16),
        'ftp':        ("[FTP]",                  "moin-ftp.png",    16, 16),
        'file':       ("[FILE]",                 "moin-ftp.png",    16, 16),
        # search forms
        'searchbutton': ("[?]",                  "moin-search.png", 16, 16),
        'interwiki':  ("[%(wikitag)s]",          "moin-inter.png",  16, 16),

        # smileys (this is CONTENT, but good looking smileys depend on looking
        # adapted to the theme background color and theme style in general)
        #vvv    ==      vvv  this must be the same for GUI editor converter
        'X-(':        ("X-(",                    'angry.png',       16, 16),
        ':D':         (":D",                     'biggrin.png',     16, 16),
        '<:(':        ("<:(",                    'frown.png',       16, 16),
        ':o':         (":o",                     'redface.png',     16, 16),
        ':(':         (":(",                     'sad.png',         16, 16),
        ':)':         (":)",                     'smile.png',       16, 16),
        'B)':         ("B)",                     'smile2.png',      16, 16),
        ':))':        (":))",                    'smile3.png',      16, 16),
        ';)':         (";)",                     'smile4.png',      16, 16),
        '/!\\':       ("/!\\",                   'alert.png',       16, 16),
        '<!>':        ("<!>",                    'attention.png',   16, 16),
        '(!)':        ("(!)",                    'idea.png',        16, 16),
        ':-?':        (":-?",                    'tongue.png',      16, 16),
        ':\\':        (":\\",                    'ohwell.png',      16, 16),
        '>:>':        (">:>",                    'devil.png',       16, 16),
        '|)':         ("|)",                     'tired.png',       16, 16),
        ':-(':        (":-(",                    'sad.png',         16, 16),
        ':-)':        (":-)",                    'smile.png',       16, 16),
        'B-)':        ("B-)",                    'smile2.png',      16, 16),
        ':-))':       (":-))",                   'smile3.png',      16, 16),
        ';-)':        (";-)",                    'smile4.png',      16, 16),
        '|-)':        ("|-)",                    'tired.png',       16, 16),
        '(./)':       ("(./)",                   'checkmark.png',   16, 16),
        '{OK}':       ("{OK}",                   'thumbs-up.png',   16, 16),
        '{X}':        ("{X}",                    'icon-error.png',  16, 16),
        '{i}':        ("{i}",                    'icon-info.png',   16, 16),
        '{1}':        ("{1}",                    'prio1.png',       15, 13),
        '{2}':        ("{2}",                    'prio2.png',       15, 13),
        '{3}':        ("{3}",                    'prio3.png',       15, 13),
        '{*}':        ("{*}",                    'star_on.png',     16, 16),
        '{o}':        ("{o}",                    'star_off.png',    16, 16),
    }
    del _

    def subscribeLink(self, page):
        """ Return subscribe/unsubscribe link to valid users

        @rtype: unicode
        @return: subscribe or unsubscribe link
        """
        if not ((self.cfg.mail_enabled or
                 self.cfg.jabber_enabled) and self.request.user.valid):
            return ''

        _ = self.request.getText
        if self.request.user.isSubscribedTo([page.page_name]):
            action, text = 'unsubscribe', _("Unsubscribe")
        else:
            action, text = 'subscribe', _("Subscribe")
        if action in self.request.cfg.actions_excluded:
            return ''
        return page.link_to(self.request, text=text,
                            querystr={'action': action},
                            css_class='nbsubscribe %s' % action,
                            title=text,
                            rel='nofollow')

    def navibar(self, d):
        request = self.request
        found = {} # pages we found. prevent duplicates
        items = [] # navibar items
        item = u'<li class="%s">%s</li>'
        current = d['page_name']

        pagenames = [u'志愿产品', u'服务产品', u'视听产品', u'实体产品', u'志愿组织', u'公益机构', u'企业志愿组织', u'学生志愿组织', u'志愿服务基地', u'应用工具']
        for pagename in pagenames:
            pagegroup = None
            
            if pagename == u'志愿产品':
                pagegroup = 'volunpedia_product_pages'
            elif pagename == u'志愿组织':
                pagegroup = 'volunpedia_organization_pages'
                
            if pagename != u'志愿产品' and pagename != u'志愿组织':
                page = Page(request, pagename)
                title = page.split_title()
                title = self.shortenPagename(title)
                link = page.link_to(request, title)
                cls = 'userlink'
                items.append(item % (cls, link))
                if pagename == u'实体产品' or pagename == u'学生志愿组织':
                    items.append(u'</ul></li>')
                found[pagename] = 1
            else:
                cls = 'userlink'
                link = u'<a href="javascript:;" onclick="var t = document.getElementById(\'' + pagegroup + u'_menu' + u'\'); if(t.style.display == \'none\') {t.style.display = \'\';} else {t.style.display = \'none\';}">' + pagename + u'</a>'
                items.append(item % (cls, link))
                items.append(u'<li id="' + pagegroup + u'_menu' + u'" class="userlink"><ul style="padding-left:2.5em">')

        # Assemble html
        items = u''.join(items)
        html = u'''
<ul id="navibar">
%s
</ul>
''' % items
        return html

    def html_head(self, d):
        head = [rightsidebar.Theme.html_head(self, d)]
        head.append(u'\n<script type="text/javascript" src="%s/%s/js/jquery.js"></script>' % (self.cfg.url_prefix_static, self.name))
        head.append(u'\n<script type="text/javascript" src="%s/%s/js/json2.js"></script>' % (self.cfg.url_prefix_static, self.name))
        head.append(u'\n<script type="text/javascript" src="%s/%s/js/ngowiki_v20140311.js"></script>' % (self.cfg.url_prefix_static, self.name))
        head.append(u'\n<script type="text/javascript" src="http://qzonestyle.gtimg.cn/qzone/openapi/qc_loader.js" data-appid=%s data-redirecturi="" charset="utf-8"></script>' % self.cfg.qq_app_id)
        head.append(u'\n<script src="http://tjs.sjs.sinajs.cn/open/api/js/wb.js?appkey=%s&debug=true" type="text/javascript" charset="utf-8"></script>' % self.cfg.wb_app_key)
        head.append(u'\n<script type="text/javascript" src="%s/%s/js/openid.js"></script>' % (self.cfg.url_prefix_static, self.name))
        head.append(u'\n<script type="text/javascript">window.url_prefix_static="%s";</script>' % (self.cfg.url_prefix_static))
        head.append(u'\n<meta property="qc:admins" content="46715120776674560541163757" />')
        head.append(u'\n<meta property="wb:webmaster" content="1a605196e8a8f55c" />')
        return '\n'.join(head)

    def wikipanel(self, d):
        """ Create wiki panel """
        _ = self.request.getText
        html = [
            u'<div class="sidepanel">', self.navibar(d), u'</div>',
            ]
        return u'\n'.join(html)

    def editbarItems(self, page):
        """ Return list of items to show on the editbar

        This is separate method to make it easy to customize the
        edtibar in sub classes.
        """
        _ = self.request.getText
        editbar_actions = []
        for editbar_item in self.request.cfg.edit_bar:
            if (editbar_item == 'Discussion' and
               (self.request.getPragma('supplementation-page', self.request.cfg.supplementation_page)
                                                   in (True, 1, 'on', '1'))):
                    editbar_actions.append(self.supplementation_page_nameLink(page))
            elif editbar_item == 'Comments':
                # we just use <a> to get same style as other links, but we add some dummy
                # link target to get correct mouseover pointer appearance. return false
                # keeps the browser away from jumping to the link target::
                editbar_actions.append('<a href="#" class="nbcomment" onClick="toggleComments();return false;">%s</a>' % _('Comments'))
            elif editbar_item == 'Edit':
                editbar_actions.append(self.editorLink(page))
            elif editbar_item == 'Info':
                editbar_actions.append(self.infoLink(page))
            elif editbar_item == 'Subscribe':
                editbar_actions.append(self.subscribeLink(page))
            elif editbar_item == 'Quicklink' and self.request.user.name == 'administrator':
                editbar_actions.append(self.quicklinkLink(page))
            elif editbar_item == 'Attachments':
                editbar_actions.append(self.attachmentsLink(page))
            elif editbar_item == 'ActionsMenu':
                editbar_actions.append(self.actionsMenu(page))
        return editbar_actions

    def pagepanel(self, d):
        """ Create page panel """
        _ = self.request.getText
        if self.shouldShowEditbar(d['page']):
            html = [
                u'<div style="padding-top:50px;border-bottom: 1px solid #AAA;margin-bottom:10px"></div>'
                u'<div class="sidepanel">',
                u'<h1>页面操作</h1>',
                self.editbar(d),
                u'</div>',
                ]
            return u'\n'.join(html)
        return ''

    def header(self, d):
        """
        Assemble page header

        @param d: parameter dictionary
        @rtype: string
        @return: page header html
        """
        _ = self.request.getText

        html = [
            # Custom html above header
            self.emit_custom_html(self.cfg.page_header1),
            self.username(d),

            # Header
            u'<div id="header">',
            self.searchform(d),
            self.logo(),
            u'<div id="locationline">',
            self.interwiki(d),
            self.title(d),
            u'</div>',
            self.trail(d),
            u'</div>',

            # Custom html below header (not recomended!)
            self.emit_custom_html(self.cfg.page_header2),

            # Sidebar
            u'<div id="sidebar">',
            self.wikipanel(d),
            self.pagepanel(d),
            u'</div>',

            # Page
            self.startPage(),

            self.msg(d),
            ]
        return u'\n'.join(html)

    def editorheader(self, d):
        """
        Assemble page header for editor

        @param d: parameter dictionary
        @rtype: string
        @return: page header html
        """
        _ = self.request.getText

        html = [
            # Custom html above header
            self.emit_custom_html(self.cfg.page_header1),
            self.username(d),

            # Header
            u'<div id="header">',
            self.searchform(d),
            self.logo(),
            u'<div id="locationline">',
            self.interwiki(d),
            self.title(d),
            u'</div>',
            self.trail(d),
            u'</div>',

            # Custom html below header (not recomended!)
            self.emit_custom_html(self.cfg.page_header2),

            # Sidebar
            u'<div id="sidebar">',
            self.wikipanel(d),
            self.pagepanel(d),
            u'</div>',

            # Page
            self.startPage(),
            
            self.msg(d),
            ]
        return u'\n'.join(html)

    def searchform(self, d):
        """
        assemble HTML code for the search forms

        @param d: parameter dictionary
        @rtype: unicode
        @return: search form html
        """
        _ = self.request.getText
        form = self.request.values
        updates = {
            'search_label': _('Search:'),
            'search_value': wikiutil.escape(form.get('value', ''), 1),
            'search_full_label': _('Text'),
            'search_title_label': _('Titles'),
            'url': self.request.href(d['page'].page_name),
            'search_icon': self.img_url('search-ltr.png')
            }
        d.update(updates)

        html = u'''
<form id="searchform" method="get" action="%(url)s">
<div id="simpleSearch">
<input type="hidden" name="action" value="fullsearch">
<input type="hidden" name="context" value="180">
<label for="searchinput">%(search_label)s</label>
<input id="searchinput" type="text" name="value" value="%(search_value)s" size="20"
    onfocus="searchFocus(this)" onblur="searchBlur(this)"
    onkeyup="searchChange(this)" onchange="searchChange(this)" alt="Search">
<input id="titlesearch" name="titlesearch" type="submit"
    value="0" alt="Search Titles" style="display:none">
<input id="fullsearch" name="fullsearch" type="image" src="%(search_icon)s" height="12" width="12"
    value="%(search_full_label)s" alt="Search Full Text">
</div>
</form>
<script type="text/javascript">
<!--// Initialize search form
var f = document.getElementById('searchform');
f.getElementsByTagName('label')[0].style.display = 'none';
var e = document.getElementById('searchinput');
searchChange(e);
searchBlur(e);
//-->
$("a#logout").click(function(){
    wb_logout();
    qq_logout();
});
</script>
''' % d
        return html

def execute(request):
    return Theme(request)
