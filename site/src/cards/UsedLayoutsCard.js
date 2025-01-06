import Table from "@mui/joy/Table";
import Card from "@mui/joy/Card";
import Link from "@mui/joy/Link";
import Sheet from "@mui/joy/Sheet";

export default function UsedLayoutsCard({ layout_names_and_links }) {
    return (
        <Card variant="outlined" sx={{ flex: 1, padding: 0 }}>
            <Sheet
                sx={(theme) => ({
                    "--TableCell-height": "40px",
                    "--TableHeader-height": "calc(1 * var(--TableCell-height))",
                    height: "calc(10 * var(--TableCell-height))",
                    overflow: "auto",
                    background: `linear-gradient(${theme.vars.palette.background.surface} 30%, rgba(255, 255, 255, 0)),
            linear-gradient(rgba(255, 255, 255, 0), ${theme.vars.palette.background.surface} 70%) 0 100%,
            radial-gradient(
              farthest-side at 50% 0,
              rgba(0, 0, 0, 0.12),
              rgba(0, 0, 0, 0)
            ),
            radial-gradient(
                farthest-side at 50% 100%,
                rgba(0, 0, 0, 0.12),
                rgba(0, 0, 0, 0)
              )
              0 100%`,
                    backgroundSize: "100% 40px, 100% 40px, 100% 14px, 100% 14px",
                    backgroundRepeat: "no-repeat",
                    backgroundAttachment: "local, local, scroll, scroll",
                    backgroundPosition: "0 var(--TableHeader-height), 0 100%, 0 var(--TableHeader-height), 0 100%",
                    backgroundColor: "background.surface",
                })}
            >
                <Table stickyHeader>
                    <thead>
                        <tr>
                            <th style={{ width: "80%" }}>Layout</th>
                            <th style={{ textAlign: "right" }}># Rounds</th>
                        </tr>
                    </thead>
                    <tbody>
                        {layout_names_and_links
                            .sort((a, b) => b.num_rounds - a.num_rounds)
                            .map((x) => (
                                <tr>
                                    <td style={{ width: "80%" }}>
                                        <Link href={x.link}>{x.name}</Link>
                                    </td>
                                    <td style={{ textAlign: "right" }}>{x.num_rounds}</td>
                                </tr>
                            ))}
                    </tbody>
                </Table>
            </Sheet>
        </Card>
    );
}
