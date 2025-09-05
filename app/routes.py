from flask import render_template, flash, redirect, url_for, request,current_app
import secrets,os
from PIL import Image
from app.forms import Regform, Logform, PostForm, UpdateAccount
from datetime import datetime
from app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from app import app, bycrypt, db

with app.app_context():
    db.create_all()



@app.route("/Regform", methods=["GET", "POST"])
def regform():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = Regform()
    if form.validate_on_submit():
        hash_password = bycrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.user_name.data.strip(),
                    email=form.email.data.strip(),
                    password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'account created for {form.user_name.data}', 'success')
        return redirect(url_for('logform'))

    return render_template("reg.html", title="registeration", form=form)


@app.route("/Logform", methods=["GET", "POST"])
def logform():
    if current_user.is_authenticated:
        return redirect(url_for("about"))
    form = Logform()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.user_name.data , 
            email = form.email.data).first()
        if user and bycrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)

            flash(f'welcom back {form.user_name.data}', 'success')
            net_pag = request.args.get("next")
            return redirect(url_for("account"))if net_pag else redirect(url_for('home'))

        else:
            flash("invailid syntyx", 'danger')
            return redirect(url_for("logform"))

    return render_template("log.html", title="login", form=form)


@app.route("/")
def home():
    posts=Post.query.all()
    return render_template("home.html", title="posts", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="about")


@app.route("/postss", methods=['GET', 'POST'])
@login_required
def postss():
    form = PostForm()
    if form.validate_on_submit():
        post=Post(title=form.title.data,author=current_user,content=form.content.data)
        db.session.add(post)
        db.session.commit()
        

    
        flash(
            f"post created by  {current_user.username}", category='success')
        return redirect(url_for('home'))

    return render_template('post1.html', title="my new post", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def saved(form_picture):
    hex_image=secrets.token_hex(10)
    _,f_ext=os.path.splitext(form_picture.filename)
    picture_fn=hex_image + f_ext
    picture_path=os.path.join(current_app.root_path,"static/image",picture_fn)
    out_put=(125,125)
    i=Image.open(form_picture)
    i.thumbnail(out_put)
    i.save(picture_path)
    return picture_fn


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    image_file=url_for('static',filename='image/' + current_user.image_file)
    form = UpdateAccount()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file=saved(form.picture.data)
            current_user.image_file=picture_file
            
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('account updated','success')
        return redirect(url_for('account'))
    
    elif request.method=="GET":
        form.username.data=current_user.username
        form.email.data=current_user.email
        

    

    return render_template("account.html", title="Account", form=form,image_file=image_file)


@app.route("/postss/<int:post_id>")
def post(post_id):
    post=Post.query.get_or_404(post_id)
    return render_template("post.html",title=post.title,post=post)


@app.route("/postss/<int:post_id>/update", methods=["GET","POSt"])
def updatepost(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author!=current_user:
        flash("you can't edit someone else post",'danger')

    form=PostForm()

    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
        db.session.commit()
        flash('updated successfully','success')
        return redirect(url_for('post',post_id=post.id))
    
    elif request.method==["GET"]:
       form.title.data=post.title
       form.content.data=post.content



        

    