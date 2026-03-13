// API client for communicating with FastAPI backend
// NEVER use mock data - all calls go through this module

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface ApiResponse<T> {
  data: T | null;
  error: string | null;
}

export interface User {
  id: string;
  email: string;
  name: string;
  created_at?: string;
}

export interface AuthResponse {
  user: User;
  access_token: string;
  token_type: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  name: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface Lesson {
  id: string;
  title: string;
  description: string;
  status: 'not_started' | 'in_progress' | 'completed';
}

export interface FractionBlock {
  id: string;
  type: string;
  position: { x: number; y: number } | null;
  color: string;
  display?: string;
  is_combined?: boolean;
}

export interface ManipulativeState {
  available_blocks: FractionBlock[];
  workspace: {
    width: number;
    height: number;
    placed_blocks: FractionBlock[];
  };
}

export interface TutorMessage {
  id: string;
  text: string;
  type: string;
  expects_response: boolean;
}

export interface LessonSession {
  id: string;
  lesson_id: string;
  user_id: string;
  status: string;
  started_at: string;
}

export interface Question {
  id: string;
  text: string;
  type: string;
  options?: string[];
  correct_answer?: string;
  fraction_pairs?: string[][];
}

export interface ProgressData {
  session: {
    id: string;
    status: string;
    progress_percentage: number;
    questions_answered: number;
    correct_answers: number;
    completed_at?: string;
  };
  achievements: Array<{
    title: string;
    description: string;
    earned_at: string;
  }>;
}

export interface CompletionData {
  completion: {
    lesson_completed: boolean;
    completion_time: string;
    final_score: number;
    mastery_level: string;
  };
  tutor_message: TutorMessage;
}

// Get auth token from memory (not localStorage)
let authToken: string | null = null;

export function setAuthToken(token: string | null) {
  authToken = token;
}

export function getAuthToken(): string | null {
  return authToken;
}

async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<ApiResponse<T>> {
  const url = `${API_URL}${endpoint}`;
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string>),
  };

  // Add auth token if available
  if (authToken) {
    headers['Authorization'] = `Bearer ${authToken}`;
  }

  try {
    const response = await fetch(url, {
      ...options,
      headers,
    });

    const data = await response.json();

    if (!response.ok) {
      return {
        data: null,
        error: data.error || `HTTP ${response.status}: ${response.statusText}`,
      };
    }

    return data;
  } catch (error) {
    return {
      data: null,
      error: error instanceof Error ? error.message : 'Network error',
    };
  }
}

// Auth endpoints
export async function register(
  request: RegisterRequest
): Promise<ApiResponse<AuthResponse>> {
  return apiRequest<AuthResponse>('/auth/register', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

export async function login(
  request: LoginRequest
): Promise<ApiResponse<AuthResponse>> {
  return apiRequest<AuthResponse>('/auth/login', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

// Lesson endpoints
export async function getLesson(): Promise<
  ApiResponse<{ lesson: Lesson; manipulative_state: ManipulativeState }>
> {
  return apiRequest('/lessons/fractions');
}

export async function startLesson(): Promise<
  ApiResponse<{ lesson_session: LessonSession; tutor_message: TutorMessage }>
> {
  return apiRequest('/lessons/fractions/start', {
    method: 'POST',
  });
}

export async function sendChat(
  sessionId: string,
  message: string
): Promise<ApiResponse<{ tutor_message: TutorMessage }>> {
  return apiRequest('/lessons/fractions/chat', {
    method: 'POST',
    body: JSON.stringify({
      session_id: sessionId,
      message,
      action_type: 'text_response',
    }),
  });
}

export async function recordAction(
  sessionId: string,
  action: {
    type: string;
    block_id?: string;
    position?: { x: number; y: number };
  }
): Promise<
  ApiResponse<{
    manipulative_state: ManipulativeState;
    tutor_message: TutorMessage;
  }>
> {
  return apiRequest('/lessons/fractions/action', {
    method: 'POST',
    body: JSON.stringify({
      session_id: sessionId,
      action,
    }),
  });
}

export async function combineBlocks(
  sessionId: string,
  blockIds: string[]
): Promise<
  ApiResponse<{
    manipulative_state: ManipulativeState;
    tutor_message: TutorMessage;
  }>
> {
  return apiRequest('/lessons/fractions/combine-blocks', {
    method: 'POST',
    body: JSON.stringify({
      session_id: sessionId,
      block_ids: blockIds,
    }),
  });
}

export async function getQuestion(
  sessionId: string
): Promise<ApiResponse<{ question: Question }>> {
  return apiRequest('/lessons/fractions/question', {
    method: 'POST',
    body: JSON.stringify({
      session_id: sessionId,
    }),
  });
}

export async function submitAnswer(
  sessionId: string,
  questionId: string,
  answer: string
): Promise<
  ApiResponse<{
    is_correct: boolean;
    tutor_message: TutorMessage;
    next_question?: Question;
  }>
> {
  return apiRequest('/lessons/fractions/answer', {
    method: 'POST',
    body: JSON.stringify({
      session_id: sessionId,
      question_id: questionId,
      answer,
    }),
  });
}

export async function getProgress(): Promise<ApiResponse<ProgressData>> {
  return apiRequest('/lessons/fractions/progress');
}

export async function completeLesson(
  sessionId: string
): Promise<ApiResponse<CompletionData>> {
  return apiRequest('/lessons/fractions/complete', {
    method: 'POST',
    body: JSON.stringify({
      session_id: sessionId,
    }),
  });
}
