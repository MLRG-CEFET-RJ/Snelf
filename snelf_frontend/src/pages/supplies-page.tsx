import { Grid } from '@mui/material';
import { observer } from 'mobx-react-lite';

import { Form } from '../components/form';
import { TableComponent } from '../components/table';
import useStore from '../core/mobx/use-store';
import { SuppliesType } from '../types/enums';

export const SuppliesPage = observer(() => {
  const { suppliesStore } = useStore();
  const filters: SuppliesType[] = [SuppliesType.DESCRIPTION];
  const {
    rows,
    columns,
    offset,
    limit,
    setOffset,
    setLimit,
    loadTableRows,
  } = suppliesStore;

  return (
    <Grid container justifyContent={"center"} gap={2} marginY={10}>
      <Grid item xs={12} marginX={10}>
        <Form loadTableRows={loadTableRows} filters={filters} limit={limit} offset={offset} />
      </Grid>
      <Grid item xs={12} marginX={10}>
        <TableComponent
          columns={columns}
          rows={rows}
          offset={offset}
          limit={limit}
          onPageChange={(newOffset) => setOffset(newOffset)}
          onRowsPerPageChange={(newLimit) => setLimit(newLimit)}
        />
      </Grid>
    </Grid>
  );
});