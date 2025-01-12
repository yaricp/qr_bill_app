import axios, { AxiosInstance } from "axios";
import { apiUrl, prefixUrl } from '@/env';
import router from "@/router";

const apiClient: AxiosInstance = axios.create({
  baseURL: `${apiUrl}${prefixUrl}`,
  headers: {
    "Content-type": "application/json",
  },
});

export const checkTokenExpired  = (err: any) => {
  if (axios.isAxiosError(err)) {
    if(err.status == 401){
      router.push({ name: 'logout' })
    }
  } else {
    console.error(err);
  } 
}

export default apiClient;
