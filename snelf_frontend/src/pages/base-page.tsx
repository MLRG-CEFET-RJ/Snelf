import { Button, Card, CardActions, CardContent, CardHeader, Dialog, DialogActions, DialogContent, DialogTitle, Typography } from "@mui/material";
import { FlexContainer } from "../components/ui/flex-container";
import { observer } from "mobx-react";
import { useState } from "react";
import { MedicinesService } from '../core/services/medicines.service';

const mediceServiceInstance = new MedicinesService();

export const BasePage = observer(() => {
    const [file, setFile] = useState<File | null>(null);
    const [errorMessage, setErrorMessage] = useState<string | null>(null);
    const [isOpen, setIsOpen] = useState<boolean>(true);

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
        setFile(event.target.files?.[0] || null);
        setErrorMessage(null);
    };

    const importFile = async (event: React.MouseEvent<HTMLButtonElement>): Promise<void> => {
        event.preventDefault();
        if (!file) {
            setErrorMessage('Por favor, selecione um arquivo antes de importar.');
            return;
        }
        try {
            await mediceServiceInstance.importFile(file);
            setIsOpen(false);
        } catch (error) {
            console.error("Erro ao importar o arquivo:", error);
            setErrorMessage('Ocorreu um erro ao importar o arquivo. Tente novamente.');
            throw error;
        }
    };

    return (
        <FlexContainer sx={{ width: '100%', height: '100%', justifyContent: 'center', alignItems: 'center' }}>
            <Card elevation={10} sx={{ width: { xs: '90%', md: '80%', lg: '70%' } }}>
                <CardHeader 
                    title="Importar Base de Dados de Transações" 
                    subheader="Importe aqui o arquivo CSV contendo a base de dados a ser utilizada para o treinamento do modelo de inferência." 
                />
                <CardContent>
                    <Typography textAlign="center" fontWeight="bold">
                        Arquivo deve conter registros separados por vírgulas, contendo as seguintes colunas:
                    </Typography>
                </CardContent>
                <CardActions sx={{ justifyContent: 'flex-end' }}>
                    <Button variant="contained" onClick={() => setIsOpen(true)}>IMPORTAR</Button>
                </CardActions>
            </Card>

            <Dialog open={isOpen} onClose={() => setIsOpen(false)}>
                <DialogTitle>Importar Base de Dados</DialogTitle>
                <DialogContent>
                    <input type="file" onChange={handleFileChange} />
                    {errorMessage && <Typography color="error">{errorMessage}</Typography>}
                </DialogContent>
                <DialogActions>
                    <Button variant="contained" onClick={importFile}>IMPORTAR</Button>
                </DialogActions>
            </Dialog>
        </FlexContainer>
    );
});
