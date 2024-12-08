import { Box, BoxProps } from "@mui/material";
import { ReactNode } from "react"

interface FlexContainerProps extends BoxProps {
    children: ReactNode;
}

export const FlexContainer: React.FC<FlexContainerProps> = (props) => {
    return (
        <Box display="flex" {...props}>
            {props.children}
        </Box>
    )
}
