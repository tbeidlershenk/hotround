-- Create Courses table with course_id as a string
CREATE TABLE Courses (
    course_id VARCHAR(50) PRIMARY KEY,  -- course_id is now a string
    course_name VARCHAR(100) NOT NULL
);

-- Create Layouts table with layout_id and course_id as strings
CREATE TABLE Layouts (
    layout_id VARCHAR(50) PRIMARY KEY,  -- layout_id is now a string
    course_id VARCHAR(50),              -- course_id remains a string
    layout_name VARCHAR(100) NOT NULL,
    par INT NOT NULL,                   -- The par for the layout
    FOREIGN KEY (course_id) REFERENCES Courses(course_id) ON DELETE CASCADE
);

-- Create Tournament Rounds table with layout_id as a string
CREATE TABLE Tournament_Rounds (
    round_id INT PRIMARY KEY AUTO_INCREMENT,
    layout_id VARCHAR(50),              -- layout_id is now a string
    average_rating DECIMAL(5, 2) NOT NULL,  -- Average rating for even par (e.g., 72.5)
    average_stroke DECIMAL(5, 2) NOT NULL,  -- Average stroke value (e.g., 70.3)
    num_players INT NOT NULL,               -- Number of players that played that round
    round_date DATE NOT NULL,               -- Date of the round played
    FOREIGN KEY (layout_id) REFERENCES Layouts(layout_id) ON DELETE CASCADE
);