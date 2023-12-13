# PlotMyVert

A much better way to save, track, view and plot vertical jump history (from the G-Vert device).

## 1.0 Development

// in composables/apiFetch.js modify the following line to point to your production server if you will deploy to a server
// const baseURL = import.meta.env.VITE_BASE_URL || 'https://vert.duz.ie';
// in /plotmyvert_backend/settings.py modify the following line to point to your production server if you will deploy to a server
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

#### 2.2.1 Docker Setup

cd plotmyvert_backend
docker build . -t "plotmyvert_backend"
// remove previous container
docker rm "plotmyvert_backend" -f
// remove untagged images (from previous builds)
docker image prune -f
// run container (Dockerfile exposes on port 8001) in debug mode for local deployment (simple)
// debug mode allows local deployment without SSL / HTTPS but is insecure for public deployment
docker run -d -p 8000:8000 --name "plotmyvert_backend" plotmyvert_backend

#### 2.2.2 Docker Run

// now that the main image is created, we can designate the database volume
// with a database volume, the database will persist between container runs
docker volume create plotmyvert_backend_db
docker run --rm -v plotmyvert_backend_db:/db -v /path/to/directory/containing/db:/host_dir alpine cp /host_dir/db.sqlite3 /db/
// docker run --rm removes the container after it is run
// -v mounts the plotmyvert_backend_db volume at /db in the container
// -v mounts the /path/to/directory/containing/db directory from your host machine at /host_dir in the container
// alpine set the lightweight distribution to do this work
// cp copies the db.sqlite3 file from the host directory to the volume

// with that created, now we can run the container
docker run -d -p YOUR_BASE_URL_PORT:8000 -e PLOTMYVERT_BACKEND_SECRET_KEY=YOUR_SECRET_KEY -v plotmyvert_backend_db:/code/db --name "plotmyvert_backend" plotmyvert_backend
// docker run starts a new container
// -d runs the container in detached mode (in the background)
// -p maps the container port (8000) to the host port (YOUR_BASE_URL_PORT)
// -e sets a real secret key and runs without debug mode - skip this if you are only deploying locally
// -v mounts the database volume to the container
// --name sets the name of the container to be referenced when restarting or removing it
// plotmyvert_backend is the name of the image to run

#### 2.2.3 SSL / HTTPS

// SSL / HTTPS is required for production deployment with a secret key (debug mode is tied to secret key generation)
// to disable this requirement, comment the following lines in /plotmyvert_backend/settings.py
// if you're deploying publicly, you should know what you are doing, how to host with Nginx or other servers etc. instructions will not be provided here
// SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
// CSRF_COOKIE_SECURE = True
// SESSION_COOKIE_SECURE = True
