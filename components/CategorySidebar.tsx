"use client";

import { categories, trendingKeywords } from "@/lib/categories";
import { SearchMode } from "@/lib/types";

interface CategorySidebarProps {
  mode: SearchMode;
  onModeChange: (mode: SearchMode) => void;
  onKeywordSelect: (keyword: string) => void;
  selectedKeyword: string | null;
}

export default function CategorySidebar({
  mode,
  onModeChange,
  onKeywordSelect,
  selectedKeyword,
}: CategorySidebarProps) {
  return (
    <aside className="w-64 shrink-0 bg-white border-r border-gray-200 p-4 overflow-y-auto h-full">
      <h3 className="text-base font-bold mb-3">🔍 검색 모드</h3>
      <div className="flex flex-col gap-2 mb-6">
        <label className="flex items-center gap-2 cursor-pointer">
          <input
            type="radio"
            checked={mode === "category"}
            onChange={() => onModeChange("category")}
            className="accent-red-500"
          />
          <span className="text-sm">카테고리 검색</span>
        </label>
        <label className="flex items-center gap-2 cursor-pointer">
          <input
            type="radio"
            checked={mode === "trending"}
            onChange={() => onModeChange("trending")}
            className="accent-red-500"
          />
          <span className="text-sm">트렌딩 키워드</span>
        </label>
      </div>

      <hr className="mb-4" />

      {mode === "category" ? (
        <>
          <h3 className="text-base font-bold mb-3">🛒 카테고리 선택</h3>
          {categories.map((cat) => (
            <div key={cat.name} className="mb-4">
              <h4 className="text-sm font-semibold text-gray-700 mb-2">{cat.name}</h4>
              <div className="flex flex-wrap gap-1.5">
                {cat.keywords.map((kw) => (
                  <button
                    key={kw}
                    onClick={() => onKeywordSelect(kw)}
                    className={`px-2.5 py-1 text-xs rounded-full border transition-colors ${
                      selectedKeyword === kw
                        ? "bg-red-500 text-white border-red-500"
                        : "bg-gray-50 text-gray-700 border-gray-200 hover:bg-red-50 hover:border-red-300"
                    }`}
                  >
                    {kw}
                  </button>
                ))}
              </div>
            </div>
          ))}
        </>
      ) : (
        <>
          <h3 className="text-base font-bold mb-3">🔥 트렌딩 키워드</h3>
          <div className="flex flex-wrap gap-1.5">
            {trendingKeywords.map((kw) => (
              <button
                key={kw}
                onClick={() => onKeywordSelect(kw)}
                className={`px-2.5 py-1 text-xs rounded-full border transition-colors ${
                  selectedKeyword === kw
                    ? "bg-red-500 text-white border-red-500"
                    : "bg-orange-50 text-orange-700 border-orange-200 hover:bg-orange-100"
                }`}
              >
                {kw}
              </button>
            ))}
          </div>
        </>
      )}
    </aside>
  );
}
