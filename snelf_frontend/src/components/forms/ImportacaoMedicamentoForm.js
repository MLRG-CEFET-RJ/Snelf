import * as React from 'react';
import { Alert, Box, Button, Grid, Paper, Typography } from '@mui/material';
import UploadFileIcon from "@mui/icons-material/UploadFile";
import LoadingSpinner from '../../pages/LoadingSpinner';
import {enviroment} from "../../enviroment/enviroment";

// const IMPORTACAO_ENDPOINT = `${enviroment.backend_url}/importarMedicamentos`;
const IMPORTACAO_ENDPOINT = `${enviroment.backend_url}/importarTransacoes`;

export default function ImportacaoMedicamentoForm() {
    const [csvFile, setCsvFile] = React.useState();
    const [filename, setFilename] = React.useState("");
    const [resultMessage, setResultMessage] = React.useState();
    const [isLoading, setIsLoading] = React.useState(false);

    const handleChange = (e) => {
        if (e.target.files.length) {
            setCsvFile(e.target.files[0]);
            setFilename(e.target.files[0].name);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        let formData = new FormData();
        await formData.append("csvFile", csvFile);
        await fetch(IMPORTACAO_ENDPOINT, {
            method: "POST",
            body: formData,
        })
        .then(r => r.json().then(data => ({ status: r.status, body: data })))
        .then(obj => {
            setIsLoading(false);
            if(obj.status===200){
                setResultMessage(<Alert variant='filled' severity='success' onClose={() => {setResultMessage()}}>CSV Importado com sucesso</Alert>);
            }else{
                setResultMessage(<Alert variant='filled' severity='error' onClose={() => {setResultMessage()}}>Ocorreu um erro na importação do CSV. Código {obj.status}</Alert>);
            }
        });
    };
    
    return (
        <Box p={{ xs: 8, sm: 6, md: 6 }} height='80vh' width='60vh' m="auto">
            {resultMessage}
            <Paper elevation={5}>
                <Box pb={5} m={5}>
                    <Grid
                        container
                        spacing={0}
                        direction="column"
                        rowSpacing={1}
                        alignItems="center"
                    >
                        {isLoading ? <LoadingSpinner /> :  <div></div> }
                        <Box pt={1} pb={1} textAlign="center">
                            <Typography variant="h5">
                                Importar Base de Dados de Medicamentos
                            </Typography>
                        </Box>

                        <Box p={1} pb={5} textAlign="center">
                            <Typography variant="h8">
                                Importe aqui o arquivo CSV contendo a base de dados a ser utilizada para o treinamento do modelo de inferência.
                            </Typography>
                        </Box>
                        <Typography textAlign="center" variant="h8">
                            <div>
                                Arquivo deve conter registros separados por vírgulas, contendo as seguintes colunas:
                            </div>
                            <ul>
                                <li>description</li>
                                <li>ean</li>
                            </ul>
                        </Typography>

                        <Grid item>
                            <Typography variant='h6'>
                                {filename}
                            </Typography>
                        </Grid>

                        <Grid item>
                            <Button component="label" variant="contained" startIcon={<UploadFileIcon />}>
                                Upload CSV
                                <input type="file" accept=".csv" onChange={handleChange} hidden />
                            </Button>
                        </Grid>
                        <Grid item>
                            <Button component="label" variant="contained" type="submit" onClick={handleSubmit}>
                                Importar
                            </Button>
                        </Grid>
                    </Grid>
                </Box>
            </Paper>
        </Box>
    );
}
