const date = new Date()
const years = []
const months = []
const days = []
var app = getApp()
for (let i = 1990; i <= date.getFullYear(); i++) {
  years.push(i)
}

for (let i = 1; i <= 12; i++) {
  months.push(i)
}

for (let i = 1; i <= 31; i++) {
  days.push(i)
}
Page({
  data: {
    idkey:-1,
    scrollTop:0,
    content:"",
    mood:"",
    day:"",
    month:"",
    year:"",
    diary_id:''
  }, 

  onLoad: function (options) {
    console.log(app.globalData.userID)
    var idkey=options.idkey;
    this.setData({
      idkey:idkey,
      mood:wx.getStorageSync("d_mood"),
      content:wx.getStorageSync("d_content"),
      month:wx.getStorageSync("d_time"),
      diary_id:wx.getStorageSync("d_id"),
    });
  },
  deleteDia:function(){
    var that=this;

    
    wx.showModal({
      title: '提示',
      content: '确认删除这篇日记吗',
      success (res) {
      if (res.confirm) {
        wx.request({
          url: 'https://luckym.top/diary/deleteDiary/',
          method: 'post',
          header:{
            'content-type': 'application/json' // 默认值
          },
          data: {
            diary_id:that.data.diary_id,
          },
          success:function(res){
            // that.data.content=res.data.content;
            console.log("删除成功")
          },
          fail:function(){
            console.log("删除失败")
          }
        })
        app.globalData.deleteDiary=true;
        wx.showToast({
          title: '删除成功',
          icon: 'none',    //如果要纯文本，不要icon，将值设为'none'
          duration: 1500     
        })
        setTimeout(function(){
          wx.navigateBack({
            delta: 1
          })  
        }.bind(this),1000)
      } else if (res.cancel) {
          // console.log('用户点击取消')
      }
      }
    })
  },
})