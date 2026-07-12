import axios from "axios";
import { logger } from "../utils/logger";

const API_BASE = "http://localhost:8000/api";

export async function searchBusiness(payload) {
  logger.info("Search request →", payload);
  const start = performance.now();

  try {
    const { data } = await axios.post(`${API_BASE}/search`, payload);
    const elapsed = (performance.now() - start).toFixed(0);

    logger.success(`Search complete in ${elapsed}ms`, {
      website: data?.business?.website,
      social: data?.social_media?.length ?? 0,
      reviews: data?.reviews?.length ?? 0,
      other: data?.search_results?.length ?? 0,
    });

    return data;
  } catch (err) {
    const elapsed = (performance.now() - start).toFixed(0);

    if (err.response) {
      // Server ne response diya but error status ke saath
      logger.error(
        `Search failed after ${elapsed}ms — HTTP ${err.response.status}`,
        err.response.data
      );
    } else if (err.request) {
      // Request gaya but koi response nahi aaya (backend down / network issue)
      logger.error(`No response from backend after ${elapsed}ms`, err.request);
    } else {
      // Request banate waqt hi error aa gaya
      logger.error("Request setup failed", err.message);
    }

    throw err;
  }
}