import React from "react";
import Table from "@mui/joy/Table";
import Box from "@mui/joy/Box";
import Card from "@mui/joy/Card";

export default function HorizontalCourseCard({ rows }) {
    const numberOfHoles = rows.length;

    return (
        <Box sx={{}}>
            <Card variant="outlined" sx={{ padding: 0, overflowX: "auto", width: "100%" }}>
                <Table variant="soft" sx={{ minWidth: numberOfHoles * 48 }}>
                    <thead>
                        {[...rows].map((hole) => (
                            <th key={hole.hole_number} style={{ textAlign: "center", padding: "8px", border: "1px #ddd" }}>
                                #{hole.hole_number}
                            </th>
                        ))}
                    </thead>
                    <tbody>
                        <tr>
                            {/* Display the distances in the row for each hole */}
                            {[...rows].map((hole) => (
                                <td key={hole.hole_number} style={{ textAlign: "center", padding: "8px" }}>
                                    {hole.distance}
                                </td>
                            ))}
                        </tr>
                    </tbody>
                </Table>
            </Card>
        </Box>
    );
}
