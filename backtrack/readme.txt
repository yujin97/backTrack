Steps to install this project in your environment:
	1. Go to the root directory of this project (Directory with Pipfile)
	2. run this command in terminal:
		pipenv --python 3.7 install django
	3. Acitivate the virtual environment with this commnad
		pipenv shell
	4. Check that the project is working by:
		1. go back to the directory of the project that containts the manage.py
		2. run the command
			python3 manage.py runserver
		3. type in the url in the browser
			http://localhost:8000/myApp/pbis
		4. IF you can see the 'Showing all PBI' page, the project is installed successfully.

About the url routes of this project:
	1. All the pages created by this app have to be accessed from url starts with
		http://localhost:8000/myApp/
	2. The admin page for managing the database
		http://localhost:8000/admin
		username: teamRed
		password: testing00@
	3. There are currently one working page only
		1. http://localhost:8000/myApp/pbis
	4. Location of static files (To put files like js, css)
		BackTrack/backtrack/Static

Functions to work on:
	1. View specific pbi page
		Can just slightlt edit class ProductOwnersViewPBI
		myApp/url.py
			myApp/views.py
			templates (can just update templates/order_list.html)
			corresponding js (can edit script.js in static)
	2. Delete function
		The view is almost done, need to modify some varible name
		files to work on: 
			myApp/url.py
			myApp/views.py
			templates (just add code to PBI_list,html)
			corresponding js (can edit script.js in static)
	3. Edit pbi
		not started
		files to work on:
			myApp/url.py
			myApp/views.py
			templates (can just add functions to the template showing specific pbi)
			corresponding js
	4. Create pbi
		not started
		filers to work on:
			myApp/url.py
			myApp/views.py
			templates (need a new templates because it is a separated page)
			corresponding js