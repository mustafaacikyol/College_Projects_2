## Project Course Registration System
### Purpose
You are expected to develop a system that will match students and instructors on the basis of demand and criteria for project courses opened at a university.  

Programming Language: There is no programming language restriction for the implementation of the desktop application, and PostgreSQL must be used for database operations.
### Content
In the desktop application, there are 3 panels: administrator panel, student panel and instructor panel.  

In the admin panel, student and instructor information can be saved, updated and updated.  

operations related to system administration,  

In the instructor panel, instructors can select appropriate students for their courses,  

In the student panel, students can choose from the teachers they want and in accordance with their interests.  

Course request procedures will be made.  

The process of matching teachers to students who will take courses will consist of two main stages:  

The 1st stage is where students who want to take the course can choose the course by agreeing with the instructors they want.  

It includes a consensual selection process.  

The duration of this phase and when it will start and end will be determined by the administrator.  

In this process, the following operations should be performed respectively:  

The student, instructor and administrator must first log in via the relevant panel with their username and password.  

After logging in to the system, the student will upload the pdf file of his/her transcript document to the system externally.  

The content of the uploaded transcript includes information that the student has previously received.  

The course information will be read in the system via OCR and converted into text, and then these data will be saved in the relevant fields in the database.  

Students who upload their transcripts to the system will be able to see the grades and information about the courses they have taken from their own panel.  

The system should list the instructors who teach the course according to the course they want to take for students who have uploaded their transcript, and the student should be able to filter the instructor list according to their interests.  

For each course the student will be able to create a request from a number of different instructors determined by the system administrator (default value: 1) and may withdraw the request unless the request is approved by any instructor.  

When creating a course request from a instructor, a student must be able to send a message to the instructor from the system within the limit of the number of characters determined by the administrator.  

A course will be added to the student from the instructor who first approved his/her request, and the course taken and instructor information will be displayed on the student's panel.  

After the instructor logs into the system, he/she should be able to choose and save their own interests to the system, so that students can see the interests of the instructor.  

The instructor should be able to view the list of students who have requested their courses from the system.  

The instructor should also be able to view students who have requests that have not yet been approved by an instructor or who have not created a request for a course that the instructor also teaches.  

However, other instructors should not see the requests that these students make from other teachers.  

Students whose courses have been approved by another instructor should not be shown to other instructors at all.  

The instructor should be able to click on one of the students listed and view the course information he/she has taken.  

The instructor should be able to create his/her own student scoring formula by selecting the ones she deems important among all the courses offered in the department and assigning coefficients for each selected course.  

The scores of the students he/she listed according to the formula he/she created should also be shown.  

The instructor should be able to filter and sort students according to a formula score he/she creates or a course grade he/she chooses. 

The instructor must be able to approve student requests for the number of quotas determined by the administrator. (The quota amount corresponds to the total number of students who can take lessons from a instructor.  

The same students who take two different courses of a instructor should be considered as 2 students and deducted from the quota. There should not be a separate quota for each course.)  

When the agreed period determined by the administrator expires, the system must close the request, acceptance and approval processes of instructors and students.  

After this stage, random assignment process should be started.  

The second stage is the process in which students who did not make an agreement or whose requests were not approved by any instructor will be distributed to the instructors.  

At this stage, the following operations should be performed:  

It should be possible to assign students automatically from the admin panel.  

Random assignment: All students will be assigned to different instructors respectively, without any conditions.  

Other operations that can be done from the admin panel:  

Access, update and delete information of all students and instructors.  

Managing all necessary parameters and system settings related to the 1st and 2nd stage processes of course selection.  

Viewing and management of all student-instructor requests along with transaction history (they should be able to add any student they want to any instructor they want).  

Registering, updating and deleting interests in the system.  

Automatic student generation should be done in the admin panel to increase the student pool.  

At this stage, students' course and letter grades should be determined randomly, provided that they are not the same for all students. 

The determined information should be added to the database in a format compatible with the students recorded in pdf.  

Production should be possible for up to 50 students at a time.  

Students can work with only one instructor for a course, and a instructor can work with more than one student.  

### Development Process  

***I developed this project using Python programming language, tkinter(for GUI) and postgresql database.***
