import axios from "axios";

const baseURL = import.meta.env.VITE_API_URL || "/api";

const api = axios.create({
    baseURL,
    headers: {
        "Content-Type": "application/json"
    }
});

const refreshApi = axios.create({ baseURL });

api.interceptors.request.use((config) => {
    const accessToken = localStorage.getItem("accessToken");

    if (accessToken) {
        config.headers.Authorization = `Bearer ${accessToken}`;
    }

    return config;
});

api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;
        const refreshToken = localStorage.getItem("refreshToken");

        if (
            error.response?.status !== 401 ||
            !refreshToken ||
            originalRequest._retry ||
            originalRequest.url.includes("/token/refresh/")
        ) {
            return Promise.reject(error);
        }

        originalRequest._retry = true;

        try {
            const response = await refreshApi.post("/token/refresh/", {
                refresh: refreshToken
            });

            const newAccessToken = response.data.access;
            const newRefreshToken = response.data.refresh || refreshToken;

            localStorage.setItem("accessToken", newAccessToken);
            localStorage.setItem("refreshToken", newRefreshToken);
            originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;

            return api(originalRequest);
        } catch (refreshError) {
            localStorage.removeItem("accessToken");
            localStorage.removeItem("refreshToken");
            return Promise.reject(refreshError);
        }
    }
);

export default api;
