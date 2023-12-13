# PlotMyVert - A Vertical Jump Tracking Application

Welcome to the Vert Performance Tracker, a comprehensive full-stack application designed exclusively for athletes using the G-Vert device (https://www.myvert.com). This application is your one-stop solution for tracking, analyzing, and visualizing your jump data in a way that's more advanced and accessible than ever before.

The Vert is an innovative tool for athletes to track their jumps during training, but the original mobile application for the Vert offers a subscription model for advanced features, and it lacks the advanced graphing capabilities and online access that this application provides.

With PlotMyVert, you can easily import your data from the Vert device. Simply use the mobile application to export your data by emailing it to yourself. This is currently the only way to extract data from the device's closed system. Once you've done this, configure your PlotMyVert account with your email login. Our application is designed to read only emails titled "Session Data to Open in Excel" and containing Excel file(s). This data is then imported into the database under your account and stored securely.

You can run this application locally, on your own server, or access my instance at https://vert.duz.ie - just create an account and start importing your data!

Email Configuration is as follows:
receive_email_login: the login username/email for the email account that will receive the data
receive_email_password: the password for the email account that will receive the data
receive_email_receiver: the email address that will receive the data (usually the same as receive_email_login, however services like hidemyemail can be used to hide your real email address but still work with this application)
mail_server: the mail server for the email account that will receive the data (e.g. imap.gmail.com)
mail_port: the mail port for the email account that will receive the data (e.g. 993)
mail_SSL: whether or not the mail server uses SSL

Consult your own service provider for the correct configuration for your email account.

Email configuration must be complete to use this application as it is the only way that you can access data from the Vert device outside of the native application. The application filters emails by subject (Session Data to Open in Excel) and receiver (the email you set up above). The application does not read any other emails. The application will delete the data email from your account after it has beene processed and imported into the database.

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
mkdir db
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
