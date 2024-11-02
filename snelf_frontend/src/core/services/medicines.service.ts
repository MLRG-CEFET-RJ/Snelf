import { BASE_URL } from '../../config/config'
import axios, { AxiosInstance } from 'axios'

export class MedicinesService {
    private baseUrl: string = `${BASE_URL}/medicamentos`
    private axiosInstace: AxiosInstance
    constructor() { 
        this.axiosInstace = axios.create({ 
            baseURL: this.baseUrl,
            headers: {
                'Content-Type': 'application/json',
                'ngrok-skip-browser-warning': 'true'
            }
        })
    }

    async importMedicines(csvFile: any) {
        console.log("chegou aqui", csvFile)
        const formData = new FormData();
        formData.append("file", csvFile);
        console.log(formData)
        try {
            const response = await this.axiosInstace.post(
                'http://localhost:8000/medicamentos/importar-csv-medicamentos', 
                formData, {
                headers: {
                  "Content-Type": "multipart/form-data",
                },
            })
            console.log(response.data)
            return response.data
       } catch (error) {
           throw error
       }
    }

    async consultByGroup(group: string, offset: number, limit: number) {
        try {
            const response = await this.axiosInstace.get(
                `/consultar-grupo?busca=${group}&offset=${offset}&limit=${limit}`
            )
            return response.data
        } catch (error) {
            throw error
        }
    }

    async consultByClean(clean: string, offset: number, limit: number) {
        try {
            const response = await this.axiosInstace.get(
                `/consultar-clean?busca=${clean}&offset=${offset}&limit=${limit}`
            )
            return response.data
        } catch (error) {
            throw error
        }
    }
}