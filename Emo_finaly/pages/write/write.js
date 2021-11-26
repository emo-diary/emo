// pages/write/write.js
var util = require('../../utils/util.js');
let date = new Date()
let year = date.getFullYear()
let month = date.getMonth()
let day = date.getDate()
let hour = date.getHours()
let minute = date.getMinutes()
let second = date.getSeconds()
var app = getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {
      info:0,
      yanse_column: 0,
    year_month: '',
    dayShow: false,
    _year: year,
    _month: month,
    day: date.getDate(),
    neirong:"",
    specific_t:'',
    mood:'悲伤',
    objectArray: [
      {
        id: 0,
        name: '悲伤',
      },
      {
        id: 1,
        name: '生气'
      },
      {
        id: 2,
        name: '焦虑'
      },
      {
        id: 3,
        name: '无语'
      },
      {
        id: 4,
        name: '失望'
      },
      {
        id: 5,
        name: '崩溃'
      },
      {
        id: 6,
        name: '委屈'
      },
      {
        id: 7,
        name: '日记'
      }
    ],
    objectIndex: 0,
  },
  textinput:function(e){
    var content = e.detail.value;
    var cnt = parseInt(content.length);
    this.setData({
      neirong:content,
      info:cnt
    })
  },
  bindPickerChange: function (e) {
    console.log('picker发送选择改变，携带值为', e.detail.value)
    this.setData({
      objectIndex: e.detail.value,
    })
   this.data.mood=this.data.objectArray[this.data.objectIndex].name
  },
  UpdateDate(){
    this.setData({
      // _year: year,
      // _month: month,
      year: year,
      month: month,
      day: day,
      year_month: year + '年' + (month + 1) + '月'

    })
    this.monthDaysUpdate(year, month)
    this.dayShow () 
  },
  todayDate () {
    let date = new Date()
    let year = date.getFullYear()
    let month = date.getMonth()
    let day = date.getDate()
 
    day = day < 10 ? '0' + day : day
 
    this.monthDaysUpdate(year, month)
 
    this.setData({
      _year: year,
      _month: month,
      year: year,
      month: month,
      day: day,
      year_month: year + '年' + (month + 1) + '月'
    })
  },
 
  /**
   * 年、月切换
   */
  yearMonthUpdate (flag) {
    let year = this.data.year
    let month = this.data.month
    let date = new Date(year, month + flag)
    
    year = date.getFullYear()
    month = date.getMonth()
 
    this.monthDaysUpdate(year, month)
 
    this.setData({
      year: year,
      month: month,
      year_month: year + '年' + (month + 1) + '月'
    })
  },
 
  /**
   * 月份天数
   * new Date： 把月份设置成下一个月，日期设置成 0，getDate()就获取这个月份的天数
   */
  monthDaysUpdate (year, month) {
    // 月份总天数
    let days = new Date(year, month + 1, 0).getDate()
    // 今天的日期
    let currYear = new Date().getFullYear()
    let currMonth = new Date().getMonth()
    let today = new Date().getDate()
    // 月份第一天是星期几
    let whichDay = new Date(year, month, 1).getDay()
    // 存放日期数组
    let dayList = []
    
    // 补空
    for (let j = 0; j < whichDay; j++) {
      let obj = { 'day': '' };
      dayList.push(obj)
    }
 
    for (let i = 1; i <= days; i++) {
      let obj = {
        'day': i,
      };
 
      if ((i < today && month <= currMonth && year <= currYear) || (month < currMonth && year <= currYear) || (year < currYear)) {
        obj['class'] = 'dl-active'  // 过去的天数
      }
      else if (i === today && month === currMonth && year === currYear) {
        obj['class'] = 'dl-today'
        obj['day'] = '今天'
      }
      else if (i > today && month >= currMonth && year >= currYear) {
        obj['class'] = 'dl-disable' // 未来的天数
      }
      else {
        obj['class'] = 'dl-disable' // 未来的天数
      }
 
      dayList.push(obj)
    }
 
    this.setData({
      dayList: dayList
    })
  },
 
  /**
   * 月份切换
   * index: -1 (前一个月) 1 (后一个月))
   */
  switchMonth (event) {
    let index = event.currentTarget.dataset.index
 
    if (parseInt(index) === -1) {
      this.yearMonthUpdate(-1)
    }
    else if (parseInt(index) === 1) {
      this.yearMonthUpdate(1)
    }
  },
 
  /**
   * 选择日期
   */
  selectDay (event) {
    let day = event.currentTarget.dataset.day
    let clazz = event.currentTarget.dataset.clazz
    let year = this.data.year
    let month = this.data.month
 
    if (clazz.indexOf('dl-disable') === -1) {
      if (day === '今天') {
        day = new Date().getDate()
      }
 
      day = day < 10 ? '0' + day : day
 
      this.setData({
        _year: year,
        _month: month,
        day: day,
        dayShow: false
      })
    }
 
    wx.pageScrollTo({
      scrollTop: 0,
      duration: 0
    })
  },
 
  /**
   * 日期面板展开
   */
  dayShow () {
    let dayShow = this.data.dayShow
    dayShow = dayShow ? false : true
    this.setData({
      dayShow: dayShow
    })
  },
 
  /**
   * 日期面板关闭
   */
  close_dayShow () {
    this.setData({
      dayShow: false
    })
  },

  editsuccess:function()
  {
    var that=this;
    wx.request({
      url: 'https://luckym.top/diary/addDiary/',
      method: 'post',
      data: {
        diary_content:this.data.neirong,
	      tips:this.data.mood,
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
          app.globalData.diasucc=true;
          var mymood='';
          if(that.data.mood!='日记')
          {
            mymood=that.data.mood;
          }
          wx.setStorage({
            key: 'mymood',
            data:mymood,
          }),
          wx.showToast({
            title: '保存成功',
            icon: 'none',    //如果要纯文本，不要icon，将值设为'none'
            duration: 1500     
          })
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
})
