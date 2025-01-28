import useStore from "../core/mobx/use-store";
import { observer } from "mobx-react-lite";
import { TableComponent } from "../components/table";
import { MedicinesFilters } from "../components/medicines-filters/medicines-filter";
import { useEffect } from "react";

export const MedicinesPage = observer(() => {
  const { medicinesStore } = useStore();
  const { rows, columns, offset, limit, rowsCount, setOffset, setLimit } =
    medicinesStore || {};
  const onPageChange = async (page: number) => {
    await medicinesStore.loadTableRows(
      {
        clean: "",
        descricaoProduto: "",
        unidadeComercial: "",
        valorUnitarioComercial: "",
      },
      offset,
      limit
    );
    setOffset?.(page);
  };

  useEffect(() => {
    const fetch = async () => {
      await medicinesStore.loadTableRows(
        {
          clean: "",
          descricaoProduto: "",
          unidadeComercial: "",
          valorUnitarioComercial: "",
        },
        offset,
        limit
      );
    };

    fetch();
  }, [offset, limit]);

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
        <TableComponent
          columns={columns || []}
          rows={rows || []}
          rowsCount={rowsCount ? Math.ceil(rowsCount / limit) : 0}
          offset={offset}
          limit={limit}
          onPageChange={(newOffset) => onPageChange(newOffset)}
          onRowsPerPageChange={(newLimit) => setLimit?.(newLimit)}
        />
      </div>
    </div>
  );
});
