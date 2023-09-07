import cv2
from flask import Flask, Response, render_template
from flask import Flask, Response, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__, static_url_path='')
app.secret_key = 'admin'  # Change this to a strong, random key
login_manager = LoginManager()
login_manager.init_app(app)

app.config['LOGIN_DISABLED'] = False  # Ensure login functionality is enabled
app.config['LOGIN_VIEW'] = 'login'

login_manager = LoginManager()
 #Added this line fixed the issue.
login_manager.init_app(app) 
login_manager.login_view = 'users.login'

# User class for user authentication (replace with your user database)
class User(UserMixin):
    def __init__(self, id):
        self.id = id

users = {'admin': {'password': 'admin'}}

camera = cv2.VideoCapture(1)  # Use 0 for default camera, replace with camera URL for IP camera

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Process the frame with OpenCV (e.g., object detection)
            # You can add your OpenCV processing code here

            # Convert the frame to JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                continue
            frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/')
def root():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    else:
        return redirect(url_for('login'))

@app.route('/main')
@login_required
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login failed. Check your username and password.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required  # Require authentication to log out
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8200, debug=False)