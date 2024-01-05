import type { AxiosInstance } from "axios";
import axios from "axios";

const ApiClient: AxiosInstance = axios.create({
  headers: { 'Content-Type': 'application/json' },
  responseType: 'json',
});

export default ApiClient;
