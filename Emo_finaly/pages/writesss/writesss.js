// pages/writes/writes.js
let date = new Date()
let year = date.getFullYear()
let month = date.getMonth()
let day = date.getDate()
var app = getApp()
Page({
  data: {
    info:0,
    _year: year,
    _month: month,
    day: day, 
    neirong:"",
  },

  textinput:function(e){
    var content = e.detail.value;
    var cnt = parseInt(content.length);
    this.setData({
      neirong:content,
      info:cnt
    })
  },
  commentsuccess:function()
  { 
    var that=this
    if (this.data.neirong)
    {
      wx.request({
        url: 'https://luckym.top/treeHole/addComment',
        method: 'post',
        data: {
          user_id:app.globalData.userID,
          tree_hole_id:wx.getStorageSync("hole_id"),
          content:this.data.neirong,
        },
        header: {
          'content-type': 'application/json' // 默认值
        },
        success (res) {
          console.log(res.data)
          if(res.data.msg=="未通过敏感词检测")
        {
          wx.showToast({
            title: '未通过敏感词检测',
            icon: 'none',    //如果要纯文本，不要icon，将值设为'none'
            duration: 1500     
          })          
        }
        else
        {
          wx.showToast({
            title: '发布成功',
            icon: 'none',    //如果要纯文本，不要icon，将值设为'none'
            duration: 1500     
          })
             app.globalData.release=true;//发布成功
             setTimeout(function(){
                wx.navigateBack({
                  delta: 1
                })  
             }.bind(this),1500)        
        }
        
        },
        fail (){
          console.log("保存评论数据失败")
          wx.showToast({
            title: '保存失败，请重试',
            icon: 'none',    //如果要纯文本，不要icon，将值设为'none'
            duration: 1500     
          })   
        }
      })
    }
    else
    {
      wx.showToast({
        title: '当前内容为空，发布失败',
        icon: 'none',    //如果要纯文本，不要icon，将值设为'none'
        duration: 1500     
      })
    }
   
    
  },
  changeParentData: function () {
    var pages =getCurrentPages();//当前页面栈
    if (pages.length >1) {
        var beforePage = pages[pages.length- 2];//获取上一个页面实例对象
        beforePage.changeData();//触发父页面中的方法
    }
  },
})