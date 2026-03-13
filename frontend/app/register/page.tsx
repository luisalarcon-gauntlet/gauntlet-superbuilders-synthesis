'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import Button from '@/components/Button';
import LoadingSpinner from '@/components/LoadingSpinner';

export default function RegisterPage() {
  const router = useRouter();
  const { register } = useAuth();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    const result = await register(email, password, name);
    if (result.success) {
      router.push('/lesson');
    } else {
      setError(result.error || 'Registration failed');
    }
    setIsLoading(false);
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
      }}
    >
      <div
        style={{
          backgroundColor: '#fff',
          padding: '40px',
          borderRadius: '12px',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
          width: '100%',
          maxWidth: '400px',
        }}
      >
        <h1
          style={{
            fontSize: '32px',
            fontWeight: 'bold',
            marginBottom: '24px',
            textAlign: 'center',
            color: '#2c3e50',
          }}
        >
          Register
        </h1>

        {error && (
          <div
            style={{
              backgroundColor: '#fee',
              border: '1px solid #e74c3c',
              borderRadius: '8px',
              padding: '12px',
              marginBottom: '20px',
              color: '#e74c3c',
            }}
          >
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '20px' }}>
            <label
              htmlFor="name"
              style={{
                display: 'block',
                marginBottom: '8px',
                fontSize: '14px',
                fontWeight: '600',
                color: '#34495e',
              }}
            >
              Name
            </label>
            <input
              id="name"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              disabled={isLoading}
              style={{
                width: '100%',
                padding: '12px',
                fontSize: '16px',
                border: '1px solid #bdc3c7',
                borderRadius: '8px',
                outline: 'none',
              }}
            />
          </div>

          <div style={{ marginBottom: '20px' }}>
            <label
              htmlFor="email"
              style={{
                display: 'block',
                marginBottom: '8px',
                fontSize: '14px',
                fontWeight: '600',
                color: '#34495e',
              }}
            >
              Email
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              disabled={isLoading}
              style={{
                width: '100%',
                padding: '12px',
                fontSize: '16px',
                border: '1px solid #bdc3c7',
                borderRadius: '8px',
                outline: 'none',
              }}
            />
          </div>

          <div style={{ marginBottom: '24px' }}>
            <label
              htmlFor="password"
              style={{
                display: 'block',
                marginBottom: '8px',
                fontSize: '14px',
                fontWeight: '600',
                color: '#34495e',
              }}
            >
              Password
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              disabled={isLoading}
              style={{
                width: '100%',
                padding: '12px',
                fontSize: '16px',
                border: '1px solid #bdc3c7',
                borderRadius: '8px',
                outline: 'none',
              }}
            />
          </div>

          <Button type="submit" disabled={isLoading} style={{ width: '100%' }}>
            {isLoading ? <LoadingSpinner /> : 'Register'}
          </Button>
        </form>

        <div style={{ marginTop: '20px', textAlign: 'center' }}>
          <p style={{ color: '#7f8c8d', marginBottom: '12px' }}>
            Already have an account?{' '}
            <a
              href="/login"
              style={{ color: '#3498db', textDecoration: 'none', fontWeight: '600' }}
            >
              Login
            </a>
          </p>
          <a
            href="/"
            style={{ color: '#7f8c8d', textDecoration: 'none', fontSize: '14px' }}
          >
            ← Back to home
          </a>
        </div>
      </div>
    </main>
  );
}
