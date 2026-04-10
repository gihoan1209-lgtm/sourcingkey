import { NextRequest, NextResponse } from "next/server";
import { excludedCategories } from "@/lib/categories";
import { Product } from "@/lib/types";

interface NaverItem {
  title: string;
  link: string;
  image: string;
  lprice: string;
  mallName: string;
  productId: string;
  productType: string;
  brand: string;
  maker: string;
  category1: string;
  category2: string;
  category3: string;
  category4: string;
}

function stripHtml(text: string): string {
  return text.replace(/<[^>]*>/g, "");
}

function isExcluded(title: string): boolean {
  return excludedCategories.some((cat) => title.includes(cat));
}

function extractKeywords(products: Product[]): string[] {
  const wordCount: Record<string, number> = {};

  for (const product of products) {
    const words = product.title
      .replace(/[^\w\s가-힣]/g, "")
      .split(/\s+/)
      .filter((w) => w.length >= 2);

    for (const word of words) {
      wordCount[word] = (wordCount[word] || 0) + 1;
    }
  }

  return Object.entries(wordCount)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 20)
    .map(([word]) => word);
}

export async function POST(request: NextRequest) {
  try {
    const { keyword, maxItems = 50 } = await request.json();

    if (!keyword) {
      return NextResponse.json({ error: "키워드를 입력해주세요." }, { status: 400 });
    }

    const clientId = process.env.NAVER_CLIENT_ID;
    const clientSecret = process.env.NAVER_CLIENT_SECRET;

    if (!clientId || !clientSecret) {
      return NextResponse.json(
        { error: "네이버 API 키가 설정되지 않았습니다." },
        { status: 500 }
      );
    }

    const params = new URLSearchParams({
      query: keyword,
      display: String(maxItems),
      sort: "sim",
    });

    const response = await fetch(
      `https://openapi.naver.com/v1/search/shop.json?${params}`,
      {
        headers: {
          "X-Naver-Client-Id": clientId,
          "X-Naver-Client-Secret": clientSecret,
        },
      }
    );

    if (!response.ok) {
      return NextResponse.json(
        { error: "네이버 API 호출 실패" },
        { status: response.status }
      );
    }

    const data = await response.json();
    const items: NaverItem[] = data.items || [];

    const products: Product[] = items
      .map((item) => ({
        title: stripHtml(item.title),
        price: item.lprice,
        image: item.image,
        url: item.link,
        reviews: "0",
        source: "네이버 쇼핑",
      }))
      .filter((p) => !isExcluded(p.title));

    const keywords = extractKeywords(products);

    return NextResponse.json({
      products,
      keywords,
      total: products.length,
    });
  } catch {
    return NextResponse.json(
      { error: "서버 오류가 발생했습니다." },
      { status: 500 }
    );
  }
}
