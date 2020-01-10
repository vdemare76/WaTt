WATT - WebApp TimeTable

This project concerns the creation of a web application aimed at generating a university timetable.

The application will allows you to create and modify the timetable and then publish it as a pdf page, web, rest api and iCAL. 
The timetable will be determined by applying constraints deriving from the training offer and from the teachers

Project actors and their main tasks

- Administrative Staff for the insertion of data concerning the educational offer of a specific academic year.
- Teachers for the insertion of requirements and preferences to be managed as useful constraints for the generation of the timetable.

The system is created using Docker technology and is currently made up of three containers

- Mysql database in which all the information supporting the system is stored.
— OpenLdap server on which suitably profWebiled test users are defined.
- Flask Python web app framework with SQLAlchemy extension for data persistence.

To run the application

1) Download and install docker desktop (latest stable version)
2) Download Watt-master branch and extract the contents of the .zip file to a folder on your filesystem.
3) Execute this docker command : docker-compose up -—build
4) At the end of the container installation and startup procedure, you can access the application by typing the web address: localhost: 5000

Test users (Username/Password)

- Administrative staff profile
	1) tam102001/pw102001
	2) tam102002/pw102002

- Teachers profile
	1) doc101001/pw101001
	2) doc101002/pw101002
	3) doc101003/pw101003
