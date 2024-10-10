import { makeObservable, observable, action, runInAction } from "mobx"
import { BaseService } from "../../core/services/base.service";
import { ProductType } from "../../types/enums";
import { suppliesStore } from "./suplies-store";
import { medicinesStore } from "./medicines-store";

class BaseStore {
    columns: string[] = [];
    type: ProductType = ProductType.MEDICAMENTOS;
    isLoading: boolean = false;
    error: string | null = null;
    status: string | null = null;
    private baseService: BaseService

    constructor() {
        makeObservable(this, {
            columns: observable,
            error: observable,
            isLoading: observable,
            status: observable,
            type: observable,
            setError: action,
            setLoading: action,
            setStatus: action,
            setType: action,
        })

        this.baseService = new BaseService();
        this.loadColumns();
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

    setType = (type: ProductType) => {
        this.type = type;
    };

    async loadColumns() {
        this.setLoading(true);
        this.setError(null);
        try {
            const response = await this.baseService.getColumns();
            const { suprimentos, medicamentos } = response.data
            console.log(suprimentos, medicamentos)
            suppliesStore.setColumns(suprimentos);
            medicinesStore.setColumns(medicamentos);
        } catch (error) {
            runInAction(() => {
                this.setError("Erro ao carregas as colunas.");
            });
        } finally {
            runInAction(() => {
                this.setLoading(false);
            });
        }

    }

}

export const baseStore = new BaseStore();