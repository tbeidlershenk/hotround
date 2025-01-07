import * as React from "react";
import { Box } from "@mui/joy";
import Typography from "@mui/joy/Typography";
import ToggleMode from "./ModeButton";
import HelpButton from "./HelpButton";

export default function Header() {
    return (
        <Box
            sx={{
                display: "flex",
                flexDirection: "row",
                justifyContent: "space-between",
                alignItems: "center",
                width: "100%",
                top: 0,
                px: 1.5,
                py: 1,
                zIndex: 10000,
                backgroundColor: "background.body",
                borderBottom: "1px solid",
                borderColor: "divider",
                position: "sticky",
                marginBottom: 2,
            }}
        >
            <Box
                sx={{
                    display: "flex",
                    flexDirection: "row",
                    alignItems: "center",
                    gap: 1.5,
                }}
            >
                <Typography component="h1" sx={{ fontWeight: "xl" }}>
                    HotRound
                </Typography>
            </Box>
            <Box sx={{ display: "flex", flexDirection: "row", gap: 1 }}>
                <HelpButton />
                <ToggleMode sx={{ alignSelf: "center" }} />
            </Box>
        </Box>
    );
}
