import React from 'react';
import { FractionBlock as FractionBlockType } from '@/lib/api';

interface FractionBlockProps {
  block: FractionBlockType;
  onDragStart?: (e: React.DragEvent, blockId: string) => void;
  onDragEnd?: (e: React.DragEvent) => void;
  onTouchStart?: (e: React.TouchEvent, blockId: string) => void;
  onTouchMove?: (e: React.TouchEvent) => void;
  onTouchEnd?: (e: React.TouchEvent) => void;
  style?: React.CSSProperties;
}

export default function FractionBlock({
  block,
  onDragStart,
  onDragEnd,
  onTouchStart,
  onTouchMove,
  onTouchEnd,
  style,
}: FractionBlockProps) {
  const displayText = block.display || block.type;
  const isPlaced = block.position !== null;

  const blockStyle: React.CSSProperties = {
    width: '80px',
    height: '80px',
    backgroundColor: block.color,
    border: '2px solid #2c3e50',
    borderRadius: '8px',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    cursor: isPlaced ? 'default' : 'grab',
    userSelect: 'none',
    touchAction: 'none',
    position: isPlaced ? 'absolute' : 'relative',
    ...(isPlaced && block.position
      ? {
          left: `${block.position.x}px`,
          top: `${block.position.y}px`,
        }
      : {}),
    ...style,
  };

  const handleDragStart = (e: React.DragEvent) => {
    if (!isPlaced && onDragStart) {
      onDragStart(e, block.id);
    }
  };

  const handleTouchStart = (e: React.TouchEvent) => {
    if (!isPlaced && onTouchStart) {
      onTouchStart(e, block.id);
    }
  };

  return (
    <div
      draggable={!isPlaced}
      onDragStart={handleDragStart}
      onDragEnd={onDragEnd}
      onTouchStart={handleTouchStart}
      onTouchMove={onTouchMove}
      onTouchEnd={onTouchEnd}
      style={blockStyle}
    >
      <div
        style={{
          fontSize: '24px',
          fontWeight: 'bold',
          color: '#fff',
          textShadow: '1px 1px 2px rgba(0,0,0,0.3)',
        }}
      >
        {displayText}
      </div>
      {block.is_combined && (
        <div
          style={{
            fontSize: '12px',
            color: '#fff',
            marginTop: '4px',
            opacity: 0.9,
          }}
        >
          Combined
        </div>
      )}
    </div>
  );
}
