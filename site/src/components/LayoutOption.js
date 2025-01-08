import * as React from "react";
import Typography from "@mui/joy/Typography";
import Card from "@mui/joy/Card";

export default function LayoutOption({ layout }) {
    return (
        <Card variant="outlined" sx={{ padding: 2, flex: 1 }}>
            <Typography variant="h6">{layout.descriptive_name}</Typography>
            <Typography>
                {"Par "}
                <Typography fontWeight={"bold"}>{layout.total_par}</Typography>
                {" • "}
                <Typography fontWeight={"bold"}>{layout.total_distance}</Typography>
                {" ft"}
                {" • "}
                <Typography fontWeight={"bold"}>{layout.num_holes}</Typography>
                {" holes"}
            </Typography>
            <Typography>Over {layout.num_rounds} rounds</Typography>
        </Card>
    );
}
