import React from "react";
import Typography from "@mui/joy/Typography";
import Card from "@mui/joy/Card";
import Box from "@mui/joy/Box";
import { LineChart } from "@mui/x-charts/LineChart";

function format_score(score) {
    if (score === 0) {
        return "E";
    }
    if (score < 0) {
        return score;
    }
    if (score > 0) {
        return `+${score}`;
    }
}

function format_rating(layout, score) {
    const rating = layout.par_rating - score * layout.stroke_value;
    return Math.round(rating);
}

export default function RatingStatsCard({ layout, score }) {
    let num_unique_scores = layout.total_score_distribution.length;
    return (
        <Card variant="outlined" sx={{ flex: 1, padding: 1, height: "400px" }}>
            <Box>
                <Box
                    sx={{
                        backgroundColor: "#007259",
                        padding: 1,
                        borderTopLeftRadius: 4,
                        borderBottomLeftRadius: 4,
                        width: "fit-content",
                        display: "inline-block",
                    }}
                >
                    <Typography level="title-md" sx={{ color: "white" }}>
                        {format_score(score)}
                    </Typography>
                </Box>
                <Box
                    sx={{
                        backgroundColor: "#008E6F",
                        padding: 1,
                        borderTopRightRadius: 4,
                        borderBottomRightRadius: 4,
                        width: "fit-content",
                        display: "inline-block",
                    }}
                >
                    <Typography level="title-md" sx={{ color: "white" }}>
                        {format_rating(layout, score)}
                    </Typography>
                </Box>
                <Box
                    sx={{
                        padding: 1,
                        borderTopRightRadius: 4,
                        borderBottomRightRadius: 4,
                        width: "fit-content",
                        display: "inline-block",
                    }}
                >
                    <Typography>
                        Total <Typography fontWeight={"bold"}>{layout.total_par + score}</Typography> • Par{" "}
                        <Typography fontWeight={"bold"}>{layout.total_par}</Typography> • Dist{" "}
                        <Typography fontWeight={"bold"}>{layout.total_distance}</Typography>
                    </Typography>
                </Box>
            </Box>
            <LineChart
                xAxis={[
                    {
                        scaleType: "band",
                        dataKey: "score",
                        label: "Score",
                        tickSize: 0, // Adjust tick size
                        style: {
                            fontSize: "9px",
                            fill: "#6b7280", // Subtle gray color for labels
                        },
                        totalTicks: 3,
                        tickLabelInterval: (value, index) => index === 0 || value === 0 || index === num_unique_scores - 1,
                        tickFormatter: (value, index) => (index === 0 || value === 0 || index === num_unique_scores - 1 ? value : ""), // Show only first, last, and par labels
                    },
                ]}
                yAxis={[
                    {
                        label: "# scorecards",
                        style: {
                            fontSize: "9px",
                            fill: "#6b7280",
                        },
                        tickSize: 0, // Adjust tick size
                    },
                ]}
                dataset={layout.total_score_distribution.sort((a, b) => b.score - a.score)}
                series={[
                    {
                        showMark: false,
                        dataKey: "count",
                        style: {
                            stroke: "#3b82f6", // Use a blue color for the line
                            strokeWidth: 2,
                        },
                    },
                ]}
                height={300}
                grid={{
                    vertical: true,
                    horizontal: true,
                    stroke: "#e5e7eb", // Subtle gray grid lines
                    strokeWidth: 1,
                }}
                tooltip={{ trigger: "none" }} // No tooltip for now
                sx={{ minWidth: "100%" }}
            />

            <Typography sx={{ fontFamily: '"Source Sans 3", sans-serif' }}>
                Averaged over <Typography fontWeight={"bold"}>{layout.num_rounds}</Typography> rounds.
            </Typography>
        </Card>
    );
}
