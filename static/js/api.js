var titleTemplate = function (title) {
    log('title', title)
    var t = `<div class="panel-body">
                                <a href="/123">
                                    <h1>${title}</h1>
                                </a>
                            </div>`
    return t
    /*
    上面的写法在 python 中是这样的
    t = """
    <div class="todo-cell">
        <button class="todo-delete">删除</button>
        <span>{}</span>
    </div>
    """.format(todo)
    */
}

var entireTemplate = function (star, author, content, title, comment) {
    var t = `<div class="panel-body">
                                <div class="author-info">
                                    <div class="Avatar">
                                        <img class="img-circle" src='{{ answer[article].author.img_url }}'>
                                    </div>
                                    <h3> ${author}</h3>
                                </div>
                                <a href="{{ url_for('question.article', id=article.id) }}">
                                    <h1>${title}</h1>
                                </a>

                                <div class="answer">
                                    <h2>${content}</h2>
                                    <button class="star">赞</button>
                                    ${star}
                                </div>

                                <div class="comment">
                                    <h5>${comment}评论</h5>
                                </div>

                            </div>`
    return t
}

var CommentTemplate = function (author, content) {
    var t = `<div >
                                    <span>${author}</span>
                                    <h4>${content}</h4>
                            </div>`
    return t
}

var insertQuestion = function (question) {
    log(question)
    var title = question.title
    var content = question.answer_content
    var comment = question.comment
    var author = question.author
    var star = question.star
    if (content) {
        var todoCell = entireTemplate(star, author, content, title, comment)
    } else {
        var todoCell = titleTemplate(title)
        // 插入 todo-list
    }
    var todoList = e('#id-question-section')
    todoList.insertAdjacentHTML('beforeend', todoCell)
}

var insertComment = function (comment) {
    log('insert', comment)
    author = comment.author
    content = comment.content
    var CommentCell = CommentTemplate(author, content)
    var todoList = e('.well')
    todoList.insertAdjacentHTML('beforeend', CommentCell)
}

var AddComment = function (comment) {
    log('add', comment)
    author = comment.author
    content = comment.content
    var CommentCell = CommentTemplate(author, content)
    var todoList = e('.well')
    todoList.insertAdjacentHTML('beforeend', CommentCell)
}

var loadComments = function () {
    // 调用 ajax api 来载入数据
    apiCommentsAll(function (r) {
        console.log('more', r)
        // 解析为 数组
        var comments = JSON.parse(r)
        // 循环添加到页面中
        console.log('q', comments)
        for (var i = 0; i < comments.length; i++) {
            var q = comments[i]
            log('insert')
            insertComment(q)
        }
    })
}

var bindEventMore = function () {
    var b = e('#id-button-more')

    b.addEventListener('click', function () {
        log('click more')
        apiQuestionMore(function (r) {
            // 收到返回的数据, 插入到页面中
            var question = JSON.parse(r)
            for (var i = 0; i < question.length; i++) {
                var q = question[i]
                insertQuestion(q)
            }
        })
    })
}

var bindEventComment = function () {
    var b = e('#id-button-comment')
    var args = ''
    if (b) {
        b.addEventListener('click', function (event) {
            args = event.target.parentElement.firstChild.nextElementSibling.innerText
            apiCommentsAll(args, function (r) {
                // 收到返回的数据, 插入到页面中
                var question = JSON.parse(r)
                for (var i = 0; i < question.length; i++) {
                    var q = question[i]
                    insertComment(q)
                }
            })
        })
    }

}

var bindEventAdd = function () {
    var b = e('#id-button-addComment')
    var v = e('#id-input-comment')
    if (b) {
        b.addEventListener('click', function (event) {
            var userId = getUserId()
            if (userId != null) {
                log('123')
                var value = v.value
                id = event.target.parentElement.parentElement.firstChild.nextElementSibling.innerText
                var args = id
                apiCommentsAdd(args, value, userId, function (r) {
                    // 收到返回的数据, 插入到页面中
                    var comment = JSON.parse(r)
                    log('comment', comment)
                    AddComment(comment)
                })
            }

        })
    }

}

var bindEventCareButton = function () {
    var b = E('.class-button-care')
    if (b) {
        for (var i = 0; i < b.length; i++) {
            b[i].addEventListener('click', function (event) {
                var userId = getUserId()
                if (userId != null) {
                    questionId = event.target.parentElement.firstChild.nextElementSibling.nextElementSibling.innerText
                    var args = questionId
                    apiQuestionCare(args, userId, function (r) {
                        // 收到返回的数据, 插入到页面中
                        var info = JSON.parse(r)
                        log('comment', info)
                        alert(info.span)
                    })

                }
            })

        }
    }
}

var bindEvents = function () {
    bindEventMore()
    bindEventComment()
    bindEventAdd()
    bindEventCareButton()
}

var __main = function () {
    bindEvents()
    // loadComments()
}

__main()





