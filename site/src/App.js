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
                <Tabs aria-label="Basic tabs" defaultValue={0} sx={{ flex: 1 }}>
                    <TabList>
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
                                backgroundColor: "background.body",
                                position: "sticky",
                            }}
                        >
                            <Box sx={{ display: "flex", flexDirection: "row", gap: 1 }}>
                                <Tab>Round Rating</Tab>
                                <Tab>Layout Search</Tab>
                            </Box>
                            <Box sx={{ display: "flex", flexDirection: "row", gap: 1 }}>
                                <HelpButton />
                                <ModeButton sx={{ alignSelf: "center" }} />
                            </Box>
                        </Box>
                    </TabList>
                    <TabPanel value={0}>
                        <RatingCalculator courseOptions={courseOptions} />
                    </TabPanel>
                    <TabPanel value={1}>
                        <LayoutSearch courseOptions={courseOptions} />
                    </TabPanel>
                </Tabs>
                <Footer />
            </Box>
        </CssVarsProvider>
    );
}

export default App;
