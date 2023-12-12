# PlotMyVert

A much better way to save, track, view and plot vertical jump history (from the G-Vert device).

## 1.0 Development

// in composables/apiFetch.js modify the following line to point to your production server if you will deploy to production
// const baseURL = import.meta.env.VITE_BASE_URL || 'https://vert.duz.ie';
// in /plotmyvert_backend/settings.py modify the following line to point to your production server if you will deploy to production
// ALLOWED_HOSTS = ['vert.duz.ie', 'http://127.0.0.1']

### 1.1 Front End

cd PROJECT_ROOT_FOLDER
npm install
// in the PlotMyVert folder, create .env
touch .env
// add the following to .env
echo 'VITE_BASE_URL="http://127.0.0.1:8000"' > .env
npm run dev -- --host=127.0.0.1

### 1.2 Back End

cd plotmyvert_backend
pyenv install 3.12.0
pyenv virtualenv 3.12.0 plotmyvert_backend
pyenv local plotmyvert_backend
// check that the correct python version is being used
pyenv version
// should return plotmyvert_backend (set by $PATH_TO_BACKEND/.python-version)
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

## 2.0 Deployment

### 2.1 Front End

cd PROJECT_ROOT_FOLDER
npm run build
node .output/server/index.mjs

### 2.2 Back End

cd plotmyvert_backend
docker build . -t "plotmyvert_backend"
// remove previous container
docker rm "plotmyvert_backend" -f
// remove untagged images (from previous builds)
docker image prune -f
// run container (Dockerfile exposes on port 8001) in debug mode for local deployment (simple)
docker run -d -p 8000:8000 --name "plotmyvert_backend" plotmyvert_backend

### 2.2.1 Additional Configuration

// to run in production mode without debug, a secret key is required
// add this to the docker run command (before the final image name)
-e PLOTMYVERT_BACKEND_SECRET_KEY="YOUR_SECRET_KEY_HERE"

// to use an existing database (e.g. named db.sqlite3), add this to the docker run command (before the final image name)
-v /path/to/database/db.sqlite3:/code/db.sqlite3

### 2.2.2 SSL / HTTPS

// SSL / HTTPS is required for production deployment with a secret key (debug mode is tied to secret key generation)
// to disable this requirement, comment the following lines in /plotmyvert_backend/settings.py
// SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
// CSRF_COOKIE_SECURE = True
// SESSION_COOKIE_SECURE = True
