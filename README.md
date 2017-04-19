
<h1>Honors Project Web Application</h1>

<p>This a Python/Flask web application.</p>

<h2>Necessary depenencies:</h2>

<ul>
    <li>Flask</li>
    <li>Flask-SQLAlchemy</li>
    <li>Flask-MySQL</li>
    <li>Flask-Login</li>
    <li>Flask-Bootstrap</li>
    <li>Flask-Mail</li>
    <li>datetime</li>
    <li>Pandas</p>
</ul>

<h2>MySQL Database setup</h2>

<p>For the database, you will need to have MySQL installed and running. You need to log in as the root user, then create a new user and database for the project. 

You will then want to grant all privileges on the database to the database user you created. </p>
<p>You will also need to create an instance directory in the main directory, and create config.py inside of it. 
In this file, you will add the secret key and database URI for your database.</p>
Example instance/config.py:<br />
<pre>
    <code>
    SECRET_KEY = 'secret_key'
    SQLALCHEMY_DATABASE_URI = 'mysql://user:password@localhost/database'
    </code>
</pre>

<p>Finally, you will need to run flask db init to initialize the database.</p>
<code>>> flask db init</code>
<p>Run flask db migrate to perform the first sqlalchemy database migration.</p>
<code>>> flask db migrate</code>
<p>And flask db upgrade to commit the migration.</p>
<code>>> flask db upgrade</code>