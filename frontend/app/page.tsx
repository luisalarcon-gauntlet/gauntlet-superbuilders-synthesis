'use client';

import { useRouter } from 'next/navigation';
import { useState } from 'react';
import Button from '@/components/Button';
import LoadingSpinner from '@/components/LoadingSpinner';

export default function LandingPage() {
  const router = useRouter();
  const [isNavigating, setIsNavigating] = useState(false);

  const handleStartLesson = () => {
    setIsNavigating(true);
    router.push('/lesson');
  };

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
      }}
    >
      {isNavigating ? (
        <LoadingSpinner />
      ) : (
        <>
          <div style={{ textAlign: 'center', marginBottom: '40px' }}>
            <h1
              style={{
                fontSize: '48px',
                fontWeight: 'bold',
                color: '#2c3e50',
                marginBottom: '16px',
              }}
            >
              Welcome to Synthesis Math Tutor
            </h1>
            <p
              style={{
                fontSize: '20px',
                color: '#7f8c8d',
                lineHeight: '1.6',
                marginBottom: '24px',
              }}
            >
              Learn about fraction equivalence through interactive exploration!
            </p>
          </div>

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
              What You'll Learn
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
                ✓ Discover that fractions like 1/2 and 2/4 represent the same amount
              </li>
              <li style={{ marginBottom: '12px' }}>
                ✓ Explore fraction manipulatives through hands-on interaction
              </li>
              <li style={{ marginBottom: '12px' }}>
                ✓ Learn from an encouraging AI tutor
              </li>
              <li>✓ Practice with guided exercises and assessments</li>
            </ul>
          </div>

          <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap', justifyContent: 'center' }}>
            <Button
              onClick={handleStartLesson}
              disabled={isNavigating}
              style={{ fontSize: '20px', padding: '16px 32px' }}
            >
              Start Lesson
            </Button>
          </div>

          <div style={{ marginTop: '32px', textAlign: 'center' }}>
            <p style={{ color: '#7f8c8d', marginBottom: '12px' }}>
              Need an account?{' '}
              <a
                href="/register"
                style={{ color: '#3498db', textDecoration: 'none', fontWeight: '600' }}
              >
                Register
              </a>
              {' or '}
              <a
                href="/login"
                style={{ color: '#3498db', textDecoration: 'none', fontWeight: '600' }}
              >
                Login
              </a>
            </p>
          </div>
        </>
      )}
    </main>
  );
}
