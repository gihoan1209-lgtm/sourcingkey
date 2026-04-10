"use client";

import { useState } from "react";
import SearchBar from "@/components/SearchBar";
import CategorySidebar from "@/components/CategorySidebar";
import ProductGrid from "@/components/ProductGrid";
import KeywordTags from "@/components/KeywordTags";
import { Product, SearchMode } from "@/lib/types";

export default function Home() {
  const [keyword, setKeyword] = useState("");
  const [mode, setMode] = useState<SearchMode>("category");
  const [selectedKeyword, setSelectedKeyword] = useState<string | null>(null);
  const [products, setProducts] = useState<Product[]>([]);
  const [relatedKeywords, setRelatedKeywords] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [total, setTotal] = useState(0);
  const [searched, setSearched] = useState(false);

  async function doSearch(searchKeyword: string) {
    if (!searchKeyword.trim()) return;
    setLoading(true);
    setSearched(true);

    try {
      const res = await fetch("/api/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ keyword: searchKeyword, maxItems: 50 }),
      });

      const data = await res.json();

      if (res.ok) {
        setProducts(data.products);
        setRelatedKeywords(data.keywords);
        setTotal(data.total);
      } else {
        alert(data.error || "검색에 실패했습니다.");
        setProducts([]);
        setRelatedKeywords([]);
        setTotal(0);
      }
    } catch {
      alert("네트워크 오류가 발생했습니다.");
    } finally {
      setLoading(false);
    }
  }

  function handleSearch() {
    doSearch(keyword);
  }

  function handleKeywordSelect(kw: string) {
    setSelectedKeyword(kw);
    setKeyword(kw);
    doSearch(kw);
  }

  function handleRelatedKeywordClick(kw: string) {
    setKeyword(kw);
    setSelectedKeyword(null);
    doSearch(kw);
  }

  return (
    <div className="flex h-screen overflow-hidden">
      <CategorySidebar
        mode={mode}
        onModeChange={setMode}
        onKeywordSelect={handleKeywordSelect}
        selectedKeyword={selectedKeyword}
      />

      <main className="flex-1 overflow-y-auto p-6">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-3xl font-bold mb-6">🛍️ 소싱에이전트</h1>

          <SearchBar
            value={keyword}
            onChange={setKeyword}
            onSearch={handleSearch}
            loading={loading}
          />

          <hr className="my-6 border-gray-200" />

          {loading && (
            <div className="flex justify-center items-center py-20">
              <div className="animate-spin rounded-full h-10 w-10 border-4 border-red-500 border-t-transparent" />
            </div>
          )}

          {!loading && searched && (
            <>
              {total > 0 && (
                <p className="text-sm text-green-600 font-semibold mb-4">
                  총 {total}개 상품을 찾았습니다.
                </p>
              )}

              <KeywordTags
                keywords={relatedKeywords}
                onKeywordClick={handleRelatedKeywordClick}
              />

              <ProductGrid products={products} />

              {total === 0 && (
                <p className="text-center text-gray-500 py-20">
                  검색 결과가 없습니다.
                </p>
              )}
            </>
          )}

          {!loading && !searched && (
            <p className="text-center text-gray-400 py-20">
              키워드를 입력하거나 카테고리에서 선택해주세요.
            </p>
          )}
        </div>
      </main>
    </div>
  );
}
