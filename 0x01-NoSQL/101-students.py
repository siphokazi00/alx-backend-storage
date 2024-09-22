#!/usr/bin/env python3
# 101-students.py
def top_students(mongo_collection):
    students = mongo_collection.find()
    result = []

    for student in students:
        scores = [topic['score'] for topic in student.get('topics', [])]
        average_score = sum(scores) / len(scores) if scores else 0
        student_info = {
            '_id': student['_id'],
            'name': student['name'],
            'averageScore': average_score
        }
        result.append(student_info)

    return sorted(result, key=lambda x: x['averageScore'], reverse=True)
