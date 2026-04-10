"use client";

interface KeywordTagsProps {
  keywords: string[];
  onKeywordClick: (keyword: string) => void;
}

export default function KeywordTags({ keywords, onKeywordClick }: KeywordTagsProps) {
  if (keywords.length === 0) return null;

  return (
    <div className="mb-6">
      <h3 className="text-sm font-bold text-gray-700 mb-2">🔗 연관 키워드</h3>
      <div className="flex flex-wrap gap-2">
        {keywords.map((kw) => (
          <button
            key={kw}
            onClick={() => onKeywordClick(kw)}
            className="px-3 py-1.5 text-xs bg-blue-50 text-blue-700 rounded-full border border-blue-200 hover:bg-blue-100 transition-colors"
          >
            {kw}
          </button>
        ))}
      </div>
    </div>
  );
}
