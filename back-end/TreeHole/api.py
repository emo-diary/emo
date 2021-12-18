# encoding:utf-8
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest, DescribeInstanceStatusRequest
import json
from aliyunsdkcore.client import AcsClient
from flask import Flask, jsonify, request, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import pymysql,pymysql.cursors
import random
from sqlalchemy import extract, and_, or_
import requests
from urllib.parse import quote
import re
import time
from fuzzywuzzy import fuzz
from sqlalchemy import *

pymysql.install_as_MySQLdb()
app=Flask(__name__)


#数据库的表详情


class User(db.Model):
    __tablename__ = "User"  # 设置表名
    user_id = db.Column(db.String(50), primary_key=True,nullable=False, index=True)  # 用户id
    number = db.Column(db.Integer, default=0)  # 被举报次数
    sadness = db.Column(db.Integer, default=0)  # 悲伤
    angry = db.Column(db.Integer, default=0)  # 生气
    anxious = db.Column(db.Integer, default=0)  # 焦虑
    speechless = db.Column(db.Integer, default=0)  # 无语
    disappointmeant = db.Column(db.Integer, default=0)  # 失望
    collapse = db.Column(db.Integer, default=0)  # 崩溃
    grievance = db.Column(db.Integer, default=0)  # 委屈
    cure = db.Column(db.Integer, default=0)  # 治愈
    def to_dict(self):
        data = {
            'user_id': self.user_id,
            'sadness': self.sadness,
            'angry': self.angry,
            'number': self.number,
            'anxious': self.anxious,
            'speechless': self.speechless,
            'disappointmeant': self.disappointmeant,
            'collapse': self.collapse,
            'grievance': self.grievance,
            'cure': self.cure
        }
        return data


class TreeHole(db.Model):
    __tablename__ = "TreeHole"  # 设置表名
    tree_hole_id = db.Column(db.String(50), primary_key=True)  # 帖id
    user_id = db.Column(db.String(50), nullable=False, index=True)  # 用户id
    content = db.Column(db.String(2000), nullable=False)  # 帖内容
    time = db.Column(db.DateTime, nullable=False, default=datetime.now)  # 时间
    likes = db.Column(db.Integer, default=0)  # 点赞数
    comments = db.Column(db.Integer, default=0)  # 评论数
    collects = db.Column(db.Integer, default=0)  # 点赞数

    def to_dict(self):
        data = {
            'tree_hole_id': self.tree_hole_id,
            'user_id': self.user_id,
            'content': self.content,
            # 'time': self.time,
            'time': self.time.strftime('%Y-%m-%d %H:%M:%S'),
            'likes': self.likes,
            'comments': self.comments,
            'collects': self.collects
        }
        return data


class ClickLike(db.Model):
    __tablename__ = "ClickLike"  # 设置表名
    tree_hole_id = db.Column(db.String(50), primary_key=True, index=True)  # 帖id
    user_id = db.Column(db.String(50), primary_key=True, index=True)  # 用户id
    time = db.Column(db.DateTime, nullable=False, default=datetime.now)  # 时间

    def to_dict(self):
        data = {
            'tree_hole_id': self.tree_hole_id,
            'user_id': self.user_id,
            # 'time':self.time
            'time': self.time.strftime('%Y-%m-%d %H:%M:%S')
        }
        return data

class Collect(db.Model):
    __tablename__ = "Collect"  # 设置表名
    tree_hole_id = db.Column(db.String(50), primary_key=True)  # 帖id
    user_id = db.Column(db.String(50), primary_key=True, index=True)  # 用户id
    time = db.Column(db.DateTime, nullable=False, default=datetime.now)  # 时间

    def to_dict(self):
        data = {
            'tree_hole_id': self.tree_hole_id,
            'user_id': self.user_id,
            # 'time':self.time
            'time': self.time.strftime('%Y-%m-%d %H:%M:%S')
        }
        return data


class Comment(db.Model):
    __tablename__ = "Comment"  # 设置表名
    comment_id = db.Column(db.String(120), primary_key=True)  # 评论id
    # parentCommentId = db.Column(db.String(50), primary_key=True)  # 父评论id
    tree_hole_id = db.Column(db.String(50), primary_key=True)  # 帖id
    user_id = db.Column(db.String(50), index=True)  # 用户id
    comment_content = db.Column(db.String(2000), nullable=False)  # 评论内容
    time = db.Column(db.DateTime, nullable=False, default=datetime.now)  # 时间

    def to_dict(self):
        data = {
            'tree_hole_id': self.tree_hole_id,
            'user_id': self.user_id,
            'comment_id':self.comment_id,
            'comment_content':self.comment_content,
            # 'time':self.time
            'time': self.time.strftime('%Y-%m-%d %H:%M:%S')
        }
        return data


class Diary(db.Model):
    __tablename__ = "Diary"  # 设置表名
    # diary_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 日记id
    diary_id = db.Column(db.String(50), primary_key=True)
    user_id = db.Column(db.String(50), nullable=False, index=True)  # 用户id
    tips = db.Column(db.String(5000), nullable=False)
    diary_content = db.Column(db.String(5000), nullable=False)  # 日记内容
    write_down_time = db.Column(db.DateTime, default=datetime.now)  # 记录日期
    

    def to_dict(self):
        data = {
            'diary_id': self.diary_id,
            'user_id': self.user_id,
            'tips': self.tips,
            'diary_content': self.diary_content,
            'write_down_time': self.write_down_time.strftime('%Y-%m-%d %H:%M:%S')
        }
        return data

class PushMsg(db.Model):
    __tablename__ = "PushMsg"
    pushmsg_id = db.Column(db.String(50), primary_key=True)  # 推送id
    content = db.Column(db.String(5000), nullable=False)  # 推送内容
    tips = db.Column(db.String(50))  # 推送标签
    
    def to_dict(self):
        data = {
            'pushmsg_id': self.pushmsg_id,
            'content': self.content,
            'tips': self.tips
        }
        return data


class Report(db.Model):
    __tablename__ = "Report"
    tree_hole_id = db.Column(db.String(50), primary_key=True, index=True)  # 帖id
    content = db.Column(db.String(5000), nullable=False)  # 树洞内容
    comment_id = db.Column(db.String(120))  # 评论id
    comment_content = db.Column(db.String(5000))  # 评论内容
    reason = db.Column(db.String(5000), nullable=False)  # 举报理由
    user_id = db.Column(db.String(50), nullable=False)  # 被举报用户id
    whether_success = db.Column(db.Boolean)  # 是否举报成功  //0 1
    time = db.Column(db.DateTime, default=datetime.now,primary_key=True)  # 举报时间

       
# 敏感词检测        
def msg_check(content,openid):

    # return 1
    # 获取凭证
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx41b775e954cfff86&secret=95b37aa9b08fc927a2d8472400320eef'
    try:
        r = requests.get(url)
        res = json.loads(r.text)
        access_token = res.get("access_token")
        # 调用检测接口
        url_2 ='https://api.weixin.qq.com/wxa/msg_sec_check?access_token='+access_token
        headers = {"Content-Type":"application/json"}
        data={
           "openid": openid,
           "scene": 1,
           "version": 2,
           "content":content.encode("utf-8").decode("latin1")
       }
        data = json.dumps(data,ensure_ascii=False)
        # return access_token
        try:
            # file_content = file_content.decode("utf-8")
            r =  requests.post(url=url_2, data=data,headers=headers)
            r.encoding = 'utf-8'
            res = json.loads(r.text)
            errcode = res.get("errcode")
            errmsg  = res.get("errmsg")
            result = res.get("result")
            # detail = res.get("detail")
            # return res
            # return result["suggest"]
            if errcode!=0 or errmsg!="ok" or result["suggest"]!="pass":  # 未通过
                return res
            else:
                return True
        except:
            return 2
    except:
        return 1


# 新建日记    
@app.route('/diary/addDiary/', methods=['POST'])
def add_diary():
    data = request.get_json()
    diary_content = data.get('diary_content')
    user_id = data.get('user_id')
    # 获取当前时间并转成字符串
    # time = datetime.strptime
    tips = data.get('tips')
    # time = data.get('time')
    now = datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    diary_id = user_id+time
    success = msg_check(diary_content,user_id)
    # return jsonify(code=400, msg=success)
    if success==True:
        try:
            diary = Diary(diary_id=diary_id,user_id=user_id,tips=tips,
                          diary_content=diary_content)
            db.session.add(diary)
            db.session.commit()
            return jsonify(code=200, msg="日记保存成功")
        except:
            # print(e)
            db.session.rollback()
            return jsonify(code=400, msg="保存失败")
    else:
        return jsonify(code=400, msg="未通过敏感词检测")
        
        
# 删除日记  我
# 日记表删除
# 前端传来日记id
@app.route('/diary/deleteDiary/', methods=['POST'])
def delete_diary():
    data = request.get_json()
    diary_id = data.get('diary_id')
    get_diary = Diary.query.filter(Diary.diary_id==diary_id).all()
    find_diary =[]  # [p.to_dict() for p in get_pushMsg]
    for p in get_diary:
        find_diary.append(p.to_dict())
    data={"find_diary":find_diary}
    count=len(find_diary)
    if count!=0:  # 是否有数据
        try:
            Diary.query.filter(Diary.diary_id==diary_id).delete()
            db.session.commit() 
            msg="删除成功"
            return jsonify(code=200, msg=msg, data=data)
        except:
            db.session.rollback()
            return jsonify(code=400, msg="删除失败")
    else:
        msg="日记不存在"
        return jsonify(code=200, msg=msg)
        
            
# 推送
# 推送表查询
# 前端传来日记标签
@app.route('/pushMsg', methods=['POST'])
def push_msg():
    data = request.get_json()
    diary_tip = data.get('diary_tip')
    user_id = data.get('user_id')
    try:
        if diary_tip == '日记' :
            # return jsonify(code=300, msg="lll")
            get_pushMsg = PushMsg.query.filter(PushMsg.tips == '治愈').all()
            
        else :
            tips = ["悲伤","生气","焦虑","无语","失望","崩溃","委屈","治愈"]
            user=User.query.filter(User.user_id == user_id).first()
            score = [user.sadness,user.angry,user.anxious,user.speechless,user.disappointmeant,user.collapse,user.grievance,user.cure]
            flag = 0
            for i in range(1,len(score)) :
                if score[i] > score[i-1] :
                    flag=i;
            if score[flag] >5 :
                get_pushMsg = PushMsg.query.filter(PushMsg.tips == tips[flag]).all()
            else :
                get_pushMsg = PushMsg.query.filter(PushMsg.tips == diary_tip).all()
        
        pushMsg = []  # [p.to_dict() for p in get_pushMsg]
        for p in get_pushMsg:
            pushMsg.append(p.to_dict())
        count = len(pushMsg)
        data = {
            "pushMsg": pushMsg
        }
        if count:
            num = random.randint(0, count - 1)
            get_one = pushMsg[num]  #
            return jsonify(code=200, msg="获取成功", data=get_one)
        else:
            get_pushMsg = PushMsg.query.filter(PushMsg.tips == '治愈').all()
            pushMsg = []  # [p.to_dict() for p in get_pushMsg]
            for p in get_pushMsg:
                pushMsg.append(p.to_dict())
            count = len(pushMsg)
            num = random.randint(0, count - 1)
            get_one = pushMsg[num]
            return jsonify(code=200, msg="获取成功", data=get_one)
            # return jsonify(code=200, msg="没有相关推送")
    except:
        return jsonify(code=400, msg="推送失败")


# 推送反馈 
# 推送表查询
# 前端传来日记标签，user_id
@app.route('/like_pushMsg', methods=['POST'])
def like_push_msg():
    data = request.get_json()
    tip = data.get('tip')
    user_id = data.get('user_id')
    is_like = data.get('is_like')
    try:
        if tip != '治愈' :
            user=User.query.filter(User.user_id == user_id).first()
            if is_like==1:
                if tip=="悲伤":
                    user.sadness+=1
                elif tip=="生气":
                    user.angry+=1
                elif tip=="焦虑":
                    user.anxious+=1
                elif tip=="无语":
                    user.speechless+=1
                elif tip=="失望":
                    user.disappointmeant+=1
                elif tip=="崩溃":
                    user.collapse+=1
                elif tip=="委屈":
                    user.grievance+=1
            else:
                if tip=="悲伤":
                    user.sadness-=1
                elif tip=="生气":
                    user.angry-=1
                elif tip=="焦虑":
                    user.anxious-=1
                elif tip=="无语":
                    user.speechless-=1
                elif tip=="失望":
                    user.disappointmeant-=1
                elif tip=="崩溃":
                    user.collapse-=1
                elif tip=="委屈":
                    user.grievance-=1
            db.session.commit()
        return jsonify(code=200, msg="反馈成功")
    except:
        db.session.rollback()
        return jsonify(code=400, msg="反馈失败")


# 获取全部日记  我
# 日记表查询
# 前端传入页数和页总量
@app.route('/diary/getAll', methods=['GET'])
def get_all_diary():
    # data = request.get_json()
    page = int(request.args.get('page'))
    per_page = int(request.args.get('per_page'))
    user_id = request.args.get('user_id')
   
    try:
        # 分页：第一个参数表示页数，第二个参数表示每页条目数，第三个参数分页异常不报错
        get_per_page = Diary.query.filter(Diary.user_id == user_id).order_by(Diary.write_down_time.desc()).paginate(
            page, per_page, False)

        diary_arr = get_per_page.items  # 获取分页后的数据
        page_num = get_per_page.pages  # 获取分页后的总页数
        curpage = get_per_page.page  # 获取当前页数
        all_diary = []
        for p in diary_arr:
            all_diary.append(p.to_dict())
        page_count = len(all_diary)
        if page_count > 0:
            return jsonify(code=200, msg="查询成功", page_num=page_num, curpage=curpage, page_count=page_count, all_diary=all_diary)
        else:
            return jsonify(code=200, msg="没有数据" ,c=per_page)
        
    except:
        return jsonify(code=400, msg="查询失败")


# 根据标签获取日记  我
# 日记表查询
# 前端传入标签、页数、页容量
@app.route('/diary/getByTips', methods=['GET'])
def get_diary_by_tips():
    # data = request.get_json()
    tips = request.args.get('tips')
    page = int(request.args.get('page'))
    per_page = int(request.args.get('per_page'))
    user_id = request.args.get('user_id')
    
    try:
        # 分页：第一个参数表示页数，第二个参数表示每页条目数，第三个参数分页异常不报错
        get_per_page = Diary.query.filter(Diary.user_id == user_id,Diary.tips == tips).order_by(Diary.write_down_time.desc()).paginate(
            page, per_page, False)
        
        diary_arr = get_per_page.items  # 获取分页后的数据
        page_num = get_per_page.pages  # 获取分页后的总页数
        curpage = get_per_page.page  # 获取当前页数
        
        all_diary=[]
        for p in diary_arr:
            all_diary.append(p.to_dict())
        page_count = len(all_diary)
        # return jsonify(code=200, msg="查询成功", page_num=page_num, curpage=curpage, data=diary_arr)
        if page_count>0:
            return jsonify(code=200, msg="查询成功", page_num=page_num, curpage=curpage,page_count=page_count,all_diary=all_diary)
        else:
            return jsonify(code=200, msg="没有数据")
    except:
        return jsonify(code=400, msg="查询失败")


# 我的点赞  我
# 点赞表和树洞表查询    根据找到的点赞找到树洞帖子的信息
# 前端需传入user_id
# 返回是否成功信息，同时返回我点赞的所有树洞，后期可看是否按页返回
@app.route('/treeHole/myLike', methods=['GET'])
def get_my_like():
    user_id = request.args.get('user_id')
    # 先从点赞表中获取我点赞的所有树洞id
    get_all_tree_hole = ClickLike.query.filter(
        ClickLike.user_id == user_id).order_by(ClickLike.time.desc()).all()
    tree_holes=[]
    for item in get_all_tree_hole:
        get_hole = TreeHole.query.filter(TreeHole.tree_hole_id == item.tree_hole_id).all()
        h_arr=[]
        for h in get_hole:
            hole=h.to_dict()
            h_arr.append(hole)
        length=len(h_arr)
        if length>0:
            tree_holes.append(hole)
        else:
            missing_hole={
                'tree_hole_id': "该树洞已删除"
            }
            # tree_holes.append(missing_hole)
    count=len(tree_holes)
    time1=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #return jsonify(a=tree_holes[0]['time'])
    # 通过树洞id去树洞表中找，并将其放进
    return jsonify(code=200, msg="查询成功", count=count,tree_holes=tree_holes)


# 我的评论  我
# 评论表和树洞表查询    根据找到的评论找到树洞帖子信息
# 前端传入user_id
# 返回是否成功信息，同时返回我的所有评论总数以及其对应树洞id
@app.route('/treeHole/myComment', methods=['GET'])
def get_my_comment():
    user_id = request.args.get('user_id')
    # 先从评论表中获取我所有评论的
    get_all_tree_hole=Comment.query.filter(
        Comment.user_id == user_id).order_by(Comment.time.desc()).all()
    tree_holes=[]
    for item in get_all_tree_hole:
        details=item.to_dict()
        get_hole = TreeHole.query.filter(TreeHole.tree_hole_id == item.tree_hole_id).all()
        h_arr=[]
        for h in get_hole:
            hole=h.to_dict()
            h_arr.append(hole)
        length=len(h_arr)
        if length>0:
            tree_holes.append(hole)
            hole['details']=details
        else:
            missing_hole={
                'tree_hole_id': "该树洞已删除",
                'details':details
            }
            # tree_holes.append(missing_hole)
    count=len(tree_holes)
    # 通过树洞id去树洞表中找，并将其放进
    return jsonify(code=200, msg="查询成功", count=count, tree_holes=tree_holes)


# 我的收藏
# 收藏表和树洞表查询    根据找到的收藏找到树洞帖子的信息
# 前端传入user_id
# 返回是否成功信息，同时返回我收藏的所有树洞，后期可看是否按页返回
@app.route('/treeHole/mycollect', methods=['GET'])
def get_my_collect():
    # data = request.get_json()
    user_id = request.args.get('user_id')
    # 先从收藏表中获取我收藏的所有树洞id
    get_all_tree_hole = Collect.query.filter(
        Collect.user_id == user_id).order_by(Collect.time.desc()).all()
    tree_holes = []
    for item in get_all_tree_hole:
        get_hole = TreeHole.query.filter(TreeHole.tree_hole_id == item.tree_hole_id).all()
        h_arr=[]
        for h in get_hole:
            hole=h.to_dict()
            h_arr.append(hole)
        length=len(h_arr)
        if length>0:
            tree_holes.append(hole)
        else:
            missing_hole={
                'tree_hole_id': "该树洞已删除"
            }
            # tree_holes.append(missing_hole)
    count=len(tree_holes)
    return jsonify(code=200, msg="查询成功", count=count, tree_holes=tree_holes)


# 树洞提交
# 需要知道当前用户
# 返回是否成功信息
@app.route('/treeHole/write', methods=['POST'])
def write_tree_hole():
    req_data = request.get_json()
    user_id = req_data.get("user_id")
    content = req_data.get("content")
    # time = req_data.get("time")
    now=datetime.now()
    time=now.strftime("%Y-%m-%d %H:%M:%S")
    tree_hole_id = user_id + time  # str(time)
    data = {
        "tree_hole_id": tree_hole_id
    }
    success = msg_check(content,user_id)
    # return jsonify(code=400, msg=success)
    if success==True:
      post = TreeHole(tree_hole_id=tree_hole_id, user_id=user_id, content=content)  # 新加入的帖子
      try:
          db.session.add(post)  # 插入
          db.session.commit()
          return jsonify(code=200, msg="发送成功", data=data)
      except:
          # print(e)
          db.session.rollback()
          return jsonify(code=400, msg="发送失败")
    else:
        return jsonify(code=400, msg="未通过敏感词检测")


#
# 点赞以及取消点赞
# 需要知道当前用户    传入树洞id号
# 返回是否成功信息以及当前是否点赞
@app.route('/treeHole/GiveALike/', methods=['POST'])
def tree_hole_like():
    req_data = request.get_json()
    user_id = req_data.get("user_id")
    tree_hole_id = req_data.get("tree_hole_id")
    
    get_like = ClickLike.query.filter(ClickLike.user_id == user_id, ClickLike.tree_hole_id == tree_hole_id).all()
    like=[]
    for p in get_like:
        like.append(p.to_dict())
    count = len(like)
    if count>0:  # 是否有数据
        ClickLike.query.filter(ClickLike.user_id == user_id, ClickLike.tree_hole_id == tree_hole_id).delete()
        db.session.commit()
        data = {
            "is_like": False
        }
        hole = TreeHole.query.filter(TreeHole.tree_hole_id == tree_hole_id).first()   # 查询树洞帖子
        if hole.likes>0:
            hole.likes-=1
        db.session.commit()
        return jsonify(code=200, msg="取消点赞成功",data=data,)
    else:
        add_like = ClickLike(tree_hole_id=tree_hole_id, user_id=user_id)
        hole = TreeHole.query.filter(TreeHole.tree_hole_id == tree_hole_id).first()  # 查询树洞帖子
        hole.likes+=1
        data = {
            "is_like": True
        }
        db.session.add(add_like)
        db.session.commit()
        return jsonify(code=200, msg="点赞成功",data=data)
    

# 评论
# 需要知道当前用户    传入树洞id号以及评论内容
# 返回是否成功信息，同时返回该树洞的所有评论（对象数组）供前端进行渲染，后期可看是否按页返回
@app.route('/treeHole/addComment', methods=['POST'])
def tree_hole_add_comment():
    req_data = request.get_json()
    user_id = req_data.get("user_id")
    tree_hole_id = req_data.get("tree_hole_id")
    content = req_data.get("content")
    # time = req_data.get("time")
    now=datetime.now()
    time=now.strftime("%Y-%m-%d %H:%M:%S")
    comment_id = tree_hole_id + time
    data = {
        "comment_id": comment_id
    }
    success = msg_check(content,user_id)
    # return jsonify(code=400, msg=success)
    if success==True:
        add_comment = Comment(comment_id=comment_id, tree_hole_id=tree_hole_id, user_id=user_id, comment_content=content)
        hole = TreeHole.query.filter(TreeHole.tree_hole_id == tree_hole_id).first()  # 查询树洞帖子
        hole.comments+=1
        try:
            db.session.add(add_comment)
            # return jsonify(data=hole.content,res=comment.comment_content)
            db.session.commit()
            return jsonify(code=200, msg="评论成功", data=data)
        
        except:
            db.session.rollback()
            return jsonify(code=400, msg="评论失败")
    else:
        return jsonify(code=400, msg="未通过敏感词检测")
        
    
# 删除评论
# 需要知道当前用户    传入评论id号
# 返回是否成功信息
@app.route('/treeHole/delete_comment', methods=['POST'])
def tree_hole_delete_comment():
    req_data = request.get_json()
    tree_hole_id= req_data.get("tree_hole_id")
    comment_id = req_data.get("comment_id")
    try:
        Comment.query.filter(Comment.comment_id == comment_id).delete()
        hole = TreeHole.query.filter(TreeHole.tree_hole_id == tree_hole_id).first()   # 查询树洞帖子
        if hole.comments>0:
            hole.comments-=1
        db.session.commit()
        return jsonify(code=200, msg="删除成功")
    except:
        db.session.rollback()
        return jsonify(code=400, msg="删除失败")
        

# 收藏以及取消收藏
# 需要知道当前用户    传入树洞id号
# 返回是否成功信息以及当前是否收藏
@app.route('/treeHole/collect', methods=['POST'])
def tree_hole_collect():
    req_data = request.get_json()
    user_id = req_data.get("user_id")
    tree_hole_id = req_data.get("tree_hole_id")
    
    get_collect = Collect.query.filter(Collect.user_id == user_id, Collect.tree_hole_id == tree_hole_id).all()  #没有数据会失败
    collect=[]
    for p in get_collect:
        collect.append(p.to_dict())
    count = len(collect)
    if count>0:  # 是否有数据
        Collect.query.filter(Collect.user_id == user_id, Collect.tree_hole_id == tree_hole_id).delete()
        db.session.commit()
        data = {
            "is_collect": False
        }
        hole = TreeHole.query.filter(TreeHole.tree_hole_id == tree_hole_id).first()   # 查询树洞帖子
        if hole.collects>0:
            hole.collects-=1
        db.session.commit()
        return jsonify(code=200, msg="取消收藏成功",data=data)
    else:
        add_collect = Collect(tree_hole_id=tree_hole_id, user_id=user_id)
        hole = TreeHole.query.filter(TreeHole.tree_hole_id == tree_hole_id).first()  # 查询树洞帖子
        hole.collects+=1
        data = {
            "is_collect": True
        }
        db.session.add(add_collect)
        db.session.commit()
        return jsonify(code=200, msg="收藏成功",data=data)


# 获取树洞
# 传入页数?
# 返回是否成功信息，同时按页返回所有树洞信息（数组）：内容、评论数、点赞数、收藏数
@app.route('/treeHole/getAll', methods=['GET'])
def get_all_tree_hole():
    # req_data = request.get_json()
    page = int(request.args.get("page"))
    per_page = int(request.args.get("per_page"))

    try:
        get_per_page = TreeHole.query.order_by(TreeHole.time.desc()).paginate(
            page, per_page, False)
        
        get_tree_holes = get_per_page.items  # 获取分页后的数据
        page_num = get_per_page.pages  # 获取分页后的总页数
        curpage = get_per_page.page  # 获取当前页数
        tree_holes = []
        for h in get_tree_holes:
            tree_holes.append(h.to_dict())
        page_count = len(tree_holes)
        if page_count > 0:
            return jsonify(code=200, msg="查询成功", page_num=page_num, curpage=curpage, page_count=page_count, tree_holes=tree_holes)
        else:
            return jsonify(code=200, msg="没有数据")
    except:
        return jsonify(code=400, msg="查询失败")
        

# 树洞详情页
# 传入树洞id
# 返回是否成功信息，同时返回该树洞的评论数、点赞数、收藏数、是否点赞/收藏
@app.route('/treeHole/detail/', methods=['GET'])
def detail():
    # req_data = request.get_json()
    tree_hole_id = request.args.get("tree_hole_id")
    user_id = request.args.get("user_id")
    try:
        get_hole = TreeHole.query.filter(TreeHole.tree_hole_id == tree_hole_id).first()  # 树洞数据
        hole = get_hole.to_dict()
        # 获取所有评论
        get_comment=Comment.query.filter(
                Comment.tree_hole_id == tree_hole_id).order_by(Comment.time.desc()).all()
        all_comment=[]  # 所有评论的列表
        for c in get_comment:
            all_comment.append(c.to_dict())
        # 获取我是否有点赞
        get_like = ClickLike.query.filter(ClickLike.user_id == user_id, ClickLike.tree_hole_id == tree_hole_id).all()  #没有数据会失败
        like=[]
        for p in get_like:
            like.append(p.to_dict())
        count = len(like)
        if count>0:  # 我是否有点赞
            is_like = True
        else:
            is_like = False
        # 获取我是否有收藏  
        get_collect = Collect.query.filter(Collect.user_id == user_id, Collect.tree_hole_id == tree_hole_id).all()  #没有数据会失败
        collect=[]
        for p in get_collect:
            collect.append(p.to_dict())
        count_2 = len(collect)
        if count_2>0:  # 我是否有收藏
            is_collect = True
        else:
            is_collect = False
        data = {
            "hole": hole,
            "all_comment": all_comment,
            "is_like": is_like,
            "is_collect":is_collect
        }
        
        return jsonify(code=200, msg="获取成功", data=data)
        
        # return jsonify(code=200, msg="获取成功")
    except:
        db.session.rollback()
        return jsonify(code=400, msg="获取失败")    
        

# 树洞内搜索功能
# 传入搜索词条
# 返回符合条件的所有树洞（按内容查询）
@app.route('/treeHole/search', methods=['GET'])
def tree_hole_search():
    text = request.args.get("text")
    # 关键词分开
    keyword_arr = text.split(' ')
    # 消除空格
    text = text.replace(" ", '')
    try:
        rule = or_(*[TreeHole.content.like('%'+keyword+'%')
                     for keyword in text])
        get_holes = db.session.query(TreeHole).filter(rule).all()
        # get_holes = db.session.query(TreeHole).filter(TreeHole.content.op('%s'%text1)(REGEX))
        tree_holes = []
        for h in get_holes:
            h1 = h.to_dict()
            a = 0
            for k in keyword_arr:
                a += fuzz.partial_ratio(k, h.content)
            h1['order'] = a
            tree_holes.append(h1)

        tree_holes = sorted(tree_holes, key=lambda r: r['order'], reverse=True)
        count = len(tree_holes)
        data = {
            "tree_holes": tree_holes,
            "count": count
        }
        return jsonify(code=200, msg="获取成功", data=data)
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(code=400, msg="获取失败")


# 删除树洞
# 传入树洞id
# 返回是否删除成功
@app.route('/treeHole/delete/', methods=['POST'])
def tree_hole_delete():
    req_data = request.get_json()
    tree_hole_id = req_data.get("tree_hole_id") 
    # user_id = req_data.get("user_id")  
    get_tree_hole = TreeHole.query.filter(TreeHole.tree_hole_id==tree_hole_id).all()
    find_tree_hole =[]  # [p.to_dict() for p in get_pushMsg]
    for h in get_tree_hole:
        find_tree_hole.append(h.to_dict())
    data={"find_tree_hole":find_tree_hole}
    count=len(find_tree_hole)
    if count!=0:
        # 
        try:
            TreeHole.query.filter(TreeHole.tree_hole_id==tree_hole_id).delete()
            db.session.commit() 
            msg="删除成功"
            return jsonify(code=200, msg=msg, data=data)
        except:
            db.session.rollback()
            return jsonify(code=400, msg="删除失败")
    else:
        msg="树洞不存在"
        return jsonify(code=200, msg=msg)


# 获取openid
# 传入code
# 返回获取成功与否和openid
@app.route('/getOpenid', methods=['GET'])
def get_openid():
    # req_data = request.get_json()
    js_code = request.args.get('code')  # req_data.get("code")
    appid = "wx41b775e954cfff86"   #  "wxe21b5675d812d613"  # 
    secret = "95b37aa9b08fc927a2d8472400320eef"   #"cedf7e505c16573b2e3c0591c5a8ac87"  #
    # grant_type =  authorization_code
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid=' + appid + '&secret=' + secret + '&js_code=' + js_code + '&grant_type=authorization_code'
    # return jsonify(code=400, msg="获取失败")
    try:
        r = requests.get(url)
        res = json.loads(r.text)
        open_id = res.get("openid")
        try:
            get_user = User.query.filter(User.user_id == open_id).all()
            users=[]
            for u in get_user:
                users.append(u.to_dict())
            count = len(users)
            if count==0:
                add_user=User(user_id=open_id)
                db.session.add(add_user)
                db.session.commit()
            return jsonify(code= 200, msg="获取成功",res=res)
        except:
            db.session.rollback()
            return jsonify(code=400, msg="获取失败2")
        
    except:
        return jsonify(code=400, msg="获取失败")


# 获取我的树洞
# 树洞表查询
# 前端传入页数和页总量和user_id
@app.route('/treeHole/getMy', methods=['GET'])
def get_my():
    # data = request.get_json()
    page = int(request.args.get('page'))
    per_page = int(request.args.get('per_page'))
    user_id = request.args.get('user_id')
    try:
        # 分页：第一个参数表示页数，第二个参数表示每页条目数，第三个参数分页异常不报错
        get_per_page = TreeHole.query.filter(TreeHole.user_id == user_id).order_by(TreeHole.time.desc()).paginate(
            page, per_page, False)

        tree_hole_arr = get_per_page.items  # 获取分页后的数据
        page_num = get_per_page.pages  # 获取分页后的总页数
        curpage = get_per_page.page  # 获取当前页数
        all_tree_hole = []
        for h in tree_hole_arr:
            all_tree_hole.append(h.to_dict())
        page_count = len(all_tree_hole)
        # return jsonify(code=200, msg="查询成功", page_num=page_num, curpage=curpage, data=diary_arr)
        if page_count > 0:
            return jsonify(code=200, msg="查询成功", page_num=page_num, curpage=curpage, page_count=page_count, all_tree_hole=all_tree_hole)
        else:
            return jsonify(code=200, msg="没有数据" ,c=per_page)
        
        
    except:
        return jsonify(code=400, msg="查询失败")


# 举报
# 需要传入树洞id号，树洞内容以及(评论id和评论内容),被举报user_id,举报理由
# 返回是否操作成功信息
@app.route('/treeHole/report', methods=['POST'])
def tree_hole_report():
    req_data = request.get_json()
    user_id = req_data.get("user_id")
    tree_hole_id = req_data.get("tree_hole_id")  # 帖id
    content = req_data.get("content")  # 树洞内容
    comment_id = req_data.get("comment_id")  # 评论id
    comment_content = req_data.get("comment_content")  # 评论内容
    reason = req_data.get("reason")  # 举报理由
    whether_success = False  # 是否举报成功
    time = datetime.now()
    # time = now.strftime("%Y-%m-%d %H:%M:%S")  # 举报时间
    
    try:
        add_report = Report(user_id=user_id, tree_hole_id=tree_hole_id, content=content, comment_id=comment_id, comment_content=comment_content, reason=reason,whether_success=whether_success)
        db.session.add(add_report)
        db.session.commit()
        return jsonify(code=200, msg="操作成功",data=content)
    
    except:
        db.session.rollback()
        return jsonify(code=400, msg="操作失败")   
        

db.create_all()

if __name__ == '__main__':
    app.run(use_reloader=False, debug=True)