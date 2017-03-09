
<h1>Honors Project Web Application</h1>

<p>This a Python/Flask web application.</p>

<h2>Necesary tools:</h2>

<ul>
    <li>Flask</li>
    <li>SQLAlchemy</li>
    <li>flask_login</li>
    <li>flask-migrate</li>
    <li>A MySQL database</li>
</ul>

<h2>Database setup</h2>

<p>For the database, you will need to have MySQL installed and running. You need to log in as the root user, then create a new user and database for the project. You will then want to grant all privileges on the database to the database user you created. </p>
<p>You will also need to create an instance directory in the honors directory, and create config.py inside of it. 
In this file, you will add the secret key and database URI for your database.</p>
<p>Finally, you will need to run flask db init, flask db migrate, then flask db upgrade.</p>

