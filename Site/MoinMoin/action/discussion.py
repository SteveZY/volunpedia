# -*- coding: iso-8859-1 -*-

import os, uuid, json, re

from MoinMoin import wikiutil
from MoinMoin.Page import Page
from MoinMoin.ngowikiutil import NgoWikiUtil
from MoinMoin.user import User

class DiscussionBoard:
    
    def __init__(self, request, pagename):
        self.request = request
        self.user = request.user
        self.pagename = pagename
        self.page = Page(self.request, self.pagename)
        self.ngowikiutil = NgoWikiUtil(self.request)
        self.ngowikiutil.open_database()
        self.pageid = self.ngowikiutil.select_page_by_path(self.pagename)["id"]

    def release(self):
        self.ngowikiutil.close_database(True)

    def like(self, sessionId):
        userId = 'anonymous-' + sessionId
        if self.user != None and self.user.valid:
            userId = self.user.id
        if not self.ngowikiutil.has_user_liked_page(userId, self.page):
            self.ngowikiutil.insert_like(self.page, userId, '')
            self.ngowikiutil.commit_database()

    def unlike(self, sessionId):
        userId = 'anonymous-' + sessionId
        if self.user != None and self.user.valid:
            userId = self.user.id
        like_info = self.ngowikiutil.select_like_by_page_and_userid(self.pageid, userId)
        if like_info != None:
            self.ngowikiutil.remove_likes_by_id(like_info["id"])
            self.ngowikiutil.commit_database()

    def addFavorite(self, sessionId):
        if self.user == None or not self.user.valid:
            return
        userId = self.user.id
        if not self.ngowikiutil.has_user_favorite_page(userId, self.page):
            self.ngowikiutil.insert_favorite(self.page, userId)
            self.ngowikiutil.commit_database()

    def removeFavorite(self, sessionId):
        if self.user == None or not self.user.valid:
            return
        userId = self.user.id
        self.ngowikiutil.remove_favorite(self.page, userId)
        self.ngowikiutil.commit_database()

    def comment(self, comment):
        if self.user == None or not self.user.valid:
            return
        self.ngowikiutil.insert_comment(self.page, self.user.id, comment)
        self.ngowikiutil.commit_database()

    def superrecommend(self, comment):
        if self.user == None or not self.user.valid:
            return
        if not self.user.isSuperUser():
            return
        self.ngowikiutil.super_recommend(self.page, comment)
        self.ngowikiutil.commit_database()

    def removecomment(self, commentid):
        if self.user == None or not self.user.valid:
            return
        comment_info = self.ngowikiutil.select_comment_by_id(commentid)
        if comment_info == None:
            return
        if not self.user.isSuperUser() and self.user.id != comment_info["user_id"]:
            return
        self.ngowikiutil.remove_comments_by_id(commentid)
        self.ngowikiutil.commit_database()

    def view(self, offset, length, sessionId):
        page_info = self.ngowikiutil.select_page_by_id(self.pageid)
        comment_list = self.ngowikiutil.select_comments_by_page(self.page, offset, length)
        if comment_list == None:
            comment_list = []
        for comment in comment_list:
            user = User(self.request, id=comment["user_id"])
            comment["user_name"] = user.name
            comment["comment"] = comment["comment"].replace("\n", "<br>")
            if self.user == None or not self.user.valid or (not self.user.isSuperUser() and self.user.id != comment["user_id"]):
                continue
            comment["_delete_"] = True
        isSuperUser = False
        if self.user != None and self.user.valid and self.user.isSuperUser():
            isSuperUser = True
        has_user_liked_page = False
        if self.user != None and self.user.valid:
            has_user_liked_page = self.ngowikiutil.has_user_liked_page(self.user.id, self.page)
        else: 
            has_user_liked_page = self.ngowikiutil.has_user_liked_page('anonymous-' + sessionId, self.page)
        has_user_favorite_page = False
        if self.user != None and self.user.valid:
            has_user_favorite_page = self.ngowikiutil.has_user_favorite_page(self.user.id, self.page)
        else: 
            has_user_favorite_page = False
        return {"commentcount": page_info["commentcount"], "likecount": page_info["likecount"], "hasUserLikedPage": has_user_liked_page, "hasUserFavoritedPage": has_user_favorite_page, "comments": {"offset": offset, "length": length, "items": comment_list}, "isSuperUser": isSuperUser, "superrecommend": page_info["superrecommend"]}

def execute(pagename, request):
    discussion_board = DiscussionBoard(request, pagename)
    try:
        form = request.values
        if form.get('do') != None:
            if form.get('do') == 'like':
                discussion_board.like(form['sessionId'])
            elif form.get('do') == 'unlike':
                discussion_board.unlike(form['sessionId'])
            elif form.get('do') == 'addFavorite':
                discussion_board.addFavorite(form['sessionId'])
            elif form.get('do') == 'removeFavorite':
                discussion_board.removeFavorite(form['sessionId'])
            elif form.get('do') == 'comment':
                discussion_board.comment(form.get('content'))
            elif form.get('do') == 'removecomment':
                discussion_board.removecomment(form.get('commentid'))
            elif form.get('do') == 'superrecommend':
                discussion_board.superrecommend(form.get('content'))
        request.write(json.dumps(discussion_board.view(int(form['from']), int(form['length']), form['sessionId'])))
    finally:
        discussion_board.release()
