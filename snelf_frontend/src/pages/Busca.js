import { Alert, Box, Button, Grid, TextField, Typography, Select, MenuItem } from '@mui/material';
import React from 'react';
import Navbar from '../components/navbar/Navbar';
import { useState } from 'react';
import Resultado from './Resultado';
import LoadingSpinner from './LoadingSpinner';
import {enviroment} from "../enviroment/enviroment";

const CONSULTA_PRODUTO_ENDPOINT = `${enviroment.backend_url}/consultarGrupo`;
const CONSULTA_CLEAN_ENDPOINT = `${enviroment.backend_url}/consultarClean`;

export default function Busca() {
    const [search, setSearch] = useState('');
    const [result, setResult] = useState([]);
    const [isLoading, setIsLoading] = React.useState(false);
    const [resultMessage, setResultMessage] = React.useState();
    const [searchType, setSearchType] = React.useState('selecione');

    const page = 'busca';

    const handleSearchType = (e) => {
        e.preventDefault();
        setSearchType(e.target.value);
    }
    
    const handleSubmit = async (e) => {
        e.preventDefault();
        setResult([]);
        setIsLoading(true);
        let formData = new FormData();
        formData.append("stringBusca", search);
        let chosenType = searchType == 'produto' ? CONSULTA_PRODUTO_ENDPOINT : CONSULTA_CLEAN_ENDPOINT;
        //debugger;
        await fetch(chosenType, {
            method: "POST",
            body: search
        }).then(r => r.json().then(data => ({ status: r.status, body: data })))
            .then(responseData => {
                setIsLoading(false);
                setResult(responseData.body.medicines);

                if (responseData.status === 200) {
                    setResultMessage(<Alert variant='filled' severity='success' onClose={() => { setResultMessage() }}>Consulta realizada com sucesso: Grupo - {responseData.body}.</Alert>);
                } else {
                    setResultMessage(<Alert variant='filled' severity='error' onClose={() => { setResultMessage() }}>Ocorreu um erro na consulta. Código {responseData.status}</Alert>);
                }
            }).catch(error => {
                console.log(error);
            });
    };


    return (
        <div>
            <Navbar />
            <Box p={{ xs: 8, sm: 6, md: 9 }} height='80vh' width='90%' m="auto">
                <Box pb={5}>
                        <Box pt={5} pb={1} textAlign="center">
                            <Typography variant="h3">
                                Busca
                            </Typography>
                        </Box>

                        <Box p={2} pb={8} textAlign="center">
                            <Typography variant="h8">
                                Digite o nome do produto desejado:
                            </Typography>
                        </Box>

                        <div style={{textAlign: 'center'}}>
                            <label style={{margin: '20px'}}>Buscar por</label>
                            <Select
                                value={searchType}
                                defaultValue='selecione'
                                autoWidth
                                onChange={handleSearchType}
                                >
                                <MenuItem value={'selecione'}>Selecione</MenuItem>
                                <MenuItem value={'produto'}>Produto</MenuItem>
                                <MenuItem value={'clean'}>CLEAN</MenuItem>
                            </Select>
                            <div style={{margin: '10px'}}></div>
                        </div>

                        
                        <TextField onChange={(event) => setSearch(event.target.value)} fullWidth label="Insira o nome do produto" id="fullWidth" />

                        <Box pt={7}>
                            <Grid style={{textAlign: "-webkit-center"}} item>
                                <Button component="label" type="submit" onClick={handleSubmit} disabled={search == '' || ['selecione', ''].includes(searchType)} variant="contained">
                                    Buscar
                                </Button>
                            </Grid>
                        </Box>
                {isLoading ? <LoadingSpinner /> : result.length != 0 ? <Resultado resultados={result} stringBusca={search} tipoBusca={searchType} /> : <div></div> }

                </Box>
            </Box>
        </div>
    )
}
