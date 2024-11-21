import React from "react";

const ResultDisplay = ({ result }) => {
    if (!result) return null;

    if (result.status !== 0) {
        return (
            <div>
                <h3>{result.title}</h3>
                {result.close_courses && (
                    <div>
                        <h4>Close Matches:</h4>
                        <ul>
                            {result.close_courses.map((course, index) => (
                                <li key={index}>{course}</li>
                            ))}
                        </ul>
                    </div>
                )}
                {result.close_layouts && (
                    <div>
                        <h4>Close Layouts:</h4>
                        <ul>
                            {result.close_layouts.map((layout, index) => (
                                <li key={index}>{layout}</li>
                            ))}
                        </ul>
                    </div>
                )}
            </div>
        );
    }

    return (
        <div>
            <h3>Rating Results</h3>
            <p>Score Rating: {result.score_rating}</p>
            <h4>Layout Information</h4>
            <p>Par: {result.layout.layout_par}</p>
            <p>Total Distance: {result.layout.layout_total_distance} ft</p>
        </div>
    );
};

export default ResultDisplay;
