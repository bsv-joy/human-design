import type { Metadata } from "next";
import { Inter, Playfair_Display } from "next/font/google";
import "./globals.css";
import { Navigation } from "./components/Navigation";
import { Player } from "./components/Player";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

const playfair = Playfair_Display({
  subsets: ["latin"],
  variable: "--font-playfair",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Human Designs | Forge Your Voice",
  description: "Create and share your own sovereign human designs and manifestos.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${inter.variable} ${playfair.variable}`}>
      <body className="antialiased bg-background text-foreground font-sans selection:bg-gold-500/30 pb-24 pt-16">
        <Navigation />
        <main className="min-h-screen">
          {children}
        </main>
        {/* <Player /> */}'
      </body>
    </html>
  );
}
