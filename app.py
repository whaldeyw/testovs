from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from base_db import TableClient, TableUser, async_session, async_sessionmaker
import asyncio


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
db = SQLAlchemy(app)

# class TableClient(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     number = db.Column(db.Integer)
#     family = db.Column(db.String(25))
#     name = db.Column(db.String(25))
#     middle_name = db.Column(db.String(25))
#     data = db.Column(db.Integer)
#     inn = db.Column(db.Integer)
#     responsible = db.Column(db.String(25))
#     status = db.Column(db.String(25))
#
# class TableUser(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     fio = db.Column(db.String(25), nullable=False)
#     loggin = db.Column(db.Text, nullable=False)
#     password = db.Column(db.Text, nullable=False)



# @app.route("/create", methods=['POST', 'GET'])
# def create():
#     if request.method == 'POST':
#         number = request.form['number']
#         family = request.form['family']
#         name = request.form['name']
#         middle_name = request.form['middle_name']
#         data = request.form['data']
#         inn = request.form['inn']
#         responsible = request.form['responsible']
#         status = request.form['status']
#
#         table = TableClient(number=number, family=family, name=name, middle_name=middle_name, data=data, inn=inn, responsible=responsible, status=status )
#
#         try:
#             db.session.add(table)
#             db.session.commit()
#             return redirect("/table")
#         except:
#             return 'При добавлении в базу возникла ошибка'
#     else:
#         return render_template('create.html')

@app.route("/create", methods=['POST', 'GET'])
async def set_user():

    if request.method == 'POST':
        number = request.form['number']
        family = request.form['family']
        name = request.form['name']
        middle_name = request.form['middle_name']
        data = request.form['data']
        inn = request.form['inn']
        responsible = request.form['responsible']
        status = request.form['status']

        table = TableClient(number=number, family=family, name=name, middle_name=middle_name, data=data, inn=inn, responsible=responsible, status=status )

        async with async_session() as session:
            session.add(TableUser(table))
            await session.commit()
      


@app.route("/table")
def table():
    table = TableClient.query.order_by(TableClient.id).all()
    return render_template('table.html', table=table)


@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        fio = request.form['fio']
        loggin = request.form['loggin']
        password = request.form['password']
        re_password = request.form['repassword']
        if password==re_password:

            tableus = TableUser(fio=fio, loggin=loggin, password=password )

            try:
                db.session.add(tableus)
                db.session.commit()
                return redirect("/table")
            except:
                return 'При добавлении в базу возникла ошибка'
        else:
            return 'Пароли не совпадают'    
    else:
        return render_template('register.html')

@app.route("/auth", methods=['POST', 'GET'])
def auth():
    if request.method == 'POST':
        loggin = request.form['loggin']
        password = request.form['password']

        data = TableClient.query.all()
        for item in data:
            if loggin == item:
                return redirect("/table")
            else:
                return 'Косяке'
    else:
        return render_template('auth.html')


if __name__=='__main__':
    
    app.run(debug=True)