import axios from "axios"

// Create an instance of axios with the base URL
const api = axios.create({
  baseURL: "https://uyowiwivczuuajwxrhme.supabase.co",
})

// Export the Axios instance
export default api
