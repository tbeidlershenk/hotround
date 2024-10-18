CREATE TABLE Courses (
    course_id INT PRIMARY KEY AUTO_INCREMENT,
    course_name VARCHAR(100) NOT NULL
    readable_course_name VARCHAR(100) NOT NULL,
);

CREATE TABLE Events (
    event_id INT PRIMARY KEY NOT NULL,
    course_id VARCHAR(50),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id) ON DELETE CASCADE
);

CREATE TABLE Tournament_Rounds (
    round_id INT PRIMARY KEY AUTO_INCREMENT,
    event_id INT NOT NULL,
    layout_id VARCHAR(50),  
    par_rating DECIMAL(5, 2) NOT NULL,
    stroke_value DECIMAL(5, 2) NOT NULL,
    num_players INT NOT NULL,
    round_date DATE NOT NULL,
    FOREIGN KEY (layout_id) REFERENCES Layouts(layout_id) ON DELETE CASCADE
);