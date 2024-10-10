import { observer } from "mobx-react";
import { useForm, SubmitHandler, Controller } from "react-hook-form";
import { Button, FormControl, Grid, InputLabel, MenuItem, Select, TextField } from "@mui/material";
import { useEffect } from "react";
import { SearchType } from "../types/enums";

interface FormProps {
    loadTableRows: any
    filters: string[]
    limit: number;
    offset: number;
}

type Inputs = {
    filter: string;
    field: string;
};

export const Form = observer(({ loadTableRows, filters, limit, offset }: FormProps) => {
    const {
        register,
        control,
        handleSubmit,
        formState: { errors },
    } = useForm<Inputs>({
        defaultValues: {
            filter: filters[0],
            field: "",
        },
    });

    const onSubmit: SubmitHandler<Inputs> = (data) => {
        // mudar isso ja to louco da cabeça
        const searchType = [SearchType.CLEAN, SearchType.GROUP].includes(data.filter as SearchType)
        if (searchType) {
            return loadTableRows(data.filter as SearchType, data.field, offset, limit);
        }
        return loadTableRows(data.field, offset, limit)
    }

    return (
        <form onSubmit={handleSubmit(onSubmit)}>
            <Grid
                container
                flexDirection={{ xs: "column", md: "row" }}
                justifyContent={{ md: "space-between" }}
                alignItems={{ xs: "center" }}
                spacing={{ xs: 3, md: 1 }}
            >
                <Grid item xs={4}>
                    <Controller
                        name="filter"
                        control={control}
                        render={({ field }) => (
                            <FormControl fullWidth>
                                <InputLabel>Filtro</InputLabel>
                                <Select {...register("filter")} {...field}>
                                    {filters.map((filter) => (
                                        <MenuItem key={filter} value={filter}>
                                            {filter}
                                        </MenuItem>
                                    ))}
                                </Select>
                            </FormControl>
                        )}
                    />
                </Grid>
                <Grid item xs={6}>
                    <Controller
                        name="field"
                        control={control}
                        render={({ field }) => (
                            <FormControl fullWidth>
                                <TextField
                                    {...register("field", { required: true })}
                                    {...field}
                                    required
                                    error={!!errors?.field}
                                    label="Pesquise aqui"
                                    variant="outlined"
                                />
                            </FormControl>
                        )}
                    />
                </Grid>
                <Grid item xs={2}>
                    <Button type="submit" variant="contained" fullWidth>
                        Buscar
                    </Button>
                </Grid>
            </Grid>
        </form>
    )
});