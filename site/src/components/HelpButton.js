import * as React from "react";
import IconButton from "@mui/joy/IconButton";
import { Help } from "@mui/icons-material";
import { Modal, Box, Typography } from "@mui/joy";

export default function HelpButton(props) {
    const [open, setOpen] = React.useState(false);
    const handleHelpToggle = () => setOpen(!open);

    return (
        <IconButton data-screenshot="toggle-mode" size="sm" variant="outlined" color="neutral" onClick={handleHelpToggle}>
            <Modal open={open} onClose={handleHelpToggle} sx={{ display: "flex", alignItems: "center", justifyContent: "center" }}>
                <Box sx={{ p: 2, backgroundColor: "background.body", borderRadius: 10, width: "70vw" }}>
                    <Typography variant="h4" component="h1" sx={{ color: "#008E6F" }}>
                        HotRound
                    </Typography>
                    <Typography sx={{ mt: 2, mb: 2 }}>
                        HotRound is a round rating calculator, to get ratings for your casual or practice rounds, just like you would in a
                        sanctioned PDGA tournament!
                    </Typography>
                    <Typography variant="h5" component="h2" sx={{ color: "#008E6F" }}>
                        How to use
                    </Typography>
                    <Typography sx={{ mt: 2, mb: 2 }}>
                        Query for a course by name, select the layout you played (using generated keywords, par, distance, and number of
                        holes), and enter your score.
                    </Typography>
                    <Typography variant="h5" component="h2" sx={{ color: "#008E6F" }}>
                        How it works
                    </Typography>
                    <Typography sx={{ mt: 2, mb: 2 }}>
                        HotRound aggregates similar layouts by utilizing layout name, hole length and total par, then extrapolates to your
                        score.
                    </Typography>
                    <Typography sx={{ mt: 2, mb: 2 }}>
                        The tool is driven by a database of PDGA sanctioned rounds. To see the rounds used to calculate your score, click
                        the links in the table.
                    </Typography>
                    <Typography>
                        The database is not exhaustive and therefore may not contain data for every course and layout. In addition, courses
                        without PDGA sanctioned tournaments cannot be rated.
                    </Typography>
                </Box>
            </Modal>
            <Help></Help>
        </IconButton>
    );
}
