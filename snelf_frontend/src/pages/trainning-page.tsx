import { Button, Dialog, DialogActions, DialogContent, DialogTitle, Typography } from "@mui/material"
import { FlexContainer } from "../components/ui/flex-container"
import { useState } from "react";
import { observer } from "mobx-react";
import useStore from "../core/mobx/use-store";

export const TrainningPage = observer(() => {
    const [isOpen, setIsOpen] = useState(false);
    const [file, setFile] = useState<File | undefined>(undefined);
    const { trainningStore } = useStore()

    const handleOpenDialog = () => setIsOpen(true);
    const handleCloseDialog = () => setIsOpen(false);

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];

        if(file) setFile(file);
    }
    
    const handleStartTrainning = () => {
        trainningStore?.startModelTrainning(file, !file );
    }
    
    const handleStopTrainning = () => {
        trainningStore?.stopModelTrainning();
    }   

    return (
        <FlexContainer flexDirection={"column"} alignItems={"center"} gap={2} marginTop={6} marginX={2}>
            <Typography fontWeight={700} fontSize={50}>
                Treinamento do Modelo
            </Typography>
            
            <Typography textAlign={"center"}>
                Clique abaixo para realizar o treinamento do modelo.
                Recomenda-se que novos treinamentos sejam realizados a partir da
                importação de novos dados no banco de dados.
            </Typography>

            <FlexContainer justifyContent={"center"} gap={2}>
                <Button variant="contained" onClick={handleOpenDialog}>TREINAR MODELO</Button>
                <Button variant="contained" onClick={handleStopTrainning}>PARAR TREINAMENTO</Button>
                <Button variant="contained" onClick={handleStartTrainning}>RETOMAR TREINAMENTO</Button>
            </FlexContainer>

            <Dialog open={isOpen} onClose={handleCloseDialog}>
                <DialogTitle>Treinar Modelo</DialogTitle>
                <DialogContent>
                    <input type="file" onChange={handleFileChange} />
                </DialogContent>
                <DialogActions>
                    <Button variant="contained" onClick={handleStartTrainning}>TREINAR MODELO</Button>
                </DialogActions>
            </Dialog>
        </FlexContainer>
    )
})