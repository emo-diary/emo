var app = getApp()
Page({
  data:{
    text:String,
    array:[],
    count:0,
    picNum:[1,3,2,0,2,1,3,0],
    name:["小鳄鱼","小松鼠","长颈鹿","鸭鸭","长颈鹿","小鳄鱼","小松鼠","鸭鸭"],
    pageNum:1,
  }, 
  onShow:function(){
    
    var that=this
    wx.request({
      url: 'https://luckym.top/treeHole/search',
      method: 'get',
      data: {
        text:this.data.text
      },
      header: {
        'content-type': 'application/json' // 默认值
      },
      success (res) {
        console.log("res.data："+res.data)
        console.log(res)
        if(res.data.msg=="没有数据"){
            that.setData({
            array:[],
            count:0,
          })
        } 
        else {
          that.setData({
            array:res.data.data.tree_holes,
            count:res.data.data.count
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
      },
    })
    console.log("数组数据为："+this.data.array)
    
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
  url: 'https://luckym.top/treeHole/getAll',
  method: 'get',
  data: {
    page: 1,
    per_page:5,
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
            // name: (Math.random() * 100000 + 200000).toFixed(0),
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

  // 搜索
  gosearch:function(){
    wx.getSetting({
      success (res){
        if (res.authSetting['scope.userInfo']) {
          // 已经授权
          console.log('已经授权');
          wx.navigateTo({
            url: '../search_result/search_result',
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
 
 
  onLoad: function () {
    

     //接受搜索文本
    console.log("receive: "+this.options.text);
    this.setData({
      text :this.options.text
    })
    console.log("设置搜索文本"+this.data.text)
    // this.get_result()

  },
  searchContent:function(event){
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
    console.log(event)
    console.log(event.currentTarget.dataset.id)
    var idkey=event.currentTarget.dataset.id;
    this.setData({
       idkey:idkey
    })
    wx.setStorageSync('hole_id', this.data.array[idkey].tree_hole_id);
    wx.setStorageSync('u_id', this.data.array[idkey].user_id);
    wx.showActionSheet({
    itemList: ['删除', '举报'],//显示的列表项
    success: function (res) { //res.tapIndex点击的列表项
       console.log("点击了列表项：" + that[res.tapIndex])
       console.log(res.tapIndex)
       if(res.tapIndex) 
        wx.navigateTo({
          url: '../complain/complain?idkey='+idkey,
        })
       else{
        wx.showToast({
          title: '请前往 [我的树洞]',
          icon: 'none',    //如果要纯文本，不要icon，将值设为'none'
          duration: 1500     
        })
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
  changeParentData: function () {
    console.log("1234567")
    var pages =getCurrentPages();//当前页面栈
    if (pages.length >1) {
        var beforePage = pages[pages.length- 2];//获取上一个页面实例对象
        beforePage.changeData();//触发父页面中的方法
    }
  },
  changeData:function(){
    var that=this
    this.setData({
      pageNum:1,
      search_text :null
    })
wx.request({
  url: 'https://luckym.top/treeHole/getAll',
  method: 'get',
  data: {
    page: 1,
    per_page:5,
  },
  header: {
    'content-type': 'application/json' // 默认值
  },
  success (res) {
    if(res.data.msg=="没有数据")
        {
          that.setData({
          array:[],
          search_text :null
        })
        } else {
          that.setData({
            array:res.data.tree_holes,
            // name: (Math.random() * 100000 + 200000).toFixed(0),
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
}
})