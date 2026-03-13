# Clone Synthesis Tutor - Math Tutoring Prototype

## Overview

A one-week prototype challenge to build an AI-powered conversational math tutor focused on teaching fraction equivalence to elementary students. The application combines a warm, encouraging chat-based tutor with interactive digital manipulatives (fraction blocks) to create an exploration-based learning experience similar to Synthesis Tutor. Students will learn that fractions like 1/2 and 2/4 are equivalent through hands-on manipulation and guided conversation.

## Goals

- Build a single, functional math lesson on fraction equivalence
- Create an engaging conversational interface with scripted tutor dialogue
- Implement interactive fraction manipulatives (visual fraction blocks)
- Design for iPad web browser usage with touch interactions
- Demonstrate the core Synthesis model of exploration-based learning
- Complete a working prototype within one week

## Users

**Primary Users:** Elementary school students (ages 6-12) learning basic fraction concepts
- Need visual, hands-on ways to understand abstract math concepts
- Respond well to encouraging, conversational guidance
- Learn best through exploration and discovery rather than direct instruction
- Require immediate feedback and validation

**Secondary Users:** Teachers and parents evaluating the tutoring approach
- Need to see clear learning outcomes and student engagement
- Want to understand how the digital manipulative aids comprehension

## Scope

**IN SCOPE for this version:**
- Single lesson focused on fraction equivalence (1/2 = 2/4 relationships)
- Chat-style tutor interface with scripted dialogue and simple branching logic
- Interactive "fraction box" workspace with draggable fraction blocks
- Touch-optimized interface for iPad web browsers
- Basic lesson flow: exploration → guided questions → comprehension check
- Simple progress tracking through the single lesson
- Warm, encouraging tutor personality and responses

## Out of Scope

**Explicitly deferred:**
- Complex LLM-based conversational AI or adaptive responses
- Multiple lessons or full curriculum development
- User accounts, progress persistence, or learning analytics
- Advanced fraction concepts beyond equivalence
- Multi-device responsive design (iPad-only focus)
- Assessment scoring or reporting features
- Integration with existing educational platforms

## Constraints

- **Timeline:** One week development sprint for rapid prototyping
- **Platform:** Must run on iPad in standard web browser
- **Content:** Single lesson on fraction equivalence only
- **Interaction:** Touch-based interface required for iPad usage
- **Deliverables:** Working prototype + demo video + documentation
- **Focus:** Quality of tutor-student interaction over technical complexity

## Stack

**Frontend:** Next.js + React (App Router, TypeScript)
- Touch event handling for iPad interactions
- Canvas or SVG for fraction block manipulatives

**Backend:** FastAPI (Python)
- Serves scripted dialogue content and lesson flow logic
- Handles lesson state and progress tracking

**Database:** Postgres
- Stores lesson scripts, dialogue trees, and session state
- Minimal schema focused on single lesson flow

**Infrastructure:** Docker + docker-compose (monorepo)
- Simplified deployment for prototype demonstration

**Auth:** JWT only
- Basic session management for lesson progress

## Key Decisions

**Scripted vs. AI-Generated Dialogue:** Using pre-written dialogue trees instead of LLM integration to ensure consistent, pedagogically sound interactions within the one-week timeline while maintaining quality control over the learning experience.

**Canvas-Based Manipulatives:** Implementing fraction blocks using HTML5 Canvas or SVG for precise touch interactions and visual feedback, essential for the hands-on learning approach that defines the Synthesis model.

**Session-Based State Management:** Storing lesson progress in session state rather than persistent user profiles, focusing on the single-lesson experience while maintaining simplicity.

**iPad-First Design:** Optimizing specifically for iPad touch interactions rather than attempting responsive design, ensuring the manipulative experience works flawlessly on the target platform.

**Monolithic Architecture:** Keeping all functionality in a single application to maximize development speed and minimize complexity during the prototype phase.