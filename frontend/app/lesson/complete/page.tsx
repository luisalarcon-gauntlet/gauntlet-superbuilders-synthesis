'use client';

import { useRouter } from 'next/navigation';
import Button from '@/components/Button';

export default function LessonCompletePage() {
  const router = useRouter();

  return (
    <main
      style={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '40px 20px',
        maxWidth: '800px',
        margin: '0 auto',
        textAlign: 'center',
      }}
    >
      <div
        style={{
          fontSize: '64px',
          marginBottom: '24px',
        }}
      >
        🎉
      </div>

      <h1
        style={{
          fontSize: '48px',
          fontWeight: 'bold',
          color: '#27ae60',
          marginBottom: '16px',
        }}
      >
        Congratulations!
      </h1>

      <p
        style={{
          fontSize: '20px',
          color: '#7f8c8d',
          lineHeight: '1.6',
          marginBottom: '32px',
        }}
      >
        You've successfully completed the fraction equivalence lesson!
      </p>

      <div
        style={{
          backgroundColor: '#fff',
          padding: '32px',
          borderRadius: '12px',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
          marginBottom: '32px',
          width: '100%',
        }}
      >
        <h2
          style={{
            fontSize: '24px',
            fontWeight: '600',
            marginBottom: '16px',
            color: '#2c3e50',
          }}
        >
          What You Learned
        </h2>
        <ul
          style={{
            listStyle: 'none',
            padding: 0,
            fontSize: '16px',
            lineHeight: '1.8',
            color: '#34495e',
          }}
        >
          <li style={{ marginBottom: '12px' }}>
            ✓ Fractions like 1/2 and 2/4 represent the same amount
          </li>
          <li style={{ marginBottom: '12px' }}>
            ✓ Equivalent fractions can be created by combining smaller pieces
          </li>
          <li style={{ marginBottom: '12px' }}>
            ✓ Visual manipulatives help understand fraction relationships
          </li>
          <li>✓ You're becoming a fraction expert!</li>
        </ul>
      </div>

      <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap', justifyContent: 'center' }}>
        <Button
          onClick={() => router.push('/lesson')}
          style={{ fontSize: '18px', padding: '14px 28px' }}
        >
          Restart Lesson
        </Button>
        <Button
          onClick={() => router.push('/')}
          variant="secondary"
          style={{ fontSize: '18px', padding: '14px 28px' }}
        >
          Return Home
        </Button>
      </div>
    </main>
  );
}
