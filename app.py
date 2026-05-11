from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model
class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(100))

    phone = db.Column(db.String(20))

    status = db.Column(db.String(50), default="New")

# Home Page
@app.route('/')
def index():
    leads = Lead.query.all()
    return render_template('index.html', leads=leads)

# Add Lead
@app.route('/add', methods=['GET', 'POST'])
def add_lead():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        status = request.form['status']

        new_lead = Lead(
            name=name,
            email=email,
            phone=phone,
            status=status
        )

        db.session.add(new_lead)
        db.session.commit()

        return redirect('/')

    return render_template('add_lead.html')

# Create Database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)