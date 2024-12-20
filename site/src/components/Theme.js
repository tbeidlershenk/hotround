import { extendTheme } from "@mui/joy/styles";

const theme = extendTheme({
    focus: {
        border: "2px solid",
        borderColor: "primary.main",
    },
    colorSchemes: {
        dark: {
            palette: {
                primary: {
                    plainBg: "#008E6F",
                    plainHoverBg: "#007259",
                    solidBg: "#008E6F",
                    solidHoverBg: "#007259",
                    outlinedBorder: "#008E6F",
                    outlinedColor: "white",
                },
            },
        },
        light: {
            palette: {
                primary: {
                    plainBg: "#008E6F",
                    plainHoverBg: "#007259",
                    solidBg: "#008E6F",
                    solidHoverBg: "#007259",
                    outlinedBorder: "#008E6F",
                    outlinedColor: "black",
                },
            },
        },
    },
});

export default theme;
