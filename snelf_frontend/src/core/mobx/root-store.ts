import { baseStore } from "./base-store";
import { medicinesStore } from "./medicines-store";
import { suppliesStore } from "./suplies-store";
import { trainningStore } from "./trainning-store";
import { foodStore } from "./food-store";
import { schoolProductsStore } from "./school-produtcs-store";

class RootStore {
    baseStore = baseStore;
    medicinesStore = medicinesStore;
    suppliesStore = suppliesStore;
    trainningStore = trainningStore;
    foodStore = foodStore;
    schoolProductsStore = schoolProductsStore;
}

export const rootStore = new RootStore();