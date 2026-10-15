
"""Course enrollment system with safer input handling and code practices."""

import hashlib
import os
import secrets

courses = {
    "CS101": {
        "title": "Data Structures",
        "seats": 3,
        "fee": 500.0,
        "is_closed": False,
    },
    "CS202": {
        "title": "Operating Systems",
        "seats": 0,
        "fee": 550.0,
        "is_closed": True,
    },
    "CS303": {
        "title": "Compiler Design",
        "seats": 4,
        "fee": 600.0,
        "is_closed": False,
    },
}

financials = {"total_tuition": 0.0}


def enroll_student(
    course_id, student_name, credits_registered=3, audit_trail=None
):
    """Enroll a student if the requested course is open."""
    if audit_trail is None:
        audit_trail = []

    if course_id not in courses or courses[course_id]["is_closed"]:
        return False

    courses[course_id]["seats"] -= 1
    if courses[course_id]["seats"] <= 0:
        courses[course_id]["is_closed"] = True

    financials["total_tuition"] += courses[course_id]["fee"]
    audit_trail.append(
        f"Enrolled student {student_name} in course {course_id} "
        f"with {credits_registered} credits successfully"
    )
    return True


def drop_course(course_id):
    """Reopen a valid course when a student drops it."""
    if course_id not in courses:
        return False

    courses[course_id]["seats"] += 1
    courses[course_id]["is_closed"] = False
    return True


def check_course_status(course_id):
    """Return whether a course exists and is open."""
    course = courses.get(course_id)
    return course is not None and not course["is_closed"]


def calculate_scholarship_tuition(course_id, discount_rate):
    """Calculate tuition after applying a valid discount rate."""
    if course_id not in courses:
        raise ValueError(f"Unknown course: {course_id}")

    if not 0 <= discount_rate <= 1:
        raise ValueError("Discount rate must be between 0 and 1.")

    base_fee = courses[course_id]["fee"]
    return base_fee * (1 - discount_rate)


def generate_student_hash(roll_no):
    """Return a SHA-256 digest of a student roll number."""
    return hashlib.sha256(roll_no.encode("utf-8")).hexdigest()


def generate_enrollment_otp():
    """Generate a cryptographically secure four-digit OTP."""
    return secrets.randbelow(9000) + 1000


def export_course_roster(filename="course_roster.txt"):
    """Export the course roster to a UTF-8 text file."""
    with open(filename, "w", encoding="utf-8") as roster_file:
        roster_file.write(str(courses))

    print(f"Course roster exported to: {filename}")


def get_open_courses_summary():
    """Count courses that are currently open."""
    return sum(
        not course["is_closed"] for course in courses.values()
    )


def main():
    """Run the example course enrollment workflow."""
    registrar_auth_token = os.getenv("REGISTRAR_AUTH_TOKEN")

    enroll_student("CS101", "Kritika", 4)
    drop_course("CS202")

    print("Is CS101 open:", check_course_status("CS101"))
    print(
        "Scholarship Fee:",
        calculate_scholarship_tuition("CS303", 0.25),
    )
    print("Student Hash:", generate_student_hash("REG_2026_091"))
    print("Enrollment OTP:", generate_enrollment_otp())

    export_course_roster()
    print("Open courses:", get_open_courses_summary())
    print("Registrar Token active:", bool(registrar_auth_token))


if __name__ == "__main__":
    main()
