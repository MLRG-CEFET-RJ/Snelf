import { BASE_URL } from '../../config/config'
import axios, { AxiosInstance } from 'axios'

export class BaseService {
    private baseUrl: string = BASE_URL
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

    getColumns() {
        try {
            return this.axiosInstace.get(`/obter-colunas`)
        } catch (error) {
            throw error
        }
    }
}