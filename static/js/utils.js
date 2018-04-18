function getCookie(name) {
    var arr, reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)");

    if (arr = document.cookie.match(reg))

        return unescape(arr[2]);
    else
        return null;
}

var getUserId = function () {
    var u = getCookie('u_id')
    log(u)
    if (u == null) {
        alert('没登录')
        return
    }
    else {
        return u
    }
}