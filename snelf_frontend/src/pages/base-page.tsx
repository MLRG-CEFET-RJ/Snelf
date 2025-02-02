import {
  Button,
  Card,
  CardActions,
  CardContent,
  CardHeader,
  Typography,
} from "@mui/material";
import { FlexContainer } from "../components/ui/flex-container";
import { observer } from "mobx-react";
import { useState } from "react";
import { MedicinesService } from "../core/services/medicines.service";

const mediceServiceInstance = new MedicinesService();

export const BasePage = observer(() => {
  const [file, setFile] = useState<File | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const handleFileChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ): void => {
    setFile(event.target.files?.[0] || null);
    setErrorMessage(null);
  };

  const importFile = async (
    event: React.MouseEvent<HTMLButtonElement>
  ): Promise<void> => {
    event.preventDefault();
    if (!file) {
      setErrorMessage("Por favor, selecione um arquivo antes de importar.");
      return;
    }
    try {
      await mediceServiceInstance.importFile(file);
      alert("Arquivo importado com sucesso!");
    } catch (error) {
      console.error("Erro ao importar o arquivo:", error);
      setErrorMessage(
        "Ocorreu um erro ao importar o arquivo. Tente novamente."
      );
    }
  };

  return (
    <FlexContainer
      sx={{
        width: "100%",
        height: "100%",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Card elevation={10} sx={{ width: { xs: "90%", md: "80%", lg: "70%" } }}>
        <CardHeader
          title="Importar Base de Dados de Transações"
          subheader="Importe aqui o arquivo CSV contendo a base de dados a ser utilizada para o treinamento do modelo de inferência."
        />
        <CardContent>
          <Typography textAlign="center" fontWeight="bold">
            Arquivo deve conter registros separados por vírgulas, contendo as
            seguintes colunas:
          </Typography>

          {/* Conteúdo do Modal agora aqui */}
          <CardActions
            sx={{ justifyContent: "center", flexDirection: "column", mt: 3 }}
          >
            <input type="file" onChange={handleFileChange} />
            {errorMessage && (
              <Typography
                color="error"
                sx={{ mt: 1.5, textAlign: "center", fontSize: "0.9rem" }}
              >
                {errorMessage}
              </Typography>
            )}
            <Button
              variant="contained"
              sx={{ mt: 2.5, width: "35%" }}
              onClick={importFile}
            >
              IMPORTAR
            </Button>
          </CardActions>
        </CardContent>
      </Card>
    </FlexContainer>
  );
});
