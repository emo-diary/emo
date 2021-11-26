// components/Searchinput/Searchinput.js
Component({
  /**
   * 组件的属性列表
   */
  properties: {

  },

  /**
   * 组件的初始数据
   */
  data: {

  },
  
  /**
   * 组件的方法列表
   */
  methods: {
    gosearch:function(){
        wx.getSetting({
          success (res){
            if (res.authSetting['scope.userInfo']) {
              // 已经授权
              console.log('已经授权');
              wx.navigateTo({
                url: '../../pages/search_result/search_result',
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
  }
})
