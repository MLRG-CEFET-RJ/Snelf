import useStore from "../core/mobx/use-store";
import { observer } from "mobx-react-lite";
import { TableComponent } from "../components/table";
import { MedicinesFilters } from "../components/medicines-filters/medicines-filter";

export const MedicinesPage = observer(() => {
  const { medicinesStore } = useStore();
  const { rows, columns, offset, limit, setOffset, setLimit } =
    medicinesStore || {};

  return (
    <div
      style={{
        width: "1700px",
        marginTop: 100,
        marginLeft: "auto",
        marginRight: "auto",
      }}
    >
      <MedicinesFilters />
      <TableComponent
        columns={columns || []}
        rows={rows || []}
        offset={offset}
        limit={limit}
        onPageChange={(newOffset) => setOffset?.(newOffset)}
        onRowsPerPageChange={(newLimit) => setLimit?.(newLimit)}
      />
    </div>
  );
});
