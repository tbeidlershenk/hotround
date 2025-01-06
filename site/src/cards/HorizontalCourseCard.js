import React from "react";
import Table from "@mui/joy/Table";
import Box from "@mui/joy/Box";
import Card from "@mui/joy/Card";

export default function HorizontalCourseCard({ layout }) {
    const holes = Array.from({ length: layout.num_holes }, (_, i) => i + 1);
    return (
        <Box sx={{}}>
            <Card variant="outlined" sx={{ padding: 0, overflowX: "auto", width: "100%" }}>
                <Table variant="soft" sx={{ minWidth: layout.num_holes * 50 }}>
                    <thead>
                        <th style={{ textAlign: "center", padding: "8px", border: "1px #ddd", minWidth: 60 }}>Hole</th>
                        {holes.map((hole) => (
                            <th key={hole} style={{ textAlign: "center", padding: "8px", border: "1px #ddd" }}>
                                #{hole}
                            </th>
                        ))}
                    </thead>
                    <tbody>
                        <tr>
                            <td style={{ textAlign: "center", padding: "8px", minWidth: 60 }}>Dist</td>
                            {holes.map((hole) => (
                                <td key={hole} style={{ textAlign: "center", padding: "8px" }}>
                                    {layout.distances[hole - 1]}
                                </td>
                            ))}
                        </tr>
                        <tr>
                            <td style={{ textAlign: "center", padding: "8px", minWidth: 60 }}>Par</td>
                            {holes.map((hole) => (
                                <td key={hole} style={{ textAlign: "center", padding: "8px" }}>
                                    {layout.pars[hole - 1]}
                                </td>
                            ))}
                        </tr>
                        <tr>
                            <td style={{ textAlign: "center", padding: "8px", minWidth: 60 }}>Avg</td>
                            {holes.map((hole) => (
                                <td
                                    key={hole}
                                    style={{
                                        textAlign: "center",
                                        padding: "8px",
                                        color: layout.averaged_hole_scores[hole - 1] > layout.pars[hole - 1] ? "red" : "#008E6F",
                                    }}
                                >
                                    {layout.averaged_hole_scores[hole - 1]}
                                </td>
                            ))}
                        </tr>
                    </tbody>
                </Table>
            </Card>
        </Box>
    );
}
