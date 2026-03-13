# API Contracts Specification

## Authentication Endpoints

### POST /auth/register
- **Description**: Register a new student user
- **Auth required**: No
- **Request body**:
```json
{
  "email": "student@example.com",
  "password": "password123",
  "name": "John Doe"
}
```
- **Response**:
```json
{
  "data": {
    "user": {
      "id": 1,
      "email": "student@example.com",
      "name": "John Doe",
      "created_at": "2024-03-07T10:30:00Z"
    },
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  },
  "error": null
}
```

### POST /auth/login
- **Description**: Login student user
- **Auth required**: No
- **Request body**:
```json
{
  "email": "student@example.com",
  "password": "password123"
}
```
- **Response**:
```json
{
  "data": {
    "user": {
      "id": 1,
      "email": "student@example.com",
      "name": "John Doe"
    },
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  },
  "error": null
}
```

## Lesson Management Endpoints

### GET /lessons/fractions
- **Description**: Get the fraction equivalence lesson data and initial state
- **Auth required**: Yes
- **Request body**: None
- **Response**:
```json
{
  "data": {
    "lesson": {
      "id": 1,
      "title": "Fraction Equivalence",
      "description": "Learn that fractions like 1/2 and 2/4 represent the same amount",
      "status": "not_started"
    },
    "manipulative_state": {
      "available_blocks": [
        {"id": "half_1", "type": "1/2", "position": null, "color": "#FF6B6B"},
        {"id": "quarter_1", "type": "1/4", "position": null, "color": "#4ECDC4"},
        {"id": "quarter_2", "type": "1/4", "position": null, "color": "#4ECDC4"}
      ],
      "workspace": {
        "width": 800,
        "height": 400,
        "placed_blocks": []
      }
    }
  },
  "error": null
}
```

### POST /lessons/fractions/start
- **Description**: Start the fraction lesson and get the first tutor message
- **Auth required**: Yes
- **Request body**: None
- **Response**:
```json
{
  "data": {
    "lesson_session": {
      "id": "session_123",
      "lesson_id": 1,
      "user_id": 1,
      "status": "in_progress",
      "started_at": "2024-03-07T10:30:00Z"
    },
    "tutor_message": {
      "id": "msg_1",
      "text": "Hi there! I'm your math tutor. Today we're going to explore fractions and discover something really cool about them. Do you see the fraction blocks on your screen? Try dragging the red block that shows 1/2 into the workspace!",
      "type": "instruction",
      "expects_response": false
    }
  },
  "error": null
}
```

## Conversation Endpoints

### POST /lessons/fractions/chat
- **Description**: Send student response or get next tutor message based on current lesson state
- **Auth required**: Yes
- **Request body**:
```json
{
  "session_id": "session_123",
  "message": "I placed the 1/2 block in the workspace",
  "action_type": "text_response"
}
```
- **Response**:
```json
{
  "data": {
    "tutor_message": {
      "id": "msg_2",
      "text": "Perfect! Now I want you to try something. Can you drag the two green 1/4 blocks and place them right next to each other in the workspace? Let's see what happens!",
      "type": "instruction",
      "expects_response": false
    }
  },
  "error": null
}
```

### POST /lessons/fractions/action
- **Description**: Record student action with the manipulative and get tutor response
- **Auth required**: Yes
- **Request body**:
```json
{
  "session_id": "session_123",
  "action": {
    "type": "place_block",
    "block_id": "quarter_1",
    "position": {"x": 100, "y": 200}
  }
}
```
- **Response**:
```json
{
  "data": {
    "manipulative_state": {
      "placed_blocks": [
        {
          "id": "quarter_1",
          "type": "1/4",
          "position": {"x": 100, "y": 200},
          "color": "#4ECDC4"
        }
      ]
    },
    "tutor_message": {
      "id": "msg_3",
      "text": "Great start! Now place the other 1/4 block right next to it.",
      "type": "encouragement",
      "expects_response": false
    }
  },
  "error": null
}
```

### POST /lessons/fractions/combine-blocks
- **Description**: Combine fraction blocks when student performs combination action
- **Auth required**: Yes
- **Request body**:
```json
{
  "session_id": "session_123",
  "block_ids": ["quarter_1", "quarter_2"]
}
```
- **Response**:
```json
{
  "data": {
    "manipulative_state": {
      "placed_blocks": [
        {
          "id": "combined_half",
          "type": "2/4",
          "display": "1/2",
          "position": {"x": 100, "y": 200},
          "color": "#4ECDC4",
          "is_combined": true
        }
      ]
    },
    "tutor_message": {
      "id": "msg_4",
      "text": "Wow! Look what happened! When you put those two 1/4 blocks together, they make the same size as the 1/2 block. This means 2/4 equals 1/2! They're equivalent fractions.",
      "type": "revelation",
      "expects_response": false
    }
  },
  "error": null
}
```

## Assessment Endpoints

### POST /lessons/fractions/question
- **Description**: Get a check-for-understanding question
- **Auth required**: Yes
- **Request body**:
```json
{
  "session_id": "session_123"
}
```
- **Response**:
```json
{
  "data": {
    "question": {
      "id": "q1",
      "text": "Which fraction is equivalent to 1/2?",
      "type": "multiple_choice",
      "options": ["1/4", "2/4", "3/4", "4/4"],
      "correct_answer": "2/4"
    }
  },
  "error": null
}
```

### POST /lessons/fractions/answer
- **Description**: Submit answer to assessment question
- **Auth required**: Yes
- **Request body**:
```json
{
  "session_id": "session_123",
  "question_id": "q1",
  "answer": "2/4"
}
```
- **Response**:
```json
{
  "data": {
    "is_correct": true,
    "tutor_message": {
      "id": "msg_5",
      "text": "Excellent! You're absolutely right. 2/4 is equivalent to 1/2. You really understand this concept!",
      "type": "praise",
      "expects_response": false
    },
    "next_question": {
      "id": "q2",
      "text": "Now try this one: Which two fractions shown below are equivalent?",
      "type": "visual_comparison",
      "fraction_pairs": [["1/3", "2/6"], ["1/4", "3/8"], ["2/3", "4/6"]]
    }
  },
  "error": null
}
```

## Progress Endpoints

### GET /lessons/fractions/progress
- **Description**: Get current lesson progress and completion status
- **Auth required**: Yes
- **Request body**: None
- **Response**:
```json
{
  "data": {
    "session": {
      "id": "session_123",
      "status": "completed",
      "progress_percentage": 100,
      "questions_answered": 3,
      "correct_answers": 3,
      "completed_at": "2024-03-07T11:15:00Z"
    },
    "achievements": [
      {
        "title": "Fraction Explorer",
        "description": "Successfully combined fraction blocks",
        "earned_at": "2024-03-07T10:45:00Z"
      },
      {
        "title": "Equivalence Expert",
        "description": "Completed lesson with 100% accuracy",
        "earned_at": "2024-03-07T11:15:00Z"
      }
    ]
  },
  "error": null
}
```

### POST /lessons/fractions/complete
- **Description**: Mark lesson as completed when student finishes all assessment questions
- **Auth required**: Yes
- **Request body**:
```json
{
  "session_id": "session_123"
}
```
- **Response**:
```json
{
  "data": {
    "completion": {
      "lesson_completed": true,
      "completion_time": "45 minutes",
      "final_score": 100,
      "mastery_level": "excellent"
    },
    "tutor_message": {
      "id": "msg_final",
      "text": "Congratulations! You've mastered fraction equivalence. You discovered that fractions like 1/2 and 2/4 represent the same amount, just divided into different pieces. Great work today!",
      "type": "completion",
      "expects_response": false
    }
  },
  "error": null
}
```