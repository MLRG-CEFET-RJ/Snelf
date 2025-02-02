import useStore from "../../core/mobx/use-store";
import { FilterType } from "../../types/types";
import { Button, TextField } from "@mui/material";
import { Controller, SubmitHandler, useForm } from "react-hook-form";

export const MedicinesFilters = () => {
  const { medicinesStore } = useStore();
  const {
    setClean,
    setDescricaoProduto,
    setUnidadeComercial,
    setValorUnitarioComercial,
  } = medicinesStore;
  const { control, handleSubmit } = useForm<FilterType>({
    defaultValues: {
      clean: "",
      descricaoProduto: "",
      unidadeComercial: "",
      valorUnitarioComercial: "",
    },
  });

  const onSubmit: SubmitHandler<FilterType> = async (data) => {
    setClean(data.clean);
    setDescricaoProduto(data.descricaoProduto);
    setUnidadeComercial(data.unidadeComercial);
    setValorUnitarioComercial(data.valorUnitarioComercial);
    await medicinesStore.loadTableRows(data);
  };

  return (
    <form
      onSubmit={handleSubmit(onSubmit)}
      style={{
        display: "flex",
        justifyContent: "space-between",
        marginBottom: 20,
      }}
    >
      <div className="input-area" style={{ display: "flex", gap: 10 }}>
        <Controller
          name="clean"
          control={control}
          render={({ field }) => <TextField {...field} label="Clean" />}
        />
        <Controller
          name="descricaoProduto"
          control={control}
          render={({ field }) => <TextField {...field} label="Descrição" />}
        />
        <Controller
          name="unidadeComercial"
          control={control}
          render={({ field }) => <TextField {...field} label="Unidade" />}
        />
        <Controller
          name="valorUnitarioComercial"
          control={control}
          render={({ field }) => (
            <TextField {...field} label="Valor unitário" />
          )}
        />
      </div>

      <Button
        type="submit"
        variant="contained"
        sx={{ justifySelf: "center", alignSelf: "center" }}
      >
        Filtrar
      </Button>
    </form>
  );
};
