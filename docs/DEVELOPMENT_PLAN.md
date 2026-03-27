# FlavorMap — 4-Week Development Plan

> **Version:** 1.0
> **Date:** 2026-03-27
> **Total Duration:** 4 Weeks
> **Milestones:** 5

---

## Timeline Overview

```
Week 1          Week 2          Week 3          Week 4
┌──────────────┬──────────────┬──────────────┬──────────────┐
│  M1    M2    │     M2       │     M3       │  M4    M5   │
│  ████  ████  │     ████     │     ████     │  ████  ████ │
└──────────────┴──────────────┴──────────────┴──────────────┘
```

---

## Milestone 1: Foundation & Basic CRUD

**Duration:** Days 1-3 (Week 1)
**Goal:** Working Django + Next.js setup with basic restaurant CRUD

| #   | Feature                                | Issue | Priority |
| --- | -------------------------------------- | ----- | -------- |
| —   | Django + Next.js project setup         | —     | Required |
| —   | Database models (Restaurant, Category) | #2    | Required |
| —   | Basic CRUD API endpoints               | #2    | Required |
| #3  | Category System                        | #3    | Required |
| —   | Admin panel configuration              | —     | Required |

### Deliverables

- [ ] Django project with migrations
- [ ] Next.js app running
- [ ] Restaurant model with CRUD API
- [ ] Category model with many-to-many relation
- [ ] Admin panel for data management

### Verification

```bash
# API
POST /api/restaurants/     # Create
GET  /api/restaurants/     # List
GET  /api/restaurants/{id} # Detail
PUT  /api/restaurants/{id} # Update
DELETE /api/restaurants/{id} # Delete

# Admin
/admin/ accessible with superuser
```

---

## Milestone 2: Core User Features (Top 5)

**Duration:** Days 4-7 (Week 1-2)
**Goal:** Essential features for user engagement

| #   | Feature                  | Issue | Priority |
| --- | ------------------------ | ----- | -------- |
| #8  | Average Rating           | #8    | High     |
| #9  | Reviews & Ratings System | #9    | High     |
| #12 | User Authentication      | #12   | High     |
| #13 | Favorites List           | #13   | Medium   |
| #16 | Search                   | #16   | Medium   |

### Deliverables

- [ ] User registration and login
- [ ] Token-based authentication
- [ ] Write/edit/delete reviews (1-5 stars)
- [ ] One review per user per restaurant
- [ ] Average rating calculation
- [ ] Add/remove favorites
- [ ] Search by name, description, location

### Verification

```bash
# Auth
POST /api/auth/register/
POST /api/auth/login/
POST /api/auth/logout/

# Reviews
POST /api/restaurants/{id}/reviews/
GET  /api/restaurants/{id}/reviews/

# Favorites
POST /api/favorites/{restaurant_id}/
GET  /api/favorites/

# Search
GET /api/restaurants/search?q=pizza
```

---

## Milestone 3: Filtering & Discovery

**Duration:** Days 8-14 (Week 2-3)
**Goal:** Help users find exactly what they want

| #   | Feature            | Issue | Priority |
| --- | ------------------ | ----- | -------- |
| #6  | Location Filter    | #6    | Medium   |
| #7  | Price Range Filter | #7    | Medium   |
| #5  | Advanced Filtering | #5    | Medium   |
| #19 | Opening Hours      | #19   | Medium   |
| #20 | Popular Ranking    | #20   | Low      |

### Deliverables

- [ ] City and district fields on Restaurant
- [ ] Location filter API
- [ ] Price range filter (€, €€, €€€)
- [ ] Combined multi-filter (category + location + price)
- [ ] Opening hours model and API
- [ ] Homepage: top-rated section
- [ ] Homepage: newest section

### Verification

```bash
# Filters
GET /api/restaurants/?city=Istanbul
GET /api/restaurants/?price=1,2
GET /api/restaurants/?category=turkish&city=Istanbul&min_rating=4

# Opening Hours
GET /api/restaurants/{id}/hours/

# Homepage
GET /api/restaurants/?sort=rating&limit=5
GET /api/restaurants/?sort=newest&limit=5
```

---

## Milestone 4: Media & Infrastructure

**Duration:** Days 15-21 (Week 3-4)
**Goal:** Photo handling and file storage infrastructure

| #   | Feature                | Issue | Priority |
| --- | ---------------------- | ----- | -------- |
| #24 | Object File Management | #24   | Required |
| #17 | Restaurant Photo       | #17   | Medium   |
| #18 | Photo Gallery          | #18   | Low      |
| #4  | Menu Management        | #4    | Medium   |
| #21 | Atomic Transactions    | #21   | Medium   |

### Deliverables

- [ ] FileStorage abstract class
- [ ] LocalFileStorage implementation
- [ ] MinioStorage implementation
- [ ] FileService with dependency injection
- [ ] Restaurant photo upload
- [ ] Multiple photos per restaurant
- [ ] Lightbox viewer
- [ ] Menu items CRUD
- [ ] Atomic transactions for multi-step operations

### Verification

```bash
# File Upload
POST /api/restaurants/{id}/photos/  # multipart/form-data

# Menu
POST /api/restaurants/{id}/menu/
GET  /api/restaurants/{id}/menu/

# Storage backends switch via env var
FILE_STORAGE_BACKEND=local|minio
```

---

## Milestone 5: Maps & Final Polish

**Duration:** Days 22-28 (Week 4)
**Goal:** Map integration, engagement features, production readiness

| #   | Feature               | Issue | Priority |
| --- | --------------------- | ----- | -------- |
| #22 | Map Integration       | #22   | Low      |
| #10 | Review Replies        | #10   | Low      |
| #11 | Review Likes          | #11   | Low      |
| #15 | Restaurant Owner Role | #15   | Low      |
| #14 | User Profile          | #14   | Low      |

### Deliverables

- [ ] Latitude/longitude fields
- [ ] Google Maps iframe on detail page
- [ ] Geocoding service
- [ ] Review replies (one level deep)
- [ ] Review likes/dislikes
- [ ] Sort reviews by helpfulness
- [ ] Restaurant owner role
- [ ] Claim restaurant flow
- [ ] User profile page
- [ ] Production deployment config

### Verification

```bash
# Maps
GET /api/restaurants/{id}/map/
GET /api/restaurants/?lat=41.0082&lng=28.9784&radius=5

# Engagement
POST /api/reviews/{id}/reply/
POST /api/reviews/{id}/like/

# Profile
GET /api/profile/
GET /api/profile/reviews/
GET /api/profile/favorites/
```

---

## Dependency Graph

```
Milestone 1 (Foundation)
    │
    ├──▶ Milestone 2 (Core Features)
    │        │
    │        ├──▶ Milestone 3 (Filtering)
    │        │        │
    │        │        └──▶ Milestone 4 (Media) ──▶ Milestone 5 (Maps & Polish)
    │        │                    │
    │        │                    └──▶ #24 (Object File Management)
    │        │                            └──▶ #17, #18 (Photos)
```

---

## Issue Distribution

| Milestone | Issues                  | Count  |
| --------- | ----------------------- | ------ |
| M1        | #2, #3, setup           | 3      |
| M2        | #8, #9, #12, #13, #16   | 5      |
| M3        | #6, #7, #5, #19, #20    | 5      |
| M4        | #24, #17, #18, #4, #21  | 5      |
| M5        | #22, #10, #11, #15, #14 | 5      |
| **Total** |                         | **23** |

---

## Risk Register

| Risk                               | Impact | Mitigation                          |
| ---------------------------------- | ------ | ----------------------------------- |
| #24 (File Storage) delays #17, #18 | High   | Implement LocalFileStorage first    |
| Auth complexity in M2              | Medium | Use Django built-in auth            |
| Map API key requirements           | Low    | Use iframe mode (no key)            |
| Time constraints                   | High   | Prioritize M1-M2, defer M5 features |

---

## Definition of Done (Per Milestone)

1. All features implemented and tested
2. API endpoints documented
3. No critical bugs
4. Code committed and pushed
5. Demo-able functionality

---

_Plan generated from PRODUCT_REQUIREMENTS.md_
