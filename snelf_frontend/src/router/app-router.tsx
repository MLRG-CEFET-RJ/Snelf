import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { HomePage } from '../pages/home-page';
import { BasePage } from '../pages/base-page';
import { MedicinesPage } from '../pages/medicines-page';
import { TrainningPage } from '../pages/trainning-page';
import { SuppliesPage } from '../pages/supplies-page';
import { FoodPage } from '../pages/food-page';
import { SchoolProductsPage } from '../pages/school-products-page';

export const AppRouter = () => {

    return (
        <Router>
            <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/base" element={<BasePage />} />
                <Route path="/medicines" element={<MedicinesPage />} />
                <Route path="/supplies" element={<SuppliesPage />} />
                <Route path="/training" element={<TrainningPage />} />
                <Route path="/food" element={<FoodPage />} />
                <Route path="/school-products" element={<SchoolProductsPage />} />
            </Routes>
        </Router>
    )
}