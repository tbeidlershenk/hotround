import * as React from "react";
import Grid from "@mui/joy/Grid";
import Typography from "@mui/joy/Typography";
import Autocomplete from "@mui/joy/Autocomplete";
import { createFilterOptions } from "@mui/material/Autocomplete";
import Button from "@mui/joy/Button";
import Input from "@mui/joy/Input";
import { Box } from "@mui/joy";
import UsedLayoutsCard from "./cards/UsedLayoutsCard";
import HorizontalCourseCard from "./cards/HorizontalCourseCard";
import RatingStatsCard from "./cards/RatingStatsCard";
import Pagination from "./components/Pagination";
import Status from "./Status";

const status_none = -1;
const status_success = 0;
const status_error_no_matches = 1;
const status_error_no_layouts = 2;
const status_error_no_rounds = 3;

export default function RatingCalculator({ courseOptions }) {
    const [course, setCourse] = React.useState("");
    const [layout, setLayout] = React.useState("");
    const [score, setScore] = React.useState(0);
    const [layoutOptions, setLayoutOptions] = React.useState([]);
    const [results, setResults] = React.useState([]);
    const [status, setStatus] = React.useState(status_none);
    const [currentPage, setCurrentPage] = React.useState(0);

    const defaultFilterOptions = createFilterOptions({ limit: 10 });

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

    async function handleCourseChange(course) {
        console.log("Course name changed to: ", course);

        if (!course || course === "") {
            setLayoutOptions([]);
            return;
        }
        fetch(`/api/layouts/${course}`, { method: "GET" })
            .then((response) => response.json())
            .then((data) => {
                setLayoutOptions(data);
            })
            .catch((error) => {
                console.error("Error fetching layouts:", error);
            });
        setCourse(course);
    }

    const handleSubmit = async (event) => {
        console.log(course, layout, score);

        if (!course || !layout) {
            alert("Please fill in all fields.");
            return;
        }

        try {
            const response = await fetch(`/api/rating/${course}/${layout}/${score}`, { method: "GET" });
            const data = await response.json();

            if (data.length === 0) {
                console.log("Returned nothing");
                return;
            }
            setResults(data);
            setCurrentPage(0);
            setStatus(data[0].status);
        } catch (error) {
            console.error("Error fetching ratings:", error);
            setResults([
                {
                    status: status_none,
                },
            ]);
        }
    };

    function body() {
        if (status == status_none) {
            return (
                <Typography variant="body1" align="center">
                    No results to display. Please enter your search criteria.
                </Typography>
            );
        } else if (status === status_success) {
            return (
                <Grid container spacing={2} sx={{ justifyContent: "center" }}>
                    <Grid item xs={12} sm={12} md={12} lg={12}>
                        <Typography>
                            Returned {results.length} results. Displaying result {currentPage + 1} of {results.length}.
                        </Typography>
                    </Grid>
                    <Grid item xs={12} sm={6} md={6} lg={6}>
                        <RatingStatsCard data={results[currentPage]} />
                    </Grid>
                    <Grid item xs={12} sm={6} md={6} lg={6}>
                        <UsedLayoutsCard rows={results[currentPage].layout.layouts} />
                    </Grid>
                    <Grid item sm={12} md={12} lg={12}>
                        <HorizontalCourseCard rows={results[currentPage].layout.layout_hole_distances} />
                    </Grid>
                    <Grid item sm={12} md={12} lg={12}>
                        <Pagination onPageForward={goNextPage} onPageBackward={goPrevPage}></Pagination>
                    </Grid>
                </Grid>
            );
        } else {
            return (
                <Typography variant="body1" align="center">
                    Failed: {status}
                </Typography>
            );
        }
    }

    return (
        <Grid container spacing={2} sx={{ justifyContent: "center", alignItems: "top", px: 2, mb: 2, flex: 1 }}>
            <Grid item container width="100vw" height="150px" spacing={2} justifyContent={"center"}>
                <Grid item xs={5} sm={2}>
                    <Autocomplete
                        label="Course Name"
                        name="courseName"
                        placeholder="Course name"
                        options={courseOptions}
                        onChange={(_, value) => {
                            handleCourseChange(value);
                        }}
                        filterOptions={defaultFilterOptions}
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
                        value={layout}
                        onInputChange={(_, value) => {
                            setLayout(value);
                        }}
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
                        onChange={(event) => {
                            setScore(event.target.value);
                        }}
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

            <Box width="76vw">{body()}</Box>
        </Grid>
    );
}
