<B>WATT2 - WebApp TimeTable</B>

This project concerns the creation of a web application aimed at generating a university timetable.

The application will allows you to create and modify the timetable and then publish it as a pdf page, web, rest api and iCAL. 
The timetable will be determined by applying the constraints deriving from the training offer and directly from the needs expressed by the professors.

Project actors and their main tasks

<ul><li><b>Administrative Staff</b> for the insertion of data concerning the educational offer of a specific academic year.</li>
<li><u><b>Professors</b></u> for the insertion of requirements and preferences to be managed as useful constraints for the generation of the timetable.</li></ul>

The system is created using Docker technology and is currently made up of three containers

<ul>
<li>Mysql database in which all the information supporting the system is stored.</li>
<li>OpenLdap server on which suitably profiled test users are defined.</li>
<li>Flask Python web app framework with SQLAlchemy extension for data persistence.</li>
</ul>

To run the application

1) Download and install docker desktop (latest stable version)
2) Download master branch of WATT and extract the contents of the .zip file to a folder on your filesystem.
3) Execute from this folder the command : docker-compose up -—build
4) At the end of the container installation and startup procedure, you can access the application by typing the web address localhost:5000

Test users (Username/Password)

- Superuser admin
	1) adm101001/pw101001

- Professors profile
	1) doc201001/pw201001
	2) doc201002/pw201002
	3) doc201003/pw201003

- Administrative staff profile
	1) tam202001/pw202001
	2) tam202002/pw202002
	
To explore the system structure, the connection parameters to the database and the openldap server are shown below
- db : watt/wwaatttt (localhost - port 3306)
- openldap : cn=admin,dc=uniparthenope,dc=it/wattpw01 (localhost - port:389)

