# Module with generic functions and file processing code

def find_question_by_value(questions, target_value, language='en'):
    return next(
        (question['title'][language] for question in questions.values() if any(item['value'] == target_value for item in question['items'])),
        None  # Default value if no item matches
    )

def find_id_by_value(questions, target_value):
    return next(
            (item['id'] for question in questions.values() for item in question['items'] if item['value'] == target_value),
            None  # Default value if no item matches    
    )



