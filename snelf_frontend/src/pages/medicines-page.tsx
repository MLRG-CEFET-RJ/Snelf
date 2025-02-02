import useStore from "../core/mobx/use-store";
import { observer } from "mobx-react-lite";
import { MedicinesFilters } from "../components/medicines-filters/medicines-filter";
import { useEffect } from "react";
import Table from "../components/table";

export const MedicinesPage = observer(() => {
  const { medicinesStore } = useStore();
  const { rows, columns, offset, limit, rowsCount, setOffset, setLimit, clean, descricaoProduto, unidadeComercial, valorUnitarioComercial } = medicinesStore || {};

  useEffect(() => {
    const fetch = async () => {
      await medicinesStore.loadTableRows(
        {
          clean: clean || "",
          descricaoProduto: descricaoProduto || "",
          unidadeComercial: unidadeComercial || "",
          valorUnitarioComercial: valorUnitarioComercial || "",
        },
        offset,
        limit
      );
    };

    fetch();
  }, [offset, limit, medicinesStore, clean, descricaoProduto, unidadeComercial, valorUnitarioComercial]);

  const handleChangePage = (_event: unknown, newPage: number) => {
    setOffset(newPage * limit);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setLimit(parseInt(event.target.value, 10));
    setOffset(0);
  };

  return (
    <div
      style={{
        width: "100vw",
        display: "flex",
        justifyContent: "center",
      }}
    >
      <div
        style={{
          marginTop: 100,
          width: "80vw",
        }}
      >
        <MedicinesFilters />
        <Table 
          columns={columns} 
          rows={rows} 
          count={rowsCount} 
          offset={offset} 
          limit={limit} 
          handleChangePage={handleChangePage} 
          handleChangeRowsPerPage={handleChangeRowsPerPage}
        />
      </div>
    </div>
  );
});
