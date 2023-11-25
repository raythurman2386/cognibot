import type { Metadata } from "next";
import { GeistSans } from "geist/font/sans";
import "./globals.css";
import { Navbar, Header, Footer } from "./components";

export const metadata: Metadata = {
  title: "CogniBot",
  description: "The worlds smartest Discord bot. Chat with GPT-4-Turbo from OpenAI or Claude 2.1 from Anthropic!",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={GeistSans.className}>
        <Navbar />
        <Header />
        {children}
        <Footer />
      </body>
    </html>
  );
}
