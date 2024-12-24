import * as React from "react";
import Typography from "@mui/joy/Typography";
import Card from "@mui/joy/Card";

export default function LayoutOption({ option }) {
    return (
        <Card variant="outlined" sx={{ padding: 2, flex: 1 }}>
            <Typography variant="h6">{option.layout_name}</Typography>
            <Typography>
                {"Par "}
                <Typography fontWeight={"bold"}>{option.layout_par}</Typography>
                {" • "}
                <Typography fontWeight={"bold"}>{option.layout_total_distance}</Typography>
                {" ft"}
                {" • "}
                <Typography fontWeight={"bold"}>{option.num_holes}</Typography>
                {" holes"}
            </Typography>
        </Card>
    );
}
