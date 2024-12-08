import { BASE_URL } from "../../config/config"
import axios, { AxiosInstance } from "axios"

export class SuppliesService {
    private baseUrl: string = `${BASE_URL}/suprimentos`
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
    async getSupplies(search: string, offset: number, limit: number) {
        try {
            const response = await this.axiosInstace.get(
                `/descricao?busca=${search}&offset=${offset}&limit=${limit}`
            )
            return response.data
        } catch (error) {
            throw error
        }
    }

    async importSupplies(csvFile?: File) {
        try {
            const response = await this.axiosInstace.post('/importar-csv-suprimentos', csvFile)
            return response.data
        } catch (error) {
            throw error
        }
    }
}