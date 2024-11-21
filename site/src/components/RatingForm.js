import React, { useState } from "react";

const RatingForm = ({ onSubmit }) => {
    const [courseName, setCourseName] = useState("");
    const [layoutName, setLayoutName] = useState("");
    const [score, setScore] = useState("");

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!courseName || !layoutName || !score) {
            alert("All fields are required!");
            return;
        }
        onSubmit(courseName, layoutName, parseInt(score, 10));
    };

    return (
        <form onSubmit={handleSubmit}>
            <div>
                <label>Course Name:</label>
                <input type="text" value={courseName} onChange={(e) => setCourseName(e.target.value)} required />
            </div>
            <div>
                <label>Layout Name:</label>
                <input type="text" value={layoutName} onChange={(e) => setLayoutName(e.target.value)} required />
            </div>
            <div>
                <label>Score (relative to par):</label>
                <input type="number" value={score} onChange={(e) => setScore(e.target.value)} required />
            </div>
            <button type="submit">Calculate Rating</button>
        </form>
    );
};

export default RatingForm;
