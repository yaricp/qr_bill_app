import axios, { AxiosInstance } from "axios";
import router from "@/router";

const apiClient: AxiosInstance = axios.create({
  baseURL: "http://localhost:8080/api/v1",
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
