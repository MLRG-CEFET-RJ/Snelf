import useStore from "../core/mobx/use-store";
import { observer } from "mobx-react-lite";
import { MedicinesFilters } from "../components/medicines-filters/medicines-filter";
import { useEffect } from "react";
import Table from "../components/table";

export const SchoolProductsPage = observer(() => {
  const { schoolProductsStore } = useStore();
  const {
    rows,
    columns,
    offset,
    limit,
    rowsCount,
    setOffset,
    setLimit,
    clean,
    descricaoProduto,
    unidadeComercial,
    valorUnitarioComercial,
  } = schoolProductsStore || {};

  // Função para transformar os objetos em arrays de strings
  const transformRows = (rows: any) => {
    if (!rows || !Array.isArray(rows)) return [];
    return rows.map(row => [
      row.CodigoNFe?.toString() || "", // Exemplo de campo
      row.DataEmissao || "",           // Exemplo de campo
      row.MunicipioEmitente || "",     // Exemplo de campo
      row.unidadecomercial || "",      // Exemplo de campo
      row.quantidadecomercial?.toString() || "", // Exemplo de campo
      // Adicione outros campos conforme necessário
    ]);
  };

  useEffect(() => {
    const fetch = async () => {
      await schoolProductsStore.loadTableRows(
        {
          clean: clean,
          descricaoProduto: descricaoProduto,
          unidadeComercial: unidadeComercial,
          valorUnitarioComercial: valorUnitarioComercial,
        },
        offset,
        limit
      );
    };
    console.log('useEffect', rows);
    fetch();
  }, [
    offset,
    limit,
    clean,
    descricaoProduto,
    unidadeComercial,
    valorUnitarioComercial,
  ]);

  const handleChangePage = (_event: unknown, newPage: number) => {
    setOffset(newPage * limit);
  };

  const handleChangeRowsPerPage = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setLimit(parseInt(event.target.value, 10));
    setOffset(0);
  };

  // Transforma as rows antes de passar para o componente Table
  const transformedRows = transformRows(rows);

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
          rows={transformedRows} // Passa as rows transformadas
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