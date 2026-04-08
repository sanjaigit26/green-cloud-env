from grader import grade_easy, grade_medium, grade_hard

TASKS = {
    "easy": {
        "description": "Assign all jobs to any region",
        "grader": grade_easy,
    },
    "medium": {
        "description": "Assign all jobs before their deadlines",
        "grader": grade_medium,
    },
    "hard": {
        "description": "Minimize carbon emissions while meeting deadlines",
        "grader": grade_hard,
    }
}
