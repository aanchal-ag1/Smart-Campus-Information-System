#python program 9
"""
===========================================================
  SMART CAMPUS INFORMATION SYSTEM
        By Aanchal Agarwal (USN: 1DS25CG002)
  Dayananda Sagar College of Engineering
  Department of Computer Science & Design
  Python Programming Lab — Lab 1 to Lab 8 Integration
===========================================================
"""

import os
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

FILE_NAME = "students.csv"
COURSE_FEE = 1500

# Utility Functions
def calculate_grade(avg):
    if avg >= 90:
        return "A+"
    elif avg >= 80:
        return "A"
    elif avg >= 70:
        return "B"
    elif avg >= 60:
        return "C"
    elif avg >= 50:
        return "D"
    else:
        return "F"


def calculate_fee(num_courses):
    return num_courses * COURSE_FEE


def initialize_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                "ID", "Name", "Age", "Department",
                "Courses", "Marks", "Average", "Grade", "Fee"
            ])


# Student Registration
def register_student():
    student_id = input("Enter Student ID: ")
    name = input("Enter Name: ")
    age = input("Enter Age: ")
    department = input("Enter Department: ")

    courses = input("Enter courses (comma-separated): ").split(",")
    courses = [course.strip() for course in courses if course.strip()]

    marks = []
    for course in courses:
        mark = float(input(f"Enter marks for {course}: "))
        marks.append(mark)

    average = np.mean(marks) if marks else 0
    grade = calculate_grade(average)
    fee = calculate_fee(len(courses))

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            student_id,
            name,
            age,
            department,
            ";".join(courses),
            ";".join(map(str, marks)),
            round(average, 2),
            grade,
            fee
        ])

    print("\nStudent registered successfully!")
    print(f"Average: {average:.2f}")
    print(f"Grade: {grade}")
    print(f"Total Fee: {fee}")


# Display Records
def display_students():
    try:
        df = pd.read_csv(FILE_NAME)
        if df.empty:
            print("No student records found.")
        else:
            print("\nStudent Records:")
            print(df.to_string(index=False))
    except Exception as e:
        print("Error reading file:", e)


# Search Student
def search_student():
    keyword = input("Enter Student ID or Name to search: ").lower()

    try:
        df = pd.read_csv(FILE_NAME)
        result = df[
            df["ID"].astype(str).str.lower().str.contains(keyword) |
            df["Name"].astype(str).str.lower().str.contains(keyword)
        ]

        if result.empty:
            print("Student not found.")
        else:
            print(result.to_string(index=False))
    except Exception as e:
        print("Error:", e)


# Sort Students
def sort_students():
    print("Sort by:")
    print("1. Name")
    print("2. Average Marks")
    print("3. Grade")

    choice = input("Enter choice: ")

    try:
        df = pd.read_csv(FILE_NAME)

        if choice == "1":
            sorted_df = df.sort_values(by="Name")
        elif choice == "2":
            sorted_df = df.sort_values(by="Average", ascending=False)
        elif choice == "3":
            sorted_df = df.sort_values(by="Grade")
        else:
            print("Invalid choice.")
            return

        print(sorted_df.to_string(index=False))
    except Exception as e:
        print("Error:", e)


# Course Enrollment Management
def enroll_course():
    student_id = input("Enter Student ID: ")
    new_course = input("Enter course to enroll: ")

    try:
        df = pd.read_csv(FILE_NAME)

        if student_id not in df["ID"].astype(str).values:
            print("Student not found.")
            return

        idx = df[df["ID"].astype(str) == student_id].index[0]
        existing_courses = str(df.at[idx, "Courses"]).split(";")

        if new_course in existing_courses:
            print("Student already enrolled in this course.")
            return

        existing_courses.append(new_course)
        df.at[idx, "Courses"] = ";".join(existing_courses)

        new_mark = float(input(f"Enter marks for {new_course}: "))
        existing_marks = list(map(float, str(df.at[idx, "Marks"]).split(";")))
        existing_marks.append(new_mark)

        average = np.mean(existing_marks)
        grade = calculate_grade(average)
        fee = calculate_fee(len(existing_courses))

        df.at[idx, "Marks"] = ";".join(map(str, existing_marks))
        df.at[idx, "Average"] = round(average, 2)
        df.at[idx, "Grade"] = grade
        df.at[idx, "Fee"] = fee

        df.to_csv(FILE_NAME, index=False)
        print("Course enrolled successfully.")
    except Exception as e:
        print("Error:", e)


# Analytics
def generate_analytics():
    try:
        df = pd.read_csv(FILE_NAME)

        if df.empty:
            print("No data available.")
            return

        print("\nStudent Records for Analytics:")
        print(df.to_string(index=False))

        df["Average"] = pd.to_numeric(df["Average"], errors="coerce")
        df.dropna(subset=["Average"], inplace=True)
        averages = df["Average"].astype(float)

        print("\nAnalytics Summary:")
        print(f"Mean Score : {np.mean(averages):.2f}")
        print(f"Median Score : {np.median(averages):.2f}")
        print(f"Max Score : {np.max(averages):.2f}")
        print(f"Min Score : {np.min(averages):.2f}")

        df_sorted = df.sort_values(by="Average", ascending=False)

        plt.figure(figsize=(10, 6))
        plt.bar(df_sorted["Name"], df_sorted["Average"])
        plt.title("Student Performance Analysis (Sorted by Average Marks)")
        plt.xlabel("Students")
        plt.ylabel("Average Marks")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig("analytics.png")
        plt.show()

        print("Analytics chart saved as analytics.png")
    except Exception as e:
        print("Error generating analytics:", e)


# Directory Scanner
def scan_directory():
    path = input("Enter directory path (leave blank for current directory): ").strip()

    if not path:
        path = "."

    try:
        files = os.listdir(path)
        print(f"\nFiles in '{os.path.abspath(path)}':")
        for file in files:
            print("-", file)
    except FileNotFoundError:
        print("Directory not found.")
    except PermissionError:
        print("Permission denied.")
    except Exception as e:
        print("Unexpected error:", e)


# Main Menu
def menu():
    initialize_file()

    while True:
        print("\n" + "=" * 50)
        print(" SMART CAMPUS INFORMATION SYSTEM ")
        print("=" * 50)
        print("1. Register Student")
        print("2. Display Student Records")
        print("3. Search Student")
        print("4. Sort Students")
        print("5. Enroll Course")
        print("6. Calculate Fee")
        print("7. Generate Performance Analytics")
        print("8. Scan Directory")
        print("9. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            register_student()
        elif choice == "2":
            display_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            sort_students()
        elif choice == "5":
            enroll_course()
        elif choice == "6":
            num = int(input("Enter number of courses: "))
            print(f"Total Fee: {calculate_fee(num)}")
        elif choice == "7":
            generate_analytics()
        elif choice == "8":
            scan_directory()
        elif choice == "9":
            print("Thank you for using Smart Campus Information System!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    menu()
