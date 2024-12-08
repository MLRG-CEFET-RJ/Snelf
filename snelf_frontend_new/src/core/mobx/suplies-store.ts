import { makeObservable, observable, action, runInAction } from "mobx";
import { SuppliesService } from "../services/supplies.service";

class SuppliesStore {
    rows: string[][] = [];
    isLoading: boolean = false;
    limit: number = 10;
    offset: number = 0;
    search: string = "";
    error: string | null = null;
    status: string | null = null;
    columns: string[] = [];
    private baseService: SuppliesService

    constructor() {
        makeObservable(this, {
            rows: observable,
            columns: observable,
            error: observable,
            isLoading: observable,
            status: observable,
            limit: observable,
            offset: observable,
            search: observable,
            setError: action,
            setLoading: action,
            setStatus: action,
            setRows: action,
            setColumns: action,
            setSearch: action,
            setOffset: action,
            setLimit: action,
        });

        this.baseService = new SuppliesService();
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

    setSearch = (search: string) => {
        this.search = search;
    };

    setOffset = (offset: number) => {
        this.offset = offset;
    };

    setLimit = (limit: number) => {
        this.limit = limit;
    };

    loadTableRows = async (search: string, offset: number, limit: number) => {
        this.setLoading(true);
        try {
            const response = await this.baseService.getSupplies(search, offset, limit);
            runInAction(() => {
                this.setRows(response.suprimentos);
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

    importSuppliesCsv = async (csvFile?: File) => {
        this.setLoading(true);
        this.setError(null);
        try {
            await this.baseService.importSupplies(csvFile);
            runInAction(() => {
                this.setStatus("CSV de suprimentos importado com sucesso.");
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

export const suppliesStore = new SuppliesStore();