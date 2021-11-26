const date = new Date()
const years = []
const months = []
const days = []
const app = getApp()
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
    scrollLeft:0,
    pageNum:1,
    setInter: '', 
    idkey:-1,
    tags:'治愈',
    flag1:true,
    years,
    year: date.getFullYear(),
    months,
    month: date.getMonth()+1,
    days,
    day: date.getDate(),
    value: [date.getMonth(), date.getFullYear()],
    isDaytime: true,  //
    array:[],
    current:[],
    currentIndexNav:0,
    navList:['全部','悲伤','生气','焦虑','无语','失望','崩溃','委屈','日记'],
    navimg:['../../icon/smile.png',
    '../../icon/sad.png',
    '../../icon/angry.png',
    '../../icon/nervous.png',
    '../../icon/speechless.png',
    '../../icon/disappoint.png',
    '../../icon/cry.png',
    '../../icon/grievance.png',
    '../../icon/diaryicon.png',
    ]
  },
  bindChange(e) {
    const val = e.detail.value
    this.setData({
      year: this.data.years[val[1]],
      month: this.data.months[val[0]],
    })
  },
  diaryContent:function(event){
    var idkey=event.currentTarget.dataset.id;
    this.setData({
      idkey:idkey
    })
    wx.setStorageSync('d_content', this.data.array[idkey].diary_content);
    wx.setStorageSync('d_mood', this.data.array[idkey].tips);
    wx.setStorageSync('d_id', this.data.array[idkey].diary_id);
    wx.setStorageSync('d_time', this.data.array[idkey].write_down_time);
    wx.navigateTo({
      url: '../diaryCon/diarycon?idkey='+idkey,
    })
  },
  editDairy:function(){
    if (app.globalData.userInfo!=null) {
      // 已经授权
      wx.navigateTo({
        url: '../write/write',
      })
    }else{
      wx.navigateTo({
        url: '../login1/login1',
        })
    }
  },

  onLoad: function () {
    //定时器用来请求日记数据
   //定时器用来请求日记数据
   if(app.globalData.userInfo!=null)
   {
      this.startSetInter();
   }
  },
  //启用定时器
  startSetInter: function () {
    var that = this;
    //将计时器赋值给setInter
    that.data.setInter = setInterval(
      function () {
        that.queryRemindCount()
      }, 500);
  },
  //定时器后续，请求数据
queryRemindCount: function () {
  if (app.globalData.userID == null) {
    return
  }
    clearInterval(this.data.setInter) // 关闭定时器
    this.getalldiary()
},

  onShow:function(){
    
    var that=this;
    // console.log(this.data.currentIndexNav)
    if(app.globalData.deleteDiary){
      app.globalData.deleteDiary=false
      if(this.data.currentIndexNav!=0)
      {
        this.gettagsdiary()
      }
      else{
        this.getalldiary()
      }
    }
    this.eat = this.selectComponent("#eat"); //组件的id
    if( app.globalData.diasucc)//保存成功
    {
      var mymood = wx.getStorageSync('mymood')
      that.setData({
        tags:mymood,
        pageNum:1,
        scrollLeft:0,
        currentIndexNav:0
      })
        this.getalldiary()
      app.globalData.deleteDiary=false;
      this.eat.showEat();
      setTimeout(function(){
        this.eat.hideEat();
      }.bind(this),3000)
    }
    
  },
  //触底响应函数，监听下拉加载----------------------------------->>>>>>>>>
  onBottom(){
    (this.data.pageNum)++;
    this.getNoticeList();
},
//获取列表失败的回调函数
getNoticeList(){
  //请求
  if(this.data.currentIndexNav!=0)
  {
    this.gettagsdiary()
  }
  else{
    this.getalldiary()
  }
},
//页面上拉触底事件的处理函数
onReachBottom: function () {
  this.onBottom();
},
//触底响应函数，监听下拉加载-----------------------------------^^^^^^^^^^>>>>>>>
/**
   * 当前激活的导航栏选项
   */
  getalldiary:function(){
    var that = this;
    wx.request({
      url: 'https://luckym.top/diary/getAll',
      method: 'get',
      data: {
        page: this.data.pageNum,
        per_page:7,
        user_id:app.globalData.userID,
      },
      header: {
        'content-type': 'application/json' // 默认值
      },
      success (res) {
        if (that.data.pageNum == 1) {
          if(res.data.all_diary!=undefined)
          {
            that.setData({
              array: res.data.all_diary,
             })
          }
          else{
            that.setData({
              array: [],
             })
          }  
        } else {
          //获取原始列表
            let noticeList = that.data.array;
            //获取新列表
            let arr = res.data.all_diary;
            //新列表数据与原列表数据合并
            let newArr = noticeList.concat(arr);
            if(arr!=undefined)
            {
              that.setData({
                  array: newArr,
              })
            }   
        }
      },
      fail (){
        console.log(fail)
        wx.showToast({
          title: '获取失败，请稍后重试',
          icon:'none',
          duration:2500,
        })
      }
    })
  },
  gettagsdiary:function(){
    var that = this;
    wx.request({
      url: 'https://luckym.top/diary/getByTips',
      method: 'get',
      data: {
        page: this.data.pageNum,
        tips:this.data.navList[this.data.currentIndexNav],
        per_page:7,
        user_id:app.globalData.userID,
      },
      header: {
        'content-type': 'application/json' // 默认值
      },
      success (res) {
        if (that.data.pageNum == 1) {
          if(res.data.all_diary!=undefined)
          {
            that.setData({
              array: res.data.all_diary,
             })
          }
          else{
            that.setData({
              array: [],
             })
          }   
        } else {
          //获取原始列表
            let noticeList = that.data.array;
            //获取新列表
            let arr = res.data.all_diary;
            //新列表数据与原列表数据合并
            let newArr = noticeList.concat(arr);
            console.log(arr)
            if(arr!=undefined)
            {
              that.setData({
                  array: newArr,
              })
            }   
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
  activeNav: function(e){
    // 绑定当前选中的菜单项索引号
    this.setData({
      currentIndexNav: e.currentTarget.dataset.index,
      pageNum:1,
      array: [], 
    })
    if(app.globalData.userInfo!=null)
   {
      if(this.data.currentIndexNav!=0){
        this.gettagsdiary()
      }
      else{
        this.getalldiary()
      }
   }
  },
})
