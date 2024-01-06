from flask_app import app
from flask_app.models.user import User
from flask import render_template,redirect,request,session,flash

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/our_story')
def story():
    return render_template('our_story.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/rsvp')
def show_rsvp():
    return render_template('rsvp.html')

@app.route('/confirm-rsvp',methods=['POST'])
def register():

    if not User.validate_register(request.form):
        return redirect('/rsvp')
    data ={
        "name": request.form['name'],
        "email": request.form['email'],
        "plus_1": request.form['plus_1'],
        "food": request.form['food'],
        "plus_one_food": request.form['plus_one_food'],
        "invite_code": request.form['invite_code']
    }
    id = User.save(data)
    session['user_id'] = id

    return redirect('/')

# @app.route('/admin')
# def admin_login():
#     return render_template('login.html')

# @app.route('/confirm-admin',methods=['POST'])
# def admin():

#     if not User.validate_admin(request.form):
#         return redirect('/admin')
#     data ={
#         "user": request.form['user'],
#         "pass": request.form['pass']
#     }
#     id = User.save(data)
#     session['user_id'] = id

#     return redirect('/rsvpinfo')

# @app.route('/rsvpinfo')
# def adminpanel():
#     all_users = User.get_all()
#     plus_ones = User.get_all_plus_ones()
#     return render_template('adminpanel.html',all_users=all_users,plus_ones=plus_ones)