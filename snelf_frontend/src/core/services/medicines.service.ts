import { BASE_URL } from '../../config/config';
import axios, { AxiosInstance } from 'axios';

export class MedicinesService {
    private baseUrl = `${BASE_URL}/`;
    private axiosInstace: AxiosInstance;

    constructor() { 
        this.axiosInstace = axios.create({ 
            baseURL: this.baseUrl,
            headers: {
                'Content-Type': 'application/json',
                'ngrok-skip-browser-warning': 'true'
            }
        });
    }

    async importFile(file: File): Promise<any> {
        try {
            const formData = new FormData();
            formData.append("file", file);
            const response = await this.axiosInstace.post(
                `${this.baseUrl}/base/import-file`, formData, 
                { headers: { "Content-Type": "multipart/form-data" }}
            );
            return response.data;
        } catch (error) {
           throw error;
        }
    }

    async consultByGroup(group: string, offset: number, limit: number): Promise<any> {
        try {
            const response = await this.axiosInstace.get(
                `/medicamentos/consultar-grupo?busca=${group}&offset=${offset}&limit=${limit}`
            );
            return response.data;
        } catch (error) {
            throw error;
        }
    }

    async consultByClean(clean: string, offset: number, limit: number): Promise<any> {
        try {
            const response = await this.axiosInstace.get(
                `/medicamentos/consultar-clean?busca=${clean}&offset=${offset}&limit=${limit}`
            );
            return response.data;
        } catch (error) {
            throw error;
        }
    }

    async consultarMedicamentos(type_search: string, target: string, offset: number, limit: number): Promise<any> {
        try {
            const response = await this.axiosInstace.get(
                `/medicamentos/buscar-produtos?type_search=${type_search}&target=${target}&offset=${offset}&limit=${limit}`
            );
            console.log(response.data)
            return response.data;
        } catch (error) {
            throw error;
        }
    }
}