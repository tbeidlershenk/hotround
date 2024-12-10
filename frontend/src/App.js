import React, { useState } from "react";
import { Box, Grid, TextField, Button, Typography, Paper, AppBar, Toolbar, Link } from "@mui/material";
import ErrorCodes from "./ErrorCodes.js"; // Import error codes

function App() {
    const [formData, setFormData] = useState({
        courseName: "",
        layoutName: "",
        score: "",
    });
    const [results, setResults] = useState(null);

    const handleInputChange = (event) => {
        const { name, value } = event.target;
        setFormData((prev) => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        const { courseName, layoutName, score } = formData;

        try {
            const response = await fetch(`/rating/${courseName}/${layoutName}/${score}`, { method: "GET" });
            const data = await response.json();

            setResults(data);
        } catch (error) {
            console.error("Error fetching ratings:", error);
            setResults({
                error: "Unable to fetch ratings. Please try again later.",
            });
        }
    };

    const accentColor = "#003462";
    const hoverColor = "#007ec7";

    return (
        <Box sx={{ display: "flex", flexDirection: "column", minHeight: "100vh" }}>
            {/* Header */}
            <AppBar position="static" sx={{ mb: 2, backgroundColor: accentColor, color: "white" }}>
                <Toolbar>
                    <Typography variant="h5" sx={{ flexGrow: 1, textAlign: "center", fontWeight: "bold" }}>
                        PDGA Rating Calculator
                    </Typography>
                    <img
                        src="https://m.discgolfscene.com/logos/clubs/9460/professional-disc-golf-association-2c5e214b5c2f.jpg"
                        alt="PDGA Logo"
                        style={{ height: "40px", marginLeft: "auto" }}
                    />
                </Toolbar>
            </AppBar>

            {/* Content */}
            <Grid
                container
                spacing={2}
                sx={{
                    minHeight: "calc(100vh - 128px)",
                    alignItems: "center",
                    justifyContent: "center",
                    px: 2,
                }}
            >
                {/* Left Column: Form */}
                <Grid item xs={12} md={5}>
                    <Paper
                        elevation={1}
                        sx={{
                            p: 4,
                            borderRadius: 4,
                            backgroundColor: "#F5F8FA",
                            border: "1px solid #D1D5DB",
                        }}
                    >
                        <Typography variant="h6" gutterBottom sx={{ fontWeight: "bold", mb: 2, color: accentColor }}>
                            Calculate Round Ratings
                        </Typography>
                        <form onSubmit={handleSubmit}>
                            <TextField
                                label="Course Name"
                                name="courseName"
                                value={formData.courseName}
                                onChange={handleInputChange}
                                fullWidth
                                margin="normal"
                                sx={{ backgroundColor: "white", borderRadius: 2 }}
                            />
                            <TextField
                                label="Layout Name"
                                name="layoutName"
                                value={formData.layoutName}
                                onChange={handleInputChange}
                                fullWidth
                                margin="normal"
                                sx={{ backgroundColor: "white", borderRadius: 2 }}
                            />
                            <TextField
                                label="Score (relative to par)"
                                name="score"
                                type="number"
                                value={formData.score}
                                onChange={handleInputChange}
                                fullWidth
                                margin="normal"
                                sx={{ backgroundColor: "white", borderRadius: 2 }}
                            />
                            <Button
                                type="submit"
                                variant="contained"
                                fullWidth
                                sx={{
                                    mt: 2,
                                    backgroundColor: accentColor,
                                    "&:hover": { backgroundColor: hoverColor },
                                    borderRadius: 2,
                                }}
                            >
                                Get Rating
                            </Button>
                        </form>
                    </Paper>
                </Grid>
                <Grid item xs={12} md={5}>
                    <Paper
                        elevation={1}
                        sx={{
                            p: 4,
                            borderRadius: 4,
                            backgroundColor: "#F5F8FA",
                            border: "1px solid #D1D5DB",
                        }}
                    >
                        <Typography variant="h6" gutterBottom sx={{ fontWeight: "bold", mb: 2, color: accentColor }}>
                            Results
                        </Typography>
                        {results ? (
                            results.error ? (
                                <Typography color="error">{results.error}</Typography>
                            ) : (
                                <Box>
                                    {results.status === ErrorCodes.SUCCESS && (
                                        <Typography variant="body1" sx={{ color: "#4B5563" }}>
                                            <strong>Status:</strong> Success <br />
                                            <strong>Score Rating:</strong> {results.score_rating} <br />
                                            <strong>Layout:</strong> {results.layout.layout_names.join(", ")}
                                        </Typography>
                                    )}
                                    {results.status === ErrorCodes.ERROR_NO_MATCHES && (
                                        <Typography variant="body1" sx={{ color: "#4B5563" }}>
                                            <strong>Status:</strong> No Course Matches Found <br />
                                            <strong>Close Courses:</strong> {results.close_courses.join(", ")}
                                        </Typography>
                                    )}
                                    {results.status === ErrorCodes.ERROR_NO_LAYOUTS && (
                                        <Typography variant="body1" sx={{ color: "#4B5563" }}>
                                            <strong>Status:</strong> No Matching Layouts Found <br />
                                            <strong>Close Layouts:</strong> {results.close_layouts.join(", ")}
                                        </Typography>
                                    )}
                                    {results.status === ErrorCodes.ERROR_NO_ROUNDS && (
                                        <Typography variant="body1" sx={{ color: "#4B5563" }}>
                                            <strong>Status:</strong> No Rounds Found
                                        </Typography>
                                    )}
                                </Box>
                            )
                        ) : (
                            <Typography sx={{ color: "#6B7280" }}>No results to display.</Typography>
                        )}
                    </Paper>
                </Grid>
            </Grid>

            <Box
                component="footer"
                sx={{
                    mt: "auto",
                    p: 2,
                    textAlign: "center",
                    backgroundColor: accentColor,
                    color: "white",
                }}
            >
                <Typography variant="body2">
                    Created by Tobias Beidler-Shenk |
                    <Link href="https://github.com/tbeidlershenk" target="_blank" sx={{ color: "lightblue", mx: 1 }}>
                        GitHub
                    </Link>
                    |
                    <Link href="https://tbeidlershenk.github.io" target="_blank" sx={{ color: "lightblue", mx: 1 }}>
                        Website
                    </Link>
                </Typography>
            </Box>
        </Box>
    );
}

export default App;
