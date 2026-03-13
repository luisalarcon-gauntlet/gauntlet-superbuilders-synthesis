import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Synthesis Math Tutor',
  description: 'AI-powered math tutor for fraction equivalence',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
