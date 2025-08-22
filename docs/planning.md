# Budget & Expense Tracking System – Requirements & Design Document

## 1. Project Overview
**Description**  
A lightweight Django web application that lets authenticated users create budgets, record expenses against those budgets, and view remaining balances and aggregate spending in a simple dashboard. The prototype focuses on clarity, maintainability, and practicing structured Django development (models, views, templates, forms, auth, and a touch of progressive enhancement with HTMX/Alpine.js).

**Primary Goals**  
- Learn / reinforce Django fundamentals (project/app layout, ORM, auth, templates, forms, class-based views).  
- Establish a clean, extensible foundation to iteratively add optional features later (receipts, notifications, charts).  
- Deliver a Minimum Viable Product (MVP) with clear separation of concerns and documented decisions.  
- Keep setup friction low (SQLite, built‑in auth, minimal dependencies).  

**Success Criteria (MVP)**  
- A user can sign up, log in, create budgets, add expenses, and view remaining funds per budget.  
- Dashboard summarises total expenses and per‑budget remaining amounts.  
- Basic validations prevent inconsistent or invalid data (e.g., negative amounts).  
- Code is organized with clear models, URLs, templates, and tests for core flows.  

**Out of Scope (initial MVP)**  
- Multi‑currency support, advanced reporting, collaboration / shared budgets.  
- Real-time notifications, async tasks.  
- Production deployment hardening (scalability, containerization).  

## 2. Core Features (MVP Scope)
1. Budget Management  
   - Create budget (name, total amount, start date, optional end date).  
   - List user budgets with remaining & spent amounts.  
   - Update / archive (soft delete or status flag).  
2. Expense Management  
   - Add expense to a selected budget (description, amount, date, optional category text).  
   - List expenses under a budget (most recent first).  
   - Edit / delete (soft or hard delete—initially hard delete for simplicity).  
3. Dashboard  
   - Aggregate view: per-budget spent vs remaining.  
   - Total expenses across all active budgets (current period filter optional later).  
4. User Authentication  
   - Sign up, login, logout (Django auth).  
   - Password reset (optional stretch—nice to configure).  
5. UX Enhancements (Light)  
   - Inline expense add form via HTMX partial update on budget detail page.  
   - Alpine.js for small interactive toggles (e.g., show/hide forms).  

**Non‑Functional Requirements**  
- Security: Enforce object ownership (no cross-user access).  
- Performance: Efficient queries with annotations for aggregates.  
- Reliability: Validation of monetary fields using Decimal.  
- Test Coverage: Core model logic, permissions, and primary CRUD flows.  

## 3. Optional Features (Future Roadmap)
- Receipt File Uploads (image/PDF) attached to an expense.  
- Notifications (email or in-app reminders) when spending nears a threshold (e.g., >80%).  
- Interactive charts (Chart.js or Plotly) on dashboard.  
- Categorization taxonomy (separate Category model + filtering/reporting).  
- Export (CSV / XLSX) of budgets and expenses.  
- Multi-user collaboration (shared budgets, role-based access).  
- API (REST or GraphQL) for integration / mobile.  

## 4. User Stories (MVP)
1. As a user, I can register and log in so that my budgets and expenses are private to me.  
   - Acceptance: After signup/login, redirected to dashboard; unauthorized users redirected to login.  
2. As a user, I can create a budget so I can track expenses against a planned amount.  
   - Acceptance: Budget appears in my budget list with 0 spent and full remaining amount.  
3. As a user, I can add an expense to a budget so I can record money I spent.  
   - Acceptance: Expense list updates and budget remaining decreases accurately.  
4. As a user, I can view a dashboard summarizing each budget’s remaining and total spending so I see my financial status quickly.  
   - Acceptance: Dashboard loads within one query set (aggregated) per user (efficient).  
5. As a user, I can edit or delete an expense so I can correct mistakes.  
   - Acceptance: Editing updates aggregates; deleting reduces spent totals accordingly.  
6. As a user, I can update a budget’s name or amount (if needed) so my plan stays current.  
   - Acceptance: Validation prevents lowering total below already spent amount.  

## 5. Data Model (Initial Draft)
Using Django’s default `User` (no custom user yet). Decimal fields use `max_digits=10, decimal_places=2`.

### Entities & Fields
**User** (Django `auth.User`)  
- (Standard fields)  
- Relation: 1 User → many Budgets, Expenses (ownership).  

**Budget**  
- id (PK, auto)  
- user (FK → User, CASCADE)  
- name (CharField, 100)  
- total_amount (Decimal)  
- start_date (DateField)  
- end_date (DateField, null/blank)  
- status (CharField: active|archived, default=active)  
- created_at (DateTime, auto_add)  
- updated_at (DateTime, auto_now)  

Derived / Aggregated (not stored):  
- spent_amount (Sum of related expenses)  
- remaining_amount = total_amount - spent_amount  
- percent_used = (spent_amount / total_amount) * 100 (guard divide-by-zero)  

**Expense**  
- id (PK)  
- budget (FK → Budget, CASCADE)  
- user (FK → User, CASCADE - redundancy to ease permission checks & potential future denormalization)  
- description (CharField, 255)  
- amount (Decimal)  
- date (DateField, default=today)  
- category (CharField, 50, optional)  
- notes (TextField, optional)  
- created_at (DateTime, auto_add)  

**Receipt** (Optional future)  
- id (PK)  
- expense (OneToOne → Expense, CASCADE)  
- file (FileField / ImageField)  
- original_filename (CharField)  
- mime_type (CharField)  
- size_bytes (PositiveInteger)  
- uploaded_at (DateTime, auto_add)  

### Relationships
- User 1—* Budget  
- Budget 1—* Expense  
- Expense 1—0..1 Receipt  

### Constraints & Validation
- Budget `total_amount` > 0.  
- Cannot set `total_amount` lower than current spent (custom clean method).  
- Expense `amount` > 0.  
- Dates: `end_date` >= `start_date` (if provided).  
- Ownership enforced in queries & view permissions.  

### Indexing / Performance
- Index on `(user, name)` for budgets.  
- Index on `(budget, date)` for expenses.  
- Potential annotation query for dashboard: `Budget.objects.filter(user=u).annotate(spent=Sum('expense__amount'))`.  

## 6. System Design (Lite)
**Architecture**  
- Monolithic Django app (e.g., core app name: `finance`).  
- Layers: Models → (Optional) Services/helpers (aggregate calculations) → Class-Based Views (ListView, CreateView, UpdateView) → Templates & Partial Templates.  
- Forms: Django ModelForms for `Budget`, `Expense`.  
- Interactivity: HTMX endpoints return partial HTML fragments (expense list, budget row refresh). Alpine.js for small UI toggles.

**Technology Choices**  
- Backend: Django (latest stable).  
- DB: SQLite (dev).  
- Templating: Django templates + partial includes for reuse.  
- Styling: Simple utility-first (optionally Tailwind via CDN) or minimal custom CSS initially.  
- Auth: Django built-in.  

**Security / Authorization**  
- All budget/expense views require login (`LoginRequiredMixin`).  
- Querysets filtered by `user`.  
- Attempt to access others’ objects returns 404 (object-level filter).  
- CSRF tokens included in HTMX forms.  

**Routing (Draft)**  
- `/` → redirect to `/dashboard/` (if authenticated) or `/accounts/login/`.  
- `/dashboard/` → summary view.  
- `/budgets/` → list budgets.  
- `/budgets/add/` → create budget.  
- `/budgets/<id>/` → budget detail (expenses + add-expense form).  
- `/budgets/<id>/edit/` → edit budget.  
- `/expenses/<id>/edit/` → edit expense.  
- `/expenses/<id>/delete/` → delete expense (POST).  
- HTMX endpoints may reuse same URLs responding with partial templates when `HX-Request` header present.  

**Templates (Key)**  
- `base.html` (layout, nav, flash messages).  
- `dashboard.html` (aggregate cards).  
- `budget_list.html`  
- `budget_detail.html` (includes: expense table partial, add expense form partial).  
- `partials/_expense_row.html`, `partials/_budget_row.html`  
- Auth templates (`registration/login.html`, etc.).  

**Aggregations**  
- Use `QuerySet.annotate` for spent totals; fallback to property computing with cached value if needed.  
- Potential service helper: `calculate_budget_aggregates(user)` to centralize logic.  

**Error Handling & Feedback**  
- Form validation errors displayed inline.  
- Use Django messages framework for create/update/delete success.  

**Logging (Minimal)**  
- Basic Django logging config (INFO) + debug toolbar optional during development.  

**Extensibility Considerations**  
- Keep receipt logic behind a feature flag (separate app or model can be added without altering core flows).  
- Provide placeholder `category` CharField now; can migrate to a normalized `Category` model later.  

## 7. Wireframe Descriptions (Text Only)
**Budget List Page**  
- Header: “My Budgets” + button [Add Budget].  
- Table/List: Columns (Name | Period | Spent | Remaining | % Used | Actions).  
- Each row includes small progress bar (CSS width = percent used).  
- If none: message “No budgets yet. Create one to get started.”  

**Budget Detail Page**  
- Top section: Budget name, date range, total, spent, remaining, percentage bar.  
- Action buttons: Edit Budget, (optional) Archive.  
- Expenses section: Table (Date | Description | Category | Amount | Actions).  
- Inline Add Expense form (fields: description, amount, date, category) collapsible.  
- On submit (HTMX), expense table refreshes without full page reload.  

**Add/Edit Expense Form**  
- Fields stacked with labels; primary button at bottom.  
- Validation messages under each field.  
- Cancel returns to budget detail.  

**Dashboard Summary**  
- Cards: (Total Budgets Active, Total Spent, Total Remaining).  
- List / grid of budgets with mini bars.  
- (Future) Chart placeholder area.  

## 8. Development Plan
### Phase 0: Project Setup
- Create virtual environment, install Django.  
- `django-admin startproject config` & app `finance`.  
- Configure settings (installed apps, templates, static).  
- Setup base template & navigation scaffold.  
- Configure auth URLs.  

### Phase 1: Models & Migrations
- Implement `Budget`, `Expense` models.  
- (Stub) `Receipt` model commented or in separate file (not migrated yet).  
- Run migrations.  
- Register models in admin for quick inspection.  

### Phase 2: Budget CRUD
- List, create, update, detail (without expenses initially).  
- Add validation logic (cannot reduce total below spent).  
- Tests: model str, creation, ownership filtering.  

### Phase 3: Expense CRUD
- Add expense create on budget detail (standard view first, then HTMX).  
- Edit & delete expense views.  
- Aggregate calculations (annotation).  
- Tests: expense creation, deletion, aggregate correctness.  

### Phase 4: Dashboard
- Implement summary view with aggregates.  
- Optimize queries (prefetch/annotate).  
- Tests: dashboard context values.  

### Phase 5: UX Enhancements (HTMX / Partial Templates)
- Convert expense add form to inline HTMX form returning updated expense table partial.  
- Add progress bars for budgets.  

### Phase 6: Hardening & Polish
- Access control tests (ensure user cannot access others’ budgets/expenses).  
- Add messages framework integration.  
- Basic styling (Tailwind via CDN if chosen).  

### Phase 7: Optional Seeds & Docs
- Create management command or fixture for sample data.  
- Update README with setup instructions.  

### Phase 8 (Future Enhancements Roadmap)
- Receipts: Add model, file upload handling, media settings.  
- Notifications: Threshold detection service + email backend.  
- Charts: Add endpoint returning JSON and embed Chart.js.  

### Testing Strategy
- Unit Tests: Models (validations), views (CRUD), permissions, aggregation accuracy.  
- Integration: Dashboard summary values, HTMX request returns partial.  
- Manual QA Checklist: Create budget → add expenses → edit/delete expense → aggregate updates → login/logout flows.  

### Risks & Mitigations
- Decimal rounding issues → use Decimal consistently; format in templates.  
- Performance with aggregation → keep dataset small (prototype); later add indexes.  
- Feature creep → adhere to MVP phases; optional features gated.  

### Tooling / Dependencies (Initial)
- Django (core).  
- (Optional) django-debug-toolbar (dev).  
- Tailwind CDN (optional).  
- HTMX (CDN) + Alpine.js (CDN).  

## 9. Acceptance Checklist (MVP Done When)
- [ ] User can register, log in, log out.  
- [ ] Create/list/update budgets.  
- [ ] Add/edit/delete expenses.  
- [ ] Dashboard shows correct aggregates.  
- [ ] Ownership enforced (tests).  
- [ ] Basic styling & usable UX.  
- [ ] Core test suite passing.  

---
**Next Action**: Begin Phase 0 – initialize Django project structure and create app `finance`.
