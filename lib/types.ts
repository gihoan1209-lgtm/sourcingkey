export interface Product {
  title: string;
  price: string;
  image: string;
  url: string;
  reviews: string;
  source: string;
}

export interface SearchResponse {
  products: Product[];
  keywords: string[];
  total: number;
}

export interface Category {
  name: string;
  keywords: string[];
}

export type SearchMode = "category" | "trending";
