import type { Metadata } from "next";
import { Geist, Geist_Mono, Red_Hat_Display } from "next/font/google";
import "./globals.css";
import { TopNav } from "@/components/TopNav";
import { AuthGuard } from "@/components/AuthGuard";
import { ThemeProvider } from "@/components/ThemeProvider";

const geistSans = Geist({ variable: "--font-geist-sans", subsets: ["latin"] });
const geistMono = Geist_Mono({ variable: "--font-geist-mono", subsets: ["latin"] });
const redHat = Red_Hat_Display({ variable: "--font-red-hat", subsets: ["latin"] });

export const metadata: Metadata = {
  title: "MatDataHub",
  description: "Advanced Engineering Physics and Materials Platform",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${geistSans.variable} ${geistMono.variable} ${redHat.variable} h-full antialiased`} suppressHydrationWarning>
      <body className="min-h-full flex flex-col bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-white overflow-hidden transition-colors duration-300">
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem disableTransitionOnChange>
          <TopNav />
          <div className="flex-1 min-w-0 flex flex-col h-full overflow-y-auto relative print-scroll-visible">
            <AuthGuard>{children}</AuthGuard>
          </div>
        </ThemeProvider>
      </body>
    </html>
  );
}
