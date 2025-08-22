# Development Roadmap (MVP + Selected Optional Futures)

> Scope: MVP features (Authentication, Budgets, Expenses, Dashboard). Optional stretch tasks appended at end.

## MVP Task Breakdown

- [ ] 1. Initialize Django Project & Repo
  - Task: Create virtualenv, install Django, `startproject config`, create core app `finance`, commit initial structure.
  - Learning Topic: Django project/app structure, settings modules, virtual environments.

- [ ] 2. Configure Settings & Base Templates
  - Task: Configure `INSTALLED_APPS`, templates dir, static files, time zone, messages, base `base.html` with navigation placeholder.
  - Learning Topic: Django settings (TEMPLATES, STATIC), template inheritance, messages framework basics.

- [ ] 3. Setup Authentication Flows
  - Task: Include `django.contrib.auth` URLs, create signup view/form, login/logout templates, redirect logic.
  - Learning Topic: Django auth views, `UserCreationForm`, `LoginRequiredMixin`, URL routing.

- [ ] 4. Define Budget & Expense Models
  - Task: Implement `Budget` and `Expense` with fields & relationships; add `__str__` and model meta ordering.
  - Learning Topic: Django ORM models, field types (DecimalField, ForeignKey), model conventions.

- [ ] 5. Model Validation & Constraints
  - Task: Add model `clean()` / validation (positive amounts, end_date >= start_date, prevent lowering total below spent via form logic later), create basic unit tests.
  - Learning Topic: Model validation lifecycle, raising `ValidationError`, Django test framework basics.

- [ ] 6. Initial Migrations & Admin Registration
  - Task: Run `makemigrations` / `migrate`, register models in admin with list display & search.
  - Learning Topic: Migration system, Django admin customization.

- [ ] 7. Budget CRUD (List, Create, Detail, Update)
  - Task: Implement class-based views & URL patterns; restrict queryset by user; templates for list/detail/create/edit.
  - Learning Topic: Class-Based Generic Views (ListView, CreateView, UpdateView, DetailView), queryset filtering for ownership.

- [ ] 8. Expense Creation (Standard Form)
  - Task: Add expense create view (initially separate page or included on detail), link from budget detail, ensure ownership enforcement.
  - Learning Topic: ModelForm basics, passing parent object context, form validation.

- [ ] 9. Expense List & Management (Edit/Delete)
  - Task: Show expenses in budget detail (ordered by date desc); add edit & delete views (POST for delete) and confirmation.
  - Learning Topic: URL patterns with PKs, method-based permissions, using `SuccessMessageMixin` or messages framework.

- [ ] 10. Aggregations & Remaining Calculations
  - Task: Annotate budgets with spent sum; compute remaining & percent; add properties or context preparation service.
  - Learning Topic: ORM aggregation (`Sum`, `annotate`), query optimization, avoiding N+1 queries.

- [ ] 11. Dashboard Summary View
  - Task: Implement `/dashboard/` showing aggregate cards and per-budget progress bars using annotated queryset.
  - Learning Topic: Custom CBV / function views, context data composition, template logic vs business logic separation.

- [ ] 12. HTMX Enhancement for Inline Expense Add
  - Task: Replace full-page expense form with inline form on budget detail; partial render updates expense table & budget header.
  - Learning Topic: HTMX request headers, partial templates, progressive enhancement patterns.

- [ ] 13. UI/UX Polish & Feedback
  - Task: Add Tailwind (CDN) or simple CSS, progress bars, messages for CRUD actions, empty-state placeholders.
  - Learning Topic: Template composition (`include`), accessibility basics, feedback patterns.

- [ ] 14. Authentication & Authorization Hardening Tests
  - Task: Add tests ensuring users cannot access others’ budgets/expenses; ensure 404 or redirect behavior.
  - Learning Topic: Test client usage, object-level permission enforcement via filtered querysets.

- [ ] 15. Core Test Suite & Documentation Pass
  - Task: Expand tests (models, views, dashboard aggregates, HTMX partial), add README setup steps, update planning docs if drifted.
  - Learning Topic: Django TestCase patterns, fixtures vs factories, documenting architectural decisions (light ADR mindset).

## Optional (Post-MVP / Stretch)

- [ ] O1. Receipt File Uploads
  - Task: Add `Receipt` model, file upload form, media settings, display thumbnail/link.
  - Learning Topic: FileField handling, MEDIA_URL/MEDIA_ROOT, serving user-uploaded files in dev.

- [ ] O2. Budget Threshold Notifications
  - Task: Add threshold check (e.g., 80%) and trigger message/email when exceeded.
  - Learning Topic: Signals vs service layer, email backend configuration.

- [ ] O3. Interactive Charts on Dashboard
  - Task: Add JSON endpoint & Chart.js integration for spending by budget.
  - Learning Topic: Lightweight API responses (JsonResponse), frontend chart library integration.

- [ ] O4. Category Normalization
  - Task: Introduce `Category` model & migrate existing expense category text.
  - Learning Topic: Data migrations, foreign key refactors, backward compatibility.

- [ ] O5. Export Budgets & Expenses (CSV)
  - Task: Add export view generating CSV for selected budget or all budgets.
  - Learning Topic: StreamingHttpResponse, CSV writing in Python.

## Suggested Learning Order (Parallel Reference)
1. Django project/app layout & settings.
2. Generic class-based views (CRUD patterns).
3. Forms & ModelForms; validation lifecycle.
4. ORM querying, filtering, aggregation & annotations.
5. Auth & permissions (LoginRequiredMixin, object ownership patterns).
6. Templates, inheritance, partials, context processors.
7. HTMX integration (partial responses & progressive enhancement).
8. Testing (unit vs integration, client, fixtures/factories).

---
Next Immediate Action: Start task 1 – initialize project & repository.
