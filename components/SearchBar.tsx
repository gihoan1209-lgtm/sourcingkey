"use client";

interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
  onSearch: () => void;
  loading: boolean;
}

export default function SearchBar({ value, onChange, onSearch, loading }: SearchBarProps) {
  return (
    <div className="flex gap-3 items-center">
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && onSearch()}
        placeholder="직접 검색어 입력 (예: 수납함, 텀블러, 캔들...)"
        className="flex-1 px-4 py-3 border border-gray-300 rounded-lg text-base focus:outline-none focus:ring-2 focus:ring-red-400 focus:border-transparent"
      />
      <button
        onClick={onSearch}
        disabled={loading}
        className="px-6 py-3 bg-red-500 text-white rounded-lg font-bold text-base hover:bg-red-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors whitespace-nowrap"
      >
        {loading ? "검색 중..." : "검색 🔍"}
      </button>
    </div>
  );
}
