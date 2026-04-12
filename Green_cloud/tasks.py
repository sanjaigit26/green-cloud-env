from grader import easy, medium, hard

TASKS = {
    "easy": {
        "description": "Assign all jobs to any region",
        "grader": easy,
    },
    "medium": {
        "description": "Assign all jobs before their deadlines",
        "grader": medium,
    },
    "hard": {
        "description": "Minimize carbon emissions while meeting deadlines",
        "grader": hard,
    }
}
