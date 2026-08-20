import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'ChronoGov — Autonomous Anti-Whale DAO Constitution & Governance Guardian',
  description: 'Self-optimizing DAO Constitution on GenLayer. Neutralizes Trojan Horse proposals, whale ambushes, and treasury drains.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-[#080d1a] text-slate-100 min-h-screen antialiased font-sans">
        {children}
      </body>
    </html>
  );
}
