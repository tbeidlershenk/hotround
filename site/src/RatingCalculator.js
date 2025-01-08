import * as React from "react";
import Grid from "@mui/joy/Grid";
import Typography from "@mui/joy/Typography";
import Autocomplete from "@mui/joy/Autocomplete";
import { createFilterOptions } from "@mui/material/Autocomplete";
import Input from "@mui/joy/Input";
import Button from "@mui/joy/Button";
import { Box, ListItem } from "@mui/joy";
import UsedLayoutsCard from "./cards/UsedLayoutsCard";
import HorizontalCourseCard from "./cards/HorizontalCourseCard";
import RatingStatsCard from "./cards/RatingStatsCard";
import LayoutOption from "./components/LayoutOption";

const status_none = -1;
const status_success = 0;
const status_error_no_matches = 1;
const status_error_no_layouts = 2;
const status_error_no_rounds = 3;

export default function RatingCalculator({ courseOptions }) {
    const [course, setCourse] = React.useState("");
    const [layout, setLayout] = React.useState(null);
    const [score, setScore] = React.useState(0);
    // Represents the status of the last API call
    const [status, setStatus] = React.useState(status_none);
    const [layoutOptions, setLayoutOptions] = React.useState([]);

    console.log("STATE");
    console.log("---------------------------");
    console.log("Course ", course);
    console.log("Layout ", layout);
    console.log("Score ", score);
    console.log("Layout options ", layoutOptions);
    console.log("Status ", status);
    console.log("---------------------------");
    console.log("");

    const inputRef = React.useRef(null);
    const defaultFilterOptions = createFilterOptions({ limit: 10 });

    async function handleCourseChange(course) {
        // Reset all state
        setLayout(null);
        setStatus(status_none);

        if (!course || course === "") {
            setLayoutOptions([]);
            return;
        }

        // Fetch aggregated layouts and rating data
        fetch(`/api/rating/${course}`, { method: "GET" })
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                setStatus(data.status);
                setLayoutOptions(data.layouts);
            })
            .catch((error) => {
                console.error("Error fetching layouts:", error);
            });

        // Set the new course
        setCourse(course);
    }

    function body() {
        if (status === status_none) {
            return (
                <Typography variant="body1" align="center">
                    No results to display. Please enter your search criteria.
                </Typography>
            );
        } else if (status === status_success) {
            if (!layout) {
                return (
                    <Typography variant="body1" align="center">
                        Please select a layout.
                    </Typography>
                );
            }
            return (
                <Grid container spacing={2} sx={{ justifyContent: "center" }}>
                    <Grid item xs={12} sm={6} md={6} lg={6}>
                        <RatingStatsCard layout={layout} score={score} />
                    </Grid>
                    <Grid item xs={12} sm={6} md={6} lg={6}>
                        <UsedLayoutsCard layout_names_and_links={layout.layout_names_and_links} />
                    </Grid>
                    <Grid item sm={12} md={12} lg={12}>
                        <HorizontalCourseCard layout={layout} />
                    </Grid>
                </Grid>
            );
        } else if (status === status_error_no_matches) {
            return (
                <Typography variant="body1" align="center">
                    Not enough PDGA sanctioned rounds found for this course, cannot calculate ratings.
                </Typography>
            );
        } else {
            return (
                <Typography variant="body1" align="center">
                    Failed: status_{status}
                </Typography>
            );
        }
    }

    return (
        <Grid container spacing={2} sx={{ justifyContent: "center", alignItems: "top", px: 2, mb: 2, flex: 1 }}>
            <Grid item container width="100vw" height="150px" spacing={2} justifyContent={"center"}>
                <Grid item xs={5} sm={2.5}>
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
                <Grid item xs={5} sm={2.5}>
                    <Autocomplete
                        label="Layout Name"
                        name="layoutName"
                        placeholder="Layout keywords"
                        slotProps={{
                            listbox: {
                                sx: {
                                    minWidth: "275px", // Allow the width to adjust to content
                                    whiteSpace: "nowrap", // Prevent content from wrapping
                                },
                            },
                        }}
                        options={layoutOptions}
                        defaultValue={layoutOptions.length > 0 ? layoutOptions[0] : null}
                        getOptionLabel={(layout) => (typeof layout === "string" ? layout : layout.descriptive_name)}
                        onChange={(_, value) => {
                            setLayout(value);
                        }}
                        renderOption={(props, layout) => (
                            <ListItem {...props}>
                                <LayoutOption layout={layout} />
                            </ListItem>
                        )}
                        variant="outlined"
                        color="primary"
                        autoHightlight
                    />
                </Grid>
                <Grid item xs={5} sm={2.5}>
                    <Input
                        label="Score (relative to par)"
                        name="score"
                        placeholder="Score"
                        type="number"
                        slotProps={{
                            input: {
                                ref: inputRef,
                                min: -1000,
                                max: 1000,
                                step: 1,
                            },
                        }}
                        onChange={(event) => {
                            if (event.target.value === "") {
                                setScore(0);
                            } else {
                                setScore(parseInt(event.target.value));
                            }
                        }}
                        variant="outlined"
                        color="primary"
                    />
                </Grid>
            </Grid>

            <Box width="76vw">{body()}</Box>
        </Grid>
    );
}
