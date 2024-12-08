import { useContext } from 'react';

import { StoreContext } from './store-context';

export default function useStore() {
  return useContext(StoreContext);
}