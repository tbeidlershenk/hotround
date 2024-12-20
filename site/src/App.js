import * as React from "react";
import Grid from "@mui/joy/Grid";
import Card from "@mui/joy/Card";
import Typography from "@mui/joy/Typography";
import CardContent from "@mui/joy/CardContent";
import CardOverflow from "@mui/joy/CardOverflow";
import Autocomplete from "@mui/joy/Autocomplete";
import { createFilterOptions } from "@mui/material/Autocomplete";
import Button from "@mui/joy/Button";
import Input from "@mui/joy/Input";
import Link from "@mui/joy/Link";
import { Box, ThemeProvider } from "@mui/joy";
import Header from "./components/Header";
import { CssVarsProvider, extendTheme } from "@mui/joy/styles";
import CssBaseline from "@mui/joy/CssBaseline";
import Footer from "./components/Footer";
import { BarChart } from "@mui/x-charts/BarChart";
import { LineChart } from "@mui/x-charts/LineChart";
import Table from "@mui/joy/Table";
import Layout from "./components/Layout";
import Course from "./components/Course";
import theme from "./components/Theme";
import Graph from "./components/Graph";
import Pagination from "./components/Pagination";

function App() {
    const [formData, setFormData] = React.useState({
        courseName: "",
        layoutName: "",
        score: "",
    });
    const [courseOptions, setCourseOptions] = React.useState([]);
    const [layoutOptions, setLayoutOptions] = React.useState([]);
    const [results, setResults] = React.useState([]);
    const [currentPage, setCurrentPage] = React.useState(0);

    const goNextPage = (event) => {
        const nextPage = (currentPage + 1) % results.length;
        setCurrentPage(nextPage);
    };

    const goPrevPage = (event) => {
        if (currentPage === 0) {
            setCurrentPage(results.length - 1);
            return;
        }
        const nextPage = (currentPage - 1) % results.length;
        setCurrentPage(nextPage);
    };

    React.useEffect(() => {
        fetch("/api/courses", { method: "GET" })
            .then((response) => response.json())
            .then((data) => {
                setCourseOptions(data);
            })
            .catch((error) => {
                console.error("Error fetching courses:", error);
            });
    }, []);

    const defaultFilterOptions = createFilterOptions();

    const filterCourseOptions = (options, state) => {
        return defaultFilterOptions(options, state).slice(0, 10);
    };

    const handleCourseChange = (event) => {
        const { name, value } = event.target;
        if (!value || value === "") {
            setLayoutOptions([]);
            return;
        } else {
            fetch(`/api/layouts/${value}`, { method: "GET" })
                .then((response) => response.json())
                .then((data) => {
                    setLayoutOptions(data);
                })
                .catch((error) => {
                    console.error("Error fetching layouts:", error);
                });
        }
        console.log(name, value);
        setFormData((prev) => ({ ...prev, [name]: value }));
    };

    const handleFormChange = (event) => {
        const { name, value } = event.target;
        console.log(name, value);
        setFormData((prev) => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        const { courseName, layoutName, score } = formData;
        console.log(courseName, layoutName, score);

        if (!courseName || !layoutName || !score) {
            alert("Please fill in all fields.");
            return;
        }

        try {
            // const response = await fetch("/api/rating/${courseName}/${layoutName}/${score}", { method: "GET" });
            // const data = await response.json();
            const data = [
                {
                    course_name: "Course Name",
                    layout_name: "Layout Name",
                    score: -5,
                    score_rating: 970,
                    layout: {
                        layout_hole_distances: [
                            {
                                hole_number: 1,
                                distance: 300,
                            },
                            {
                                hole_number: 2,
                                distance: 350,
                            },
                            {
                                hole_number: 3,
                                distance: 400,
                            },
                            {
                                hole_number: 4,
                                distance: 450,
                            },
                            {
                                hole_number: 5,
                                distance: 500,
                            },
                            {
                                hole_number: 6,
                                distance: 550,
                            },
                            {
                                hole_number: 7,
                                distance: 600,
                            },
                            {
                                hole_number: 8,
                                distance: 650,
                            },
                            {
                                hole_number: 9,
                                distance: 700,
                            },
                            {
                                hole_number: 10,
                                distance: 750,
                            },
                            {
                                hole_number: 11,
                                distance: 800,
                            },
                            {
                                hole_number: 12,
                                distance: 850,
                            },
                            {
                                hole_number: 13,
                                distance: 900,
                            },
                            {
                                hole_number: 14,
                                distance: 950,
                            },
                            {
                                hole_number: 15,
                                distance: 1000,
                            },
                            {
                                hole_number: 16,
                                distance: 1050,
                            },
                            {
                                hole_number: 17,
                                distance: 1100,
                            },
                            {
                                hole_number: 18,
                                distance: 1150,
                            },
                        ],
                        layout_total_distance: 10000,
                        layout_par: 54,
                        layouts: [
                            {
                                id: 1,
                                layout_name: "Layout 1",
                                pdga_live_link: "https://www.pdga.com/tour/event/12345",
                                num_rounds: 1,
                            },
                            {
                                id: 2,
                                layout_name: "Layout 2",
                                pdga_live_link: "https://www.pdga.com/tour/event/12345",
                                num_rounds: 1,
                            },
                            {
                                id: 3,
                                layout_name: "Layout 3",
                                pdga_live_link: "https://www.pdga.com/tour/event/12345",
                                num_rounds: 2,
                            },
                            {
                                id: 3,
                                layout_name: "Layout 4",
                                pdga_live_link: "https://www.pdga.com/tour/event/12345",
                                num_rounds: 16,
                            },
                            {
                                id: 3,
                                layout_name: "Layout 5",
                                pdga_live_link: "https://www.pdga.com/tour/event/12345",
                                num_rounds: 5,
                            },
                            {
                                id: 3,
                                layout_name: "Layout 6",
                                pdga_live_link: "https://www.pdga.com/tour/event/12345",
                                num_rounds: 8,
                            },
                            {
                                id: 3,
                                layout_name: "Layout 7",
                                pdga_live_link: "https://www.pdga.com/tour/event/12345",
                                num_rounds: 1,
                            },
                            {
                                id: 3,
                                layout_name: "Layout 8",
                                pdga_live_link: "https://www.pdga.com/tour/event/12345",
                                num_rounds: 4,
                            },
                            {
                                id: 3,
                                layout_name: "Layout 9",
                                pdga_live_link: "https://www.pdga.com/tour/event/12345",
                                num_rounds: 32,
                            },
                            {
                                id: 3,
                                layout_name: "Layout 9",
                                pdga_live_link: "https://www.pdga.com/tour/event/12345",
                                num_rounds: 32,
                            },
                            {
                                id: 3,
                                layout_name: "Layout 9",
                                pdga_live_link: "https://www.pdga.com/tour/event/12345",
                                num_rounds: 32,
                            },
                            {
                                id: 3,
                                layout_name: "Layout 9",
                                pdga_live_link: "https://www.pdga.com/tour/event/12345",
                                num_rounds: 32,
                            },
                        ],
                    },
                    rounds: [
                        {
                            round_date: "2021-01-01",
                            num_rounds: 1,
                            round_rating: 980,
                        },
                        {
                            round_date: "2021-01-01",
                            num_rounds: 1,
                            round_rating: 970,
                        },
                        {
                            round_date: "2021-01-01",
                            num_rounds: 2,
                            round_rating: 960,
                        },
                        {
                            round_date: "2021-01-01",
                            num_rounds: 3,
                            round_rating: 950,
                        },
                        {
                            round_date: "2021-01-01",
                            num_rounds: 5,
                            round_rating: 940,
                        },
                        {
                            round_date: "2021-01-01",
                            num_rounds: 10,
                            round_rating: 930,
                        },
                        {
                            round_date: "2021-01-01",
                            num_rounds: 4,
                            round_rating: 920,
                        },
                        {
                            round_date: "2021-01-01",
                            num_rounds: 2,
                            round_rating: 910,
                        },
                        {
                            round_date: "2021-01-02",
                            num_rounds: 1,
                            round_rating: 900,
                        },
                    ],
                    percentile: 80,
                },
                {
                    course_name: "Course Name",
                    layout_name: "Layout Name",
                    score: -6,
                    score_rating: 980,
                    layout: {
                        layout_hole_distances: [
                            {
                                hole_number: 1,
                                distance: 300,
                            },
                            {
                                hole_number: 2,
                                distance: 350,
                            },
                            {
                                hole_number: 3,
                                distance: 400,
                            },
                            {
                                hole_number: 4,
                                distance: 450,
                            },
                            {
                                hole_number: 5,
                                distance: 500,
                            },
                            {
                                hole_number: 6,
                                distance: 550,
                            },
                            {
                                hole_number: 7,
                                distance: 600,
                            },
                            {
                                hole_number: 8,
                                distance: 650,
                            },
                            {
                                hole_number: 9,
                                distance: 700,
                            },
                            {
                                hole_number: 10,
                                distance: 750,
                            },
                            {
                                hole_number: 11,
                                distance: 800,
                            },
                            {
                                hole_number: 12,
                                distance: 850,
                            },
                            {
                                hole_number: 13,
                                distance: 900,
                            },
                            {
                                hole_number: 14,
                                distance: 950,
                            },
                            {
                                hole_number: 15,
                                distance: 1000,
                            },
                            {
                                hole_number: 16,
                                distance: 1050,
                            },
                            {
                                hole_number: 17,
                                distance: 1100,
                            },
                            {
                                hole_number: 18,
                                distance: 1150,
                            },
                        ],
                        layout_total_distance: 10000,
                        layout_par: 54,
                        layouts: [
                            {
                                id: 1,
                                layout_name: "Layout 1",
                                pdga_live_link: "https://www.pdga.com/tour/event/12345",
                                num_rounds: 1,
                            },
                            {
                                id: 2,
                                layout_name: "Layout 2",
                                pdga_live_link: "https://www.pdga.com/tour/event/12345",
                                num_rounds: 1,
                            },
                            {
                                id: 3,
                                layout_name: "Layout 3",
                                pdga_live_link: "https://www.pdga.com/tour/event/12345",
                                num_rounds: 2,
                            },
                            {
                                id: 3,
                                layout_name: "Layout 4",
                                pdga_live_link: "https://www.pdga.com/tour/event/12345",
                                num_rounds: 16,
                            },
                            {
                                id: 3,
                                layout_name: "Layout 5",
                                pdga_live_link: "https://www.pdga.com/tour/event/12345",
                                num_rounds: 5,
                            },
                            {
                                id: 3,
                                layout_name: "Layout 6",
                                pdga_live_link: "https://www.pdga.com/tour/event/12345",
                                num_rounds: 8,
                            },
                            {
                                id: 3,
                                layout_name: "Layout 7",
                                pdga_live_link: "https://www.pdga.com/tour/event/12345",
                                num_rounds: 1,
                            },
                            {
                                id: 3,
                                layout_name: "Layout 8",
                                pdga_live_link: "https://www.pdga.com/tour/event/12345",
                                num_rounds: 4,
                            },
                            {
                                id: 3,
                                layout_name: "Layout 9",
                                pdga_live_link: "https://www.pdga.com/tour/event/12345",
                                num_rounds: 32,
                            },
                            {
                                id: 3,
                                layout_name: "Layout 9",
                                pdga_live_link: "https://www.pdga.com/tour/event/12345",
                                num_rounds: 32,
                            },
                            {
                                id: 3,
                                layout_name: "Layout 9",
                                pdga_live_link: "https://www.pdga.com/tour/event/12345",
                                num_rounds: 32,
                            },
                            {
                                id: 3,
                                layout_name: "Layout 9",
                                pdga_live_link: "https://www.pdga.com/tour/event/12345",
                                num_rounds: 32,
                            },
                        ],
                    },
                    rounds: [
                        {
                            round_date: "2021-01-01",
                            num_rounds: 1,
                            round_rating: 980,
                        },
                        {
                            round_date: "2021-01-01",
                            num_rounds: 1,
                            round_rating: 970,
                        },
                        {
                            round_date: "2021-01-01",
                            num_rounds: 2,
                            round_rating: 960,
                        },
                        {
                            round_date: "2021-01-01",
                            num_rounds: 3,
                            round_rating: 950,
                        },
                        {
                            round_date: "2021-01-01",
                            num_rounds: 5,
                            round_rating: 940,
                        },
                        {
                            round_date: "2021-01-01",
                            num_rounds: 10,
                            round_rating: 930,
                        },
                        {
                            round_date: "2021-01-01",
                            num_rounds: 4,
                            round_rating: 920,
                        },
                        {
                            round_date: "2021-01-01",
                            num_rounds: 2,
                            round_rating: 910,
                        },
                        {
                            round_date: "2021-01-02",
                            num_rounds: 1,
                            round_rating: 900,
                        },
                    ],
                    percentile: 80,
                },
            ];

            setResults(data);
            setCurrentPage(0);
        } catch (error) {
            console.error("Error fetching ratings:", error);
            setResults([]);
        }
    };

    const handleNext = () => {
        if (currentPage < results.length - 1) {
            setCurrentPage((prev) => prev + 1);
        }
    };

    const handlePrevious = () => {
        if (currentPage > 0) {
            setCurrentPage((prev) => prev - 1);
        }
    };

    console.log(window.innerWidth);
    console.log(window.document.documentElement.clientWidth);

    return (
        <CssVarsProvider disableTransitionOnChange theme={theme} colorScheme={"dark"}>
            <CssBaseline />
            <Box container spacing={2} sx={{ display: "flex", flexDirection: "column", minHeight: "100vh", maxHeight: "100vh" }}>
                <Header />
                {/* Input Form */}

                <Grid container spacing={2} sx={{ justifyContent: "center", alignItems: "top", px: 2, mb: 2, flex: 1 }}>
                    <Grid item container width="100vw" height="150px" spacing={2} justifyContent={"center"}>
                        <Grid item xs={5} sm={2}>
                            <Autocomplete
                                freeSolo
                                label="Course Name"
                                name="courseName"
                                placeholder="Course name"
                                options={courseOptions}
                                filterOptions={filterCourseOptions}
                                onChange={handleCourseChange}
                                onInputChange={handleCourseChange}
                                inputValue={formData.courseName}
                                variant="outlined"
                                color="primary"
                            />
                        </Grid>
                        <Grid item xs={5} sm={2}>
                            <Autocomplete
                                freeSolo
                                label="Layout Name"
                                name="layoutName"
                                placeholder="Layout name"
                                options={layoutOptions}
                                onChange={handleFormChange}
                                onInputChange={handleFormChange}
                                inputValue={formData.layoutName}
                                variant="outlined"
                                color="primary"
                            />
                        </Grid>
                        <Grid item xs={5} sm={2}>
                            <Input
                                label="Score (relative to par)"
                                name="score"
                                placeholder="Score"
                                type="number"
                                value={formData.score}
                                onChange={handleFormChange}
                                variant="outlined"
                                color="primary"
                            />
                        </Grid>
                        <Grid item xs={5} sm={2}>
                            <Button variant="solid" color="primary" onClick={handleSubmit} size="sm" fullWidth>
                                Calculate
                            </Button>
                        </Grid>
                    </Grid>

                    <Box width="76vw">
                        {results.length > 0 ? (
                            <Grid container spacing={2} sx={{ justifyContent: "center" }}>
                                <Grid item xs={12} sm={12} md={12} lg={12}>
                                    <Typography>
                                        Returned {results.length} results. Displaying result {currentPage + 1} of {results.length}.
                                    </Typography>
                                </Grid>
                                <Grid item xs={12} sm={6} md={6} lg={6}>
                                    <Graph data={results[currentPage]} />
                                </Grid>
                                <Grid item xs={12} sm={6} md={6} lg={6}>
                                    <Layout rows={results[currentPage].layout.layouts} />
                                </Grid>
                                <Grid item sm={12} md={12} lg={12}>
                                    <Course rows={results[currentPage].layout.layout_hole_distances} />
                                </Grid>
                                <Grid item sm={12} md={12} lg={12}>
                                    <Pagination onPageForward={goNextPage} onPageBackward={goPrevPage}></Pagination>
                                </Grid>
                            </Grid>
                        ) : (
                            <Typography variant="body1" align="center">
                                No results to display. Please enter your search criteria.
                            </Typography>
                        )}
                    </Box>
                </Grid>
                <Footer />
            </Box>
        </CssVarsProvider>
    );
}

export default App;
