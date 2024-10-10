import { Form } from '../components/form';
import useStore from '../core/mobx/use-store';
import { Grid } from '@mui/material';
import { observer } from 'mobx-react-lite';
import { TableComponent } from '../components/table';
import { SearchType } from '../types/enums';

export const MedicinesPage = observer(() => {
  const { medicinesStore } = useStore()
  const filters: SearchType[] = [SearchType.CLEAN, SearchType.GROUP]
  const {
    rows,
    columns,
    offset,
    limit,
    setOffset,
    setLimit,
    loadTableRows,
  } = medicinesStore || {};

  console.log(rows)

  return (
    <Grid container justifyContent={"center"} gap={2} marginY={10}>
      <Grid item xs={12} marginX={10}>
        <Form loadTableRows={loadTableRows}  filters={filters} limit={limit} offset={offset} />
      </Grid>
      <Grid item xs={12} marginX={10}>
        <TableComponent
          columns={columns || []}
          rows={rows || []}
          offset={offset ?? 0}
          limit={limit ?? 10}
          onPageChange={(newOffset) => setOffset?.(newOffset)}
          onRowsPerPageChange={(newLimit) => setLimit?.(newLimit)}
        />
      </Grid>
    </Grid>
  );
});
