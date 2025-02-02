import { makeObservable, observable, action, runInAction } from "mobx";
import { MedicinesService } from "../../core/services/medicines.service";
import { FilterType } from "../../types/types";

class MedicinesStore {
  rows: string[][] = [];
  rowsCount: number | undefined;
  isLoading: boolean = false;
  error: string | null = null;
  limit: number = 10;
  offset: number = 0;
  status: string | null = null;
  columns: string[] = [];
  private baseService: MedicinesService;
  clean: string | null = null;
  descricaoProduto: string | null = null;
  unidadeComercial: string | null = null;
  valorUnitarioComercial: string | null = null;

  constructor() {
    makeObservable(this, {
      rows: observable,
      rowsCount: observable,
      isLoading: observable,
      error: observable,
      limit: observable,
      offset: observable,
      status: observable,
      columns: observable,
      clean: observable,
      descricaoProduto: observable,
      unidadeComercial: observable,
      valorUnitarioComercial: observable,
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

  setClean = (clean: string) => {
    this.clean = clean
  }

  setDescricaoProduto = (descricaoProduto: string) => {
    this.clean = descricaoProduto
  }

  setUnidadeComercial = (unidadeComercial: string) => {
    this.clean = unidadeComercial
  }

  setValorUnitarioComercial = (valorUnitarioComercial: string) => {
    this.clean = valorUnitarioComercial
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

  setRowsCount = (rowsCount: number) => {
    this.rowsCount = rowsCount;
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

  loadTableRows = async (
    filters: FilterType,
    offset: number = 0,
    limit: number = 10
  ) => {
    this.setLoading(true);
    this.setError(null);

    this.setRows([]);

    try {
      const response = await this.baseService.consultarMedicamentos(
        filters,
        offset,
        limit
      );
      console.log(response)
      this.quantidadeRegistros()
      runInAction(() => {
        this.setRows(response);
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
      await this.baseService.importFile(csvFile);
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

  quantidadeRegistros = async () => {
    const qtdRegistros = await this.baseService.totalRegistros();
    runInAction(() => {
      this.setRowsCount(qtdRegistros);
    });
    return;
  };
}

export const medicinesStore = new MedicinesStore();
