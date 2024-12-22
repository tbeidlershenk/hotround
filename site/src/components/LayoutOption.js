import * as React from "react";
import Grid from "@mui/joy/Grid";
import Typography from "@mui/joy/Typography";
import Autocomplete from "@mui/joy/Autocomplete";
import { createFilterOptions } from "@mui/material/Autocomplete";
import Button from "@mui/joy/Button";
import Input from "@mui/joy/Input";
import { Box } from "@mui/joy";
import Card from "@mui/joy/Card";
import ListItem from "@mui/joy/ListItem";

export default function LayoutOption({ option }) {
    return (
        <Card>
            <Typography variant="h6">{option.layout_name}</Typography>
            <Typography>
                {"Par "}
                <Typography fontWeight={"bold"}>{option.layout_par}</Typography>
            </Typography>
            <Typography>
                <Typography fontWeight={"bold"}>{option.layout_total_distance}</Typography>
                {" ft"}
            </Typography>
            <Typography>
                <Typography fontWeight={"bold"}>{option.num_holes}</Typography>
                {" holes"}
            </Typography>
        </Card>
    );
}
