CREATE TABLE Courses (
    course_id INT PRIMARY KEY AUTO_INCREMENT,
    course_name VARCHAR(100) NOT NULL,
    readable_course_name VARCHAR(100) NOT NULL,
);

CREATE TABLE Events (
    event_id INT PRIMARY KEY NOT NULL,
    date DATE NOT NULL,
    FOREIGN KEY (course_id) REFERENCES Courses(course_id) ON DELETE CASCADE
);

CREATE TABLE Tournament_Rounds (
    round_id INT PRIMARY KEY AUTO_INCREMENT,
    layout_name VARCHAR(200),  
    round_number INT NOT NULL,
    num_players INT NOT NULL,
    layout_par INT NOT NULL,
    high_rating DECIMAL(4, 2) NOT NULL,
    low_rating DECIMAL(4, 2) NOT NULL,
    par_rating DECIMAL(5, 2) NOT NULL,
    stroke_value DECIMAL(5, 2) NOT NULL,
    FOREIGN KEY (event_id) REFERENCES Events(event_id) ON DELETE CASCADE
);