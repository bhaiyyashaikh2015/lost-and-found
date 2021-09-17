from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

DB_NAME = "database.db"

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['SECRET_KEY'] = "secret key"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


class User(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    addr = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    state = db.Column(db.String(20), nullable=False)
    zip = db.Column(db.Integer, nullable=False)


class LostItem(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    iname = db.Column(db.String(50), nullable=False)
    idesc = db.Column(db.String(120), nullable=False)
    iloc = db.Column(db.String(120), nullable=False)
    uploader_email = db.Column(db.String(120), nullable=False)




class FoundItem(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    iname = db.Column(db.String(50), nullable=False)
    idesc = db.Column(db.String(120), nullable=False)
    iloc = db.Column(db.String(120), nullable=False)
    uploader_email = db.Column(db.String(120), nullable=False)



@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password)
        # print(hashed_password)
        addr = request.form.get('addr')
        city = request.form.get('city')
        state = request.form.get('state')
        zip = request.form.get('zip')
        user = User(fname=fname, lname=lname, email=email, password=hashed_password, addr=addr, city=city, state=state, zip=zip)
        db.session.add(user)
        db.session.commit()
        # print("data added in database")
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        session['email'] = email
        user = User.query.filter_by(email=email).first()
        # print(email)
        # print(password)

        if user:
            if check_password_hash(user.password, password):
                print("login successful")    # flash()
                flash("You have been logged in successfully!")
                return redirect(url_for("dashboard"))
            else:
                print("incorrect password")
                flash("You have entered Wrong Password!")
        else:
            print("email does not exist")
            flash("You have entered Wrong Email-id!")

    return render_template("login.html")


@app.route('/dashboard')
def dashboard():
    if "email" in session:
        email = session['email']
        lostitems = LostItem.query.all()
        founditems = FoundItem.query.all()
        print(type(lostitems))
        return render_template("dashboard.html", email=email, lostitems=lostitems, founditems=founditems)
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop("email", None)
    flash("You have been logged out successfully!")
    return redirect(url_for("login"))


@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        option = request.form.get('options')
        print(option, "hello")

        if "1" == option:
            print("In Lost...")
            iname = request.form.get('iname')
            idesc = request.form.get('idesc')
            iloc = request.form.get('iloc')
            uploader_email = session['email']

            item = LostItem(iname=iname, idesc=idesc, iloc=iloc, uploader_email=uploader_email)
            db.session.add(item)
            db.session.commit()
            print("data added in lost database")
            flash("Your lost item has been added successfully!")
            return redirect(url_for("lost"))

        if option == "2":

            print("In found...")
            iname = request.form.get('iname')
            idesc = request.form.get('idesc')
            iloc = request.form.get('iloc')
            uploader_email = session['email']

            item = FoundItem(iname=iname, idesc=idesc, iloc=iloc, uploader_email=uploader_email)
            print(type(item))
            db.session.add(item)
            db.session.commit()
            print("data added in found database")
            flash("Found item has been added successfully!")
            return redirect(url_for("found"))

    return render_template("add_item.html")


# def write_file(data):
#     with open(data, 'wb') as file:
#         file.write(data)


@app.route('/lost')
def lost():
    items = LostItem.query.all()
    print(type(items))
    # print(items[1])
    # print(items[2])
    # print(items[3])

    # # this code is for write image in current folder
    # j = 0
    # for i in items:
    #     j+=1
    #     with open("photo"+str(j)+".jpg", 'wb') as f:
    #         f.write(i.ipic)



        # write_file(i.ipic)
        # print(newpic)
        # print(i.ipic)
        # print(i.iname)
        # print(i.idesc)
        # print(type(i))

    # iname = items.iname
    # idesc = items.idesc
    # showItem = Item(ipic=newpic, iname=iname, idesc=idesc)

    return render_template("lost.html", items=items)


@app.route('/found')
def found():
    items = FoundItem.query.all()
    return render_template("found.html", items=items)


@app.route("/delete_lost/<int:sno>")
def delete_lost(sno):
    item = LostItem.query.filter_by(sno=sno).first()
    db.session.delete(item)
    db.session.commit()
    return redirect("/dashboard")


@app.route("/search", methods=['POST', 'GET'])
def search():
    matched = []
    if request.method == 'POST':
        s = request.form['search']
        print(s)
        items = LostItem.query.all()
        print(items[1])

        for i in items:
            print(i.iname)
            if s == i.iname:
                print("found")
                matched.append(i)
        return render_template('search.html', items=matched)


if __name__ == '__main__':
    app.run(debug=True)