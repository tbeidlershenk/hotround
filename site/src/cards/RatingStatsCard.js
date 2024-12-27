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

function format_rating(data, score) {
    const rating = data.par_rating - score * data.stroke_value;
    return Math.round(rating);
}

export default function RatingStatsCard({ data, score }) {
    return (
        <Card variant="outlined" sx={{ flex: 1, padding: 2, height: "400px" }}>
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
                        {format_rating(data, score)}
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
                        Total <Typography fontWeight={"bold"}>{data.layout_par + score}</Typography> • Par{" "}
                        <Typography fontWeight={"bold"}>{data.layout_par}</Typography> • Dist{" "}
                        <Typography fontWeight={"bold"}>{data.layout_total_distance}</Typography>
                    </Typography>
                </Box>
            </Box>
            <LineChart
                xAxis={[{ scaleType: "band", dataKey: "round_rating" }]}
                dataset={data.rounds.sort((a, b) => a.round_rating - b.round_rating)}
                series={[{ dataKey: "num_rounds" }]}
                height={300}
                grid={{ vertical: true, horizontal: true }}
                tooltip={{ trigger: "none" }}
            />
            <Typography sx={{ fontFamily: '"Source Sans 3", sans-serif' }}>
                Averaged over <Typography fontWeight={"bold"}>{data.rounds.length}</Typography> rounds. You scored in the top{" "}
                <Typography fontWeight={"bold"}>{data.percentile}%!</Typography>
            </Typography>
        </Card>
    );
}
