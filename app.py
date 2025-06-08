from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import pytz  # <--- ADD THIS

# Configure Flask app
app = Flask(__name__)

# --- Database Configuration ---
# Create a path for the SQLite database file
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'a_very_secret_key_for_your_app_please_change_this'

# Initialize the database
db = SQLAlchemy(app)

# --- Database Models ---
# Define your local timezone (South African Standard Time)
SAST_TZ = pytz.timezone('Africa/Johannesburg')


# Define the Project table
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    hourly_rate = db.Column(db.Float, default=0.0)
    sessions = db.relationship('Session', backref='project', lazy=True, cascade="all, delete-orphan")
    total_hours = db.Column(db.Float, default=0.0)
    estimated_cost = db.Column(db.Float, default=0.0)

    def __repr__(self):
        return f"Project('{self.name}', '{self.type}')"


# Define the Session table
class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    # Ensure this default is a lambda function that returns a datetime object
    # This creates an OFFSET-AWARE datetime at the time of creation
    start_time = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(SAST_TZ))
    end_time = db.Column(db.DateTime, nullable=True)
    duration_minutes = db.Column(db.Integer, default=0)
    work_details = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"Session('{self.start_time}', '{self.end_time}', Project ID: {self.project_id}')"


# --- Routes ---

@app.route('/')
def index():
    projects = Project.query.all()
    return render_template('index.html', projects=projects)


@app.route('/create_project', methods=['GET', 'POST'])
def create_project():
    if request.method == 'POST':
        project_name = request.form['project_name']
        project_type = request.form['project_type']
        try:
            hourly_rate = float(request.form['hourly_rate'])
            if hourly_rate < 0:
                flash('Hourly rate cannot be negative.', 'error')
                return redirect(url_for('create_project'))
        except ValueError:
            flash('Invalid hourly rate. Please enter a number.', 'error')
            return redirect(url_for('create_project'))

        new_project = Project(name=project_name, type=project_type, hourly_rate=hourly_rate)
        db.session.add(new_project)
        db.session.commit()

        flash('Project created successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('create_project.html')


@app.route('/project/<int:project_id>')
def view_project(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('view_project.html', project=project)


@app.route('/project/<int:project_id>/start_session', methods=['POST'])
def start_session(project_id):
    project = Project.query.get_or_404(project_id)
    active_session = Session.query.filter_by(project_id=project.id, end_time=None).first()

    if active_session:
        flash('A session is already active for this project! End it before starting a new one.', 'warning')
    else:
        new_session = Session(project_id=project.id, start_time=datetime.now(SAST_TZ))
        db.session.add(new_session)
        db.session.commit()
        flash('Session started!', 'success')
    return redirect(url_for('view_project', project_id=project.id))


@app.route('/project/<int:project_id>/end_session', methods=['POST'])
def end_session(project_id):
    project = Project.query.get_or_404(project_id)
    active_session = Session.query.filter_by(project_id=project.id, end_time=None).first()

    if not active_session:
        flash('No active session to end for this project!', 'warning')
    else:
        active_session.end_time = datetime.now(SAST_TZ)

        # Ensure both datetimes are timezone-aware before subtraction
        # If active_session.start_time is naive (from old data), make it aware
        if active_session.start_time.tzinfo is None:
            active_session.start_time = SAST_TZ.localize(active_session.start_time)

        duration_delta = active_session.end_time - active_session.start_time
        active_session.duration_minutes = int(duration_delta.total_seconds())
        if active_session.duration_minutes < 0:
            active_session.duration_minutes = 0

        active_session.work_details = request.form.get('work_details')
        project.total_hours += active_session.duration_minutes / 3600.0
        project.estimated_cost = project.total_hours * project.hourly_rate

        db.session.commit()
        flash('Session ended and time logged!', 'success')
    return redirect(url_for('view_project', project_id=project.id))


if __name__ == '__main__':
    with app.app_context():
        # Uncomment the next line *only if* you are okay with deleting all data
        # and need to guarantee a fresh database schema for testing.
        db.drop_all()
        db.create_all()
    app.run(debug=True)