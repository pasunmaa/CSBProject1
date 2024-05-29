Cyber Security Base Project 1

The application is a stock asset registry, where logged in users can manage (add, update, view and delete) see their own transactions. The application is the web application built on top of django framework. Per project's definitions there are five documented vulnerabilities in the application. The application and flaws are tested on Chrome browser.

The application itself is far from the complete and have some issues related e.g. to usability and favicons, but it's built for demonstrating the vulnerabilities not for the real use.

In the db.sqlite3 database there are three users. User names and password are:
admin   admin
petri   salainen1
kalle   salainen1

The server can be tested locally by running 'python manage.py runserver' on projects rootfolder.
Access the application from a browser by typing http://localhost:8000/ on the address field.