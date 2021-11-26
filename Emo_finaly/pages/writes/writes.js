// pages/writes/writes.js
let date = new Date()
let year = date.getFullYear()
let month = date.getMonth()
let day = date.getDate()
var app = getApp()
var util = require('../../utils/util.js');
Page({
  data: {
    info:0,
    _year: year,
    _month: month,
    day: day, 
    neirong:"",
    tree_hole_id:"",
    specific_t:""
  },

  textinput:function(e){
    var content = e.detail.value;
    var cnt = parseInt(content.length);
    this.setData({
      neirong:content,
      info:cnt
    })
  },
  releasesuccess:function()
  {
    let that = this;
     let currentTime = util.formatTime(new Date());
     that.setData({
      specific_t: currentTime,
     })
    wx.setStorageSync('s_day', this.data.day);
    wx.setStorageSync('s_year', this.data._year);
    wx.setStorageSync('s_month', this.data._month+1);
    wx.setStorageSync('s_content', this.data.neirong);
    wx.setStorageSync('s_time', this.data.specific_t);
    if (this.data.neirong)
    {
      wx.request({
        url: 'https://luckym.top//treeHole/write',
        method: 'post',
        data: {
          content:this.data.neirong,
          user_id:app.globalData.userID,
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
            title: '保存成功',
            icon: 'none',    //如果要纯文本，不要icon，将值设为'none'
            duration: 1500     
          })
          that.setData({
            tree_hole_id: res.data.tree_hole_id,
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
          console.log("保存日记数据失败")
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

   
    
    
  }
})