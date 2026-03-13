'use client';

import React, { useState, useRef } from 'react';
import FractionBlock from './FractionBlock';
import { ManipulativeState, FractionBlock as FractionBlockType } from '@/lib/api';

interface FractionWorkspaceProps {
  manipulativeState: ManipulativeState;
  onBlockPlace?: (blockId: string, position: { x: number; y: number }) => void;
  onBlockCombine?: (blockIds: string[]) => void;
}

export default function FractionWorkspace({
  manipulativeState,
  onBlockPlace,
  onBlockCombine,
}: FractionWorkspaceProps) {
  const [draggedBlock, setDraggedBlock] = useState<string | null>(null);
  const [touchStartPos, setTouchStartPos] = useState<{ x: number; y: number } | null>(null);
  const workspaceRef = useRef<HTMLDivElement>(null);

  const handleDragStart = (e: React.DragEvent, blockId: string) => {
    setDraggedBlock(blockId);
    e.dataTransfer.effectAllowed = 'move';
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    if (!draggedBlock || !workspaceRef.current || !onBlockPlace) return;

    const rect = workspaceRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    // Constrain to workspace bounds
    const constrainedX = Math.max(0, Math.min(x, manipulativeState.workspace.width - 80));
    const constrainedY = Math.max(0, Math.min(y, manipulativeState.workspace.height - 80));

    onBlockPlace(draggedBlock, { x: constrainedX, y: constrainedY });
    setDraggedBlock(null);
  };

  const handleTouchStart = (e: React.TouchEvent, blockId: string) => {
    if (e.touches.length === 1) {
      const touch = e.touches[0];
      setDraggedBlock(blockId);
      if (workspaceRef.current) {
        const rect = workspaceRef.current.getBoundingClientRect();
        setTouchStartPos({
          x: touch.clientX - rect.left,
          y: touch.clientY - rect.top,
        });
      }
    }
  };

  const handleTouchMove = (e: React.TouchEvent) => {
    if (!draggedBlock || !touchStartPos || !workspaceRef.current || !onBlockPlace) return;
    e.preventDefault();

    const touch = e.touches[0];
    const rect = workspaceRef.current.getBoundingClientRect();
    const x = touch.clientX - rect.left;
    const y = touch.clientY - rect.top;

    const constrainedX = Math.max(0, Math.min(x, manipulativeState.workspace.width - 80));
    const constrainedY = Math.max(0, Math.min(y, manipulativeState.workspace.height - 80));

    onBlockPlace(draggedBlock, { x: constrainedX, y: constrainedY });
  };

  const handleTouchEnd = () => {
    setDraggedBlock(null);
    setTouchStartPos(null);
  };

  // Check for blocks that should be combined (two 1/4 blocks next to each other)
  const checkForCombination = () => {
    const placedBlocks = manipulativeState.workspace.placed_blocks;
    const quarterBlocks = placedBlocks.filter(
      (b) => b.type === '1/4' && !b.is_combined && b.position
    );

    if (quarterBlocks.length >= 2 && onBlockCombine) {
      // Simple check: if two 1/4 blocks are close together, combine them
      for (let i = 0; i < quarterBlocks.length; i++) {
        for (let j = i + 1; j < quarterBlocks.length; j++) {
          const block1 = quarterBlocks[i];
          const block2 = quarterBlocks[j];
          if (block1.position && block2.position) {
            const distance = Math.sqrt(
              Math.pow(block1.position.x - block2.position.x, 2) +
                Math.pow(block1.position.y - block2.position.y, 2)
            );
            if (distance < 100) {
              // Close enough to combine
              onBlockCombine([block1.id, block2.id]);
              return;
            }
          }
        }
      }
    }
  };

  return (
    <div style={{ margin: '20px 0' }}>
      <h3 style={{ marginBottom: '12px', fontSize: '18px' }}>Fraction Workspace</h3>
      <div
        ref={workspaceRef}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        onTouchMove={handleTouchMove}
        onTouchEnd={handleTouchEnd}
        style={{
          width: `${manipulativeState.workspace.width}px`,
          height: `${manipulativeState.workspace.height}px`,
          border: '2px solid #34495e',
          borderRadius: '8px',
          backgroundColor: '#ecf0f1',
          position: 'relative',
          marginBottom: '20px',
          touchAction: 'none',
        }}
      >
        {manipulativeState.workspace.placed_blocks.map((block) => (
          <FractionBlock key={block.id} block={block} />
        ))}
      </div>

      <div style={{ marginTop: '20px' }}>
        <h4 style={{ marginBottom: '12px', fontSize: '16px' }}>Available Blocks</h4>
        <div
          style={{
            display: 'flex',
            gap: '12px',
            flexWrap: 'wrap',
          }}
        >
          {manipulativeState.available_blocks
            .filter((block) => !block.position)
            .map((block) => (
              <FractionBlock
                key={block.id}
                block={block}
                onDragStart={handleDragStart}
                onDragEnd={() => {
                  setDraggedBlock(null);
                  checkForCombination();
                }}
                onTouchStart={handleTouchStart}
                onTouchMove={handleTouchMove}
                onTouchEnd={() => {
                  handleTouchEnd();
                  checkForCombination();
                }}
              />
            ))}
        </div>
      </div>
    </div>
  );
}
