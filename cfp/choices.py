SESSION_TYPE_CHOICES = (
    ("talk", "A talk (25 minutes)"),
    ("workshop", "A workshop (3 hours)"),
    ("poster", "A poster"),
    (
        "kids-workshop",
        "An Education Summit workshop for young coders (Saturday, 50 mins)",
    ),
    (
        "teachers-workshop",
        "An Education Summit workshop for educators (Sunday, 50 mins)",
    ),
    ("teachers-talk", "An Education Summit talk for educators (Sunday, 25 mins)"),
    ("other", "Something else"),
)


STATE_TYPE_CHOICES = (
    ("confirm", "Confirmed"),
    ("cancel", "Cancelled"),
    ("accept", "Accepted"),
    ("reject", "Plan to Reject"),
    ("withdrawn", "Withdrawn"),
    ("placeholder", "Schedule Placeholder"),
)
