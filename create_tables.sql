CREATE TABLE Courses (
    course_id INT PRIMARY KEY AUTO_INCREMENT,
    course_name VARCHAR(100) NOT NULL,
    readable_course_name VARCHAR(100) NOT NULL
);

CREATE TABLE Events (
    event_id INT PRIMARY KEY NOT NULL,
    date DATE NOT NULL,
    course_id INT NOT NULL,
    FOREIGN KEY (course_id) REFERENCES Courses(course_id) ON DELETE CASCADE
);

CREATE TABLE Rounds (
    round_id INT PRIMARY KEY AUTO_INCREMENT,
    layout_name VARCHAR(200),  
    round_number INT NOT NULL,
    num_players INT NOT NULL,
    layout_par INT NOT NULL,
    high_rating INT NOT NULL,
    low_rating INT NOT NULL,
    par_rating INT NOT NULL,
    stroke_value DECIMAL(5, 2) NOT NULL,
    event_id INT NOT NULL,
    FOREIGN KEY (event_id) REFERENCES Events(event_id) ON DELETE CASCADE
);