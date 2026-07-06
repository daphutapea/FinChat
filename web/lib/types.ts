export interface Source {
  index: number;
  source: string;
  ticker?: string | null;
  company?: string | null;
  type?: string | null;
  excerpt: string;
}

export interface ChatResponse {
  answer: string;
  routed_to: string | null;
  sources: Source[];
  error?: string;
}

export interface Company {
  ticker: string;
  name: string;
}
