import { makeObservable, observable, action, runInAction } from "mobx";
import { SearchType } from "../../types/enums";
import { MedicinesService } from "../../core/services/medicines.service";

class MedicinesStore {
    rows: string[][] = [];
    isLoading: boolean = false;
    error: string | null = null;
    limit: number = 10;
    offset: number = 0;
    status: string | null = null;
    columns: string[] = [];
    private baseService: MedicinesService;

    constructor() {
        makeObservable(this, {
            rows: observable,
            isLoading: observable,
            error: observable,
            limit: observable,
            offset: observable,
            status: observable,
            columns: observable,
            setError: action,
            setLoading: action,
            setStatus: action,
            setRows: action,
            setColumns: action,
            setOffset: action,
            setLimit: action,
            loadTableRows: action,
            importMedicinesCsv: action,
        });

        this.baseService = new MedicinesService();
    }

    setLoading = (isLoading: boolean) => {
        this.isLoading = isLoading;
    };

    setError = (error: string | null) => {
        this.error = error;
    };

    setStatus = (status: string | null) => {
        this.status = status;
    };

    setRows = (rows: string[][]) => {
        this.rows = rows;
    };

    setColumns = (nextColumns: string[]) => {
        this.columns = nextColumns;
    };

    setOffset = (offset: number) => {
        this.offset = offset;
    };

    setLimit = (limit: number) => {
        this.limit = limit;
    };

    loadTableRows = async (searchType: SearchType, search: string, offset: number, limit: number) => {
        this.setLoading(true);
        this.setError(null);
        let response: any = null;
        try {
            switch (searchType) {
                case SearchType.CLEAN:
                    response = await this.baseService.consultByClean(search, offset, limit);
                    break;
                case SearchType.GROUP:
                    response = await this.baseService.consultByGroup(search, offset, limit);
                    break;
            }
            runInAction(() => {
                this.setRows(response.medicamentos);
            });
        } catch (error) {
            runInAction(() => {
                this.setError("Erro ao carregar os dados da tabela.");
            });
        } finally {
            runInAction(() => {
                this.setLoading(false);
            });
        }
    };

    importMedicinesCsv = async (csvFile: File) => {
        this.setLoading(true);
        this.setError(null);
        try {
            await this.baseService.importMedicines(csvFile);
            runInAction(() => {
                this.setStatus("CSV de medicamentos importado com sucesso.");
            });
        } catch (error) {
            runInAction(() => {
                this.setError("Erro ao importar CSV de medicamentos.");
            });
        } finally {
            runInAction(() => {
                this.setLoading(false);
            });
        }
    };
}

export const medicinesStore = new MedicinesStore();