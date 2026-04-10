import { Product } from "@/lib/types";

interface ProductCardProps {
  product: Product;
}

export default function ProductCard({ product }: ProductCardProps) {
  return (
    <div className="border border-gray-200 rounded-xl overflow-hidden bg-white hover:shadow-lg transition-shadow">
      <div className="aspect-square relative bg-gray-100">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={product.image}
          alt={product.title}
          className="w-full h-full object-cover"
          loading="lazy"
        />
      </div>
      <div className="p-3">
        <h3 className="text-sm font-bold leading-tight line-clamp-2 mb-2 min-h-[2.5rem]">
          {product.title}
        </h3>
        <p className="text-lg font-bold text-red-500 mb-1">
          {Number(product.price).toLocaleString()}원
        </p>
        <p className="text-xs text-gray-500 mb-3">
          리뷰 {product.reviews}개 · {product.source}
        </p>
        <a
          href={product.url}
          target="_blank"
          rel="noopener noreferrer"
          className="block w-full text-center px-3 py-2 bg-[#03C75A] text-white text-sm font-bold rounded-lg hover:bg-[#02b350] transition-colors"
        >
          네이버 쇼핑에서 보기
        </a>
      </div>
    </div>
  );
}
