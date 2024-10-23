INSERT INTO Courses (course_name, readable_course_name)
VALUES 
('Aperture_Park', 'Aperture Park');
INSERT INTO Events (event_id, date, course_id)
VALUES 
(78686, '2024-09-21', (SELECT course_id FROM Courses WHERE readable_course_name = 'Aperture Park')),
(79178, '2024-08-25', (SELECT course_id FROM Courses WHERE readable_course_name = 'Aperture Park')),
(77161, '2024-05-20', (SELECT course_id FROM Courses WHERE readable_course_name = 'Aperture Park')),
(68714, '2023-08-12', (SELECT course_id FROM Courses WHERE readable_course_name = 'Aperture Park')),
(66784, '2023-05-14', (SELECT course_id FROM Courses WHERE readable_course_name = 'Aperture Park')),
(61939, '2022-08-27', (SELECT course_id FROM Courses WHERE readable_course_name = 'Aperture Park')),
(57344, '2022-05-08', (SELECT course_id FROM Courses WHERE readable_course_name = 'Aperture Park')),
(53371, '2021-08-28', (SELECT course_id FROM Courses WHERE readable_course_name = 'Aperture Park'));
INSERT INTO Rounds (layout_name, round_number, num_players, layout_par, high_rating, low_rating, par_rating, stroke_value, event_id)
VALUES 
('U of L - BLUE', 1, 7, 56, 1013, 913, 913, 11.11, 78686),
('U of L - BLUE', 2, 7, 56, 1002, 935, 912, 11.17, 78686),
('U of L - BLUE', 1, 4, 56, 913, 824, 913, 11.13, 78686),
('U of L - BLUE', 2, 4, 56, 902, 857, 913, 11.25, 78686);