import { useLocation, useNavigate } from "react-router-dom";
import SectionCard from "../components/SectionCard";

export default function Results() {
  const { state } = useLocation();
  const navigate = useNavigate();

  if (!state?.data) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center">
        <p className="text-gray-500 mb-4">No results to show.</p>
        <button onClick={() => navigate("/")} className="text-indigo-600 underline">
          Go back to search
        </button>
      </div>
    );
  }

  const { business, social_media, documents, reviews, search_results } = state.data;

  return (
    <div className="max-w-4xl mx-auto px-4 py-10">
      <button onClick={() => navigate("/")} className="text-indigo-600 mb-6 inline-block">
        ← New Search
      </button>

      <h1 className="text-3xl font-bold text-gray-800 mb-1">{business.name}</h1>
      <p className="text-gray-500 mb-6">{business.address}</p>

      <SectionCard title="Business Overview" icon="🏢">
        <p><strong>Website:</strong> {business.website || "Not found"}</p>
        <p><strong>Phone:</strong> {business.phone || "Not found"}</p>
        <p><strong>Email:</strong> {business.email || "Not found"}</p>
        <p><strong>Description:</strong> {business.description || "Not available"}</p>
      </SectionCard>

      <SectionCard title="Social Profiles" icon="🌐" count={social_media?.length}>
        {social_media?.length ? social_media.map((s, i) => (
          <a key={i} href={s.url} target="_blank" rel="noreferrer" className="block py-1 text-indigo-600 hover:underline">
            {s.platform}: {s.title}
          </a>
        )) : <p className="text-gray-400">No social profiles found</p>}
      </SectionCard>

      <SectionCard title="Public Documents" icon="📄" count={documents?.length}>
        {documents?.length ? documents.map((d, i) => (
          <a key={i} href={d.url} target="_blank" rel="noreferrer" className="block py-1 text-indigo-600 hover:underline">{d.title}</a>
        )) : <p className="text-gray-400">No documents found</p>}
      </SectionCard>

      <SectionCard title="Reviews" icon="⭐" count={reviews?.length}>
        {reviews?.length ? reviews.map((r, i) => (
          <div key={i} className="py-2 border-b last:border-none">
            <a href={r.url} target="_blank" rel="noreferrer" className="text-indigo-600 hover:underline font-medium">{r.source}</a>
            <p className="text-sm text-gray-500">{r.snippet}</p>
          </div>
        )) : <p className="text-gray-400">No reviews found</p>}
      </SectionCard>

      <SectionCard title="Search Results" icon="🔎" count={search_results?.length}>
        {search_results?.length ? search_results.map((r, i) => (
          <div key={i} className="py-2 border-b last:border-none">
            <a href={r.url} target="_blank" rel="noreferrer" className="text-indigo-600 hover:underline font-medium">{r.title}</a>
            <p className="text-sm text-gray-500">{r.description}</p>
          </div>
        )) : <p className="text-gray-400">No other results found</p>}
      </SectionCard>
    </div>
  );
}