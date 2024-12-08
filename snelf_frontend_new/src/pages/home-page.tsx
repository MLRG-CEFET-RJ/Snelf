import { Typography } from "@mui/material"
import { FlexContainer } from "../components/ui/flex-container"

export const HomePage = () => {

    return (
        <FlexContainer
            sx={{
                height: '100%',
                justifyContent: 'center',
                alignItems: 'center',
            }}>
            <FlexContainer
                sx={{
                    flexDirection: 'column',
                    justifyContent: 'center',
                    alignItems: 'center',
                    maxWidth: '70%',
                }}>
                <Typography
                    sx={{
                        fontSize: { xs: 50, md: 60, lg: 70 }
                    }}
                >
                    SNELF
                </Typography>
                <Typography
                    sx={{
                        fontSize: { xs: 20, md: 30, lg: 40 },
                        textAlign: 'center'
                    }}
                >
                    O SNELF é uma plataforma para detecção de disparidades de preços em compras públicas. 
                    O objetivo é auxiliar na auditoria de notas fiscais relacionadas a compras, 
                    e verificar possíveis fraudes.
                </Typography>
            </FlexContainer>
        </FlexContainer>
    )
}