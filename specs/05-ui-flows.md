# UI Flows Specification - Synthesis Math Tutor Clone

## Page Flows

### Landing Page
- **Page name**: Landing Page
- **Route**: `/`
- **Auth required**: no
- **Purpose**: Welcome page that introduces the fraction equivalence lesson and starts the learning experience.
- **User flow**:
  1. User sees welcome message and lesson introduction
  2. User clicks "Start Lesson" button
  3. System navigates to the lesson page
- **Components on this page**:
  - `WelcomeHeader` - displays title and brief description of the fraction lesson
  - `StartButton` - large, prominent button to begin the lesson
  - `LessonPreview` - shows a preview of what the student will learn
- **API calls made**: None
- **On success behavior**: Navigate to `/lesson`
- **On error behavior**: N/A (static page)

### Lesson Page
- **Page name**: Lesson Page
- **Route**: `/lesson`
- **Auth required**: no
- **Purpose**: Main interactive lesson interface combining conversational tutor with digital fraction manipulatives.
- **User flow**:
  1. User sees initial tutor message introducing fractions
  2. User interacts with fraction manipulatives in the workspace
  3. Tutor asks questions based on current lesson state
  4. User provides answers through chat or manipulative interactions
  5. System evaluates responses and provides feedback
  6. Lesson progresses through exploration, guided practice, and assessment phases
  7. Upon completion, user sees success message and option to restart
- **Components on this page**:
  - `TutorChat` - chat interface displaying tutor messages and student responses
  - `ChatInput` - input field for student to type responses to tutor
  - `FractionWorkspace` - interactive area containing fraction manipulatives
  - `FractionBlock` - individual draggable fraction pieces (1/2, 1/4, etc.)
  - `EquivalenceChecker` - visual indicator showing when fractions are equivalent
  - `LessonProgress` - progress bar showing current lesson phase
  - `ActionButtons` - context-sensitive buttons for manipulative actions (combine, split, etc.)
- **API calls made**:
  - `POST /api/lesson/start` - initialize new lesson session
  - `POST /api/lesson/action` - submit student action or response
  - `GET /api/lesson/state` - get current lesson state and next tutor message
  - `POST /api/lesson/complete` - mark lesson as completed
- **On success behavior**: 
  - Display tutor feedback and progress to next lesson phase
  - Update manipulatives based on student actions
  - Show completion celebration when lesson finished
- **On error behavior**: 
  - Show "Something went wrong. Please try again." message
  - Retry failed API calls automatically once
  - Allow manual retry if automatic retry fails

### Lesson Complete Page
- **Page name**: Lesson Complete
- **Route**: `/lesson/complete`
- **Auth required**: no
- **Purpose**: Celebration page shown when student successfully completes the fraction equivalence lesson.
- **User flow**:
  1. User sees congratulations message and lesson summary
  2. User can choose to restart the lesson or return to landing page
- **Components on this page**:
  - `CompletionCelebration` - animated success message with confetti
  - `LessonSummary` - recap of key concepts learned
  - `ActionButtons` - buttons to restart lesson or return home
- **API calls made**: None
- **On success behavior**: Navigate based on user choice
- **On error behavior**: N/A (static page)

## Navigation Structure

```
/
├── lesson/
│   └── complete/
```

## Shared Components

- **`Layout`** - Root layout component with consistent styling and iPad optimization
- **`LoadingSpinner`** - Loading indicator for API calls
- **`ErrorBoundary`** - Catches and displays React errors gracefully
- **`Button`** - Reusable button component with consistent styling
- **`Modal`** - Overlay component for confirmations or additional information
- **`Toast`** - Non-intrusive notification component for feedback messages
- **`FractionVisualizer`** - Reusable component for displaying fraction representations
- **`TouchHandler`** - Wrapper component optimizing touch interactions for iPad