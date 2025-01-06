import * as React from "react";
import { useColorScheme } from "@mui/joy/styles";
import IconButton from "@mui/joy/IconButton";
import DarkModeRoundedIcon from "@mui/icons-material/DarkModeRounded";
import LightModeIcon from "@mui/icons-material/LightMode";

export default function ModeButton(props) {
    const { onClick, sx, ...other } = props;
    const { mode, setMode } = useColorScheme();
    const [mounted, setMounted] = React.useState(false);
    React.useEffect(() => {
        setMode("dark");
        setMounted(true);
    }, []);
    if (!mounted) {
        return <IconButton size="sm" variant="outlined" color="neutral" {...other} sx={sx} disabled />;
    }
    return (
        <IconButton
            data-screenshot="toggle-mode"
            size="sm"
            variant="outlined"
            color="neutral"
            {...other}
            onClick={(event) => {
                if (mode === "light") {
                    setMode("dark");
                } else {
                    setMode("light");
                }
                onClick?.(event);
            }}
            sx={[
                mode === "dark" ? { "& > *:first-of-type": { display: "none" } } : { "& > *:first-of-type": { display: "initial" } },
                mode === "light" ? { "& > *:last-of-type": { display: "none" } } : { "& > *:last-of-type": { display: "initial" } },
                ...(Array.isArray(sx) ? sx : [sx]),
            ]}
        >
            <DarkModeRoundedIcon />
            <LightModeIcon />
        </IconButton>
    );
}
