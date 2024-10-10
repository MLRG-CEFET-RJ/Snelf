import { BASE_URL } from "../../config/config"
import axios, { AxiosInstance } from "axios"

export class TrainningService {
    private baseUrl: string = `${BASE_URL}/treinamento`
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
    async startTrainning(csvFile?: File, forceRestart?: boolean) {
        try {
            const response = await this.axiosInstace.post(
                `/treinamentos/descricao`,
                {
                    csv_file: csvFile,
                    force_restart: forceRestart
                }
            )
            return response.data
        } catch (error) {
            throw error
        }
    }

    async stopTrainning() {
        try {
            const response = await this.axiosInstace.get('/parar-treinamento')
            return response.data
        } catch (error) {
            throw error
        }
    }

    async getTrainningStatus() {
        try {
            const response = await this.axiosInstace.get('/obter-status-treinamento')
            return response.data
        } catch (error) {
            throw error
        }
    }
}