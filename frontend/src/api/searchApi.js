import axios from "axios";

const API_BASE = "http://localhost:8000/api";

export async function searchBusiness(payload) {
  const { data } = await axios.post(`${API_BASE}/search`, payload);
  return data;
}