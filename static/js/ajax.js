var log = function() {
    console.log.apply(console, arguments)
}

var e = function(sel) {
    return document.querySelector(sel)
}

var E = function(sel) {
    return document.querySelectorAll(sel)
}

/*
 ajax 函数
*/
var ajax = function(method, path, data, reseponseCallback) {
    var r = new XMLHttpRequest()
    // 设置请求方法和请求地址
    r.open(method, path, true)
    // 设置发送的数据的格式为 application/json
    // 这个不是必须的
    r.setRequestHeader('Content-Type', 'application/json')
    // 注册响应函数
    r.onreadystatechange = function() {
        if(r.readyState === 4) {
            // r.response 存的就是服务器发过来的放在 HTTP BODY 中的数据
            reseponseCallback(r.response)
        }
    }
    // 把数据转换为 json 格式字符串
    data = JSON.stringify(data)
    // 发送请求
    r.send(data)
}

// TODO API
// 获取所有 todo
var apiQuestionMore = function(callback) {
    var path = '/api/question/next'
    ajax('GET', path, '', callback)
}

var apiCommentsAll = function(args, callback) {
    var path = '/api/comment/all?id=' + args
    ajax('GET', path, '', callback)
}
var apiCommentsAdd = function(args, value, user_id, callback) {
    log('a', args, value, user_id)
    var path = '/api/comment/add?id=' + args + '&value=' + value + '&user_id='+user_id
    ajax('GET', path, '', callback)
}
var apiQuestionCare = function(args, user_id, callback) {
    log('a', args, user_id)
    var path = '/api/question/care?id=' + args + '&user_id='+user_id
    ajax('GET', path, '', callback)
}
// 增加一个 todo
// var apiQuestionMore = function(list, callback) {
//     var path = '/api/question/next'
//     ajax('GET', path, list, callback)
// }

