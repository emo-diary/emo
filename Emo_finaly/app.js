// app.js

App({
  globalData: {
    deleteDiary:false,
    diasucc:false,
    release:false,
    deletetree:false,
    code:null,
    userInfo: null,
    userID:null,
    openId:null,
  },
  onLaunch() {
    // 展示本地存储能力
    const logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)
    var that = this

}
 
})