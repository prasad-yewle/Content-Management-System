Content-Management-System

Welcome to the Django Project! This is a project built using the Django Rest framework for Python. The purpose of this project is to provide a platform for users to create and share content.

<h2>Features</h2>
<ul>
<li>User authentication and authorization</li>
<li>User profile management</li>
<li>Content creation</li>
<li>Content Update and delete</li>
<li>Search functionality</li>
</ul>

<h2>To run this project locally, follow these steps:</h2>
<ol>
<li>Clone the repository to your local machine.</li>
<li>Install the required dependencies by running pip install -r requirements.txt.</li>
<li>Set up the database by running python manage.py migrate.</li>
<li>Start the development server by running python manage.py runserver</li>
</ol>

<h2> API's</h2>
<h4>Registration --- POST method</h4>
<pre>
<code>
http://localhost:8000/api/register/
</code>
</pre>

<h4>Login --- POST method</h4>
<pre>
<code>
http://localhost:8000/api/token/
</code>
</pre>

<h4>Create Content --- POST method</h4>
<pre>
<code>
http://localhost:8000/api/content/
</code>
</pre>

<h4>View Content --- GET method</h4>
<pre>
<code>
http://localhost:8000/api/content/
</code>
</pre>

<h4>Update Content --- PUT method</h4>
<pre>
<code>
http://localhost:8000/api/content/<int:id>/update/
</code>
</pre>

<h4>Delete Content --- Delete method</h4>
<pre>
<code>
http://localhost:8000/api/content/<int:id>/delete/
</code>
</pre>

<h4>Search Content --- GET method</h4>
<pre>
<code>
http://localhost:8000/api/search/?q=
</code>
</pre>





