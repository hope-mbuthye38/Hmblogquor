from flask import render_template,redirect,url_for,abort,request,flash
from app.main import main
from app.models import User,Blog,Comment,Subscriber
from .forms import UpdateProfile,CreateBlog
from .. import db
from app.request import get_quotes
from flask_login import login_required,current_user
from ..email import mail_message
import secrets
import os

@main.route('/')
def index():
    quotes = get_quotes()
    page = request.args.get('page',1, type = int )
    blogs = Blog.query.order_by(Blog.posted.desc()).paginate(page = page, per_page = 3)
    return render_template('index.html', quote = quotes,blogs=blogs)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join('app/static/photos', picture_filename)
    form_picture.save(picture_path)

@main.route('/profile/<name>')
@login_required
def profile(name):
    user = User.query.filter_by(username = name).first()
    profile_pic_path = url_for('static',filename = 'photos/'+ current_user.profile_pic_path)
    if user == None:
        abort(404)

    return render_template('profile/profile.html',user = user)
    return render_template('profile/profile.html',user = user, profile_pic_path=profile_pic_path)
@main.route('/user/<name>/updateprofile', methods = ['POST','GET'])
@login_required
@main.route('/user/<name>/updateprofile', methods = ['POST','GET'])
@login_required
def updateprofile(name):
    form = UpdateProfile()
    user = User.query.filter_by(username = name).first()
    if user == None:
        abort(404)
    if form.validate_on_submit():
        user.bio = form.bio.data
        user.save()
        return redirect(url_for('.profile',name = name))
    return render_template('profile/updateprofile.html',form =form)
@main.route('/new_post', methods=['POST','GET'])
@login_required
def new_blog():
    subscribers = Subscriber.query.all()
    form = CreateBlog()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        user_id =  current_user._get_current_object().id
        blog = Blog(title=title,content=content,user_id=user_id)
        blog.save()
        for subscriber in subscribers:
            mail_message("New Blog Post","email/new_blog",subscriber.email,blog=blog)
        return redirect(url_for('main.index'))
        flash('You Posted a new Blog')
    return render_template('newblog.html', form = form)
@main.route('/blog/<id>')
def blog(id):
    comments = Comment.query.filter_by(blog_id=id).all()
    blog = Blog.query.get(id)
    return render_template('blog.html',blog=blog,comments=comments)
    
@main.route('/blog/<blog_id>/update', methods = ['GET','POST'])
@login_required
def updateblog(blog_id):
    blog = Blog.query.get(blog_id)
    if blog.user != current_user:
        abort(403)
    form = CreateBlog()
    if form.validate_on_submit():
        blog.title = form.title.data
        blog.content = form.content.data
        db.session.commit()
        flash("You have updated your Blog!")
        return redirect(url_for('main.blog',id = blog.id)) 
    if request.method == 'GET':
        form.title.data = blog.title
        form.content.data = blog.content
    return render_template('newblog.html', form = form)
@main.route('/comment/<blog_id>', methods = ['Post','GET'])
@login_required
def comment(blog_id):
   
    comment =request.form.get('newcomment')
    new_comment = Comment(comment = comment, user_id = current_user._get_current_object().id, blog_id=blog_id)
    new_comment.save()
    return redirect(url_for('main.index',comment=comment))
@main.route('/subscribe',methods = ['POST','GET'])
def subscribe():
    email = request.form.get('subscriber')
    new_subscriber = Subscriber(email = email)
    new_subscriber.save_subscriber()
    mail_message("login to hmblogquor","email/welcome_subscriber",new_subscriber.email,new_subscriber=new_subscriber)
    flash('Sucessfuly subscribed')
    return redirect(url_for('main.index'))
@main.route('/blog/<blog_id>/delete', methods = ['POST'])
@login_required
def delete_post(blog_id):
    blog = Blog.query.get(blog_id)
    if blog.user != current_user:
        abort(403)
    blog.delete()
    flash("You have deleted your Blog succesfully!")
    return redirect(url_for('main.index'))
@main.route('/user/<string:username>')
def user_posts(username):
    user = User.query.filter_by(username=username).first()
    page = request.args.get('page',1, type = int )
    blogs = Blog.query.filter_by(user=user).order_by(Blog.posted.desc()).paginate(page = page, per_page = 3)
    return render_template('userposts.html',blogs=blogs,user = user)
 
@main.route ('/user/<string:username')
def user_comment(blog_id):
    comment =request.form.get('newcomment')
    new_comment = Comment(comment = comment, user_id = current_user._get_current_object().id, blog_id=blog_id)
    new_comment.save()
    return redirect(url_for('main.index',comment=comment))
@main.route('/subscribe',methods = ['POST','GET'])
def subscribe():
    email = request.form.get('subscriber')
    new_subscriber = Subscriber(email = email)
    new_subscriber.save_subscriber()
    mail_message("Subscribed to hmblogquor","email/welcome_subscriber",new_subscriber.email,new_subscriber=new_subscriber)
    flash('Sucessfuly subscribed')
    return redirect(url_for('main.index'))
@main.route('/blog/<blog_id>/delete', methods = ['POST'])
@login_required
def delete_post(blog_id):
    blog = Blog.query.get(blog_id)
    if blog.user != current_user:
        abort(403)
    blog.delete()
    flash("You have deleted your Blog succesfully!")
    return redirect(url_for('main.index'))
@main.route('/user/<string:username>')
def user_posts(username):
    user = User.query.filter_by(username=username).first()
    page = request.args.get('page',1, type = int )
    blogs = Blog.query.filter_by(user=user).order_by(Blog.posted.desc()).paginate(page = page, per_page = 4)
    return render_template('userposts.html',blogs=blogs,user = user)
