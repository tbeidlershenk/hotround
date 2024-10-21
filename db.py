import json


with open('test/test_course_data.json', 'r') as file:
    course_data = json.load(file)

    insert_courses = """
    INSERT INTO Courses (course_name, readable_course_name)
    VALUES (%s, %s);
    """

    insert_events = """
    INSERT INTO Events (event_id, course_id)
    VALUES (%s, (SELECT course_id FROM Courses WHERE readable_course_name = %s));
    """

    insert_rounds = """
    INSERT INTO Tournament_Rounds (event_id, layout_id, par_rating, stroke_value, num_players, round_date)
    VALUES (%s, %s, %s, %s, %s, %s);
    """

    course_inserts = []
    event_inserts = []
    round_inserts = []

    for course, details in course_data.items():
        course_inserts.append((course, details["name"]))
        for event in details["events"]:
            event_inserts.append((event["event_id"], details["date"]))
        for round_info in details["rounds"]:
            round_inserts.append((
                event["event_id"],
                round_info["course_layout"],
                round_info["par_rating"],
                round_info["stroke_value"],
                round_info["players"],
                event["date"]
            ))

    print(insert_courses)
    print(course_inserts)
    print(insert_events)
    print(event_inserts)
    print(insert_rounds)
    print(round_inserts)
