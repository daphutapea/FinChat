import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "FinChat - Chat with SEC 10-K Filings",
  description:
    "A Retrieval-Augmented Generation chatbot that answers questions about 25 major companies' SEC 10-K filings - grounded in the source, cited, and honest.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
