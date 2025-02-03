import { FilterType } from "../../types/types";
import { BASE_URL } from "../../config/config";
import axios, { AxiosInstance } from "axios";

export class SchoolProductsService {
  private baseUrl = `${BASE_URL}/`;
  private axiosInstace: AxiosInstance;

  constructor() {
    this.axiosInstace = axios.create({
      baseURL: this.baseUrl,
      headers: {
        "Content-Type": "application/json",
        "ngrok-skip-browser-warning": "true",
      },
    });
  }

  async importFile(file: File): Promise<any> {
    try {
      const formData = new FormData();
      formData.append("file", file);
      const response = await this.axiosInstace.post(
        `${this.baseUrl}base/import-file`,
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  async consultarProdutosEscolares(
    filters: FilterType,
    offset: number,
    limit: number
  ): Promise<any> {
    try {
      const response = await this.axiosInstace.get(
        `/produtos-escolares/buscar-produtos?offset=${offset}&limit=${limit}`,
        { params: filters }
      );
      console.log(response.data);
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  async totalRegistros(filters: FilterType): Promise<any> {
    const response = await this.axiosInstace.get(
      "/produtos-escolares/quantidade-resgistros",
      { params: filters }
    );
    return response.data;
  }
}
