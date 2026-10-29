
import re
import sqlite3

# Исходные данные
students = [
    {'name': 'Aida', 'group': 'IS-24-01', 'score': 82, 'attendance': 91, 'email': 'aida@atu.edu.kz'},
    {'name': 'Miras', 'group': 'IS-24-01', 'score': 69, 'attendance': 88, 'email': 'miras@atu.edu.kz'},
    {'name': 'Dana', 'group': 'IS-24-02', 'score': 91, 'attendance': 96, 'email': 'dana@atu.edu.kz'},
    {'name': 'Timur', 'group': 'IS-24-02', 'score': 74, 'attendance': 62, 'email': 'timur_at_atu.kz'},
    {'name': 'Aliya', 'group': 'IS-24-03', 'score': 87, 'attendance': 79, 'email': 'aliya@atu.edu.kz'},
    {'name': 'Arman', 'group': 'IS-24-03', 'score': 55, 'attendance': 72, 'email': 'arman@atu.edu.kz'}
]

# Задание 1. Императивный и декларативный подход
print("=== ЗАДАНИЕ 1 ===")

passed_imperative = []
for student in students:
    if student['score'] >= 75:
        passed_imperative.append(student['name'])

passed_declarative = [
    student['name'] for student in students
    if student['score'] >= 75
]

print("Императивный вариант:", passed_imperative)
print("Декларативный вариант:", passed_declarative)
print("Результаты совпадают:", passed_imperative == passed_declarative)

# Задание 2. Функции any() и all()
print("\n=== ЗАДАНИЕ 2 ===")

has_excellent = any(s['score'] >= 90 for s in students)
all_attended = all(s['attendance'] >= 60 for s in students)
average_score = (
    sum(s['score'] for s in students) / len(students)
    if students else 0
)

print("Есть оценка >= 90:", has_excellent)
print("У всех посещаемость >= 60%:", all_attended)
print("Средний балл:", round(average_score, 1))

changed_students = [s.copy() for s in students]
changed_students[0]['attendance'] = 59
print("После изменения посещаемости Aida:",
      all(s['attendance'] >= 60 for s in changed_students))

# Задание 3. Регулярные выражения
print("\n=== ЗАДАНИЕ 3 ===")

group_pattern = r'^[A-Z]{2}-\d{2}-\d{2}$'
email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

invalid_groups = [
    s['group'] for s in students
    if not re.fullmatch(group_pattern, s['group'])
]
invalid_emails = [
    s['email'] for s in students
    if not re.fullmatch(email_pattern, s['email'])
]

print("Некорректные группы:", invalid_groups)
print("Некорректные email:", invalid_emails)

for student in students:
    if student['email'] == 'timur_at_atu.kz':
        student['email'] = 'timur@atu.edu.kz'

invalid_emails_after_fix = [
    s['email'] for s in students
    if not re.fullmatch(email_pattern, s['email'])
]
print("Email после исправления:", invalid_emails_after_fix)

# Задание 4. Создание базы SQLite
print("\n=== ЗАДАНИЕ 4 ===")

connection = sqlite3.connect(':memory:')
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE students (
    name TEXT,
    group_name TEXT,
    score INTEGER,
    attendance INTEGER,
    email TEXT
)
""")

cursor.executemany("""
INSERT INTO students
(name, group_name, score, attendance, email)
VALUES (?, ?, ?, ?, ?)
""", [
    (s['name'], s['group'], s['score'], s['attendance'], s['email'])
    for s in students
])

connection.commit()
print("Таблица students создана.")
print("Количество записей:", len(students))

# Задание 5. SQL-фильтрация и группировка
print("\n=== ЗАДАНИЕ 5 ===")

cursor.execute("""
SELECT name, score, attendance
FROM students
WHERE score >= 75 AND attendance >= 70
ORDER BY score DESC
""")

print("Студенты с оценкой >= 75 и посещаемостью >= 70:")
for row in cursor.fetchall():
    print(row)

cursor.execute("""
SELECT group_name,
       COUNT(*) AS student_count,
       ROUND(AVG(score), 1) AS average_score
FROM students
GROUP BY group_name
HAVING AVG(score) >= 70
ORDER BY average_score DESC
""")

print("\nСтатистика по группам:")
for row in cursor.fetchall():
    print(row)

# Задание 6. SQL и проверка email
print("\n=== ЗАДАНИЕ 6 ===")

cursor.execute("""
SELECT name, group_name, score, email
FROM students
WHERE score >= 70 AND attendance >= 70
ORDER BY score DESC
""")

for place, row in enumerate(cursor.fetchall(), start=1):
    name, group_name, score, email = row
    valid = bool(re.fullmatch(email_pattern, email))
    status = "email корректен" if valid else "email некорректен"
    print(f"{place}. {name} | {group_name} | {score} | {email} | {status}")

# Индивидуальный вариант 9
print("\n=== ИНДИВИДУАЛЬНЫЙ ВАРИАНТ 9 ===")

cursor.execute("""
SELECT name, group_name, score, email
FROM students
WHERE name LIKE 'A%' AND score >= 70
ORDER BY score DESC
""")

variant_result = cursor.fetchall()

if variant_result:
    for name, group_name, score, email in variant_result:
        starts_with_a = bool(re.fullmatch(r'^A.*', name))
        print(
            f"{name} | {group_name} | {score} | "
            f"имя начинается с A: {starts_with_a}"
        )
else:
    print("Подходящих студентов нет.")

connection.close()
print("\n=== РАБОТА ЗАВЕРШЕНА ===")
