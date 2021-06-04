const mongoose = require('mongoose')
mongoose.connect('http://123.57.239.180:27017/Course')
const conn = mongoose.connection
conn.on('connected',function(){
    console.log('数据库连接成功')
}) 
