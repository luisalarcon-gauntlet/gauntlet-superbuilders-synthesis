import React from 'react';
import { TutorMessage } from '@/lib/api';

interface TutorChatProps {
  messages: Array<{ id: string; text: string; type: string; sender: 'tutor' | 'student' }>;
}

export default function TutorChat({ messages }: TutorChatProps) {
  return (
    <div
      style={{
        border: '1px solid #bdc3c7',
        borderRadius: '8px',
        padding: '16px',
        minHeight: '300px',
        maxHeight: '500px',
        overflowY: 'auto',
        backgroundColor: '#fff',
        marginBottom: '20px',
      }}
    >
      {messages.length === 0 ? (
        <p style={{ color: '#7f8c8d', fontStyle: 'italic' }}>
          Start the lesson to see tutor messages...
        </p>
      ) : (
        messages.map((message) => (
          <div
            key={message.id}
            style={{
              marginBottom: '16px',
              display: 'flex',
              justifyContent: message.sender === 'tutor' ? 'flex-start' : 'flex-end',
            }}
          >
            <div
              style={{
                maxWidth: '70%',
                padding: '12px 16px',
                borderRadius: '12px',
                backgroundColor: message.sender === 'tutor' ? '#3498db' : '#95a5a6',
                color: '#fff',
              }}
            >
              <p style={{ margin: 0, lineHeight: '1.5' }}>{message.text}</p>
            </div>
          </div>
        ))
      )}
    </div>
  );
}
