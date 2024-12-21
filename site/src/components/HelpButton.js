import * as React from "react";
import { useColorScheme } from "@mui/joy/styles";
import IconButton, { IconButtonProps } from "@mui/joy/IconButton";
import DarkModeRoundedIcon from "@mui/icons-material/DarkModeRounded";
import LightModeIcon from "@mui/icons-material/LightMode";
import { Help } from "@mui/icons-material";
import { Modal, Box, Typography } from "@mui/joy";

export default function HelpButton(props) {
    const [open, setOpen] = React.useState(false);
    const handleHelpToggle = () => setOpen(!open);

    return (
        <IconButton data-screenshot="toggle-mode" size="sm" variant="outlined" color="neutral" onClick={handleHelpToggle}>
            <Modal open={open} onClose={handleHelpToggle} sx={{ display: "flex", alignItems: "center", justifyContent: "center" }}>
                <Box sx={{ p: 2, backgroundColor: "background.body", borderRadius: 10, width: "70vw" }}>
                    <Typography variant="h5" component="h2" sx={{ color: "#008E6F" }}>
                        How to use
                    </Typography>
                    <Typography sx={{ mt: 2, mb: 2 }}>
                        Use the search inputs to query by course name, layout name, then enter the your score and click calculate.
                    </Typography>
                    <Typography variant="h5" component="h2" sx={{ color: "#008E6F" }}>
                        How it works
                    </Typography>
                    <Typography sx={{ mt: 2, mb: 2 }}>
                        The calculator aggregates similar layouts by utilizing layout name, hole length and total par, then extrapolates to
                        your score.
                    </Typography>
                    <Typography sx={{ mt: 2, mb: 2 }}>
                        The tool is driven by a database PDGA sanctioned rounds. To see the rounds used to calculate your score, click the
                        links in the table.
                    </Typography>
                </Box>
            </Modal>
            <Help></Help>
        </IconButton>
    );
}
