import { useLocation, useNavigate } from "react-router-dom";
import SectionCard from "../components/SectionCard";

function SnapshotRow({ label, value }) {
  return (
    <div className="flex justify-between py-2 border-b last:border-none">
      <span className="text-gray-500">{label}</span>
      <span className="text-gray-800 font-medium">{value}</span>
    </div>
  );
}

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

  const { business, snapshot, ai_summary, social_media, reviews, search_results } = state.data;

  return (
    <div className="max-w-4xl mx-auto px-4 py-10">
      <button onClick={() => navigate("/")} className="text-indigo-600 mb-6 inline-block">
        ← New Search
      </button>

      <h1 className="text-3xl font-bold text-gray-800 mb-1">{business.name}</h1>
      <p className="text-gray-500 mb-6">{snapshot.location}</p>

      <SectionCard title="Business Snapshot" icon="📍">
        <SnapshotRow label="Business Type" value={snapshot.business_type} />
        <SnapshotRow label="Location" value={snapshot.location} />
        <SnapshotRow label="Website" value={business.website || "Not found"} />
        <SnapshotRow label="Phone" value={business.phone || "Not found"} />
        <SnapshotRow label="Email" value={business.email || "Not found"} />
        <SnapshotRow
          label="Verified Website"
          value={snapshot.verified_website ? "✓ Available" : "✗ Not confirmed"}
        />
      </SectionCard>

      <SectionCard title="Auto-Generated Summary" icon="🧠">
        <p className="text-gray-700 leading-relaxed">{ai_summary}</p>
        <p className="text-xs text-gray-400 mt-3 italic">
          Generated from publicly collected data, not a live AI-generated write-up.
        </p>
      </SectionCard>

      <SectionCard title="Social Profiles" icon="🌐" count={social_media?.length}>
        {social_media?.length ? social_media.map((s, i) => (
          <a key={i} href={s.url} target="_blank" rel="noreferrer" className="block py-1 text-indigo-600 hover:underline">
            {s.platform}: {s.title}
          </a>
        )) : <p className="text-gray-400">No social profiles found</p>}
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