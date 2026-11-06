"""
=============================================================================
Student Performance Analysis and Visualization System (Python)
=============================================================================
A beginner-friendly academic analysis tool built with foundational Python:
- Variables, Data Types & Arithmetic Operators
- Conditional Statements (if-elif-else)
- Lists and Dictionaries for records
- Functions for marks, percentage, and grade points
- Object-Oriented Programming (Classes, Objects, Constructors, and Methods)
- Calculation of Marks, Percentage, Grade, SGPA, and CGPA
- Visual ASCII Bar Chart Output in Terminal (Zero External Dependencies)
=============================================================================
"""

import sys

# ---------------------------------------------------------------------------
# 1. CORE FUNCTIONS (Calculations & Grading)
# ---------------------------------------------------------------------------

def calculate_total(marks_dict):
    """
    Calculates total marks from a dictionary of subject marks.
    Uses basic loop accumulation.
    """
    total = 0
    for subject in marks_dict:
        total = total + marks_dict[subject]
    return total


def calculate_percentage(total_marks, subject_count):
    """
    Calculates percentage based on total marks and number of subjects (out of 100).
    """
    if subject_count <= 0:
        return 0.0
    max_possible = subject_count * 100
    percentage = (total_marks / max_possible) * 100
    return round(percentage, 2)


def marks_to_grade_point(mark):
    """
    Converts subject mark (0-100) to 4.0 Grade Point Scale and letter grade
    using standard if-elif-else conditional branching.
    """
    mark = float(mark)
    if mark >= 80:
        return 4.00, "A+", "Outstanding"
    elif mark >= 75:
        return 3.75, "A", "Excellent"
    elif mark >= 70:
        return 3.50, "A-", "Very Good"
    elif mark >= 65:
        return 3.25, "B+", "Good"
    elif mark >= 60:
        return 3.00, "B", "Above Average"
    elif mark >= 55:
        return 2.75, "B-", "Average"
    elif mark >= 50:
        return 2.50, "C+", "Below Average"
    elif mark >= 45:
        return 2.25, "C", "Pass"
    elif mark >= 40:
        return 2.00, "D", "Conditional Pass"
    else:
        return 0.00, "F", "Fail"


def calculate_sgpa(course_list):
    """
    Computes Semester Grade Point Average (SGPA).
    course_list: list of dicts [{'name': str, 'marks': float, 'credits': float}]
    Formula: sum(credit * grade_point) / sum(credits)
    """
    total_credits = 0.0
    total_quality_points = 0.0

    for course in course_list:
        credits = float(course.get("credits", 3.0))
        marks = float(course.get("marks", 0.0))
        gp, letter, _ = marks_to_grade_point(marks)
        quality_point = credits * gp

        total_credits = total_credits + credits
        total_quality_points = total_quality_points + quality_point

    if total_credits <= 0:
        return 0.0, 0.0, 0.0

    sgpa = round(total_quality_points / total_credits, 2)
    return sgpa, total_credits, round(total_quality_points, 2)


def calculate_cgpa(semesters_list):
    """
    Computes Cumulative Grade Point Average (CGPA) across multiple semesters.
    Formula: sum(Total QP of all semesters) / sum(Total Credits of all semesters)
    """
    grand_credits = 0.0
    grand_qp = 0.0

    for sem in semesters_list:
        courses = sem.get("courses", [])
        sgpa, sem_credits, sem_qp = calculate_sgpa(courses)
        grand_credits = grand_credits + sem_credits
        grand_qp = grand_qp + sem_qp

    if grand_credits <= 0:
        return 0.0, 0.0, 0.0

    cgpa = round(grand_qp / grand_credits, 2)
    return cgpa, grand_credits, round(grand_qp, 2)


# ---------------------------------------------------------------------------
# 2. OBJECT-ORIENTED PROGRAMMING (Classes & Inheritance)
# ---------------------------------------------------------------------------

class Person:
    """Base class representing a person."""
    def __init__(self, name):
        self.name = name


class Student(Person):
    """
    Derived class representing a student.
    Encapsulates roll number, subject marks dictionary, and performance methods.
    """
    def __init__(self, roll_no, name, marks=None):
        super().__init__(name)
        self.roll_no = roll_no
        # Dictionary storing { 'Subject Name': marks }
        self.marks = marks if marks is not None else {}

    def add_mark(self, subject, mark):
        self.marks[subject] = float(mark)

    def get_total(self):
        return calculate_total(self.marks)

    def get_percentage(self):
        return calculate_percentage(self.get_total(), len(self.marks))

    def get_overall_grade(self):
        pct = self.get_percentage()
        gp, grade, remarks = marks_to_grade_point(pct)
        return grade, gp, remarks

    def get_sgpa(self, credit_per_subject=3.0):
        courses = []
        for sub, score in self.marks.items():
            courses.append({"name": sub, "marks": score, "credits": credit_per_subject})
        sgpa, credits, qp = calculate_sgpa(courses)
        return sgpa

    def display_report(self):
        total = self.get_total()
        pct = self.get_percentage()
        grade, gp, remarks = self.get_overall_grade()
        sgpa = self.get_sgpa()

        print("\n" + "=" * 60)
        print(f" STUDENT ACADEMIC REPORT: {self.name.upper()} (Roll #{self.roll_no})")
        print("=" * 60)
        print(f"{'Subject':<25}{'Marks':<10}{'Grade':<8}{'Grade Point':<12}")
        print("-" * 60)
        for subject, score in self.marks.items():
            sub_gp, sub_grade, _ = marks_to_grade_point(score)
            print(f"{subject:<25}{score:<10.1f}{sub_grade:<8}{sub_gp:<12.2f}")
        print("-" * 60)
        print(f"Total Marks      : {total:.1f} / {len(self.marks) * 100}")
        print(f"Percentage       : {pct:.2f}%")
        print(f"Overall Grade    : {grade} ({remarks})")
        print(f"Semester SGPA    : {sgpa:.2f} / 4.00")
        print("=" * 60)


class PerformanceSystem:
    """
    Manages a collection of students, class-wide analytics, and visual charts.
    """
    def __init__(self):
        self.students = []

    def add_student(self, student):
        self.students.append(student)

    def print_class_summary(self):
        if not self.students:
            print("No student records available.")
            return

        print("\n" + "=" * 76)
        print("            STUDENT ACADEMIC PERFORMANCE SUMMARY TABLE")
        print("=" * 76)
        print(f"{'Roll':<6}{'Name':<22}{'Total':<8}{'Pct (%)':<10}{'Grade':<8}{'SGPA (4.0)':<10}{'Status'}")
        print("-" * 76)

        total_percentages = 0.0
        top_student = None
        highest_pct = -1.0

        for s in self.students:
            tot = s.get_total()
            pct = s.get_percentage()
            grade, _, _ = s.get_overall_grade()
            sgpa = s.get_sgpa()
            status = "PASS" if pct >= 40.0 else "FAIL"

            total_percentages = total_percentages + pct
            if pct > highest_pct:
                highest_pct = pct
                top_student = s

            print(f"{s.roll_no:<6}{s.name:<22}{tot:<8.0f}{pct:>5.1f}%    {grade:<8}{sgpa:>5.2f}     {status}")

        avg_pct = total_percentages / len(self.students)
        print("=" * 76)
        print(f"Total Students  : {len(self.students)}")
        print(f"Class Average   : {avg_pct:.2f}%")
        if top_student:
            print(f"Top Performer   : {top_student.name} ({highest_pct:.1f}%)")
        print("=" * 76)

    def print_visual_chart(self):
        """
        Visualizes student SGPA in terminal using ASCII bar graph.
        """
        if not self.students:
            print("No students to visualize.")
            return

        print("\n" + "=" * 70)
        print("       STUDENT SGPA VISUALIZATION CHART (4.00 SCALE)")
        print("=" * 70)
        for s in self.students:
            sgpa = s.get_sgpa()
            # 4.0 scale mapped to 40 characters bar width (each 0.1 = 1 char)
            bar_len = int((sgpa / 4.0) * 35)
            bar = "■" * bar_len
            print(f"{s.name:<20} [{sgpa:>4.2f}] | {bar}")
        print("=" * 70)
        print("Scale: 0.00 ----------------------- 2.00 ---------------------- 4.00")


# ---------------------------------------------------------------------------
# 3. SAMPLE DATA SEEDING
# ---------------------------------------------------------------------------

def seed_sample_system():
    system = PerformanceSystem()
    students_data = [
        (101, "Amina Al-Mansoor", {"Mathematics": 94, "Science": 91, "English": 88, "Python Programming": 98, "History": 85}),
        (102, "David Chen", {"Mathematics": 82, "Science": 86, "English": 79, "Python Programming": 92, "History": 80}),
        (103, "Fatima Zahra", {"Mathematics": 74, "Science": 71, "English": 83, "Python Programming": 77, "History": 75}),
        (104, "Lucas Silva", {"Mathematics": 62, "Science": 65, "English": 58, "Python Programming": 70, "History": 60}),
        (105, "Hannah Brooks", {"Mathematics": 48, "Science": 52, "English": 44, "Python Programming": 55, "History": 41}),
    ]

    for roll, name, marks in students_data:
        student = Student(roll, name, marks)
        system.add_student(student)

    return system


# ---------------------------------------------------------------------------
# 4. INTERACTIVE CLI RUNNER
# ---------------------------------------------------------------------------

def run_custom_input():
    print("\n--- Enter New Student Record & Calculate GPA/SGPA ---")
    try:
        roll_input = input("Enter Student Roll Number: ").strip()
        roll_no = int(roll_input) if roll_input else 106
        name = input("Enter Student Full Name: ").strip()
        if not name:
            name = "Student User"

        print("\nEnter marks (0 to 100) for standard courses:")
        subjects = ["Mathematics", "Science", "English", "Python Programming", "History"]
        student_marks = {}
        for sub in subjects:
            val = input(f"  {sub}: ").strip()
            score = float(val) if val else 75.0
            score = max(0.0, min(100.0, score))
            student_marks[sub] = score

        s = Student(roll_no, name, student_marks)
        s.display_report()

    except Exception as e:
        print(f"Input error: {e}. Please enter valid numeric marks.")


def main():
    system = seed_sample_system()

    # If run in non-interactive or automated environment, print summary and chart
    if not sys.stdin.isatty():
        system.print_class_summary()
        system.print_visual_chart()
        return

    while True:
        print("\n==================================================")
        print(" STUDENT PERFORMANCE ANALYSIS & VISUALIZATION")
        print("==================================================")
        print("1. View Sample Records & Class Summary Table")
        print("2. View ASCII SGPA Visualization Chart")
        print("3. Enter Your Marks & Calculate (GPA / SGPA / CGPA)")
        print("4. Inspect Individual Student Full Report")
        print("5. Exit System")
        print("==================================================")

        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            system.print_class_summary()
        elif choice == "2":
            system.print_visual_chart()
        elif choice == "3":
            run_custom_input()
        elif choice == "4":
            print("\nAvailable students:")
            for idx, s in enumerate(system.students, start=1):
                print(f"  {idx}. Roll {s.roll_no}: {s.name}")
            pick = input("Enter number to view report: ").strip()
            if pick.isdigit() and 1 <= int(pick) <= len(system.students):
                system.students[int(pick) - 1].display_report()
            else:
                print("Invalid selection.")
        elif choice == "5":
            print("\nExiting Student Performance System. Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1 through 5.")


if __name__ == "__main__":
    main()
