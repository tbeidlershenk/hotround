import * as React from "react";
import { Box } from "@mui/joy";
import Header from "./components/Header";
import { CssVarsProvider } from "@mui/joy/styles";
import CssBaseline from "@mui/joy/CssBaseline";
import Footer from "./components/Footer";
import theme from "./components/Theme";
import RatingCalculator from "./RatingCalculator";

function App() {
    const [courseOptions, setCourseOptions] = React.useState([]);

    React.useEffect(() => {
        document.title = "HotRound";
        fetch("/api/courses", { method: "GET" })
            .then((response) => response.json())
            .then((data) => {
                setCourseOptions(data);
            })
            .catch((error) => {
                console.error("Error fetching courses:", error);
            });
    }, []);

    return (
        <CssVarsProvider disableTransitionOnChange theme={theme} colorScheme={"dark"}>
            <CssBaseline />
            <Box sx={{ display: "flex", flexDirection: "column", minHeight: "100vh" }}>
                <Header />
                <RatingCalculator courseOptions={courseOptions} />
                <Footer />
            </Box>
        </CssVarsProvider>
    );
}

export default App;
