# FleetLog-Ai

A backend API for managing vehicles and vehicle inspections, built with **Django, Django REST Framework, PostgreSQL, JWT authentication, and django-filter**.

The project is being developed phase by phase to understand backend development from the fundamentals rather than starting directly with complex abstractions.

The current implementation covers **project setup, CRUD operations, validation and business rules, JWT authentication, role-based permissions, object-level permissions, search, filtering, and pagination.**

---

## 🚀 Tech Stack

* **Backend:** Python, Django, Django REST Framework
* **Database:** PostgreSQL
* **Authentication:** JWT using `djangorestframework-simplejwt`
* **Filtering:** `django-filter`
* **API Testing:** Postman
* **Version Control:** Git & GitHub
* **Architecture:** Django MVT + REST API architecture

---

# 📌 Project Overview

FleetLog-Ai is designed around a vehicle inspection workflow.

The backend manages:

* Users and their roles
* Tenants
* Vehicles
* Inspections
* Inspection checklist items
* Inspection assignments
* API authentication and authorization

The project focuses on understanding how these components work together in a real backend application.

---

# 🏗️ Project Architecture

The project is divided into multiple Django applications based on responsibility:

```text
fleetlog/
│
├── accounts/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── permissions.py
│
├── vehicle/
│   ├── models.py
│   ├── serializers.py
│   └── views.py
│
├── inspection/
│   ├── models.py
│   ├── serializers.py
│   └── views.py
│
├── uploads/
├── fleetservice/
├── report/
├── analytics/
│
├── manage.py
└── requirements.txt
```

Each app has a separate responsibility so that the project can grow without putting all functionality into one Django app.

---

# 🗄️ Database Architecture

The application uses **PostgreSQL** as the primary relational database.

## Main Entities

| Entity        | Purpose                                         |
| ------------- | ----------------------------------------------- |
| Tenant        | Represents an organization/tenant               |
| User          | Stores users and their roles                    |
| Vehicle       | Stores vehicle information                      |
| Inspection    | Represents an inspection performed on a vehicle |
| ChecklistItem | Stores individual inspection checklist items    |

---

# 🔗 Entity Relationships

The current database structure can be represented conceptually as:

```text
                    ┌──────────────┐
                    │    Tenant    │
                    └──────┬───────┘
                           │
                           │ 1 : N
                           ▼
                    ┌──────────────┐
                    │     User     │
                    │              │
                    │ role         │
                    │ tenant       │
                    └──────┬───────┘
                           │
                           │
              ┌────────────┴────────────┐
              │                         │
              │                         │
              ▼                         ▼
       ┌──────────────┐          ┌──────────────┐
       │   Vehicle    │          │  Inspection  │
       │              │◄─────────│              │
       │ tenant       │  1 : N   │ vehicle      │
       └──────────────┘          │ assessor     │
                                 └──────┬───────┘
                                        │
                                        │ 1 : N
                                        ▼
                                ┌────────────────┐
                                │ ChecklistItem  │
                                │                │
                                │ inspection     │
                                └────────────────┘
```

### Relationship Summary

**Tenant → User**

```text
Tenant 1 ──── N User
```

A tenant can have multiple users.

---

**Tenant → Vehicle**

```text
Tenant 1 ──── N Vehicle
```

Vehicles belong to a tenant.

---

**Vehicle → Inspection**

```text
Vehicle 1 ──── N Inspection
```

A vehicle can have multiple inspections over time.

---

**User → Inspection**

The inspection stores the assigned assessor.

```text
User 1 ──── N Inspection
```

An assessor can be assigned to multiple inspections.

---

**Inspection → ChecklistItem**

```text
Inspection 1 ──── N ChecklistItem
```

An inspection contains multiple checklist items.

---

# 👥 User Roles

The custom `User` model extends Django's `AbstractUser`.

Current roles:

```text
Renter
Supervisor
Assessor
```

The user also belongs to a tenant.

Conceptually:

```text
User
 ├── username
 ├── email
 ├── password
 ├── role
 └── tenant → Tenant
```

This allows authorization rules to consider both the **user's role** and, later, their **tenant context**.

---

# 🔐 Authentication

JWT authentication is implemented using:

**Django REST Framework + Simple JWT**

Authentication flow:

```text
Register
   ↓
Login
   ↓
Access Token + Refresh Token
   ↓
Authenticated API Request
   ↓
JWT Validation
   ↓
Permission Check
   ↓
API Response
```

The JWT payload has also been customized to include relevant information such as:

```text
role
tenant_id
```

This allows authenticated requests to carry application-specific user context.

---

# 🛡️ Authorization & Permissions

Role-based permission classes have been implemented:

```text
IsRenter
IsSupervisor
IsAssessor
```

These permissions control which API operations can be performed by different roles.

For example:

```text
Renter
   ↓
Limited access

Supervisor
   ↓
Broader inspection access

Assessor
   ↓
Inspection-related operations
```

The exact permissions are enforced at the API level rather than relying only on frontend restrictions.

---

# 🔒 Object-Level Permissions

The project also demonstrates the difference between:

### Role-level permission

```text
"Is this user an Assessor?"
```

and

### Object-level permission

```text
"Is this Assessor assigned to THIS inspection?"
```

For inspection operations, object-level authorization is implemented around the inspection's assigned assessor.

Conceptually:

```text
Request
   ↓
Is authenticated?
   ↓
Does role allow this operation?
   ↓
Is user assigned to this inspection?
   ↓
Allow / Deny
```

A Supervisor can also be permitted to act on the inspection according to the implemented permission rule.

This prevents a user from accessing or modifying an object simply because they have the correct general role.

---

# ✅ Validation & Business Rules

The project demonstrates validation at two different layers.

## Model-Level Validation

Used for rules that belong to the data/model itself.

Examples include:

* Registration number format
* Basic field validation

---

## Serializer-Level Validation

Used for API-specific and cross-field validation.

Examples:

### Odometer

The odometer value should not decrease.

```text
Previous: 45,000 km
New:      46,500 km     ✅

Previous: 45,000 km
New:      43,000 km     ❌
```

### Inspection Date

An inspection cannot have a date that violates the relationship with the vehicle's creation date.

```text
Vehicle created:
01 Jan 2026

Inspection:
05 Jan 2026       ✅

Inspection:
20 Dec 2025       ❌
```

The project intentionally demonstrates both **model-level validation** and **serializer-level `validate()`** so the difference between the two approaches is clear.

---

# 🔎 Search, Filtering & Pagination

Vehicle and Inspection list APIs support:

### Filtering

Implemented using:

```text
django-filter
```

Example:

```text
GET /vehicles/?status=active
```

---

### Search

Search functionality can be implemented across relevant fields using Django query expressions such as:

```text
Q objects
```

This allows multiple fields/conditions to be combined.

---

### Pagination

Large result sets are divided into smaller pages instead of returning every record at once.

Conceptually:

```text
Database
   ↓
Queryset
   ↓
Filtering
   ↓
Search
   ↓
Pagination
   ↓
Serializer
   ↓
JSON Response
```

---

# 🧩 API Design

The project initially uses **hand-written DRF `APIView` classes** for CRUD operations.

This was intentional.

Instead of immediately using:

```text
GenericAPIView
Mixins
ViewSets
Routers
```

the project first implements the request/response flow explicitly.

This makes it easier to understand:

```text
HTTP Request
     ↓
APIView
     ↓
Serializer
     ↓
Model
     ↓
PostgreSQL
     ↓
Model
     ↓
Serializer
     ↓
JSON Response
```

More advanced DRF abstractions can be introduced later after understanding the underlying flow.

---

# 📚 Development Phases

## Phase 0 — Project Setup

Completed:

* Django project setup
* PostgreSQL configuration
* Django app structure
* `accounts`
* `vehicle`
* `inspection`
* `uploads`
* `fleetservice`
* `report`
* `analytics`
* Tenant model
* Custom User model
* `AUTH_USER_MODEL` configured before the first migration

The custom user model was introduced at the beginning to avoid changing the authentication model after database migrations had already been created.

---

## Phase 1 — Plain CRUD

Implemented:

* Vehicle CRUD
* Inspection CRUD
* ChecklistItem CRUD
* UUID primary keys
* Hand-written DRF `APIView` classes

The goal of this phase was to understand the basic CRUD request lifecycle before introducing DRF abstractions such as generic views and ViewSets.

---

## Phase 2 — Validation & Business Rules

Implemented:

* Registration number regex validation
* Odometer validation
* Inspection date validation
* Cross-field validation
* Model-level validators
* Serializer-level `validate()`

The phase demonstrates where different types of validation can be implemented.

---

## Phase 3 — JWT Authentication

Implemented:

* Custom User model
* User roles
* Tenant relationship
* Registration
* Login
* Access tokens
* Refresh tokens
* Custom JWT claims
* `role`
* `tenant_id`

Authentication is implemented using:

```text
djangorestframework-simplejwt
```

Registration is intentionally open at this stage to demonstrate authentication first. Authorization restrictions are introduced in the following phases.

---

## Phase 4 — Role-Based Permissions

Implemented:

```text
IsRenter
IsSupervisor
IsAssessor
```

API access is restricted according to the authenticated user's role.

---

## Phase 4.1 — Object-Level Permissions

Implemented object-specific authorization for inspections.

Example:

```text
Assessor A
    ↓
Assigned to Inspection #123
    ↓
Can perform permitted operations on #123

Inspection #456
    ↓
Assigned to Assessor B
    ↓
Assessor A → Denied
```

This demonstrates why checking only a user's role is not always sufficient.

---

## Phase 5 — Search, Filtering & Pagination

Implemented on Vehicle and Inspection list endpoints:

* Filtering
* Search
* Django `Q` objects where required
* Pagination
* Queryset-based API responses

This phase moves the project beyond basic CRUD toward more practical API functionality.

---

# 🧪 API Testing

The APIs are tested using **Postman**.

Testing includes:

* User registration
* Login
* JWT authentication
* Token refresh
* Vehicle CRUD
* Inspection CRUD
* ChecklistItem CRUD
* Validation failures
* Role-based authorization
* Object-level authorization
* Search
* Filtering
* Pagination

Example authorization test:

```text
Assessor assigned to inspection
        ↓
PATCH inspection
        ↓
200 OK
```

Whereas:

```text
Renter
   ↓
PATCH restricted inspection
   ↓
403 Forbidden
```

The purpose of these tests is to verify both successful operations and intentionally rejected requests.

---

# 🔄 Current Request Flow

A typical authenticated request follows this structure:

```text
Client / Postman
       │
       ▼
   HTTP Request
       │
       ▼
     APIView
       │
       ├──────────────► Authentication
       │                    │
       │                    ▼
       │              JWT Validation
       │
       ├──────────────► Role Permission
       │
       ├──────────────► Object Permission
       │
       ▼
    Serializer
       │
       ├──────────────► Validation
       │
       ▼
    Queryset / Model
       │
       ▼
   PostgreSQL
       │
       ▼
    Serializer
       │
       ▼
   JSON Response
```

---

# 🎯 What I Learned

Through the project, I have worked through the backend development lifecycle progressively:

* Django project and app structure
* Custom user models
* Database relationships
* PostgreSQL integration
* UUID primary keys
* Django models
* Foreign keys
* CRUD APIs
* DRF APIViews
* Serializers
* Model validation
* Serializer validation
* Cross-field validation
* JWT authentication
* Custom JWT claims
* Role-based permissions
* Object-level permissions
* Querysets
* `Q` objects
* Search
* Filtering
* Pagination
* API testing with Postman

The project is intentionally being developed incrementally so that each feature builds on the previous one.

---

# 🛣️ Planned Next Steps

Future phases will extend the backend with features such as:

* Improved tenant isolation
* More granular object permissions
* Image/file upload handling
* Advanced inspection workflows
* Reporting APIs
* Analytics APIs
* Additional filtering and query capabilities
* Vehicle inspection service integration
* `fleetservice` API for future computer-vision integration

These features will be added progressively rather than treating the project as a single large implementation.

---

# 📁 Current Project Status

| Phase | Feature                        | Status      |
| ----- | ------------------------------ | ----------- |
| 0     | Project & database setup       | ✅ Completed |
| 1     | Plain CRUD APIs                | ✅ Completed |
| 2     | Validation & business rules    | ✅ Completed |
| 3     | JWT authentication             | ✅ Completed |
| 4     | Role-based permissions         | ✅ Completed |
| 4.1   | Object-level permissions       | ✅ Completed |
| 5     | Search, filtering & pagination | ✅ Completed |
| 6+    | Additional backend features    | 🔄 Planned  |

---

# 👨‍💻 Project Focus

FleetLog-Ai is primarily a **backend learning and implementation project** focused on understanding how Django and Django REST Framework components work together in a structured API application.

The emphasis is on understanding the underlying concepts first and introducing higher-level abstractions as the project evolves.
