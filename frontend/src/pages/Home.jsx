import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { searchBusiness } from "../api/searchApi";

const STATUS_MESSAGES = [
  "Searching Google...",
  "Finding LinkedIn...",
  "Collecting public information...",
  "Analyzing results...",
  "Preparing report...",
];

export default function Home() {
  const [businessName, setBusinessName] = useState("");
  const [location, setLocation] = useState("");
  const [address, setAddress] = useState("");
  const [loading, setLoading] = useState(false);
  const [statusIndex, setStatusIndex] = useState(0);
  const navigate = useNavigate();

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!businessName.trim() || !location.trim()) return;

    setLoading(true);
    const interval = setInterval(() => {
      setStatusIndex((i) => (i + 1) % STATUS_MESSAGES.length);
    }, 1500);

    try {
      const data = await searchBusiness({
        business_name: businessName,
        location: location,
        address: address || null,
      });
      navigate("/results", { state: { data } });
    } catch (err) {
      alert("Search failed. Is the backend running on port 8000?");
    } finally {
      clearInterval(interval);
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4">
      <h1 className="text-4xl font-bold text-gray-800 mb-2">Business OSINT Search</h1>
      <p className="text-gray-500 mb-8">Public, open-source business intelligence lookup</p>

      <form onSubmit={handleSearch} className="w-full max-w-xl bg-white shadow-lg rounded-2xl p-6 space-y-4">
        <input
          type="text"
          placeholder="Business Name"
          value={businessName}
          onChange={(e) => setBusinessName(e.target.value)}
          className="w-full border border-gray-200 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-400"
        />
        <input
          type="text"
          placeholder="Location (city, state)"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          className="w-full border border-gray-200 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-400"
        />
        <input
          type="text"
          placeholder="Address (optional)"
          value={address}
          onChange={(e) => setAddress(e.target.value)}
          className="w-full border border-gray-200 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-400"
        />
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-indigo-600 text-white font-medium rounded-xl py-3 hover:bg-indigo-700 transition disabled:opacity-60"
        >
          {loading ? STATUS_MESSAGES[statusIndex] : "Search"}
        </button>
      </form>
    </div>
  );
}