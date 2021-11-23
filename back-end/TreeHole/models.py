'''
Author: your name
Date: 2021-11-15 16:09:42
LastEditTime: 2021-11-16 22:13:00
LastEditors: Please set LastEditors
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: \python\1TreeHole\app\models.py
'''
# 数据模型
from __init__ import db
from datetime import datetime

# 声明模型类

# 用户表：
# 用户id
# openid varchar(200)


class TreeHole(db.Model):
    __tablename__ = "TreeHole"  # 设置表名
    tree_hole_id = db.Column(db.String(50), primary_key=True)  # 帖id
    user_id = db.Column(db.String(50), nullable=False, index=True)  # 用户id
    content = db.Column(db.String(2000), nullable=False)  # 帖内容!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    time = db.Column(db.DateTime, nullable=False, default=datetime.now)  # 时间
    likes = db.Column(db.Integer, default=0)  # 点赞数
    comments = db.Column(db.Integer, default=0)  # 评论数
    collects = db.Column(db.Integer, default=0)  # 点赞数

    def to_dict(self):
        data = {
            'tree_hole_id': self.tree_hole_id,
            'user_id': self.user_id,
            'content': self.content,
            'time': self.time,
            'likes': self.likes,
            'comments': self.comments,
            'collects': self.collects,
            # 'comments': url_for('get_comment_json', article_id=self.id),  # 这里返回一个路由
            # 'new_comment': {'comments': self.filter_c}  # 创建过滤函数，查询所有评论
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
            'time': self.time
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
            'time': self.time
        }
        return data


class Comment(db.Model):
    __tablename__ = "Comment"  # 设置表名
    comment_id = db.Column(db.String(120), primary_key=True)  # 评论id
    # parentCommentId = db.Column(db.String(50), primary_key=True)  # 父评论id
    tree_hole_id = db.Column(db.String(50), primary_key=True)  # 帖id
    user_id = db.Column(db.String(50), index=True)  # 用户id
    comment_content = db.Column(db.String(2000), nullable=False)  # 评论内容!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    time = db.Column(db.DateTime, nullable=False, default=datetime.now)  # 时间

    def to_dict(self):
        data = {
            'tree_hole_id': self.tree_hole_id,
            'user_id': self.user_id,
            'comment_id': self.comment_id,
            'comment_content': self.comment_content,
            'time': self.time
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

    '''__mapper_args__ = {
         "order_by": write_down_time.desc()
    }'''

    def to_dict(self):
        data = {
            'diary_id': self.diary_id,
            'user_id': self.user_id,
            'tips': self.tips,
            'diary_content': self.diary_content,
            'write_down_time': self.write_down_time
        }
        return data


class PushMsg(db.Model):
    __tablename__ = "PushMsg"
    pushmsg_id = db.Column(db.String(50), primary_key=True)  # 推送id
    content = db.Column(db.String(5000), nullable=False)  # 推送内容!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
    tips = db.Column(db.String(50))  # 推送标签!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    def to_dict(self):
        data = {
            'pushmsg_id': self.pushmsg_id,
            'content': self.content,
            'tips': self.tips
        }
        return data


try:
    db.create_all()    # 创建当前应用中声明的所有模型类对应的数据表，db.drop_all()是删除表
except:
    pass
