import React, { useState } from "react";
import Box from "@mui/joy/Box";
import Button from "@mui/joy/Button";
import Typography from "@mui/joy/Typography";

export default function Pagination({ count, onPageForward, onPageBackward }) {
    return (
        <Box
            sx={{
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                gap: 1,
                padding: 2,
            }}
        >
            <Button variant="solid" onClick={onPageBackward}>
                Prev
            </Button>
            <Button variant="solid" onClick={onPageForward}>
                Next
            </Button>
        </Box>
    );
}
