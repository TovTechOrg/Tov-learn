students_grades = [{"name": "Alice", "grade": 85}, {"name": "Bob", "grade": 95}, {"name": "Charlie", "grade": 78}, {"name": "David", "grade": 68}]

for s in students_grades:
    if s["grade"] >= 90:
        rank = "מצוין"
    elif s["grade"] >= 80:
        rank = "טוב מאוד"
    elif s["grade"] >= 70:
        rank = "טוב"
    else:
        rank = "נדרש שיפור"
    print(f"{s['name']}: {s['grade']} ⸺ {rank}")
