import { baseStore } from "./base-store";
import { medicinesStore } from "./medicines-store";
import { suppliesStore } from "./suplies-store";
import { trainningStore } from "./trainning-store";

class RootStore {
    baseStore = baseStore;
    medicinesStore = medicinesStore;
    suppliesStore = suppliesStore;
    trainningStore = trainningStore;
}

export const rootStore = new RootStore();