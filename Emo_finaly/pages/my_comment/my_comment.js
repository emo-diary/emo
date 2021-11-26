var app = getApp()
Page({
  data:{
    array:[],
    picNum:[1,3,2,0,2,1,3,0],
    name:["小鳄鱼","小松鼠","长颈鹿","鸭鸭","长颈鹿","小鳄鱼","小松鼠","鸭鸭"]
  },
  onLoad:function(){
    var that=this;
    wx.request({
      url: 'https://luckym.top/treeHole/myComment',
      method: 'get',
      data: {
        user_id:app.globalData.userID,
      },
      header: {
        'content-type': 'application/json' // 默认值
      },
      success (res) {
        if(res.data.msg=="没有数据")
            {
              that.setData({
              array:[],
            })
            } else {
              that.setData({
                array:res.data.tree_holes,
              })        
        }
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
  // 编辑树洞帖子
  editDairy:function(){
    wx.getSetting({
      success (res){
        if (res.authSetting['scope.userInfo']) {
          // 已经授权
          console.log('已经授权');
          wx.navigateTo({
            url: '../writes/writes',
          })
        }else{
          console.log('未授权');
          wx.navigateTo({
            url: '../login2/login2',
          })
        }
      }
    })
  },
  changeData:function(){
    var that=this
    this.setData({
      pageNum:1
    })
    wx.request({
      url: 'https://luckym.top/treeHole/myComment',
      method: 'get',
      data: {
        user_id:app.globalData.userID,
      },
      header: {
        'content-type': 'application/json' // 默认值
      },
      success (res) {
        console.log(res)
        if(res.data.msg=="没有数据")
            {
              that.setData({
              array:[],
            })
            } else {
              that.setData({
                array:res.data.tree_holes,
              })        
        }
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
  //点赞
  add_dianzan(e){
    var that=this
    var idkey=e.currentTarget.dataset.id;
    // console.log(e)
    idkey=idkey.substr(0,idkey.length-1)
    var addchange="array["+idkey+"].likes"
    // console.log(idkey)
    // console.log(this.data.array[idkey])
    // console.log("tree_hole_id： "+this.data.array[idkey].tree_hole_id)
    wx.request({
      url: 'https://luckym.top/treeHole/GiveALike/',
      method: 'post',
      data: {
        user_id: app.globalData.userID,
        tree_hole_id: this.data.array[idkey].tree_hole_id,
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
            [addchange]:that.data.array[idkey].likes+1
          })
        }
        else{
          that.setData({
            [addchange]:that.data.array[idkey].likes-1
          })
        }
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
  add_collect(e){
    var that=this
    var idkey=e.currentTarget.dataset.id;
    // console.log(e)
    idkey=idkey.substr(0,idkey.length-1)
    var addchange="array["+idkey+"].collects"
    wx.request({
      url: 'https://luckym.top/treeHole/collect',
      method: 'post',
      data: {
        user_id: app.globalData.userID,
        tree_hole_id: this.data.array[idkey].tree_hole_id,
      },
      header: {
        'content-type': 'application/json' // 默认值
      },
      success (res) {
        console.log(res)
        var is_collect=res.data.data.is_collect
        console.log("is_collect: "+is_collect)
        if(is_collect){
          that.setData({
            [addchange]:that.data.array[idkey].collects+1
          })
        }
        else{
          that.setData({
            [addchange]:that.data.array[idkey].collects-1
          })
        }
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
  //评论
  add_comment(e){
    wx.navigateTo({
      url: '../detail/detail',
    })
  },
  dianzanContent:function(event){
    var idkey=event.currentTarget.dataset.id;
    this.setData({
      idkey:idkey
    })
    wx.setStorageSync('hole_id', this.data.array[idkey].tree_hole_id);
    wx.setStorageSync('u_id', this.data.array[idkey].user_id);
    wx.navigateTo({
      url: '../detail/detail?idkey='+idkey,
    })
  },

  choiceop:function(event){
    var that=this
    // console.log(event)
    // console.log(event.currentTarget.dataset.id)
    var idkey=event.currentTarget.dataset.id;
    this.setData({
       idkey:idkey
    })
    wx.setStorageSync('hole_id', this.data.array[idkey].tree_hole_id);
    wx.setStorageSync('u_id', this.data.array[idkey].user_id);
    wx.showActionSheet({
    itemList: ['删除评论'],//显示的列表项
    success: function (res) { //res.tapIndex点击的列表项
      //  console.log("点击了列表项：" + that[res.tapIndex])
      //  console.log(res.tapIndex)
       if(!(res.tapIndex)) {
        //  console.log("确认删除")
         wx.request({
          url: 'https://luckym.top/treeHole/delete_comment',
          method: 'post',
          data: {
            tree_hole_id: that.data.array[idkey].tree_hole_id,
            comment_id: that.data.array[idkey].details.comment_id
          },
          header: {
            'content-type': 'application/json' // 默认值
          },
          success (res) {
            // wx.redirectTo({
            //   url: '../my_comment/my_comment',
            // })
            that.changeData()
            wx.showToast({
              title: '删除成功',
              icon:'none',
              duration:2500,
            })
          },
          fail (){
            wx.showToast({
              title: '删除失败',
              icon:'none',
              duration:2500,
            })
          }
        })
       }
       else{
        console.log("取消删除")
       }
    },
    fail: function (res) { 
      console.log("操作失败")
    },
    complete:function(res){
      console.log("操作完成")
    }
  })

  },

})