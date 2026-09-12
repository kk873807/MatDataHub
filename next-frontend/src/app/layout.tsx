import type { Metadata } from "next";
import { Geist, Geist_Mono, Red_Hat_Display } from "next/font/google";
import "./globals.css";
import { TopNav } from "@/components/TopNav";
import { AuthGuard } from "@/components/AuthGuard";
import { ThemeProvider } from "@/components/ThemeProvider";
import { AiChatWidget } from "@/components/AiChatWidget";

const geistSans = Geist({ variable: "--font-geist-sans", subsets: ["latin"] });
const geistMono = Geist_Mono({ variable: "--font-geist-mono", subsets: ["latin"] });
const redHat = Red_Hat_Display({ variable: "--font-red-hat", subsets: ["latin"] });

export const metadata: Metadata = {
  title: "MatDataHub",
  description: "Advanced Engineering Physics and Materials Platform",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${geistSans.variable} ${geistMono.variable} ${redHat.variable} min-h-screen antialiased`} suppressHydrationWarning>
      <body suppressHydrationWarning className="min-h-screen flex flex-col bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-white transition-colors duration-300">
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem disableTransitionOnChange>
          <TopNav />
          <div className="flex-1 w-full flex flex-col relative print-scroll-visible">
            <AuthGuard>{children}</AuthGuard>
          </div>
        </ThemeProvider>
        <AiChatWidget />
      </body>
    </html>
  );
}
