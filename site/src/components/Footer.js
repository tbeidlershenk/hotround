import * as React from "react";
import { Box, IconButton } from "@mui/joy";
import Typography from "@mui/joy/Typography";
import Link from "@mui/joy/Link";

export default function FooterSection() {
    return (
        <Box
            sx={{
                display: "flex",
                flexDirection: "row",
                justifyContent: "right",
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
                marginTop: 2,
            }}
        >
            <Typography>
                <Link href="https://github.com/tbeidlershenk" target="_blank" sx={{ mx: 1 }}>
                    GitHub
                </Link>
            </Typography>
            <Typography>
                <Link href="https://tbeidlershenk.github.io" target="_blank" sx={{ mx: 1 }}>
                    My Website
                </Link>
            </Typography>
        </Box>
    );
}
