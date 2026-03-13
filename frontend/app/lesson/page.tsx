'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import {
  getLesson,
  startLesson,
  sendChat,
  recordAction,
  combineBlocks,
  getQuestion,
  submitAnswer,
  getProgress,
  completeLesson,
  ManipulativeState,
  TutorMessage,
  LessonSession,
  Question,
} from '@/lib/api';
import { useAuth } from '@/contexts/AuthContext';
import LoadingSpinner from '@/components/LoadingSpinner';
import TutorChat from '@/components/TutorChat';
import ChatInput from '@/components/ChatInput';
import FractionWorkspace from '@/components/FractionWorkspace';
import LessonProgress from '@/components/LessonProgress';
import Button from '@/components/Button';

interface ChatMessage {
  id: string;
  text: string;
  type: string;
  sender: 'tutor' | 'student';
}

export default function LessonPage() {
  const router = useRouter();
  const { isAuthenticated, isLoading: authLoading } = useAuth();
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lessonSession, setLessonSession] = useState<LessonSession | null>(null);
  const [manipulativeState, setManipulativeState] = useState<ManipulativeState | null>(null);
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [currentQuestion, setCurrentQuestion] = useState<Question | null>(null);
  const [progressPercentage, setProgressPercentage] = useState(0);
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (authLoading) return;

    // Load lesson - API endpoints require auth, but we'll handle errors gracefully
    loadLesson();
  }, [authLoading]);

  const loadLesson = async () => {
    try {
      setIsLoading(true);
      setError(null);

      // Get lesson data
      const lessonResponse = await getLesson();
      if (lessonResponse.error || !lessonResponse.data) {
        const errorMsg = lessonResponse.error || 'Failed to load lesson';
        setError(errorMsg);
        return;
      }

      setManipulativeState(lessonResponse.data.manipulative_state);

      // Start lesson session
      const startResponse = await startLesson();
      if (startResponse.error || !startResponse.data) {
        setError(startResponse.error || 'Failed to start lesson');
        return;
      }

      setLessonSession(startResponse.data.lesson_session);
      const tutorMsg = startResponse.data.tutor_message;
      setChatMessages([
        {
          id: tutorMsg.id,
          text: tutorMsg.text,
          type: tutorMsg.type,
          sender: 'tutor',
        },
      ]);

      // Load progress
      await loadProgress();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const loadProgress = async () => {
    try {
      const progressResponse = await getProgress();
      if (progressResponse.data) {
        setProgressPercentage(progressResponse.data.session.progress_percentage);
      }
    } catch (err) {
      // Progress loading is not critical, so we'll just log
      console.error('Failed to load progress:', err);
    }
  };

  const handleChatSend = async (message: string) => {
    if (!lessonSession || isSubmitting) return;

    try {
      setIsSubmitting(true);
      setError(null);

      // Add student message to chat
      const studentMsg: ChatMessage = {
        id: `student_${Date.now()}`,
        text: message,
        type: 'text_response',
        sender: 'student',
      };
      setChatMessages((prev) => [...prev, studentMsg]);

      // Send to API
      const response = await sendChat(lessonSession.id, message);
      if (response.error || !response.data) {
        setError(response.error || 'Failed to send message');
        return;
      }

      // Add tutor response
      const tutorMsg = response.data.tutor_message;
      setChatMessages((prev) => [
        ...prev,
        {
          id: tutorMsg.id,
          text: tutorMsg.text,
          type: tutorMsg.type,
          sender: 'tutor',
        },
      ]);

      await loadProgress();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleBlockPlace = async (blockId: string, position: { x: number; y: number }) => {
    if (!lessonSession || isSubmitting) return;

    try {
      setIsSubmitting(true);
      setError(null);

      const response = await recordAction(lessonSession.id, {
        type: 'place_block',
        block_id: blockId,
        position,
      });

      if (response.error || !response.data) {
        setError(response.error || 'Failed to place block');
        return;
      }

      setManipulativeState(response.data.manipulative_state);

      // Add tutor message
      const tutorMsg = response.data.tutor_message;
      setChatMessages((prev) => [
        ...prev,
        {
          id: tutorMsg.id,
          text: tutorMsg.text,
          type: tutorMsg.type,
          sender: 'tutor',
        },
      ]);

      await loadProgress();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleBlockCombine = async (blockIds: string[]) => {
    if (!lessonSession || isSubmitting) return;

    try {
      setIsSubmitting(true);
      setError(null);

      const response = await combineBlocks(lessonSession.id, blockIds);
      if (response.error || !response.data) {
        setError(response.error || 'Failed to combine blocks');
        return;
      }

      setManipulativeState(response.data.manipulative_state);

      // Add tutor message
      const tutorMsg = response.data.tutor_message;
      setChatMessages((prev) => [
        ...prev,
        {
          id: tutorMsg.id,
          text: tutorMsg.text,
          type: tutorMsg.type,
          sender: 'tutor',
        },
      ]);

      await loadProgress();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleGetQuestion = async () => {
    if (!lessonSession || isSubmitting) return;

    try {
      setIsSubmitting(true);
      setError(null);

      const response = await getQuestion(lessonSession.id);
      if (response.error || !response.data) {
        setError(response.error || 'Failed to get question');
        return;
      }

      setCurrentQuestion(response.data.question);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleSubmitAnswer = async (answer: string) => {
    if (!lessonSession || !currentQuestion || isSubmitting) return;

    try {
      setIsSubmitting(true);
      setError(null);

      const response = await submitAnswer(lessonSession.id, currentQuestion.id, answer);
      if (response.error || !response.data) {
        setError(response.error || 'Failed to submit answer');
        return;
      }

      // Add tutor feedback
      const tutorMsg = response.data.tutor_message;
      setChatMessages((prev) => [
        ...prev,
        {
          id: tutorMsg.id,
          text: tutorMsg.text,
          type: tutorMsg.type,
          sender: 'tutor',
        },
      ]);

      // If there's a next question, set it
      if (response.data.next_question) {
        setCurrentQuestion(response.data.next_question);
      } else {
        setCurrentQuestion(null);
      }

      await loadProgress();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleComplete = async () => {
    if (!lessonSession || isSubmitting) return;

    try {
      setIsSubmitting(true);
      setError(null);

      const response = await completeLesson(lessonSession.id);
      if (response.error || !response.data) {
        setError(response.error || 'Failed to complete lesson');
        return;
      }

      // Navigate to completion page
      router.push('/lesson/complete');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (authLoading || isLoading) {
    return (
      <main style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <LoadingSpinner />
      </main>
    );
  }

  if (error && !manipulativeState) {
    const isAuthError = error.includes('401') || error.includes('Unauthorized');
    return (
      <main style={{ minHeight: '100vh', padding: '40px', textAlign: 'center' }}>
        <h2 style={{ color: '#e74c3c', marginBottom: '16px' }}>Error</h2>
        <p style={{ color: '#7f8c8d', marginBottom: '24px' }}>{error}</p>
        {isAuthError && (
          <p style={{ color: '#7f8c8d', marginBottom: '24px' }}>
            Please{' '}
            <a href="/login" style={{ color: '#3498db', textDecoration: 'underline' }}>
              log in
            </a>{' '}
            to access the lesson.
          </p>
        )}
        <div style={{ display: 'flex', gap: '12px', justifyContent: 'center' }}>
          <Button onClick={loadLesson}>Retry</Button>
          {isAuthError && (
            <Button onClick={() => router.push('/login')} variant="secondary">
              Go to Login
            </Button>
          )}
        </div>
      </main>
    );
  }

  return (
    <main
      style={{
        minHeight: '100vh',
        padding: '20px',
        maxWidth: '1200px',
        margin: '0 auto',
      }}
    >
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

      <LessonProgress progressPercentage={progressPercentage} />

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '20px' }}>
        <div>
          <h2 style={{ marginBottom: '16px', fontSize: '24px' }}>Tutor Chat</h2>
          <TutorChat messages={chatMessages} />
          <ChatInput
            onSend={handleChatSend}
            disabled={isSubmitting || !lessonSession}
            placeholder="Type your response to the tutor..."
          />
        </div>

        <div>
          <h2 style={{ marginBottom: '16px', fontSize: '24px' }}>Fraction Manipulatives</h2>
          {manipulativeState && (
            <FractionWorkspace
              manipulativeState={manipulativeState}
              onBlockPlace={handleBlockPlace}
              onBlockCombine={handleBlockCombine}
            />
          )}
        </div>
      </div>

      {currentQuestion && (
        <div
          style={{
            backgroundColor: '#fff',
            padding: '24px',
            borderRadius: '8px',
            marginBottom: '20px',
            border: '2px solid #3498db',
          }}
        >
          <h3 style={{ marginBottom: '16px', fontSize: '20px' }}>Question</h3>
          <p style={{ marginBottom: '16px', fontSize: '18px' }}>{currentQuestion.text}</p>
          {currentQuestion.options && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginBottom: '16px' }}>
              {currentQuestion.options.map((option, index) => (
                <Button
                  key={index}
                  variant="secondary"
                  onClick={() => handleSubmitAnswer(option)}
                  disabled={isSubmitting}
                >
                  {option}
                </Button>
              ))}
            </div>
          )}
        </div>
      )}

      <div style={{ display: 'flex', gap: '12px', justifyContent: 'center' }}>
        {!currentQuestion && (
          <Button onClick={handleGetQuestion} disabled={isSubmitting || !lessonSession}>
            Get Assessment Question
          </Button>
        )}
        <Button onClick={handleComplete} disabled={isSubmitting || !lessonSession} variant="secondary">
          Complete Lesson
        </Button>
      </div>
    </main>
  );
}
