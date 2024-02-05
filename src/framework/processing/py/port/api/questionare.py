# Questionare structure, it is always mandatory title and description in EN/NL
# A dictionary where each key is a question identifier and each value is a dict
#        containing 'title', 'description', and 'items'. 'items' is a list of dicts, each
#        representing a possible answer with an 'id' and 'value'.

questions = {
    "q1": {
        "title": {
            "en": "1. How often do you seek social interactions in your daily life?",
            "nl": "1. Hoe vaak zoekt u sociale interacties in uw dagelijks leven?",
        },
        "description": {
            "en": "Choose the most suitable situation",
            "nl": "Kies de meest geschikte situatie",
        },
        "items": [
            {
                "id": "Q1_1",
                "value": "Every single day I am out for a drink with friends",
            },
            {
                "id": "Q1_2",
                "value": "A few times a week, I attend a meetup where I live",
            },
            {"id": "Q1_3", "value": "So and So"},
            {
                "id": "Q1_4",
                "value": "Prefer not to have social interactions, but sometimes it is nice to meet people",
            },
            {
                "id": "Q1_5",
                "value": "I refuse to leave my basement, next question please !!!",
            },
        ],
    },  # end of page 1 questions
    "q2": {
        "title": {
            "en": "2. Do you feel energized and rejuvenated by spending time with people?",
            "nl": "2. Voelt u zich energiek en verjongd door tijd door te brengen met anderen?",
        },
        "description": {
            "en": "Choose the most suitable situation",
            "nl": "Kies de meest geschikte situatie",
        },
        "items": [
            {"id": "Q2_1", "value": "YES!!!! This is so me"},
            {
                "id": "Q2_2",
                "value": "Ya, I fell more energetic after talking with people",
            },
            {
                "id": "Q2_3",
                "value": "More or less, I think it depends who are the persons",
            },
            {"id": "Q2_4", "value": "No, dealing with people drains me"},
            {
                "id": "Q2_5",
                "value": "NO !!!! I am now flat in the sofa due to social interaction exaustion!!!",
            },
        ],
    },  # end of page 2 questions
    "q3": {
        "title": {
            "en": "3. How comfortable do you feel being the center of attention in a group setting?",
            "nl": "3. Voelt u zich energiek en verjongd door tijd door te brengen met anderen?",
        },
        "description": {
            "en": "Choose the most suitable situation",
            "nl": "Kies de meest geschikte situatie",
        },
        "items": [
            {
                "id": "Q3_1",
                "value": "Totally confortable, I am the center of group's attention, there is no group without me!!!",
            },
            {"id": "Q3_2", "value": "I like to be the center of attention"},
            {"id": "Q3_3", "value": "Sometimes yes, sometimes no"},
            {"id": "Q3_4", "value": "I find it unconfortable"},
            {
                "id": "Q3_5",
                "value": "If someone looks at me,  I will run to the emergency exit",
            },
        ],
    },  # end of page 3 questions
}  # end of question dic
