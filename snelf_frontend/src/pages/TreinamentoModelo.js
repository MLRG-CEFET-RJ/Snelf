import React from 'react'
import Navbar from '../components/navbar/Navbar'
import { Alert, Box, Button, Grid, Typography } from '@mui/material'
import { Link } from 'react-router-dom';
import LoadingSpinner from './LoadingSpinner';
import {enviroment} from "../enviroment/enviroment";
import { useState, useEffect } from 'react';

//const TREINAMENTO_ENDPOINT = `${enviroment.backend_url}/treinarModelo`; 
const TREINAMENTO_ENDPOINT_TREINO = `${enviroment.backend_url}/treinar-modelo-de-verdade`;
const TREINAMENTO_ENDPOINT_STATUS = `${enviroment.backend_url}/obter-status-treinamento`;

export default function TreinamentoModelo() {
    
    const [resultMessage, setResultMessage] = React.useState();
    const [isLoading, setIsLoading] = React.useState(false);
    //const [status, setStatus] = useState(null);
    
    const [statusList, setStatusList] = useState([]);

    const getStatus = async () => {
        try {
            const response = await fetch(TREINAMENTO_ENDPOINT_STATUS);
            const data = await response.json();
            setStatusList(prevList => [...prevList, data]);
        } catch (error) {
            console.error(error);
        }
    };
    
    useEffect(() => {
        const intervalId = setInterval(getStatus, 5000); // chamada à API a cada 5 segundos
        return () => clearInterval(intervalId); // limpa o intervalo ao desmontar o componente
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        try{
                await fetch(TREINAMENTO_ENDPOINT_TREINO , {
                    method: "POST",
                })
                .then(r => r.json().then(data => ({ status: r.status })))
                .then(obj => {
                if(obj.status===200){
                    setResultMessage(<Alert variant='filled' severity='success' onClose={() => {setResultMessage()}}>Treinamento iniciado com sucesso</Alert>);
                }else{
                    setResultMessage(<Alert variant='filled' severity='error' onClose={() => {setResultMessage()}}>Ocorreu um erro no treinamento do modelo. Código {obj.status}</Alert>);
                }
                setIsLoading(false)
                getStatus();
                
            });

        } catch(e) {
            setIsLoading(false);
        }
    };

    return (
        <div>
            <Navbar />
            {isLoading ? (<LoadingSpinner /> ) : 
            (<Box p={{ xs: 8, sm: 6, md: 9 }} height='80vh' width='80vh' m="auto">
                    <Grid
                        container
                        spacing={0}
                        direction="column"
                        rowSpacing={1}
                        alignItems="center"
                    >
                        <Box pt={5} pb={1} textAlign="center">
                            <Typography variant="h3">
                                Treinamento do Modelo
                            </Typography>
                        </Box>

                        <Box p={2} pb={8} textAlign="center">
                            <Typography variant="h8">
                                Clique abaixo para realizar o treinamento do modelo.
                                Recomenda-se que novos treinamentos sejam realizados
                                 a partir da importação de novos dados no banco de dados.
                            </Typography>
                        </Box>

                        <Box pt={7}>
                            <Grid item>
                                <Button component={Link} to={"/"} onClick={handleSubmit} disabled={isLoading} variant="contained">
                                    Treinar Modelo 
                                </Button>
                            </Grid>
                        </Box>
                    </Grid>
                    <br></br><br></br>

                {resultMessage}

                <Box pb={5}>
                {statusList.length > 0 && (
                        <div style={{ borderRadius: "10px", padding: "10px", backgroundColor: "#B0C4DE" }}>
                            <Typography variant="h6">Status:</Typography>
                            {statusList.slice(-3).map((status, index) => (
                                <Typography key={index} variant="body1">{status}</Typography>
                            ))}
                        </div>
                    )}
                        
                </Box>
            </Box>
            )}
        </div>
    );
}
