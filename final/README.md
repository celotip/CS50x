# YUUMORI HELP NEEDED
#### Video Demo:  <https://youtu.be/yyIuH3yP7dQ>
#### Description:
This is a web application that can be used to post questions, "donate" money, and register into a team. Features that are included in this website include:
* A sign up feature which stores a unique username and password
* A login feature if user is signed up
* A navigation bar to view different htmls in the page.
* A forum to post questions and view reply if any exists.
* A donation box to 'donate' money. Data is then stored and the total donations is viewed.
* A registration form where you can select your role from available options. Data of name and role is then stored and displayed.

Files that are included in this folder are:
1. app.py: contains the script for running Flask
2. database.db: a database for storing data of users, questions and replies, and registrants
3. helpers.py: contains apology and login_required functions
4. requirements.txt: contains some required packages that the web app depends on.
5. templates: contains all the html files that are used in the web app

I will describe the relationship between the templates and app.py below:
1. layout.html shows the layout of all the .html files. I included a navbar which I obtained from bootstraps.
1. apology.html shows an image with an error message, if an error happens
1. login.html shows 2 text boxes to enter a username and password. a button is provided to submit the username and passwords. The page will be directed to apology.html if the user fails to provide a valid username and password.
1. signup.html 3 text boxes to enter a username, a password, and retype password. a button is provided to submit the username and passwords. The page will be directed to apology.html if the user fails to provide a valid username and password or if the passwords do not match. Otherwise, the username and password will be stored in database.db
1. index.html shows the homepage. No login is required, so you can view it without having to login.
1. members.html shows a table of members. No login is required.
1. posts.html shows the posts made by admins. Login is required. You will be redirected to the login page.
1. forum.html shows the forum page. Here, you can submit questions or view replies if any. When you post a question, the data will be stored in database.db and displayed in a table below the submit form. Replies can only be viewed if admin has added a reply. If there is, a button will appear and will redirect you to reply1.html if you click it.
1. donate.html shows the donation page. Here, you can "donate" some money. The data will be stored in database.db and a total of all donations from all users in the database will be displayed.
1. register.html shows the registration form. You can input your name here, and select a role from the list of options. The data will be stored in database.db and displayed in a form of a table.


