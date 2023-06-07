import axios from "axios";
import {environments} from "../configs/environment"

const axiosClient = axios.create({
    baseURL: environments.API_URL,
    headers: {
        "content-type": "application/json",
    },
});

axiosClient.interceptors.request.use(async (config) => {
    return config;
});

axiosClient.interceptors.response.use(
    (response) => {
        if (response && response.data) {
            return response.data;
        }
        return response;
    },
    async (error) => {
        throw error;
    }
);

export default axiosClient;
