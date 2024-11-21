import React, { useState } from "react";
import axios from "axios";
import RatingForm from "./components/RatingForm";
import ResultDisplay from "./components/ResultDisplay";
import ErrorCodes from "./enums/ErrorCodes";

const App = () => {
    const [result, setResult] = useState(null);

    const handleFormSubmit = async (courseName, layoutName, score) => {
        try {
            const response = await axios.get(`http://localhost:5000/rating/${courseName}/${layoutName}/${score}`);
            setResult(response.data);
        } catch (error) {
            console.error("Error fetching rating:", error);
            setResult({
                status: ErrorCodes.ERROR_NO_ROUNDS,
                title: "An error occurred while fetching the data.",
            });
        }
    };

    return (
        <div>
            <h1>Disc Golf Round Ratings</h1>
            <RatingForm onSubmit={handleFormSubmit} />
            <ResultDisplay result={result} />
        </div>
    );
};

export default App;
