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
    comment_id:"",
    comment_content:"",
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
    if (this.data.neirong)
    {
      console.log(app.globalData.userID)
      console.log(this.data.content_wrap.content)
      console.log(wx.getStorageSync("hole_id"))
      console.log(this.data.neirong)
      wx.request({
        url: 'https://luckym.top/treeHole/report',
        method: 'post',
        data: {
          user_id:app.globalData.userID,
          content:this.data.content_wrap.content,
          tree_hole_id:wx.getStorageSync("hole_id"),
          comment_id:this.data.comment_id,
          comment_content:this.data.comment_content,
          reason:this.data.neirong,

        },
        header: {
          'content-type': 'application/json' // 默认值
        },
        success (res) {
          console.log(res.data)

          wx.showToast({
            title: '提交成功',
            icon: 'none',    //如果要纯文本，不要icon，将值设为'none'
            duration: 1500     
          })
          app.globalData.release=true;
          setTimeout(function(){
            wx.navigateBack({
              delta: 1
            })  
          }.bind(this),1500)
  
        },
        fail (){
          console.log("保存评论数据失败")
          wx.showToast({
            title: '提交失败',
            icon: 'none',    //如果要纯文本，不要icon，将值设为'none'
            duration: 1500     
          })
        }
      })
    }
    else
    {
      wx.showToast({
        title: '当前内容为空，提交失败',
        icon: 'none',    //如果要纯文本，不要icon，将值设为'none'
        duration: 1500     
      })
    }
   
    
  },
  
  onLoad: function (options) {
    var idkey=options.idkey;
    this.setData({
      idkey:idkey,
      hole_id:wx.getStorageSync("hole_id"),
      u_id:wx.getStorageSync("u_id"),
      comment_id:wx.getStorageSync("comment_id"),
      comment_content:wx.getStorageSync("comment_content"),
    });
    console.log("举报页面获取到评论的内容是"+this.data.comment_content)
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
        console.log(res)
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
  },
  onShow: function () {
    this.setData({
      hole_id:wx.getStorageSync("hole_id"),
      u_id:wx.getStorageSync("u_id"),
      comment_id:wx.getStorageSync("comment_id"),
      comment_content:wx.getStorageSync("comment_content"),
    });
    // console.log("举报页面获取到评论的内容是"+this.data.comment_content)
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
        console.log(res)
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
  },
})