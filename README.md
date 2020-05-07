Readme


Steps to install this project in your environment:
	1. Go to the root directory of this project (Directory with Pipfile)
	2. run this command in terminal:
		pipenv --python 3.7 install django
	3. Acitivate the virtual environment with this commnad
		pipenv shell
	4. Install the required dependencies:
		pip install -r requirements.txt
	4. Check that the project is working by:
		1. go back to the directory of the project that containts the manage.py
		2. run the command
			python3 manage.py runserver
		3. type in the url in the browser
			http://localhost:8000/login
		4. IF you can see the Login page, the project is installed successfully.

About the url routes of this project:
	1. First page (Login page)
		http://localhost:8000/login
	2. The admin page for managing the database
		http://localhost:8000/admin
		username: glcmgcd
		password: testing00@
	3. Entry Point of the system
		1. http://localhost:8000/login

Limitation of the project:
	1. All required functions are implemented to fufill the basic requirement
	2. Error Messages for showing ivalid input are not implemented for some functions
		1. Create PBI Function
			1. User would not be able to create a PBI if invalid data is used
			2. But error messages would be not shown in the user interface for the function
		2. Create Task Function
			1. User would not be able to create a Task if invalid data is used
			2. But error messages would be not shown in the user interface for the function
		3. Create Project Function
			1. User would not be able to create a Project if invalid data is used
			2. But error messages would be not shown in the user interface for the function
		4. Priority Insertion Function
			1. User would not be able to insert a PBI to another priority if invalid data is used
			2. But error messages would be not shown in the user interface for the function
