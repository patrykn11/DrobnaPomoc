import api from "../../../shared/api/api";

const AuthService = {
    loginUser: async (username, password) => {
        try {
            const response = await api.post("/accounts/login/", {
                username,
                password
            });

            return response.data;
        } catch (error) {
            console.error("Błąd logowania:", error.response?.data || error.message);
            throw error;
        }
    },

    registerUser: async (formData) => {
        try {
            const response = await api.post("/accounts/register/", formData);
            return response.data;
        } catch (error) {
            console.error("Błąd rejestracji:", error.response?.data || error.message);
            throw error;
        }
    },

    getCurrentUser: async () => {
        try {
            const response = await api.get("/accounts/me/");
            return response.data;
        } catch (error) {
            console.error("Błąd pobierania użytkownika:", error.response?.data || error.message);
            throw error;
        }
    },

    logoutUser: async () => {
        const refreshToken = localStorage.getItem("refreshToken");

        if (!refreshToken) {
            return;
        }

        try {
            await api.post("/accounts/logout/", {
                refresh: refreshToken
            });
        } catch (error) {
            console.error("Błąd wylogowania:", error.response?.data || error.message);
            throw error;
        }
    },

    saveTokens: (tokens) => {
        localStorage.setItem("accessToken", tokens.access);
        localStorage.setItem("refreshToken", tokens.refresh);
    },

    clearTokens: () => {
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
    },

    hasSession: () => {
        return Boolean(localStorage.getItem("refreshToken"));
    }
};

export default AuthService;
