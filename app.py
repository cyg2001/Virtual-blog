from flask import Flask, url_for, render_template, request
import pymysql
import io
import sys
import string
import datetime
app = Flask(__name__)
conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='virtualman',
        passwd='84711841',
        db='virtualblog',
        charset='utf8',
    )
def SendSQL(sql):
    cursor = conn.cursor()

    cursor.execute(sql)
    results = cursor.fetchall()  # 接受返回结果行
    # for row in results:
    cursor.close()
    return results

def GetAllArticles():
    title = list()
    content = list()

    ans = SendSQL("SELECT * FROM `virtualblog`.`virtual_articles` LIMIT 0,1000")
    return ans


def GetAllArticleClass():
    res = list()
    ans = SendSQL("SELECT * FROM `virtualblog`.`virtual_sort` LIMIT 0,1000")
    for row in ans:
        res.append(row[1])
    return res
@app.route('/index')
@app.route('/')
def index():
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    artistclass = GetAllArticleClass()
    artists = GetAllArticles()
    return render_template('index.html', **locals())
    # **locals()

@app.route('/about')
def about():
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    artistclass = GetAllArticleClass()
    artists = GetAllArticles()

    return render_template('about.html', **locals())
@app.route('/article',methods=['GET','POST'])
def article():
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    artistclass = GetAllArticleClass()
    artists = GetAllArticles()

    article_id = request.args.get("article_id")
    res = SendSQL("SELECT * FROM `virtualblog`.`virtual_articles` WHERE `article_id` = '"+article_id+"' LIMIT 0,1000")
    print(res)
    for i in res:
        id = i[0]
        article_title = i[1]
        article_content = i[2]
        article_user = 'Virtualman'
        article_datatime = i[5]
        article_views = i[3]
        article_comment_count=i[4]
        article_like_count = i[6]
    article_views=article_views+1
    SendSQL("UPDATE `virtualblog`.`virtual_articles` SET `article_views` = "+str(article_views)+" WHERE `article_id` = "+str(id))



    if request.method=='POST':
        article_id = request.args.get("article_id")
        user_name = request.form.get('user_name')
        # comment_mail
        comment_mail = request.form.get('comment_mail')
        comment_url = request.form.get('comment_url')
        comment_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        comment_content=request.form.get('comment_content')
        sql = "INSERT INTO `virtualblog`.`virtual_comment`(`comment_user_name`, `comment_article_id`, `comment_datatime`, `comment_content`, `comment_mail`, `comment_url`) VALUES ('"+user_name+"', "+str(article_id)+", '"+str(comment_time)+"', '"+comment_content+"', '"+comment_mail+"', '"+comment_url+"')"
        SendSQL(sql)
        article_comment_count = article_comment_count + 1
        SendSQL("UPDATE `virtualblog`.`virtual_articles` SET `article_comment_count` = " + str(article_comment_count) + " WHERE `article_id` = " + str(id))

    # 显示评论：
    sql = "SELECT * FROM `virtualblog`.`virtual_comment` WHERE `comment_article_id` = '" + str(
        id) + "' LIMIT 0,1000"
    comments = SendSQL(sql)
    return render_template('article.html', **locals())
@app.route('/admin')

@app.route('/admin')
@app.route('/admin/editor',methods=['POST','GET'])
def admin_ediotr():
    if request.method == 'POST':
        article_title = request.form.get('title')
        article_time = request.form.get('time')
        article_content = request.form.get('content')
        print(article_title, article_time, article_content)

        ans = SendSQL("INSERT INTO `virtualblog`.`virtual_articles`(`article_title`, `article_content`, `article_datatime`) VALUES ('"+article_title+"','"+article_content+"', '"+article_time+"')")
        print(ans)
        message = '文章发布成功'
        return render_template('editor.html', **locals())
    else:
        return render_template('editor.html', **locals())


@app.route('/articleClass',methods=['POST','GET'])
def articleClass():
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    artistclass = GetAllArticleClass()
    artists = GetAllArticles()

    classname = request.args.get('classname')
    res = SendSQL("SELECT * FROM `virtualblog`.`virtual_sort` WHERE `sort_name` LIKE '%s' " % classname)
    sort_id = res[0][0]
    artists = SendSQL("SELECT * FROM `virtualblog`.`virtual_articles` WHERE `article_class_id` = '"+str(sort_id)+"' LIMIT 0,1000")
    return render_template('articelClass.html', **locals())

if __name__ == '__main__':
    app.run()
