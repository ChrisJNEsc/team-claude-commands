# Feature → Repository Mapping

Quick lookup: Feature area → which repo(s) to investigate.

## Frontend Only
| Feature | Repo | Path Hint |
|---------|------|-----------|
| Boards/Kanban | jobnimbus-frontend | libs/features/boards |
| Contact/Job Details | jobnimbus-frontend | libs/features/contact-details, libs/features/job-details |
| Navigation/Search | jobnimbus-frontend | libs/features/navigation, libs/features/search |
| Tasks | jobnimbus-frontend | libs/features/tasks |
| Activity Feed | jobnimbus-frontend | libs/features/activities |
| Calendar | jobnimbus-frontend | libs/features/calendar |
| Documents | jobnimbus-frontend | libs/features/documents |
| Photos | jobnimbus-frontend | libs/features/photos |
| Forms | jobnimbus-frontend | libs/features/forms |
| E-Signature | jobnimbus-frontend | libs/features/esignature |
| Home Page | jobnimbus-frontend | libs/features/home |
| Invoices UI | jobnimbus-frontend | libs/features/invoices |
| Estimates UI | jobnimbus-frontend | libs/features/estimates |
| Payments UI | jobnimbus-frontend | libs/features/payments |
| Reports/Insights | jobnimbus-frontend | libs/features/reports, libs/features/insights |
| Settings UI | jobnimbus-frontend | libs/features/settings |
| Admin Panel UI | jobnimbus-frontend | libs/features/admin |

## Backend Only
| Feature | Repo | Path Hint |
|---------|------|-----------|
| Core API/Entities | dotnet-monolith | src/Api, src/Domain |
| Automations Engine | dotnet-monolith | src/Automations |
| Webhooks | dotnet-monolith | src/Webhooks |
| QuickBooks Sync | dotnet-monolith | src/Integrations/QuickBooks |
| Import/Export | dotnet-monolith | src/Import, src/Export |
| PDF Generation | dotnet-monolith | src/Pdf |
| Email Service | dotnet-monolith | src/Email |
| Supplier Orders | suppliers | src/ |

## Full-Stack (check both)
| Feature | Frontend | Backend |
|---------|----------|---------|
| Engage/Messaging | engage | engage-*, dotnet-monolith |
| Notifications | jobnimbus-frontend | dotnet-monolith |
| Payments/FinTech | jobnimbus-frontend | dotnet-monolith |
| EagleView/HOVER | jobnimbus-frontend | dotnet-monolith |
| Material Orders | jobnimbus-frontend | suppliers, dotnet-monolith |
| Public API issues | N/A | dotnet-monolith |
| Zapier | jobnimbus-frontend | dotnet-monolith |

## Mobile
| Feature | Repo |
|---------|------|
| iOS App | ios-app |
| Android App | android-leads-sales-projects |

## Decision Tree
```
Is it UI-only (styling, layout, component behavior)?
  → Frontend repo only

Is it data/API (wrong data, missing fields, sync issues)?
  → Backend repo (dotnet-monolith) first, then check if FE caching issue

Is it integration (QuickBooks, EagleView, suppliers)?
  → Backend repo for integration logic

Is it Engage/messaging?
  → engage (FE) + engage-* services (BE)

Is it mobile?
  → ios-app or android-leads-sales-projects
```
