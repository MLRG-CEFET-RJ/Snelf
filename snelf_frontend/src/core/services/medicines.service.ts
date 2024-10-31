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

    async importMedicines(csvFile: File) {
        const formData = new FormData();
        formData.append("file", csvFile);
        console.log(formData)
        try {
            const response = await axios.post('http://127.0.0.1:8000/medicamentos/importar-csv-medicamentos', csvFile, {
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