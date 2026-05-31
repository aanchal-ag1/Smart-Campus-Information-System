
"""
===========================================================
  SMART CAMPUS INFORMATION SYSTEM
        By Aanchal Agarwal (USN: 1DS25CG002)
  Dayananda Sagar College of Engineering
  Department of Computer Science & Design
  Python Programming Lab — Lab 1 to Lab 8 Integration
===========================================================
"""

# ─────────────────────────────────────────────
#  IMPORTS
# ─────────────────────────────────────────────
import sys
import os
import json
import math
import datetime

# Configure standard output for UTF-8 encoding strings safely
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Data Science & Visualization Dependencies
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # non-interactive backend (safe for all OS)
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ═══════════════════════════════════════════════════════════════════════════════
#  LAB 1 – STUDENT REGISTRATION & GRADE EVALUATION
#  Topics: variables, input/output, if-elif-else, loops, lists
# ═══════════════════════════════════════════════════════════════════════════════


students = {}


def assign_grade(marks):
    """Return letter grade and result based on average marks (0-100)."""
    if marks >= 90:
        return "O",  "Pass"
    elif marks >= 80:
        return "A+", "Pass"
    elif marks >= 70:
        return "A",  "Pass"
    elif marks >= 60:
        return "B+", "Pass"
    elif marks >= 50:
        return "B",  "Pass"
    elif marks >= 40:
        return "C",  "Pass"
    else:
        return "F",  "Fail"


def register_student():
    """Lab 1 – Register a new student and evaluate their grade."""
    print("\n" + "─" * 50)
    print("  LAB 1 │ STUDENT REGISTRATION & GRADE EVALUATION")
    print("─" * 50)

    usn   = input("  Enter USN          : ").strip().upper()
    if not usn:
        print("  [!] USN cannot be empty.")
        return
    if usn in students:
        print(f"  [!] Student {usn} already registered.")
        return

    name  = input("  Enter Student Name : ").strip()
    dept  = input("  Enter Department   : ").strip()
    sem   = input("  Enter Semester (1-8): ").strip()

    subjects = []
    try:
        n = int(input("  Number of subjects : "))
        if n <= 0:
            raise ValueError
    except ValueError:
        print("  [!] Invalid number of subjects.")
        return

    total = 0
    for i in range(1, n + 1):
        sub_name = input(f"  Subject {i} name     : ").strip()
        while True:
            try:
                marks = float(input(f"  Marks in {sub_name}  : "))
                if 0 <= marks <= 100:
                    break
                print("  [!] Marks must be between 0 and 100.")
            except ValueError:
                print("  [!] Enter a numeric value.")
        subjects.append({"subject": sub_name, "marks": marks})
        total += marks

    avg   = total / n
    grade, result = assign_grade(avg)

    student = {
        "name":      name,
        "dept":      dept,
        "semester":  sem,
        "subjects":  subjects,
        "total":     round(total, 2),
        "average":   round(avg, 2),
        "grade":     grade,
        "result":    result,
        "courses":   [],
        "fees_paid": 0.0,
        "reg_date":  str(datetime.date.today()),
    }
    students[usn] = student

    print(f"\n  ✔ Student {name} ({usn}) registered successfully!")
    print(f"  Average Marks : {avg:.2f}  |  Grade : {grade}  |  Result : {result}")


def view_student():
    """Display all details of a registered student."""
    print("\n" + "─" * 50)
    print("  LAB 1 │ VIEW STUDENT DETAILS")
    print("─" * 50)
    usn = input("  Enter USN : ").strip().upper()
    if usn not in students:
        print("  [!] Student not found.")
        return
    s = students[usn]
    print(f"\n  USN        : {usn}")
    print(f"  Name       : {s['name']}")
    print(f"  Department : {s['dept']}")
    print(f"  Semester   : {s['semester']}")
    print(f"  Reg. Date  : {s['reg_date']}")
    print(f"\n  {'Subject':<25} {'Marks':>6}")
    print(f"  {'─'*25} {'─'*6}")
    for sub in s["subjects"]:
        print(f"  {sub['subject']:<25} {sub['marks']:>6.1f}")
    print(f"  {'─'*25} {'─'*6}")
    print(f"  {'Total':<25} {s['total']:>6.1f}")
    print(f"  {'Average':<25} {s['average']:>6.1f}")
    print(f"  {'Grade':<25} {s['grade']:>6}")
    print(f"  {'Result':<25} {s['result']:>6}")
    print(f"  {'Courses Enrolled':<25} {', '.join(s['courses']) if s['courses'] else 'None':>6}")
    print(f"  {'Fees Paid':<25} ₹{s['fees_paid']:>5.2f}")


# ═══════════════════════════════════════════════════════════════════════════════
#  LAB 2 – COURSE ENROLLMENT MANAGEMENT
#  Topics: lists, tuples, sets, dictionaries
# ═══════════════════════════════════════════════════════════════════════════════

# Available courses stored as {code: {"name":…, "credits":…, "seats":…}}
courses = {
    "CS101": {"name": "Introduction to Python",   "credits": 4, "seats": 60},
    "CS102": {"name": "Data Structures",           "credits": 4, "seats": 60},
    "CS103": {"name": "Database Management",       "credits": 3, "seats": 55},
    "CS104": {"name": "Computer Networks",         "credits": 3, "seats": 55},
    "MA101": {"name": "Engineering Mathematics",   "credits": 4, "seats": 70},
    "EE101": {"name": "Basic Electronics",         "credits": 3, "seats": 65},
    "PH101": {"name": "Engineering Physics",       "credits": 3, "seats": 65},
}
# track enrollments per course  {code: set of USNs}
enrollments = {code: set() for code in courses}


def list_courses():
    """Display all available courses."""
    print(f"\n  {'Code':<8} {'Course Name':<30} {'Credits':>7} {'Seats':>6} {'Enrolled':>8}")
    print(f"  {'─'*8} {'─'*30} {'─'*7} {'─'*6} {'─'*8}")
    for code, info in courses.items():
        enrolled = len(enrollments[code])
        print(f"  {code:<8} {info['name']:<30} {info['credits']:>7} {info['seats']:>6} {enrolled:>8}")


def enroll_student():
    """Lab 2 – Enroll a student in one or more courses."""
    print("\n" + "─" * 50)
    print("  LAB 2 │ COURSE ENROLLMENT MANAGEMENT")
    print("─" * 50)
    usn = input("  Enter USN : ").strip().upper()
    if usn not in students:
        print("  [!] Student not found. Please register first.")
        return

    list_courses()
    codes = input("\n  Enter course code(s) to enroll (comma-separated): ").strip().upper().split(",")
    enrolled_now = []
    for code in codes:
        code = code.strip()
        if code not in courses:
            print(f"  [!] Course {code} does not exist.")
            continue
        if code in students[usn]["courses"]:
            print(f"  [!] Already enrolled in {code}.")
            continue
        if len(enrollments[code]) >= courses[code]["seats"]:
            print(f"  [!] No seats available in {code}.")
            continue
        students[usn]["courses"].append(code)
        enrollments[code].add(usn)
        enrolled_now.append(code)

    if enrolled_now:
        print(f"\n  ✔ Enrolled in: {', '.join(enrolled_now)}")
        print(f"  Current courses: {', '.join(students[usn]['courses'])}")


def drop_course():
    """Lab 2 – Drop a course for a student."""
    print("\n" + "─" * 50)
    print("  LAB 2 │ DROP COURSE")
    print("─" * 50)
    usn  = input("  Enter USN         : ").strip().upper()
    if usn not in students:
        print("  [!] Student not found.")
        return
    if not students[usn]["courses"]:
        print("  [!] No courses enrolled.")
        return
    print(f"  Enrolled courses  : {', '.join(students[usn]['courses'])}")
    code = input("  Enter course code to drop: ").strip().upper()
    if code not in students[usn]["courses"]:
        print("  [!] Not enrolled in that course.")
        return
    students[usn]["courses"].remove(code)
    enrollments[code].discard(usn)
    print(f"  ✔ Dropped {code}. Remaining: {', '.join(students[usn]['courses']) or 'None'}")


# ═══════════════════════════════════════════════════════════════════════════════
#  LAB 3 – STUDENT RECORDS MANAGEMENT
#  Topics: functions, lists of dicts, CRUD operations
# ═══════════════════════════════════════════════════════════════════════════════

def display_all_students():
    """Lab 3 – Display all registered students in a tabular format."""
    print("\n" + "─" * 50)
    print("  LAB 3 │ STUDENT RECORDS MANAGEMENT")
    print("─" * 50)
    if not students:
        print("  [!] No students registered yet.")
        return
    print(f"\n  {'USN':<12} {'Name':<22} {'Dept':<10} {'Sem':>3} {'Avg':>6} {'Grade':>6} {'Result':>7}")
    print(f"  {'─'*12} {'─'*22} {'─'*10} {'─'*3} {'─'*6} {'─'*6} {'─'*7}")
    for usn, s in students.items():
        print(f"  {usn:<12} {s['name']:<22} {s['dept']:<10} {s['semester']:>3} "
              f"{s['average']:>6.1f} {s['grade']:>6} {s['result']:>7}")
    print(f"\n  Total students registered: {len(students)}")


def update_student():
    """Lab 3 – Update student name or department."""
    print("\n" + "─" * 50)
    print("  LAB 3 │ UPDATE STUDENT RECORD")
    print("─" * 50)
    usn = input("  Enter USN : ").strip().upper()
    if usn not in students:
        print("  [!] Student not found.")
        return
    s = students[usn]
    print(f"  Current Name : {s['name']}  |  Dept : {s['dept']}")
    new_name = input(f"  New name (press Enter to keep '{s['name']}'): ").strip()
    new_dept = input(f"  New dept (press Enter to keep '{s['dept']}'): ").strip()
    if new_name:
        s["name"] = new_name
    if new_dept:
        s["dept"] = new_dept
    print("  ✔ Student record updated.")


def delete_student():
    """Lab 3 – Delete a student record."""
    print("\n" + "─" * 50)
    print("  LAB 3 │ DELETE STUDENT RECORD")
    print("─" * 50)
    usn = input("  Enter USN to delete : ").strip().upper()
    if usn not in students:
        print("  [!] Student not found.")
        return
    confirm = input(f"  Confirm delete '{students[usn]['name']}' ({usn})? (yes/no): ").strip().lower()
    if confirm == "yes":
        for code in students[usn].get("courses", []):
            enrollments[code].discard(usn)
        del students[usn]
        print("  ✔ Student record deleted.")
    else:
        print("  [!] Deletion cancelled.")


# ═══════════════════════════════════════════════════════════════════════════════
#  LAB 4 – SEARCHING & SORTING STUDENT DATA
#  Topics: linear search, binary search, bubble sort, sort(), sorted()
# ═══════════════════════════════════════════════════════════════════════════════

def linear_search(key, field="name"):
    """Linear search across all students by name or USN."""
    results = []
    key_lower = key.lower()
    for usn, s in students.items():
        if field == "usn":
            if usn.lower() == key_lower:
                results.append((usn, s))
        elif field == "name":
            if key_lower in s["name"].lower():
                results.append((usn, s))
        elif field == "dept":
            if key_lower in s["dept"].lower():
                results.append((usn, s))
    return results


def binary_search_by_name(name_key):
    """Binary search on name-sorted list of students."""
    sorted_list = sorted(students.items(), key=lambda x: x[1]["name"].lower())
    lo, hi      = 0, len(sorted_list) - 1
    target      = name_key.lower()
    while lo <= hi:
        mid = (lo + hi) // 2
        mid_name = sorted_list[mid][1]["name"].lower()
        if mid_name == target:
            return [sorted_list[mid]]
        elif mid_name < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return []


def bubble_sort_students(field="average", reverse=False):
    """Bubble sort student list by a numeric field."""
    items = list(students.items())
    n = len(items)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            val_j  = items[j][1].get(field, 0)
            val_j1 = items[j + 1][1].get(field, 0)
            if (val_j > val_j1) if not reverse else (val_j < val_j1):
                items[j], items[j + 1] = items[j + 1], items[j]
    return items


def search_and_sort_menu():
    """Lab 4 – Interactive search & sort menu."""
    print("\n" + "─" * 50)
    print("  LAB 4 │ SEARCH & SORT STUDENT DATA")
    print("─" * 50)
    print("  1. Linear Search  (by USN / Name / Dept)")
    print("  2. Binary Search  (by exact Name)")
    print("  3. Sort by Average (Bubble Sort – Ascending)")
    print("  4. Sort by Average (Python built-in – Descending)")
    print("  5. Sort by Name   (Alphabetical)")
    ch = input("  Choice: ").strip()

    if ch == "1":
        field = input("  Search by (usn/name/dept): ").strip().lower()
        key   = input("  Enter search key           : ").strip()
        res   = linear_search(key, field)
        if res:
            for usn, s in res:
                print(f"  Found → {usn} | {s['name']} | {s['dept']} | Avg: {s['average']}")
        else:
            print("  No matching records found.")

    elif ch == "2":
        name = input("  Enter exact name: ").strip()
        res  = binary_search_by_name(name)
        if res:
            for usn, s in res:
                print(f"  Found → {usn} | {s['name']} | {s['dept']} | Avg: {s['average']}")
        else:
            print("  No matching records found.")

    elif ch == "3":
        sorted_list = bubble_sort_students("average")
        print(f"\n  {'USN':<12} {'Name':<22} {'Average':>8}  (Bubble Sort ↑)")
        for usn, s in sorted_list:
            print(f"  {usn:<12} {s['name']:<22} {s['average']:>8.1f}")

    elif ch == "4":
        sorted_list = sorted(students.items(), key=lambda x: x[1]["average"], reverse=True)
        print(f"\n  {'USN':<12} {'Name':<22} {'Average':>8}  (Built-in sort ↓)")
        for usn, s in sorted_list:
            print(f"  {usn:<12} {s['name']:<22} {s['average']:>8.1f}")

    elif ch == "5":
        sorted_list = sorted(students.items(), key=lambda x: x[1]["name"].lower())
        print(f"\n  {'USN':<12} {'Name':<22} {'Grade':>6}  (Alphabetical ↑)")
        for usn, s in sorted_list:
            print(f"  {usn:<12} {s['name']:<22} {s['grade']:>6}")

    else:
        print("  Invalid choice.")


# ═══════════════════════════════════════════════════════════════════════════════
#  LAB 5 – FEE CALCULATION USING FUNCTIONS
#  Topics: functions, default args, lambda, recursion
# ═══════════════════════════════════════════════════════════════════════════════

BASE_TUITION  = 50000.0   # ₹ per semester
CREDIT_FEE    = 1500.0    # ₹ per credit
EXAM_FEE      = 800.0
LIBRARY_FEE   = 500.0
LAB_FEE       = 2000.0
HOSTEL_FEE    = 12000.0
TRANSPORT_FEE = 3000.0
SCHOLARSHIP_RATES = {"O": 0.20, "A+": 0.15, "A": 0.10, "B+": 0.05}


def calculate_tuition(num_credits, base=BASE_TUITION, rate=CREDIT_FEE):
    """Tuition = base + credits × rate."""
    return base + num_credits * rate


def apply_scholarship(total, grade):
    """Apply grade-based scholarship discount (lambda)."""
    discount = (lambda g, r: r.get(g, 0))(grade, SCHOLARSHIP_RATES)
    return total - total * discount, discount * 100


def compound_fee(principal, rate, years):
    """Recursive compound interest for fee instalment plans."""
    if years == 0:
        return principal
    return compound_fee(principal * (1 + rate / 100), rate, years - 1)


def calculate_fees():
    """Lab 5 – Full fee calculation for a student."""
    print("\n" + "─" * 50)
    print("  LAB 5 │ FEE CALCULATION")
    print("─" * 50)
    usn = input("  Enter USN : ").strip().upper()
    if usn not in students:
        print("  [!] Student not found.")
        return
    s = students[usn]

    hostel    = input("  Hostel accommodation? (yes/no): ").strip().lower() == "yes"
    transport = input("  Transport facility?   (yes/no): ").strip().lower() == "yes"

    # Total enrolled credits
    total_credits = sum(courses[c]["credits"] for c in s["courses"] if c in courses)
    tuition       = calculate_tuition(total_credits)
    exam          = EXAM_FEE
    library       = LIBRARY_FEE
    lab           = LAB_FEE
    hostel_amt    = HOSTEL_FEE if hostel else 0
    transport_amt = TRANSPORT_FEE if transport else 0

    gross = tuition + exam + library + lab + hostel_amt + transport_amt
    net, disc_pct = apply_scholarship(gross, s["grade"])

    print(f"\n  Fee Breakdown for {s['name']} ({usn})")
    print(f"  {'─'*45}")
    print(f"  {'Tuition (Base + Credits)':<30} ₹{tuition:>9,.2f}")
    print(f"  {'  Credits enrolled':<30} {total_credits} credits")
    print(f"  {'Examination Fee':<30} ₹{exam:>9,.2f}")
    print(f"  {'Library Fee':<30} ₹{library:>9,.2f}")
    print(f"  {'Lab Fee':<30} ₹{lab:>9,.2f}")
    if hostel:
        print(f"  {'Hostel Fee':<30} ₹{hostel_amt:>9,.2f}")
    if transport:
        print(f"  {'Transport Fee':<30} ₹{transport_amt:>9,.2f}")
    print(f"  {'─'*45}")
    print(f"  {'Gross Total':<30} ₹{gross:>9,.2f}")
    print(f"  {'Scholarship Discount':<30} {disc_pct:.0f}%  (-₹{gross-net:,.2f})")
    print(f"  {'NET PAYABLE':<30} ₹{net:>9,.2f}")

    # Update paid record
    students[usn]["fees_paid"] = round(net, 2)
    print(f"\n  ✔ Fee record updated.")

    # Bonus: compound interest for EMI (2 years, 6%)
    emi_total = compound_fee(net / 4, 6, 2)
    print(f"  Quarterly EMI plan (2 yrs, 6% p.a.): ₹{emi_total:,.2f} per instalment")


# ═══════════════════════════════════════════════════════════════════════════════
#  LAB 6 – FILE-BASED ACADEMIC RECORD MANAGEMENT
#  Topics: file I/O, JSON, CSV, text files, with-open
# ═══════════════════════════════════════════════════════════════════════════════

RECORDS_DIR   = "campus_records"
STUDENTS_FILE = os.path.join(RECORDS_DIR, "students.json")
REPORT_FILE   = os.path.join(RECORDS_DIR, "academic_report.txt")
CSV_FILE      = os.path.join(RECORDS_DIR, "students.csv")


def _ensure_dir():
    os.makedirs(RECORDS_DIR, exist_ok=True)


def save_to_json():
    """Lab 6 – Save all student records to a JSON file."""
    _ensure_dir()
    # Convert sets (enrollments) → lists for JSON serialisation
    payload = {usn: dict(s) for usn, s in students.items()}
    with open(STUDENTS_FILE, "w") as f:
        json.dump(payload, f, indent=4)
    print(f"  ✔ Records saved to '{STUDENTS_FILE}'")


def load_from_json():
    """Lab 6 – Load student records from JSON file."""
    global students
    if not os.path.exists(STUDENTS_FILE):
        print("  [!] No saved file found.")
        return
    with open(STUDENTS_FILE, "r") as f:
        data = json.load(f)
    students.update(data)
    print(f"  ✔ Loaded {len(data)} records from '{STUDENTS_FILE}'")


def export_to_csv():
    """Lab 6 – Export student data to CSV."""
    _ensure_dir()
    if not students:
        print("  [!] No data to export.")
        return
    rows = []
    for usn, s in students.items():
        rows.append({
            "USN":      usn,
            "Name":     s["name"],
            "Dept":     s["dept"],
            "Semester": s["semester"],
            "Total":    s["total"],
            "Average":  s["average"],
            "Grade":    s["grade"],
            "Result":   s["result"],
            "Courses":  ";".join(s["courses"]),
            "FeesPaid": s["fees_paid"],
        })
    df = pd.DataFrame(rows)
    df.to_csv(CSV_FILE, index=False)
    print(f"  ✔ CSV exported to '{CSV_FILE}'")


def generate_text_report():
    """Lab 6 – Write a formatted academic report text file."""
    _ensure_dir()
    lines = []
    lines.append("=" * 65)
    lines.append("  DAYANANDA SAGAR COLLEGE OF ENGINEERING")
    lines.append("  Smart Campus Information System – Academic Report")
    lines.append(f"  Generated: {datetime.datetime.now().strftime('%d-%b-%Y  %H:%M:%S')}")
    lines.append("=" * 65)
    lines.append("")
    for usn, s in students.items():
        lines.append(f"  USN: {usn:<12}  Name: {s['name']:<20}  Dept: {s['dept']}")
        lines.append(f"  Semester: {s['semester']}  Average: {s['average']:.2f}  Grade: {s['grade']}  Result: {s['result']}")
        lines.append(f"  Courses : {', '.join(s['courses']) or 'None'}")
        lines.append(f"  Fees Paid: ₹{s['fees_paid']:,.2f}")
        lines.append("  " + "-" * 60)
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  ✔ Academic report written to '{REPORT_FILE}'")


def file_management_menu():
    """Lab 6 – File management sub-menu."""
    print("\n" + "─" * 50)
    print("  LAB 6 │ FILE-BASED ACADEMIC RECORD MANAGEMENT")
    print("─" * 50)
    print("  1. Save records to JSON")
    print("  2. Load records from JSON")
    print("  3. Export to CSV")
    print("  4. Generate Text Report")
    print("  5. Read & Display Report File")
    ch = input("  Choice: ").strip()
    if ch == "1":
        save_to_json()
    elif ch == "2":
        load_from_json()
    elif ch == "3":
        export_to_csv()
    elif ch == "4":
        generate_text_report()
    elif ch == "5":
        if not os.path.exists(REPORT_FILE):
            print("  [!] Report file not found. Generate it first.")
        else:
            with open(REPORT_FILE, "r", encoding="utf-8") as f:
                print(f.read())
    else:
        print("  Invalid choice.")


# ═══════════════════════════════════════════════════════════════════════════════
#  LAB 7 – DIRECTORY SCANNING WITH EXCEPTION HANDLING
#  Topics: os module, os.walk, try-except-finally, custom exceptions
# ═══════════════════════════════════════════════════════════════════════════════

class DirectoryNotFoundError(Exception):
    """Custom exception for missing directory."""
    pass


class InvalidExtensionError(Exception):
    """Custom exception for invalid file extension filter."""
    pass


def scan_directory(path, ext_filter=None):
    """
    Recursively scan a directory and return matching files.
    Raises DirectoryNotFoundError if path doesn't exist.
    Raises InvalidExtensionError if ext_filter is malformed.
    """
    if not os.path.exists(path):
        raise DirectoryNotFoundError(f"Directory '{path}' does not exist.")
    if not os.path.isdir(path):
        raise DirectoryNotFoundError(f"'{path}' is not a directory.")

    if ext_filter:
        ext_filter = ext_filter.strip().lower()
        if not ext_filter.startswith("."):
            raise InvalidExtensionError(f"Extension must start with '.' (e.g. '.py'), got: {ext_filter}")

    found_files  = []
    total_size   = 0
    dir_count    = 0
    project_dirs = []

    try:
        for root, dirs, files in os.walk(path):
            dir_count += len(dirs)
            for fname in files:
                fpath = os.path.join(root, fname)
                try:
                    fsize = os.path.getsize(fpath)
                except OSError:
                    fsize = 0
                if ext_filter is None or fname.lower().endswith(ext_filter):
                    found_files.append({
                        "name":    fname,
                        "path":    fpath,
                        "size_kb": round(fsize / 1024, 2),
                    })
                    total_size += fsize
                if fname.endswith((".py", ".ipynb")):
                    project_dirs.append(root)

    except PermissionError as e:
        print(f"  [!] Permission denied: {e}")
    finally:
        print(f"  [Info] Scan complete. Directories visited: {dir_count + 1}")

    return found_files, round(total_size / 1024, 2), list(set(project_dirs))


def directory_scan_menu():
    """Lab 7 – Interactive directory scanner."""
    print("\n" + "─" * 50)
    print("  LAB 7 │ DIRECTORY SCANNING WITH EXCEPTION HANDLING")
    print("─" * 50)
    path       = input("  Enter directory path to scan (default: '.'): ").strip() or "."
    ext_filter = input("  Filter by extension (e.g. .py, .txt – or press Enter for all): ").strip() or None

    try:
        files, total_kb, proj_dirs = scan_directory(path, ext_filter)
    except DirectoryNotFoundError as e:
        print(f"  [Error] {e}")
        return
    except InvalidExtensionError as e:
        print(f"  [Error] {e}")
        return
    except Exception as e:
        print(f"  [Unexpected Error] {e}")
        return

    if not files:
        print("  No matching files found.")
        return

    label = f"(filter: *{ext_filter})" if ext_filter else "(all files)"
    print(f"\n  Scan results for '{path}' {label}")
    print(f"  {'─'*70}")
    print(f"  {'File Name':<35} {'Size (KB)':>10}  Path")
    print(f"  {'─'*35} {'─'*10}  {'─'*24}")
    for f in files[:50]:              # cap display at 50 lines
        short_path = f["path"][-40:] if len(f["path"]) > 40 else f["path"]
        print(f"  {f['name']:<35} {f['size_kb']:>10.2f}  ...{short_path}")
    if len(files) > 50:
        print(f"  ... and {len(files) - 50} more files")
    print(f"\n  Total matching files  : {len(files)}")
    print(f"  Total size            : {total_kb:.2f} KB")
    if proj_dirs:
        print(f"  Python project dirs   : {len(proj_dirs)}")
        for d in proj_dirs[:5]:
            print(f"    → {d}")


# ═══════════════════════════════════════════════════════════════════════════════
#  LAB 8 – PERFORMANCE ANALYTICS (NumPy, Pandas, Matplotlib)
#  Topics: arrays, descriptive stats, DataFrames, bar/pie/line charts
# ═══════════════════════════════════════════════════════════════════════════════

CHARTS_DIR = "campus_charts"


def _ensure_charts_dir():
    os.makedirs(CHARTS_DIR, exist_ok=True)


def performance_analytics():
    """Lab 8 – Generate statistical analysis and charts for all students."""
    print("\n" + "─" * 50)
    print("  LAB 8 │ STUDENT PERFORMANCE ANALYTICS")
    print("─" * 50)

    if len(students) < 2:
        print("  [!] Need at least 2 students for analytics. Add more and retry.")
        return

    _ensure_charts_dir()

    # ── Build Pandas DataFrame ────────────────────────────────────────
    records = []
    for usn, s in students.items():
        records.append({
            "USN":      usn,
            "Name":     s["name"],
            "Dept":     s["dept"],
            "Average":  s["average"],
            "Grade":    s["grade"],
            "Result":   s["result"],
            "FeesPaid": s["fees_paid"],
        })
    df = pd.DataFrame(records)

    # ── NumPy Statistics ──────────────────────────────────────────────
    avg_arr  = np.array(df["Average"].tolist())
    print(f"\n  NumPy Descriptive Statistics")
    print(f"  {'─'*45}")
    print(f"  Count  : {len(avg_arr)}")
    print(f"  Mean   : {np.mean(avg_arr):.2f}")
    print(f"  Median : {np.median(avg_arr):.2f}")
    print(f"  Std Dev: {np.std(avg_arr):.2f}")
    print(f"  Min    : {np.min(avg_arr):.2f}  ({df.loc[df['Average'].idxmin(), 'Name']})")
    print(f"  Max    : {np.max(avg_arr):.2f}  ({df.loc[df['Average'].idxmax(), 'Name']})")
    print(f"  Range  : {np.ptp(avg_arr):.2f}")
    percentiles = np.percentile(avg_arr, [25, 50, 75])
    print(f"  Q1/Q2/Q3: {percentiles[0]:.2f} / {percentiles[1]:.2f} / {percentiles[2]:.2f}")

    # ── Pandas Group Analysis ─────────────────────────────────────────
    print(f"\n  Pandas – Department-wise Summary")
    print(f"  {'─'*45}")
    dept_stats = df.groupby("Dept")["Average"].agg(["count", "mean", "min", "max"]).round(2)
    dept_stats.columns = ["Count", "Mean", "Min", "Max"]
    print(dept_stats.to_string())

    print(f"\n  Pandas – Grade Distribution")
    print(f"  {'─'*45}")
    grade_counts = df["Grade"].value_counts().sort_index()
    print(grade_counts.to_string())

    pass_rate = (df["Result"] == "Pass").mean() * 100
    print(f"\n  Overall Pass Rate : {pass_rate:.1f}%")

    # ── Chart 1 : Bar – Average Marks per Student ─────────────────────
    fig, ax = plt.subplots(figsize=(max(8, len(df) * 1.2), 5))
    colors  = ["#2ecc71" if r == "Pass" else "#e74c3c" for r in df["Result"]]
    bars    = ax.bar(df["Name"], df["Average"], color=colors, edgecolor="white", linewidth=0.8)
    ax.axhline(np.mean(avg_arr), color="#3498db", linestyle="--", linewidth=1.5, label=f"Mean ({np.mean(avg_arr):.1f})")
    for bar, val in zip(bars, df["Average"]):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5, f"{val:.1f}",
                ha="center", va="bottom", fontsize=8)
    ax.set_title("Student Average Marks", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Student")
    ax.set_ylabel("Average Marks")
    ax.set_ylim(0, 110)
    ax.tick_params(axis="x", rotation=30)
    pass_patch = mpatches.Patch(color="#2ecc71", label="Pass")
    fail_patch = mpatches.Patch(color="#e74c3c", label="Fail")
    ax.legend(handles=[pass_patch, fail_patch, ax.get_lines()[0]])
    plt.tight_layout()
    chart1 = os.path.join(CHARTS_DIR, "bar_avg_marks.png")
    plt.savefig(chart1, dpi=150)
    plt.close()
    print(f"\n  ✔ Chart 1 saved: {chart1}")

    # ── Chart 2 : Pie – Grade Distribution ───────────────────────────
    grade_counts = df["Grade"].value_counts()
    grade_colors = {"O": "#2ecc71", "A+": "#27ae60", "A": "#3498db",
                    "B+": "#9b59b6", "B": "#f39c12", "C": "#e67e22", "F": "#e74c3c"}
    pie_colors   = [grade_colors.get(g, "#95a5a6") for g in grade_counts.index]
    fig, ax      = plt.subplots(figsize=(7, 7))
    wedges, texts, autotexts = ax.pie(
        grade_counts.values, labels=grade_counts.index,
        autopct="%1.1f%%", startangle=140,
        colors=pie_colors, pctdistance=0.80,
        wedgeprops={"edgecolor": "white", "linewidth": 1.5}
    )
    for t in autotexts:
        t.set_fontsize(10)
    ax.set_title("Grade Distribution", fontsize=14, fontweight="bold", pad=16)
    plt.tight_layout()
    chart2 = os.path.join(CHARTS_DIR, "pie_grade_dist.png")
    plt.savefig(chart2, dpi=150)
    plt.close()
    print(f"  ✔ Chart 2 saved: {chart2}")

    # ── Chart 3 : Grouped Bar – Dept-wise Performance ─────────────────
    if len(df["Dept"].unique()) >= 2:
        dept_mean = df.groupby("Dept")["Average"].mean().sort_values(ascending=False)
        fig, ax   = plt.subplots(figsize=(max(7, len(dept_mean) * 1.5), 5))
        ax.bar(dept_mean.index, dept_mean.values,
               color="#3498db", edgecolor="white", linewidth=0.8)
        ax.axhline(np.mean(avg_arr), color="#e74c3c", linestyle="--",
                   linewidth=1.5, label=f"Overall Mean ({np.mean(avg_arr):.1f})")
        for i, (dept, val) in enumerate(dept_mean.items()):
            ax.text(i, val + 0.5, f"{val:.1f}", ha="center", va="bottom", fontsize=9)
        ax.set_title("Department-wise Average Performance", fontsize=13, fontweight="bold")
        ax.set_xlabel("Department")
        ax.set_ylabel("Average Marks")
        ax.set_ylim(0, 110)
        ax.legend()
        plt.tight_layout()
        chart3 = os.path.join(CHARTS_DIR, "bar_dept_performance.png")
        plt.savefig(chart3, dpi=150)
        plt.close()
        print(f"  ✔ Chart 3 saved: {chart3}")

    # ── Chart 4 : Histogram – Marks Distribution ─────────────────────
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(avg_arr, bins=10, range=(0, 100), color="#9b59b6",
            edgecolor="white", linewidth=0.8)
    ax.axvline(np.mean(avg_arr), color="#e74c3c", linestyle="--",
               linewidth=1.5, label=f"Mean = {np.mean(avg_arr):.1f}")
    ax.axvline(np.median(avg_arr), color="#27ae60", linestyle="-.",
               linewidth=1.5, label=f"Median = {np.median(avg_arr):.1f}")
    ax.set_title("Distribution of Average Marks", fontsize=13, fontweight="bold")
    ax.set_xlabel("Average Marks")
    ax.set_ylabel("Number of Students")
    ax.legend()
    plt.tight_layout()
    chart4 = os.path.join(CHARTS_DIR, "hist_marks_dist.png")
    plt.savefig(chart4, dpi=150)
    plt.close()
    print(f"  ✔ Chart 4 saved: {chart4}")

    print(f"\n  All charts saved in '{CHARTS_DIR}/' directory.")


# ═══════════════════════════════════════════════════════════════════════════════
#  SAMPLE DATA LOADER  (for quick demo)
# ═══════════════════════════════════════════════════════════════════════════════

def load_sample_data():
    """Populate the system with sample students for demo / testing."""
    sample = [
        ("1DS24CS001", "Aanya Sharma",    "CSE", "2",
         [("Python",75), ("DBMS",88), ("Networks",70), ("Maths",92), ("Physics",60)]),
        ("1DS24CS002", "Bharat Kumar",    "CSE", "2",
         [("Python",92), ("DBMS",95), ("Networks",88), ("Maths",96), ("Physics",90)]),
        ("1DS24CS003", "Chitra Reddy",    "CSE", "2",
         [("Python",55), ("DBMS",48), ("Networks",52), ("Maths",50), ("Physics",45)]),
        ("1DS24CS004", "Devraj Nair",     "CSE", "2",
         [("Python",82), ("DBMS",78), ("Networks",80), ("Maths",85), ("Physics",79)]),
        ("1DS24EC001", "Esha Patel",      "ECE", "2",
         [("Circuits",70), ("Electronics",75), ("Maths",68), ("Physics",80), ("Python",65)]),
        ("1DS24EC002", "Farhan Qureshi",  "ECE", "2",
         [("Circuits",88), ("Electronics",90), ("Maths",85), ("Physics",92), ("Python",78)]),
        ("1DS24ME001", "Gauri Iyer",      "ME",  "2",
         [("Mechanics",62), ("Thermodynamics",58), ("Maths",70), ("Physics",65), ("Python",55)]),
        ("1DS24ME002", "Harish Menon",    "ME",  "2",
         [("Mechanics",38), ("Thermodynamics",35), ("Maths",42), ("Physics",40), ("Python",30)]),
    ]
    default_courses = ["CS101", "MA101", "PH101"]
    for usn, name, dept, sem, subs in sample:
        if usn in students:
            continue
        marks_list = [{"subject": s, "marks": m} for s, m in subs]
        total  = sum(m for _, m in subs)
        avg    = total / len(subs)
        grade, result = assign_grade(avg)
        students[usn] = {
            "name":      name,
            "dept":      dept,
            "semester":  sem,
            "subjects":  marks_list,
            "total":     round(total, 2),
            "average":   round(avg, 2),
            "grade":     grade,
            "result":    result,
            "courses":   list(default_courses),
            "fees_paid": 0.0,
            "reg_date":  str(datetime.date.today()),
        }
        for code in default_courses:
            enrollments[code].add(usn)
    print(f"  ✔ {len(sample)} sample students loaded.")


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════

BANNER = r"""
╔══════════════════════════════════════════════════════════════════╗
║       DAYANANDA SAGAR COLLEGE OF ENGINEERING                    ║
║       SMART CAMPUS INFORMATION SYSTEM                           ║
║       Dept. of CSE  │  Python Lab Integration  │  2025-26       ║
╚══════════════════════════════════════════════════════════════════╝
"""

MENU = """
  ┌─────────────────────────────────────────────────────┐
  │   L A B   M O D U L E S                            │
  ├──────┬──────────────────────────────────────────────┤
  │  1   │  LAB 1 – Register Student / View Details     │
  │  2   │  LAB 2 – Course Enrollment & Drop            │
  │  3   │  LAB 3 – View / Update / Delete Records      │
  │  4   │  LAB 4 – Search & Sort Students              │
  │  5   │  LAB 5 – Fee Calculation                     │
  │  6   │  LAB 6 – File-based Record Management        │
  │  7   │  LAB 7 – Directory Scanner                   │
  │  8   │  LAB 8 – Performance Analytics & Charts      │
  ├──────┼──────────────────────────────────────────────┤
  │  D   │  Load Demo/Sample Data                       │
  │  Q   │  Quit                                        │
  └──────┴──────────────────────────────────────────────┘
"""

LAB1_MENU  = "\n  1. Register New Student\n  2. View Student Details\n  → "
LAB2_MENU  = "\n  1. List Available Courses\n  2. Enroll Student\n  3. Drop Course\n  → "
LAB3_MENU  = "\n  1. View All Students\n  2. Update Student\n  3. Delete Student\n  → "


def main():
    print(BANNER)
    while True:
        print(MENU)
        choice = input("  Enter choice: ").strip().upper()

        if choice == "1":
            sub = input(LAB1_MENU).strip()
            if sub == "1":
                register_student()
            elif sub == "2":
                view_student()

        elif choice == "2":
            sub = input(LAB2_MENU).strip()
            if sub == "1":
                list_courses()
            elif sub == "2":
                enroll_student()
            elif sub == "3":
                drop_course()

        elif choice == "3":
            sub = input(LAB3_MENU).strip()
            if sub == "1":
                display_all_students()
            elif sub == "2":
                update_student()
            elif sub == "3":
                delete_student()

        elif choice == "4":
            search_and_sort_menu()

        elif choice == "5":
            calculate_fees()

        elif choice == "6":
            file_management_menu()

        elif choice == "7":
            directory_scan_menu()

        elif choice == "8":
            performance_analytics()

        elif choice == "D":
            load_sample_data()

        elif choice == "Q":
            save_to_json()
            print("\n  Thank you for using Smart Campus Information System!")
            print("  All records saved. Goodbye!\n")
            break

        else:
            print("  [!] Invalid choice. Please try again.")


# ─────────────────────────────────────────────
if __name__ == "__main__":
    main()