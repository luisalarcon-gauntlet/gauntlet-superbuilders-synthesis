import React from 'react';

interface LessonProgressProps {
  progressPercentage: number;
}

export default function LessonProgress({ progressPercentage }: LessonProgressProps) {
  return (
    <div style={{ marginBottom: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
        <span style={{ fontSize: '14px', fontWeight: '600' }}>Lesson Progress</span>
        <span style={{ fontSize: '14px', color: '#7f8c8d' }}>{progressPercentage}%</span>
      </div>
      <div
        style={{
          width: '100%',
          height: '24px',
          backgroundColor: '#ecf0f1',
          borderRadius: '12px',
          overflow: 'hidden',
        }}
      >
        <div
          style={{
            width: `${progressPercentage}%`,
            height: '100%',
            backgroundColor: '#3498db',
            transition: 'width 0.3s ease',
          }}
        />
      </div>
    </div>
  );
}
