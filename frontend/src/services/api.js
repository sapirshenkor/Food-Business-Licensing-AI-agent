import axios from "axios";

// My FastAPI backend URL
const BASE_URL = "http://localhost:8000/api";

const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// API service functions
export const businessLicensingAPI = {
  submitSurvey: async (surveyData) => {
    try {
      console.log("🚀 Sending survey data:", surveyData);

      const response = await api.post("/survey/submit", surveyData);

      console.log("✅ Survey response received:", response.data);
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      console.error("❌ Survey submission failed:", error);

      return {
        success: false,
        error: error.response?.data?.detail || "שגיאה בשליחת הטופס",
        status: error.response?.status,
      };
    }
  },

  // Get system health (test connection)
  getHealth: async () => {
    try {
      const response = await api.get("/health");
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      console.error("❌ Health check failed:", error);
      return {
        success: false,
        error: "לא ניתן להתחבר לשרת",
      };
    }
  },

  // Test API connection
  testConnection: async () => {
    try {
      console.log("🔍 Testing API connection...");

      const response = await api.get("/survey/test");

      console.log("✅ API connection successful:", response.data);
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      console.error("❌ API connection test failed:", error);
      return {
        success: false,
        error: "לא ניתן להתחבר לשרת",
      };
    }
  },
};

export const { submitSurvey, getHealth, testConnection } = businessLicensingAPI;

export default businessLicensingAPI;
