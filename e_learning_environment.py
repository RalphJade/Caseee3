from platform_admin import PlatformAdmin
from student import Student
from instructor import Instructor
from announcement import Announcement

class E_Learning_Environment:
    def __init__(self):
        self.platform_admin = PlatformAdmin()
        self.platform_admin.load_data()  # Load data on startup
        self.courses = self.platform_admin.courses
        self.students = []
        self.instructors = []
        self.announcements = []
    
    def set_courses(self, courses):
        self.courses = courses

    def main_menu(self):
        while True:
            print("\nWelcome to E-Learning Environment!")
            print("Sign in as Student(1) or Instructor(2):")
            print("1. Student")
            print("2. Instructor")
            print("3. Sign in as Admin")
            print("4. Exit")
            choice = input("Select an option: ")

            if choice == "1":
                self.student_menu()
            elif choice == "2":
                self.instructor_menu()
            elif choice == "3":
                if self.platform_admin.admin_login():  # Static method call
                    self.admin_menu()
            elif choice == "4":
                self.platform_admin.save_data()  # Save data on exit
                print("Exiting the platform. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def student_menu(self):
        student = self.get_student_by_name()
        if not student:
            print("Student not found.")
            return

        while True:
            print(f"\nWelcome, {student.name}")
            print("1. View My Grades")
            print("2. Submit Assignment")
            print("3. Enroll in Courses")
            print("4. View All Enrolled Courses")
            print("5. View Discussion Threads")
            print("6. Display All Schedule")
            print("7. View Announcements")
            print("8. Logout")
            choice = input("Select an option: ")

            if choice == "1":
                self.view_student_grades(student)
            elif choice == "2":
                self.submit_assignment(student)
            elif choice == "3":
                self.enroll_in_courses(student)
            elif choice == "4":
                self.view_student_courses(student)
            elif choice == "5":
                self.view_discussion_threads(student)
            elif choice == "6":
                self.display_all_schedules()
            elif choice == "7":
                self.view_announcements(student)
            elif choice == "8":
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")

    def get_student_by_name(self):
        name = input("Enter your name: ")
        return next((s for s in self.platform_admin.students if s.name == name), None)

    def view_student_grades(self, student):
        print(f"\nGrades for {student.name}:")
        found_grades = False

        for enrollment in self.platform_admin.enrollments._enrollments:
            if enrollment.get('student_id') == student.student_id:
                found_grades = True
                # Assuming you have a method to fetch the course and grade
                print(f"Course: {enrollment['course_name']}, Grade: {enrollment.get('grade', 'N/A')}")
        
        if not found_grades:
            print("No grades found.")

    def submit_assignment(self, student):
        print("\nYour Courses:")
        for course in student.enrolled_courses:
            print(f"- {course.course_name}")

        course_name = input("Enter the course name for which you want to submit an assignment: ").strip()
        course = next((c for c in student.enrolled_courses if c.course_name == course_name), None)

        if not course:
            print("You are not enrolled in this course.")
            return

        assignment_title = input("Enter the assignment title: ").strip()
        assignment = next((a for a in course.assignments if a.title == assignment_title), None)

        if not assignment:
            print("Assignment not found in this course.")
            return

        submission_content = input("Enter your submission content: ").strip()
        print(f"Assignment '{assignment_title}' submitted successfully for course '{course_name}'.")
        print(f"Submission Content: {submission_content}")

    def enroll_in_courses(self, student):
        print("\nAvailable Courses:")
        for course in self.platform_admin.courses:
            print(f"{course.course_name} (Instructor: {course.instructor.name})")

        course_name = input("Enter the course name to enroll in: ")
        course = next((c for c in self.platform_admin.courses if c.course_name == course_name), None)

        if course:
            self.platform_admin.enrollments.enroll_student(student, course)
            print(f"Enrolled in {course_name} successfully!")
        else:
            print("Course not found.")

    def view_student_courses(self, student):
        print(f"\nEnrolled Courses for {student.name}:")
        if not student.enrolled_courses:
            print("You are not enrolled in any courses.")
            return

        for course in student.enrolled_courses:
            print(f"{course.course_name} (Instructor: {course.instructor.name})")

    def display_all_schedules(self):
        print("All schedules:")
        for course in self.courses:
            if hasattr(course, 'schedule') and course.schedule:  # Ensure the course has a schedule
                print(course.schedule.display_schedule())
            else:
                print(f"Course: {course.course_name} has no schedule assigned.")


    def instructor_menu(self):
        instructor = self.get_instructor_by_name()
        if not instructor:
            print("Instructor not found.")
            return

        while True:
            print(f"\nWelcome, {instructor.name}")
            print("1. Assign Assignments")
            print("2. Input Grades")
            print("3. View Enrolled Students")
            print("4. View Courses Taught")
            print("5. View Discussion Threads")
            print("6. Create Announcements")
            print("7. View Announcements")
            print("8. Logout")
            choice = input("Select an option: ")

            if choice == "1":
                instructor.assign_assignments()
            elif choice == "2":
                instructor.input_grades()
            elif choice == "3":
                instructor.view_enrolled_students()
            elif choice == "4":
                instructor.view_courses_taught()
            elif choice == "5":
                instructor.view_discussion_threads()
            elif choice == "6":
                title = input("Enter announcement title: ")
                content = input("Enter announcement content: ")
                date = input("Enter announcement date (YYYY-MM-DD): ")
                recipient_groups = input("Enter recipient groups (e.g., Student, Instructor, Admin): ").split(", ")
                self.create_announcement(title, content, date, recipient_groups)
            elif choice == "7":
                self.view_announcements(instructor)
            elif choice == "8":
                print(f"Goodbye, {instructor.name}!")
                break
            else:
                print("Invalid choice. Please select a valid option.")

    def get_instructor_by_name(self):
        name = input("Enter your name: ")
        return next((i for i in self.platform_admin.instructors if i.name == name), None)

    def assign_assignments(self, instructor):
        print("Available Courses:")
        for course in self.platform_admin.courses:
            if course.instructor.instructor_id == instructor.instructor_id:
                print(f"- {course.course_name} ({course.course_code})")

        course_code = input("Enter the course code to assign an assignment: ")
        course = next((c for c in self.platform_admin.courses if c.course_code == course_code), None)

        if course:
            title = input("Enter assignment title: ")
            description = input("Enter assignment description: ")
            due_date = input("Enter due date (YYYY-MM-DD): ")
            course.assign_assignment(title, description, due_date)
        else:
            print("Course not found.")

    def input_grades(self, instructor):
    # Get the course code and find the corresponding course taught by the instructor
        course_code = input("Enter the course code: ")
        course = next(
            (c for c in self.platform_admin.courses if c.course_code == course_code and c.instructor == instructor),
        None
    )

        if course:
        # Proceed to input grades for the students in this course
            student_id = input("Enter the student ID: ")
            grade = input("Enter the grade: ")

        # Add grade for the student (assuming the course has a list of enrolled students)
        student = next((s for s in course.enrolled_students if s.student_id == student_id), None)
        if student:
            student.add_grade(course, grade)  # Assuming there's a method to add grades to the student
            print(f"Grade for student {student.name} in course {course.course_name} has been updated.")
        else:
            print("Student not found in the course.")
            print("Course not found or you're not assigned to this course.")

    def view_enrolled_students(self, instructor):
        print(f"\nStudents enrolled in courses taught by {instructor.name}:")
        for course in instructor.courses_taught:
            print(f"\nCourse: {course.course_name}")
            if course._students:  # Check if there are enrolled students
                for student in course._students:
                    print(f"- {student.name}")
            else:
                print("No students enrolled in this course.")

    def view_courses_taught(self, instructor):
        print(f"\nCourses taught by {instructor.name}:")
        if instructor.courses_taught:
            for course in instructor.courses_taught:
                print(f"- {course.course_name} (Code: {course.course_code})")
        else:
            print("This instructor is not teaching any courses.")

    def view_discussion_threads(self, user):
        """Allow students and instructors to view discussion threads of enrolled courses."""
        print("\nAvailable Discussion Threads:")
        for course in user.enrolled_courses:
            print(f"\nCourse: {course.course_name}")
            for thread in course.discussion_threads:
                thread.display_thread()
        
        # Option to add a post to a discussion thread
        if isinstance(user, Student) or isinstance(user, Instructor):
            add_post_choice = input("\nDo you want to add a post? (yes/no): ")
            if add_post_choice.lower() == "yes":
                self.add_post_to_thread(user)

    def add_post_to_thread(self, user):
        """Allow user to add a post to a discussion thread."""
        course_name = input("Enter the course name for the thread you want to post in: ")
        course = next((c for c in user.enrolled_courses if c.course_name == course_name), None)

        if not course:
            print("Course not found.")
            return

        thread_title = input("Enter the title of the thread you want to post in: ")
        thread = next((t for t in course.discussion_threads if t.title == thread_title), None)

        if not thread:
            print("Discussion thread not found.")
            return

        message = input("Enter your message: ")
        thread.add_post(user, message)
        print("Post added successfully!")

    def create_announcement(self, title, content, date, recipient_groups):
        """Method to create an announcement."""
        announcement = Announcement(title, content, date, recipient_groups)
        self.announcements.append(announcement)
        print("Announcement created.")

    def view_announcements(self, user):
        """Method to view announcements for the given user."""
        print("\nAnnouncements:")
        for announcement in self.announcements:
            if user.role in announcement.recipient_groups:  # Assuming user has a role attribute
                print(f"- {announcement.title} ({announcement.date}): {announcement.content}")
        if not any(user.role in announcement.recipient_groups for announcement in self.announcements):
            print("No announcements available.")


    def admin_menu(self):
        while True:
            print("\nAdmin Menu")
            print("1. View All Students") 
            print("2. View All Instructors")
            print("3. View All Courses")
            print("4. Create a New Course")
            print("5. Manage Users (Add/Remove Students/Instructors)")
            print("6. View System Statistics")
            print("7. Clear All Announcements")
            print("8. Exit Admin Menu")
            choice = input("Select an option: ")

            if choice == "1":
                self.view_all_students()
            elif choice == "2":
                self.view_all_instructors()
            elif choice == "3":
                self.view_all_courses()
            elif choice == "4":
                self.create_course()
            elif choice == "5":
                self.manage_users()
            elif choice == "6":
                self.view_system_statistics()
            elif choice == "7":
                self.clear_announcements()
            elif choice == "8":
                print("Exiting Admin Menu...")
                break
            else:
                print("Invalid choice. Please try again.")
    def view_all_students(self):
        print("\nAll Students:")
        for student in self.platform_admin.students:
            print(f"- {student.name} (ID: {student.student_id})")

    def view_all_instructors(self):
        print("\nAll Instructors:")
        for instructor in self.platform_admin.instructors:
            print(f"- {instructor.name} (ID: {instructor.instructor_id})")

    def view_all_courses(self):
        print("\nAll Courses:")
        for course in self.platform_admin.courses:
            print(f"- {course.course_name} (Code: {course.course_code})")

    @staticmethod
    def add_student(students, name, student_id, email):
        new_student = Student(name=name, student_id=student_id, email=email)
        students.append(new_student)
        print(f"Student '{name}' added successfully.")

    @staticmethod
    def remove_student(students, name):
        student = next((s for s in students if s.name == name), None)
        if student:
            students.remove(student)
            print(f"Student '{name}' removed successfully.")
        else:
            print("Student not found.")
    
    @staticmethod
    def add_instructor(instructors, name, instructor_id, email):
        new_instructor = Instructor(name=name, instructor_id=instructor_id, email=email)
        instructors.append(new_instructor)
        print(f"Instructor '{name}' added successfully.")

    @staticmethod
    def remove_instructor(instructors, name):
        instructor = next((i for i in instructors if i.name == name), None)

        if instructor:
            instructors.remove(instructor)
            print(f"Instructor '{name}' removed successfully.")
        else:
            print("Instructor not found.")

    def manage_users(self):
        while True:
            print("\nManage Users Menu:")
            print("1. Add Student")
            print("2. Remove Student")
            print("3. Add Instructor")
            print("4. Remove Instructor")
            print("5. Back to Admin Menu")
            choice = input("Select an option: ")

            if choice == "1":
                name = input("Enter student name: ")
                student_id = input("Enter student ID: ")
                email = input("Enter email: ")
                E_Learning_Environment.add_student(self.platform_admin.students, name, student_id, email)
                self.platform_admin.save_data()  # Save to JSON
            elif choice == "2":
                name = input("Enter the name of the student to remove: ")
                E_Learning_Environment.remove_student(self.platform_admin.students, name)
                self.platform_admin.save_data()  # Save to JSON
            elif choice == "3":
                name = input("Enter instructor name: ")
                instructor_id = input("Enter instructor ID: ")
                email = input("Enter email: ")
                E_Learning_Environment.add_instructor(self.platform_admin.instructors, name, instructor_id, email)
                self.platform_admin.save_data()  # Save to JSON
            elif choice == "4":
                name = input("Enter the name of the instructor to remove: ")
                E_Learning_Environment.remove_instructor(self.platform_admin.instructors, name)
                self.platform_admin.save_data()  # Save to JSON
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please try again.")

    def clear_announcements(self):
        self.announcements.clear()
        print("All announcements cleared.")