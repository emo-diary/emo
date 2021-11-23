'''
Author: your name
Date: 2021-11-15 16:09:35
LastEditTime: 2021-11-16 22:43:44
LastEditors: Please set LastEditors
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: \python\1TreeHole\app\api.py
'''
# 各个接口的编写
import flask
from flask import json
from __init__ import db
from models import User, TreeHole, ClickLike, Collect, Comment, Diary, PushMsg
from flask import Flask, request, jsonify, Blueprint, render_template
from flask import abort, redirect, session
from sqlalchemy import extract, and_
from datetime import datetime
import random
app = Flask(__name__)


# 新建日记
@app.route('/diary/addDiary/', methods=['POST'])
def add_diary():
    data = request.get_json()
    diary_content = data.get('diary_content')
    user_id = data.get('user_id')
    tips = data.get('tips')
    now = datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    diary_id = user_id + time
    try:
        diary = Diary(diary_id=diary_id, user_id=user_id, tips=tips,
                      diary_content=diary_content)
        db.session.add(diary)
        db.session.commit()
        return jsonify(code=200, msg="日记保存成功")
    except:
        # print(e)
        db.session.rollback()
        return jsonify(code=400, msg="保存失败")


# 删除日记  我
# 日记表删除
# 前端传来日记id
@app.route('/diary/deleteDiary/', methods=['POST'])
def delete_diary():
    data = request.get_json()
    diary_id = data.get('diary_id')
    get_diary = Diary.query.filter(Diary.diary_id == diary_id).all()
    find_diary = []  # [p.to_dict() for p in get_pushMsg]
    for p in get_diary:
        find_diary.append(p.to_dict())
    data = {"find_diary": find_diary}
    count = len(find_diary)
    if count != 0:  # 是否有数据
        try:
            Diary.query.filter(Diary.diary_id == diary_id).delete()
            db.session.commit()
            msg = "删除成功"
            return jsonify(code=200, msg=msg, data=data)
        except:
            db.session.rollback()
            return jsonify(code=400, msg="删除失败")
    else:
        msg = "日记不存在"
        return jsonify(code=200, msg=msg)


# 推送  我
# 推送表查询
# 前端传来日记标签
@app.route('/pushMsg', methods=['POST'])
def push_msg():
    data = request.get_json()
    diary_tip = data.get('diary_tip')

    try:
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
            return jsonify(code=200, msg="没有相关推送")
    except:
        return jsonify(code=400, msg="推送失败")


# 获取全部日记  我
# 日记表查询
# 前端传入页数和页总量
@app.route('/diary/getAll', methods=['GET'])
def get_all_diary():
    # data = request.get_json()
    page = int(request.args.get('page'))
    per_page = int(request.args.get('per_page'))
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1111
    user_id = request.args.get('user_id')

    try:
        # 分页：第一个参数表示页数，第二个参数表示每页条目数，第三个参数分页异常不报错
        get_per_page = Diary.query.filter(Diary.user_id == user_id).order_by(Diary.write_down_time.desc()).paginate(
            page, per_page, False)
        # objects = db.session.query(Protocols).filter_by(is_default=0).order_by(sqlalchemy.func.field(Protocols.parent_protocol, "ip", "udp", "tcp"))

        diary_arr = get_per_page.items  # 获取分页后的数据
        page_num = get_per_page.pages  # 获取分页后的总页数
        curpage = get_per_page.page  # 获取当前页数
        all_diary = []
        for p in diary_arr:
            all_diary.append(p.to_dict())
        page_count = len(all_diary)
        # return jsonify(code=200, msg="查询成功", page_num=page_num, curpage=curpage, data=diary_arr)
        if page_count > 0:
            return jsonify(code=200, msg="查询成功", page_num=page_num, curpage=curpage, page_count=page_count,
                           all_diary=all_diary)
        else:
            return jsonify(code=200, msg="没有数据", c=per_page)

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
        get_per_page = Diary.query.filter(Diary.user_id == user_id, Diary.tips == tips).order_by(
            Diary.write_down_time.desc()).paginate(
            page, per_page, False)

        diary_arr = get_per_page.items  # 获取分页后的数据
        page_num = get_per_page.pages  # 获取分页后的总页数
        curpage = get_per_page.page  # 获取当前页数

        all_diary = []
        for p in diary_arr:
            all_diary.append(p.to_dict())
        page_count = len(all_diary)
        # return jsonify(code=200, msg="查询成功", page_num=page_num, curpage=curpage, data=diary_arr)
        if page_count > 0:
            return jsonify(code=200, msg="查询成功", page_num=page_num, curpage=curpage, page_count=page_count,
                           all_diary=all_diary)
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
    # data = request.get_json()
    # ！！！！！！！！！！！！！！！！！！！！！
    user_id = request.args.get('user_id')
    # 先从点赞表中获取我点赞的所有树洞id
    get_all_tree_hole = ClickLike.query.filter(
        ClickLike.user_id == user_id).order_by(ClickLike.time.desc()).all()
    tree_holes = []
    for item in get_all_tree_hole:
        get_hole = TreeHole.query.filter(TreeHole.tree_hole_id == item.tree_hole_id).all()
        h_arr = []
        for h in get_hole:
            hole = h.to_dict()
            h_arr.append(hole)
        length = len(h_arr)
        if length > 0:
            tree_holes.append(hole)
        else:
            missing_hole = {
                'tree_hole_id': "该树洞已删除"
            }
            tree_holes.append(missing_hole)
    count = len(tree_holes)
    # 通过树洞id去树洞表中找，并将其放进
    return jsonify(code=200, msg="查询成功", count=count, tree_holes=tree_holes)


# 我的评论  我
# 评论表和树洞表查询    根据找到的评论找到树洞帖子信息
# 前端不用穿任何数据
# 返回是否成功信息，同时返回我的所有评论总数以及其对应树洞id
@app.route('/treeHole/myComment', methods=['GET'])
def get_my_comment():
    # data = request.get_json()
    # ！！！！！！！！！！！！！！！！！！！！！
    user_id = request.args.get('user_id')
    # 先从评论表中获取我所有评论的
    get_all_tree_hole = Comment.query.filter(
        Comment.user_id == user_id).order_by(Comment.time.desc()).all()
    tree_holes = []
    for item in get_all_tree_hole:
        get_hole = TreeHole.query.filter(TreeHole.tree_hole_id == item.tree_hole_id).all()
        h_arr = []
        for h in get_hole:
            hole = h.to_dict()
            h_arr.append(hole)
        length = len(h_arr)
        if length > 0:
            tree_holes.append(hole)
            details = item.to_dict()
            hole['details'] = details
        else:
            missing_hole = {
                'tree_hole_id': "该树洞已删除",
                'details': details
            }
            tree_holes.append(missing_hole)
    count = len(tree_holes)
    # 通过树洞id去树洞表中找，并将其放进
    return jsonify(code=200, msg="查询成功", count=count, tree_holes=tree_holes)


# 我的收藏
# 收藏表和树洞表查询    根据找到的收藏找到树洞帖子的信息
# 前端无需传入任何数据
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
        h_arr = []
        for h in get_hole:
            hole = h.to_dict()
            h_arr.append(hole)
        length = len(h_arr)
        if length > 0:
            tree_holes.append(hole)
        else:
            missing_hole = {
                'tree_hole_id': "该树洞已删除"
            }
            tree_holes.append(missing_hole)
    count = len(tree_holes)
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
    now = datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    tree_hole_id = user_id + time  # str(time)
    data = {
        "tree_hole_id": tree_hole_id
    }
    post = TreeHole(tree_hole_id=tree_hole_id, user_id=user_id, content=content)  # 新加入的帖子
    try:
        db.session.add(post)  # 插入
        db.session.commit()
        return jsonify(code=200, msg="发送成功", data=data)
    except:
        # print(e)
        db.session.rollback()
        return jsonify(code=400, msg="发送失败")


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
    like = []
    for p in get_like:
        like.append(p.to_dict())
    count = len(like)
    if count > 0:  # 是否有数据
        ClickLike.query.filter(ClickLike.user_id == user_id, ClickLike.tree_hole_id == tree_hole_id).delete()
        db.session.commit()
        data = {
            "is_like": False
        }
        hole = TreeHole.query.filter(TreeHole.tree_hole_id == tree_hole_id).first()  # 查询树洞帖子
        if hole.likes > 0:
            hole.likes -= 1
        db.session.commit()
        return jsonify(code=200, msg="取消点赞成功", data=data, )
    else:
        add_like = ClickLike(tree_hole_id=tree_hole_id, user_id=user_id)
        hole = TreeHole.query.filter(TreeHole.tree_hole_id == tree_hole_id).first()  # 查询树洞帖子
        hole.likes += 1
        data = {
            "is_like": True
        }
        db.session.add(add_like)
        db.session.commit()
        return jsonify(code=200, msg="点赞成功", data=data)


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
    now = datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    comment_id = tree_hole_id + time
    data = {
        "comment_id": comment_id
    }
    add_comment = Comment(comment_id=comment_id, tree_hole_id=tree_hole_id, user_id=user_id, comment_content=content)
    hole = TreeHole.query.filter(TreeHole.tree_hole_id == tree_hole_id).first()  # 查询树洞帖子
    hole.comments += 1
    try:
        db.session.add(add_comment)
        db.session.commit()
        return jsonify(code=200, msg="评论成功", data=data)

    except:
        db.session.rollback()
        return jsonify(code=400, msg="评论失败")


# 删除评论
# 需要知道当前用户    传入评论id号
# 返回是否成功信息
@app.route('/treeHole/delete_comment', methods=['POST'])
def tree_hole_delete_comment():
    req_data = request.get_json()
    tree_hole_id = req_data.get("tree_hole_id")
    comment_id = req_data.get("comment_id")
    try:
        Comment.query.filter(Comment.comment_id == comment_id).delete()
        hole = TreeHole.query.filter(TreeHole.tree_hole_id == tree_hole_id).first()  # 查询树洞帖子
        if hole.comments > 0:
            hole.comments -= 1
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

    get_collect = Collect.query.filter(Collect.user_id == user_id,
                                       Collect.tree_hole_id == tree_hole_id).all()  # 没有数据会失败
    collect = []
    for p in get_collect:
        collect.append(p.to_dict())
    count = len(collect)
    if count > 0:  # 是否有数据
        Collect.query.filter(Collect.user_id == user_id, Collect.tree_hole_id == tree_hole_id).delete()
        db.session.commit()
        data = {
            "is_collect": False
        }
        hole = TreeHole.query.filter(TreeHole.tree_hole_id == tree_hole_id).first()  # 查询树洞帖子
        if hole.collects > 0:
            hole.collects -= 1
        db.session.commit()
        return jsonify(code=200, msg="取消收藏成功", data=data)
    else:
        add_collect = Collect(tree_hole_id=tree_hole_id, user_id=user_id)
        hole = TreeHole.query.filter(TreeHole.tree_hole_id == tree_hole_id).first()  # 查询树洞帖子
        hole.collects += 1
        data = {
            "is_collect": True
        }
        db.session.add(add_collect)
        db.session.commit()
        return jsonify(code=200, msg="收藏成功", data=data)


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
            return jsonify(code=200, msg="查询成功", page_num=page_num, curpage=curpage, page_count=page_count,
                           tree_holes=tree_holes)
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
        get_comment = Comment.query.filter(
            Comment.tree_hole_id == tree_hole_id).order_by(Comment.time.desc()).all()
        all_comment = []  # 所有评论的列表
        for c in get_comment:
            all_comment.append(c.to_dict())
        # 获取我是否有点赞
        get_like = ClickLike.query.filter(ClickLike.user_id == user_id,
                                          ClickLike.tree_hole_id == tree_hole_id).all()  # 没有数据会失败
        like = []
        for p in get_like:
            like.append(p.to_dict())
        count = len(like)
        if count > 0:  # 我是否有点赞
            is_like = True
        else:
            is_like = False
        # 获取我是否有收藏
        get_collect = Collect.query.filter(Collect.user_id == user_id,
                                           Collect.tree_hole_id == tree_hole_id).all()  # 没有数据会失败
        collect = []
        for p in get_collect:
            collect.append(p.to_dict())
        count_2 = len(collect)
        if count_2 > 0:  # 我是否有收藏
            is_collect = True
        else:
            is_collect = False
        data = {
            "hole": hole,
            "all_comment": all_comment,
            "is_like": is_like,
            "is_collect": is_collect
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
    # req_data = request.get_json()
    text = request.args.get("text")
    try:
        get_holes = db.session.query(TreeHole).filter(TreeHole.content.like('%{keyword}%'.format(keyword=text))).all()

        tree_holes = []
        for h in get_holes:
            tree_holes.append(h.to_dict())
        count = len(tree_holes)

        # hole = [h.to_dict() for h in get_holes.items]  # 对每个查询结果转化
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
    get_tree_hole = TreeHole.query.filter(TreeHole.tree_hole_id == tree_hole_id).all()
    find_tree_hole = []  # [p.to_dict() for p in get_pushMsg]
    for h in get_tree_hole:
        find_tree_hole.append(h.to_dict())
    data = {"find_tree_hole": find_tree_hole}
    count = len(find_tree_hole)
    if count != 0:
        try:
            TreeHole.query.filter(TreeHole.tree_hole_id == tree_hole_id).delete()
            db.session.commit()
            msg = "删除成功"
            return jsonify(code=200, msg=msg, data=data)
        except:
            db.session.rollback()
            return jsonify(code=400, msg="删除失败")
    else:
        msg = "树洞不存在"
        return jsonify(code=200, msg=msg)


@app.route('/getOpenid', methods=['GET'])
def get_openid():
    # req_data = request.get_json()
    js_code = request.args.get('code')  # req_data.get("code")
    appid = "wx41b775e954cfff86"  # "wxe21b5675d812d613"  #
    secret = "95b37aa9b08fc927a2d8472400320eef"  # "cedf7e505c16573b2e3c0591c5a8ac87"  #
    # grant_type =  authorization_code
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid=' + appid + '&secret=' + secret + '&js_code=' + js_code + '&grant_type=authorization_code'
    # return jsonify(code=400, msg="获取失败")
    try:
        r = requests.get(url)
        res = json.loads(r.text)
        open_id = res.get("openid")
        return jsonify(code=200, msg="获取成功", res=res)
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
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1111
    user_id = request.args.get('user_id')
    try:
        # 分页：第一个参数表示页数，第二个参数表示每页条目数，第三个参数分页异常不报错
        get_per_page = TreeHole.query.filter(TreeHole.user_id == user_id).order_by(TreeHole.time.desc()).paginate(
            page, per_page, False)
        # objects = db.session.query(Protocols).filter_by(is_default=0).order_by(sqlalchemy.func.field(Protocols.parent_protocol, "ip", "udp", "tcp"))

        tree_hole_arr = get_per_page.items  # 获取分页后的数据
        page_num = get_per_page.pages  # 获取分页后的总页数
        curpage = get_per_page.page  # 获取当前页数
        all_tree_hole = []
        for h in tree_hole_arr:
            all_tree_hole.append(h.to_dict())
        page_count = len(all_tree_hole)
        # return jsonify(code=200, msg="查询成功", page_num=page_num, curpage=curpage, data=diary_arr)
        if page_count > 0:
            return jsonify(code=200, msg="查询成功", page_num=page_num, curpage=curpage, page_count=page_count,
                           all_tree_hole=all_tree_hole)
        else:
            return jsonify(code=200, msg="没有数据", c=per_page)


    except:
        return jsonify(code=400, msg="查询失败")


if __name__ == '__main__':
    app.run()
