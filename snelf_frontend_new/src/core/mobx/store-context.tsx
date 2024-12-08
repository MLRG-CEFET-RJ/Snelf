import React, { createContext, useContext, useRef } from 'react';

import { rootStore } from './root-store'

export type IValueMap = Record<string, unknown>
type RootStoreType = typeof rootStore

export interface ProviderProps extends IValueMap {
  children: React.ReactNode
}

export const StoreContext = createContext<RootStoreType>({} as any)

export function StoreProvider(props: ProviderProps) {
  const { children, ...stores } = props
  const parentValue = useContext(StoreContext)
  const mutableProviderRef = useRef({ ...parentValue, ...stores })
  const value = mutableProviderRef.current

  return <StoreContext.Provider value={value}>{children}</StoreContext.Provider>
}

StoreProvider.displayName = 'StoreProvider'