var app = getApp()
// pages/detail/detail.js
Page({
  data: {
    idkey:0,
    hole_id:"",
    u_id:"",
    //帖子详情
    post_id:3,
    picNum:[1,3,2,0,2,1,3,0],
    name:["小鳄鱼","小松鼠","长颈鹿","鸭鸭","长颈鹿","小鳄鱼","小松鼠","鸭鸭"],
    is_like:false,
    is_collect:false,
    collects:Number,
    comments:Number,
    focus: false,
    content_wrap:{},
    //评论列表
    array:[]
  },
  onLoad: function (options) {
    var idkey=options.idkey;
    this.setData({
      idkey:idkey,
      hole_id:wx.getStorageSync("hole_id"),
      u_id:wx.getStorageSync("u_id"),
    });
    var that=this
    wx.request({
      url: 'https://luckym.top//treeHole/detail/',
      method: 'get',
      data: {
        tree_hole_id:this.data.hole_id,
        user_id:this.data.u_id,
      },
      header: {
        'content-type': 'application/json' // 默认值
      },
      success (res) {
        // console.log(res)
        that.setData({
          array: res.data.data.all_comment,
          content_wrap:res.data.data.hole,
          is_like:      res.data.data.is_like,
          is_collect:   res.data.data.is_collect
         })
      },
      fail (){
        wx.showToast({
          title: '获取失败，请稍后重试',
          icon:'none',
          duration:2500,
        })
      }
    })
  },
  onShow: function () {
    // var idkey=options.idkey;
    this.setData({
      hole_id:wx.getStorageSync("hole_id"),
      u_id:wx.getStorageSync("u_id"),
    });
    var that=this
    wx.request({
      url: 'https://luckym.top//treeHole/detail/',
      method: 'get',
      data: {
        tree_hole_id:this.data.hole_id,
        user_id:this.data.u_id,
      },
      header: {
        'content-type': 'application/json' // 默认值
      },
      success (res) {
        // console.log(res)
        that.setData({
          array: res.data.data.all_comment,
          content_wrap:res.data.data.hole,
         })
      },
      fail (){
        wx.showToast({
          title: '获取失败，请稍后重试',
          icon:'none',
          duration:2500,
        })
      }
    })
    that.changeParentData()
  },
  
  //评论编辑函数
  editDairy:function(){
    if (app.globalData.userInfo!=null) {
      // 已经授权
      wx.navigateTo({
        url: '../writesss/writesss',
      })
    }else{
       wx.reLaunch({
        url: '../login1/login1',
        })
    }
  },
  //点赞
  add_dianzan(){
    var that=this
    var addchange="content_wrap.likes"  
    wx.request({
      url: 'https://luckym.top/treeHole/GiveALike/',
      method: 'post',
      data: {
        user_id: app.globalData.userID,
        tree_hole_id: this.data.content_wrap.tree_hole_id,
      },
      header: {
        'content-type': 'application/json' // 默认值
      },
      success (res) {
        console.log(res)
        var is_like=res.data.data.is_like
        console.log("is_like: "+is_like)
        if(is_like){
          that.setData({
            [addchange]: that.data.content_wrap.likes + 1
          })
        }
        else{
          that.setData({
             [addchange]: that.data.content_wrap.likes - 1
          })
        }
        that.changeParentData()
      },
      fail (){
        wx.showToast({
          title: '获取失败，请稍后重试',
          icon:'none',
          duration:2500,
        })
      }
    })


  },
  //收藏
  add_collect(){
    var that=this
    var addchange="content_wrap.collects"  
    wx.request({
      url: 'https://luckym.top/treeHole/collect',
      method: 'post',
      data: {
        user_id: app.globalData.userID,
        tree_hole_id: this.data.content_wrap.tree_hole_id,
      },
      header: {
        'content-type': 'application/json' // 默认值
      },
      success (res) {
        console.log(res)
        var is_collect=res.data.data.is_collect
        console.log("is_like: "+is_collect)
        if(is_collect){
          that.setData({
            [addchange]: that.data.content_wrap.collects + 1
          })
        }
        else{
          that.setData({
             [addchange]: that.data.content_wrap.collects - 1
          })
        }
        that.changeParentData()
      },
      fail (){
        wx.showToast({
          title: '获取失败，请稍后重试',
          icon:'none',
          duration:2500,
        })
      }
    })


  },

  choiceop:function(event){
    var that=this
    wx.setStorageSync('hole_id', this.data.hole_id);
    wx.setStorageSync('u_id', this.data.u_id);
    wx.showActionSheet({
    itemList: ['删除', '举报'],//显示的列表项
    success: function (res) { //res.tapIndex点击的列表项
       console.log("点击了列表项：" + that[res.tapIndex])
       console.log(res.tapIndex)
       if(res.tapIndex) 
        wx.navigateTo({
          url: '../complain/complain',
        })
       else{
        wx.showToast({
          title: '请前往 [我的树洞]',
          icon: 'none',    //如果要纯文本，不要icon，将值设为'none'
          duration: 1500     
        })
       }
       that.changeParentData()
    },
    fail: function (res) { 
      console.log("操作失败")
    },
    complete:function(res){
      console.log("操作完成")
    }
  })

  },

  choiceopcomment:function(event){
    var that=this
    console.log(event)
    console.log(event.currentTarget.dataset.id)
    var idkey=event.currentTarget.dataset.id;
    this.setData({
       idkey:idkey
    })
    console.log(this.data.array[idkey].comment_content)
    
    wx.setStorageSync('hole_id', this.data.hole_id);
    wx.setStorageSync('u_id', this.data.u_id);
    wx.setStorageSync('comment_id', this.data.array[idkey].comment_id);
    wx.setStorageSync('comment_content', this.data.array[idkey].comment_content);
    wx.showActionSheet({
    itemList: ['删除', '举报'],//显示的列表项
    success: function (res) { //res.tapIndex点击的列表项
       console.log("点击了列表项：" + that[res.tapIndex])
       console.log(res.tapIndex)
       if(res.tapIndex) 
        wx.navigateTo({
          url: '../complain_comment/complain_comment?idkey=idkey'+idkey,
        })
       else{
        wx.showToast({
          title: '请前往 [我的评论]',
          icon: 'none',    //如果要纯文本，不要icon，将值设为'none'
          duration: 1500     
        })
       }
       that.changeParentData()
    },
    fail: function (res) { 
      console.log("操作失败")
    },
    complete:function(res){
      console.log("操作完成")
    }
  })

  },

  changeParentData: function () {
    var pages =getCurrentPages();//当前页面栈
    if (pages.length >1) {
        var beforePage = pages[pages.length- 2];//获取上一个页面实例对象
        beforePage.changeData();//触发父页面中的方法
    }
  }
  
})