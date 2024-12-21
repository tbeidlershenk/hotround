import * as React from "react";
import Grid from "@mui/joy/Grid";
import Typography from "@mui/joy/Typography";
import Autocomplete from "@mui/joy/Autocomplete";
import { createFilterOptions } from "@mui/material/Autocomplete";
import Button from "@mui/joy/Button";
import { Box } from "@mui/joy";
import SearchedLayoutsCard from "./cards/SearchedLayoutsCard";
import HorizontalCourseCard from "./cards/HorizontalCourseCard";
import Pagination from "./components/Pagination";

const defaultFilterOptions = createFilterOptions({ limit: 10 });

export default function RatingCalculator({ courseOptions }) {
    const [courseName, setCourseName] = React.useState("");
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

    const handleSubmit = async (event) => {
        fetch(`/api/layouts/${courseName}`, { method: "GET" })
            .then((response) => response.json())
            .then((data) => {
                setLayoutOptions(data);
            })
            .catch((error) => {
                console.error("Error fetching layouts:", error);
            });
    };

    return (
        <Grid container spacing={2} sx={{ justifyContent: "center", alignItems: "top", px: 2, mb: 2, flex: 1 }}>
            <Grid item container width="100vw" height="150px" spacing={2} justifyContent={"center"}>
                <Grid item xs={8} sm={4}>
                    <Autocomplete
                        freeSolo
                        label="Course Name"
                        name="courseName"
                        placeholder="Course name"
                        options={courseOptions}
                        filterOptions={defaultFilterOptions}
                        inputValue={courseName}
                        variant="outlined"
                        color="primary"
                    />
                </Grid>
                <Grid item xs={8} sm={4}>
                    <Button variant="solid" color="primary" onClick={handleSubmit} size="sm" fullWidth>
                        Search
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
                            <SearchedLayoutsCard rows={results[currentPage].layout.layouts} />
                        </Grid>
                        <Grid item sm={12} md={12} lg={12}>
                            <HorizontalCourseCard rows={results[currentPage].layout.layout_hole_distances} />
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
    );
}
