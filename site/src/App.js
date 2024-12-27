import * as React from "react";
import { Box } from "@mui/joy";
import Header from "./components/Header";
import { CssVarsProvider } from "@mui/joy/styles";
import CssBaseline from "@mui/joy/CssBaseline";
import Footer from "./components/Footer";
import theme from "./components/Theme";
import RatingCalculator from "./RatingCalculator";
import LayoutSearch from "./LayoutSearch";
import HelpButton from "./components/HelpButton";
import ModeButton from "./components/ModeButton";
import Tab from "@mui/joy/Tab";
import TabList from "@mui/joy/TabList";
import TabPanel from "@mui/joy/TabPanel";
import Tabs from "@mui/joy/Tabs";

function App() {
    const [courseOptions, setCourseOptions] = React.useState([]);

    React.useEffect(() => {
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
