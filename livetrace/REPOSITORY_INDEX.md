# JobNimbus Repository Index

> **Purpose**: Quick reference guide for code searches and issue investigation
> **Last Updated**: 2025-11-24
> **Total Repositories**: 205

---

## Quick Search Guide

### By Issue Type
- **Contact Issues**: `jobnimbus-frontend` (contacts module), `jncore-monolith-api` (/api1/contacts), `dotnet-monolith` (/api2/contacts)
- **Job Issues**: `jobs-frontend` (/jobs/*), `jncore-monolith-api` (/api1/jobs), `dotnet-monolith` (/api2/jobs)
- **Invoice Issues**: `financials-frontend` (/invoices/*), `financials-api` (/api/invoices)
- **Payment Processing**: `payments-frontend`, `payments-backend` (/api/payments), `financials-api`
- **Communication Issues**: `engage` (SMS/calls), `text-messaging`, `notification-center-backend`
- **Estimation Issues**: `sumoquote`, `estimate-signing-frontend`, `measurements-frontend`
- **File Issues**: `files-backend` (/api/files), `file-upload-processor`, `file-upload-postprocessor`, `document-builder`
- **Authentication Issues**: `auth-backend` (JWT/tokens), `auth-ui` (login/signup)
- **Mobile Issues**: `android-*`, `ios-*`, `jnapp-*`
- **Search Issues**: `search`, `globalsearch-opensearch`
- **Reporting Issues**: `reporting-backend`, `reporting-frontend`

### By API Endpoint Pattern
- **/api1/\*** → `jncore-monolith-api` (Legacy Node.js API)
- **/api2/\*** → `dotnet-monolith` (.NET API)
- **/api/invoices** → `financials-api`
- **/api/payments** → `payments-backend`
- **/api/files** → `files-backend`
- **/api/search** → `search`
- **/api/forms** → `forms-backend`
- **/api/automations** → `smart-automations-backend`
- **/engage/\*** → `engage` (PHP API)

### By Frontend URL Pattern
- **/jobs/\***, **/projects/\*** → `jobs-frontend`
- **/invoices/\*** → `financials-frontend`
- **/payments/\*** → `payments-frontend`
- **/checkout/\*** → `payments-checkout-frontend`
- **/estimates/\*** → `sumoquote-frontend`, `estimate-signing-frontend`
- **/measurements/\*** → `measurements-frontend`
- **/forms/\*** → `forms-frontend`
- **/reports/\*** → `reporting-frontend`
- **/boards/\*** → `boards-frontend`
- **/login**, **/signup** → `auth-ui`

---

## Common Error Patterns

### Payment Errors
- "Payment declined", "Payrix error", "Card processing failed" → `payments-backend`
- "Invoice not found", "Invoice creation failed" → `financials-api`
- "Merchant account error" → `payments-backend`

### File Upload Errors
- "Virus detected", "File validation failed" → `file-upload-processor`
- "File too large", "Upload timeout" → `files-backend`
- "S3 upload failed", "Storage error" → `files-backend`
- "Thumbnail generation failed" → `file-upload-postprocessor`

### Authentication Errors
- "Invalid token", "JWT expired", "Unauthorized" → `auth-backend`
- "Login failed", "Invalid credentials" → `auth-ui`, `auth-backend`
- "Session expired" → `auth-backend`

### Database Errors
- PostgreSQL connection/query errors → Check service's database (see Database Ownership Map)
- Couchbase timeout/connection → `jncore-monolith-api`
- DynamoDB throttling → Check Lambda services (`payments-backend`, `auth-backend`, `custom-fields-backend`)
- MySQL errors → `engage`
- CosmosDB/DocumentDB errors → `sumoquote`

### API Errors
- 4xx errors on /api1/* → `jncore-monolith-api`
- 4xx errors on /api2/* → `dotnet-monolith`
- 5xx errors → Check specific microservice API
- CORS errors → `web-router`, API Gateway config
- Rate limiting → API Gateway, specific service

### Communication Errors
- "SMS send failed", "Twilio error" → `text-messaging`, `engage`
- "Email delivery failed" → `notification-center-backend`, `engage`
- "Phone number validation" → `text-messaging`

### Search Errors
- "Search timeout", "OpenSearch error" → `search`
- "Index not found" → `search`, `globalsearch-opensearch`

---

## Database Ownership Map

### PostgreSQL
- `dotnet-monolith` - Primary monolith database
- `financials-api` - Financial data
- `text-messaging` - SMS messages
- `payments-backend` - Payment transactions
- `files-backend` - File metadata
- `notification-center-backend` - Notifications
- `conversations-backend` - Conversation threads
- `job-costing-backend` - Job costs
- `tiered-pricing-backend` - Pricing tiers
- `suppliers` - Supplier data
- `accounts-payable` - AP data

### Couchbase
- `jncore-monolith-api` - Legacy core data (contacts, jobs, activities)

### DynamoDB
- `payments-backend` - Payment processing data
- `accounting-sync-backend` - Sync state and mappings
- `custom-fields-backend` - Custom field definitions
- `auth-backend` - Auth tokens and keys
- `marketing-hub` - Marketing campaigns

### MySQL
- `engage` - SMS, email, call data

### CosmosDB/DocumentDB
- `sumoquote` - Estimate and quote data

### MongoDB
- `forms-backend` - Form definitions and submissions
- `smart-automations-backend` - Automation rules

### Elasticsearch/OpenSearch
- `jncore-monolith-api` - Search indexing (legacy)
- `search` - Modern search service
- `jnapp-backend` - Mobile search

---

## Core Applications

### jobnimbus-frontend
**Purpose**: Main CRM frontend application for JobNimbus
**Tech Stack**: React 19, TypeScript, Nx monorepo, Single-SPA microfrontends, Material UI (migrating to UntitledUI), Tailwind CSS
**URL Routes**: /contacts/*, /activities/*, /settings/*, /dashboard, /calendar/*, /tasks/*
**Key Features**: Job management, contacts, activities, files, financials, communications, settings, custom fields
**Type**: Frontend Application (Microfrontend Architecture)
**Related**: jobnimbus-mcp, web-root, web-state, styles, design-system

### jncore-monolith-api
**Purpose**: Legacy Node.js REST API serving /api1 endpoints for JobNimbus core functionality
**Tech Stack**: Node.js 20+, Express, Couchbase, Elasticsearch, RabbitMQ, MongoDB adapters
**API Endpoints**: /api1/contacts, /api1/jobs, /api1/activities, /api1/files, /api1/users, /api1/tasks, /api1/related, /api1/statuses, /api1/folders
**Key Features**: Public API, file management, user auth, job/contact CRUD, integrations
**Type**: Backend API (Monolith)
**Related**: dotnet-monolith, jncore-* services

### jncore (Package Set)
**Purpose**: Suite of monolithic backend services for legacy JobNimbus core
**Tech Stack**: Node.js (various versions)
**Components**:
- jncore-monolith-api - Primary API
- jncore-monolith-files-api - File operations
- jncore-monolith-workers - Background jobs
- jncore-monolith-ghostscript-workers - PDF/document processing
- jncore-quickbooks-desktop-sync-api - QuickBooks Desktop integration
- jncore-timebased-automation - Scheduled automation
- jncore-adhoc-scripts - Utility scripts
**Type**: Backend Services (Monolith Suite)

### dotnet-monolith
**Purpose**: .NET monolith hosting API2 and background workers
**Tech Stack**: .NET 8, C#, Entity Framework Core, PostgreSQL, RabbitMQ
**API Endpoints**: /api2/contacts, /api2/jobs, /api2/activities, /api2/tasks, /api2/users, /api2/companies, /api2/workflows, /api2/customfields
**Key Features**: API2 endpoints, worker processes, data migrations, business logic
**Type**: Backend API + Workers
**Related**: jncore-monolith-api, various microservices

---

## Communication & Engagement

### engage
**Purpose**: SMS, email, and voice communications platform
**Tech Stack**: PHP 8.3+, CodeIgniter 3, MySQL, TypeScript/Node.js Lambdas, Twilio, Pusher
**API Endpoints**: /engage/sms, /engage/calls, /engage/conversations, /engage/contacts
**Key Features**: Text messaging, call management, conversation tracking, 10DLC registration, contact sync
**Type**: Full-Stack Application (PHP backend + React wrapper)
**Related**: engage-single-spa-wrapper, engage-10dlc-registration, engage-base-infra, text-messaging

### text-messaging
**Purpose**: Modern .NET-based text messaging service replacing Engage PHP components
**Tech Stack**: .NET 8, C#, Clean Architecture (Domain/Infrastructure layers), PostgreSQL
**API Endpoints**: /api/text-messaging/send, /api/text-messaging/receive, /api/text-messaging/conversations
**Key Features**: SMS sending/receiving, message processing, Twilio integration, event-driven architecture
**Type**: Backend Service (Microservice)
**Related**: engage, notification-center-backend

### notification-center-backend
**Purpose**: Centralized notification management system
**Tech Stack**: .NET 8, C#, PostgreSQL, AWS services
**API Endpoints**: /api/notifications, /api/notifications/preferences, /api/notifications/templates
**Key Features**: Multi-channel notifications, delivery tracking, user preferences, notification templates
**Type**: Backend Service (Microservice)
**Related**: text-messaging, engage

---

## Estimating & Sales

### sumoquote
**Purpose**: Comprehensive estimating and quoting platform for roofing contractors
**Tech Stack**: .NET 8, C# (20+ projects), Angular/TypeScript frontend, CosmosDB/DocumentDB, Azure services
**API Endpoints**: /api/sumoquote/estimates, /api/sumoquote/quotes, /api/sumoquote/materials, /api/sumoquote/pricing, /api/sumoquote/measurements
**Key Features**: Estimate creation, material ordering, pricing, measurements, PDF generation, document signing, SumoReport analytics
**Type**: Full-Stack Application (Monolith + Microservices)
**Related**: sumoquote-frontend, sumoquote-standalone-frontend, sumoquote-zapier, estimate-signing-frontend

### estimate-signing-frontend
**Purpose**: Digital signature collection for estimates and proposals
**Tech Stack**: React, TypeScript, Single-SPA microfrontend
**URL Routes**: /estimates/sign/*, /proposals/sign/*
**Key Features**: E-signature workflows, document viewing, signature capture, mobile-friendly
**Type**: Frontend Application (Microfrontend)
**Related**: sumoquote, document-builder, files-backend

### measurements-frontend
**Purpose**: Property measurement and roof diagram tools
**Tech Stack**: React, TypeScript, Single-SPA microfrontend
**URL Routes**: /measurements/*, /diagrams/*
**Key Features**: Measurement imports (EagleView, HoverCraft), diagram editing, area calculations
**Type**: Frontend Application (Microfrontend)
**Related**: sumoquote

---

## Financial Management

### financials-api
**Purpose**: Financial operations API including invoicing and payment tracking
**Tech Stack**: .NET 8, C#, PostgreSQL
**API Endpoints**: /api/invoices, /api/invoices/{id}, /api/payments/history, /api/financials/reports
**Key Features**: Invoice management, payment processing, financial reporting, accounting integrations
**Type**: Backend API (Microservice)
**Related**: financials-frontend, payments-backend, accounting-sync-backend

### financials-frontend
**Purpose**: Financial management UI for invoices, payments, and accounting
**Tech Stack**: React, TypeScript, Single-SPA microfrontend
**URL Routes**: /invoices/*, /financials/*
**Key Features**: Invoice creation, payment collection, financial dashboards
**Type**: Frontend Application (Microfrontend)
**Related**: financials-api, payments-frontend

### payments-backend
**Purpose**: Payment processing backend integrating with Payrix and other payment providers
**Tech Stack**: .NET 8, C#, PostgreSQL, DynamoDB, AWS Lambdas
**API Endpoints**: /api/payments, /api/payments/process, /api/payments/merchants, /api/payments/transactions
**Key Features**: Payment gateway integration, transaction processing, merchant management, fee tracking
**Type**: Backend Service (Microservice)
**Related**: payments-frontend, payments-checkout-frontend, financials-api

### payments-frontend
**Purpose**: Payment management UI
**Tech Stack**: React, TypeScript, Nx monorepo, Single-SPA microfrontend
**URL Routes**: /payments/*, /payments/settings/*
**Key Features**: Payment forms, transaction history, merchant settings
**Type**: Frontend Application (Microfrontend)
**Related**: payments-backend, payments-checkout-frontend

### accounting-sync-backend
**Purpose**: Two-way sync between JobNimbus and accounting systems (QuickBooks, Xero)
**Tech Stack**: .NET 8, C#, AWS Lambda, DynamoDB, PostgreSQL
**API Endpoints**: /api/accounting/sync, /api/accounting/quickbooks, /api/accounting/xero
**Key Features**: Contact sync, invoice sync, payment sync, job sync, credit memo sync, tax sync
**Type**: Backend Service (Event-Driven Lambdas)
**Related**: financials-api, jn-to-sq-sync

### accounts-payable
**Purpose**: Accounts payable management system
**Tech Stack**: .NET 8, C#, Clean Architecture, PostgreSQL, AWS Lambda
**API Endpoints**: /api/ap/bills, /api/ap/vendors, /api/ap/payments
**Key Features**: Bill tracking, vendor management, payment processing, approval workflows
**Type**: Backend Service (Microservice)
**Related**: financials-api, payments-backend

### tiered-pricing-backend
**Purpose**: Pricing tier management for products and services
**Tech Stack**: .NET 8, C#, PostgreSQL
**API Endpoints**: /api/pricing/tiers, /api/pricing/products
**Key Features**: Price tier configuration, volume discounts, customer-specific pricing
**Type**: Backend API (Microservice)
**Related**: tiered-pricing-frontend, products-frontend

---

## Material & Supply Chain

### suppliers
**Purpose**: Material supplier integration platform
**Tech Stack**: .NET 8, C#, PostgreSQL, AWS Lambdas
**API Endpoints**: /api/suppliers, /api/suppliers/catalog, /api/suppliers/orders, /api/suppliers/branches
**Key Features**: Supplier catalog sync, product mapping, order management, branch management, pricing updates
**Type**: Backend Service (Microservice + Lambdas)
**Related**: supplier-settings-frontend, material-order-frontend, products-frontend

### material-order-frontend
**Purpose**: Material ordering UI for placing orders with suppliers
**Tech Stack**: React, TypeScript, Single-SPA microfrontend
**URL Routes**: /materials/order/*, /suppliers/orders/*
**Key Features**: Order creation, supplier selection, product search, order tracking
**Type**: Frontend Application (Microfrontend)
**Related**: suppliers, products-frontend

### products-frontend
**Purpose**: Product and service catalog management
**Tech Stack**: React, TypeScript, Single-SPA microfrontend
**URL Routes**: /products/*, /catalog/*
**Key Features**: Product creation, pricing, categorization, supplier mapping
**Type**: Frontend Application (Microfrontend)
**Related**: suppliers, material-order-frontend

---

## Files & Documents

### files-backend
**Purpose**: File management backend for document storage and processing
**Tech Stack**: .NET 8, C#, PostgreSQL, AWS S3, Lambda processors
**API Endpoints**: /api/files, /api/files/upload, /api/files/{id}, /api/files/share, /api/files/folders
**Key Features**: File upload/download, thumbnail generation, file organization, sharing, metadata management
**Type**: Backend Service (Microservice + Lambdas)
**Related**: file-upload-processor, file-upload-postprocessor, document-builder

### file-upload-processor
**Purpose**: Processes uploaded files for virus scanning and validation
**Tech Stack**: Node.js, TypeScript, AWS Lambda
**API Endpoints**: Event-driven (S3 triggers), no direct HTTP endpoints
**Key Features**: File validation, virus scanning, metadata extraction, S3 integration
**Type**: Backend Service (Lambda)
**Related**: files-backend, file-upload-postprocessor

### file-upload-postprocessor
**Purpose**: Post-processing of uploaded files (resizing, conversion, indexing)
**Tech Stack**: Node.js, TypeScript, AWS Lambda
**API Endpoints**: Event-driven (S3/SNS triggers), no direct HTTP endpoints
**Key Features**: Image resizing, format conversion, search indexing
**Type**: Backend Service (Lambda)
**Related**: files-backend, file-upload-processor

### document-builder
**Purpose**: Template-based document generation
**Tech Stack**: Node.js, TypeScript, AWS Lambda, React frontend
**API Endpoints**: /api/documents/templates, /api/documents/generate, /api/documents/preview
**Key Features**: Document templates, merge fields, PDF generation, document preview
**Type**: Full-Stack Application (Backend Lambdas + Frontend)
**Related**: files-backend, estimate-signing-frontend

---

## Search & Discovery

### search
**Purpose**: Dedicated search service with OpenSearch backend
**Tech Stack**: .NET 8 API, Node.js Lambda mappers, AWS OpenSearch, MSK Kafka
**API Endpoints**: /api/search, /api/search/contacts, /api/search/jobs, /api/search/documents
**Key Features**: Real-time indexing, complex authorization, sub-200ms queries, multi-type search (contacts, jobs, documents)
**Type**: Backend Service (API + Event-Driven)
**Related**: globalsearch-opensearch, jn-opensearch

---

## Jobs & Projects

### jobs-frontend
**Purpose**: Job/project management UI
**Tech Stack**: React, TypeScript, Single-SPA microfrontend
**URL Routes**: /jobs/*, /projects/*
**Key Features**: Job creation, status tracking, workflow management, job details
**Type**: Frontend Application (Microfrontend)
**Related**: job-costing-backend, boards-frontend

### job-costing-backend
**Purpose**: Job costing and profitability tracking
**Tech Stack**: .NET 8, C#, PostgreSQL, AWS Lambda
**API Endpoints**: /api/job-costing, /api/job-costing/budgets, /api/job-costing/profitability
**Key Features**: Cost tracking, budget management, profitability analysis
**Type**: Backend Service (Microservice)
**Related**: jobs-frontend, financials-api

### boards-frontend
**Purpose**: Kanban-style project boards for job workflow visualization
**Tech Stack**: React, TypeScript, Single-SPA microfrontend
**URL Routes**: /boards/*, /workflow/*
**Key Features**: Drag-and-drop boards, workflow stages, job cards
**Type**: Frontend Application (Microfrontend)
**Related**: jobs-frontend

---

## Forms & Workflows

### forms-backend
**Purpose**: Custom form builder and submission management backend
**Tech Stack**: Node.js, TypeScript, MongoDB
**API Endpoints**: /api/forms, /api/forms/{id}, /api/forms/submissions, /api/forms/webhooks
**Key Features**: Form creation, field types, submission storage, webhook triggers
**Type**: Backend Service (Microservice)
**Related**: forms-frontend

### forms-frontend
**Purpose**: Form builder and viewer UI
**Tech Stack**: React, TypeScript, Single-SPA microfrontend
**URL Routes**: /forms/*, /forms/builder/*, /forms/submissions/*
**Key Features**: Drag-and-drop form builder, form rendering, submission viewing
**Type**: Frontend Application (Microfrontend)
**Related**: forms-backend

### smart-automations-backend
**Purpose**: Workflow automation engine
**Tech Stack**: Node.js, TypeScript, MongoDB
**API Endpoints**: /api/automations, /api/automations/triggers, /api/automations/actions
**Key Features**: Trigger configuration, action execution, automation rules
**Type**: Backend Service (Microservice)
**Related**: smart-automations-frontend

### smart-automations-frontend
**Purpose**: Automation builder UI
**Tech Stack**: React, TypeScript, Single-SPA microfrontend
**URL Routes**: /automations/*, /workflow/automations/*
**Key Features**: Automation creation, trigger setup, action configuration
**Type**: Frontend Application (Microfrontend)
**Related**: smart-automations-backend

---

## Custom Fields & Configuration

### custom-fields-backend
**Purpose**: Dynamic custom field management system
**Tech Stack**: Node.js, TypeScript, AWS Lambda, DynamoDB
**API Endpoints**: /api/custom-fields, /api/custom-fields/definitions, /api/custom-fields/values
**Key Features**: Custom field definitions, field types, validation, job field sync
**Type**: Backend Service (Lambda-based)
**Related**: job-field-settings-frontend

### job-field-settings-frontend
**Purpose**: Job field configuration UI
**Tech Stack**: React, TypeScript, Single-SPA microfrontend
**URL Routes**: /settings/job-fields/*, /settings/custom-fields/*
**Key Features**: Field visibility, required fields, field ordering
**Type**: Frontend Application (Microfrontend)
**Related**: custom-fields-backend

---

## Authentication & Authorization

### auth-backend
**Purpose**: Authentication and authorization services
**Tech Stack**: Node.js, TypeScript, AWS Lambda, DynamoDB
**API Endpoints**: /api/auth/login, /api/auth/token, /api/auth/validate, /api/auth/refresh
**Key Features**: JWT validation, API key management, authorizer Lambda, resource tokens, S2S authentication
**Type**: Backend Service (Lambda-based)
**Related**: auth-ui

### auth-ui
**Purpose**: Authentication UI (login, signup, password reset)
**Tech Stack**: React, TypeScript
**URL Routes**: /login, /signup, /reset-password, /forgot-password
**Key Features**: Login forms, OAuth integration, password management
**Type**: Frontend Application
**Related**: auth-backend

---

## Reporting & Analytics

### reporting-backend
**Purpose**: Business intelligence and reporting backend
**Tech Stack**: Node.js, Python (ETL), PostgreSQL, Redshift
**API Endpoints**: /api/reports, /api/reports/generate, /api/reports/schedule, /api/reports/data
**Key Features**: Report generation, data aggregation, custom reports, JN data loading
**Type**: Backend Service (Microservice + ETL)
**Related**: reporting-frontend

### reporting-frontend
**Purpose**: Reporting dashboard UI
**Tech Stack**: React, TypeScript, Single-SPA microfrontend
**URL Routes**: /reports/*, /analytics/*, /insights/*
**Key Features**: Report builder, chart visualizations, scheduled reports
**Type**: Frontend Application (Microfrontend)
**Related**: reporting-backend

---

## Infrastructure & DevOps

### cd-pipeline-infra
**Purpose**: Continuous deployment pipeline infrastructure
**Tech Stack**: OpenTofu/Terraform, Python (Lambda), AWS Step Functions, API Gateway
**Key Features**: Multi-service deployments (Lambda, ECS, Terraform, static), dynamic environments, deployment orchestration, API-driven
**Type**: Infrastructure (IaC)
**Related**: cicd-infra, cd-dashboard

### jnlocal
**Purpose**: Unified CLI tool for local development and deployments
**Tech Stack**: Go 1.22+
**Key Features**: Generate .env files, deploy services, manage dynamic environments, query deployments, Terraform env vars
**Type**: CLI Tool
**Related**: cd-pipeline-infra, all service repos

### jn-base-infra
**Purpose**: Foundation infrastructure for JobNimbus AWS accounts
**Tech Stack**: Terraform
**Key Features**: VPC, subnets, security groups, Route53, CloudFront base
**Type**: Infrastructure (IaC)
**Related**: jn-shared-infra, app-base-networking

### jn-shared-infra
**Purpose**: Shared infrastructure resources across applications
**Tech Stack**: Terraform
**Key Features**: Shared databases, caches, message queues, IAM roles
**Type**: Infrastructure (IaC)
**Related**: jn-base-infra

### spacelift-infra
**Purpose**: Spacelift.io IaC management platform configuration
**Tech Stack**: Terraform
**Key Features**: Stack configuration, policies, worker pools
**Type**: Infrastructure (IaC)
**Related**: All Terraform repos

---

## Mobile Applications

### android-leads-sales-projects
**Purpose**: Android app for leads and sales management
**Tech Stack**: Kotlin, Android SDK
**Key Features**: Lead capture, sales tracking, mobile CRM
**Type**: Mobile Application (Android)
**Related**: jobnimbus-frontend

### ios-leads-sales-projects
**Purpose**: iOS app for leads and sales management
**Tech Stack**: Swift, iOS SDK
**Key Features**: Lead capture, sales tracking, mobile CRM
**Type**: Mobile Application (iOS)
**Related**: jobnimbus-frontend

### jnapp-backend
**Purpose**: Backend services for JobNimbus mobile app (legacy)
**Tech Stack**: NestJS, TypeScript, gRPC, Protobuf, Elasticsearch, KafkaJS
**Key Features**: Document signing (dsign), mobile-specific APIs, protobuf services
**Type**: Backend Service (Microservices)
**Related**: jnapp-frontend, android/ios apps

### jnapp-frontend
**Purpose**: Mobile-optimized web application components
**Tech Stack**: Angular 18, TypeScript, Nx monorepo, Material Angular, NgXS state management
**Key Features**: Web elements, mobile widgets, financial integrations, payment checkout
**Type**: Frontend Application (Web Components)
**Related**: jnapp-backend, android/ios apps

---

## Marketing & Integrations

### marketing-hub
**Purpose**: Marketing automation and campaign management
**Tech Stack**: .NET 8 API, React frontend, DynamoDB, Node.js Lambdas
**Key Features**: Campaign creation, contact segmentation, email/SMS campaigns, conversation simulator
**Type**: Full-Stack Application
**Related**: engage, text-messaging

### zapier
**Purpose**: Zapier integration app for JobNimbus
**Tech Stack**: Node.js, TypeScript
**Key Features**: Triggers, actions, authentication for Zapier platform
**Type**: Integration Service
**Related**: sumoquote-zapier

### sumoquote-zapier
**Purpose**: Zapier integration specifically for SumoQuote
**Tech Stack**: Node.js, TypeScript
**Key Features**: SumoQuote triggers/actions, estimate automation
**Type**: Integration Service
**Related**: sumoquote, zapier

---

## Web Infrastructure

### web-root
**Purpose**: Single-SPA root configuration for microfrontend orchestration
**Tech Stack**: JavaScript, Single-SPA, SystemJS
**Key Features**: Microfrontend loading, routing, shared dependencies
**Type**: Frontend Infrastructure
**Related**: All *-frontend repos, web-state

### web-state
**Purpose**: Shared state management across microfrontends
**Tech Stack**: JavaScript, Redux
**Key Features**: Global state, user context, cross-app communication
**Type**: Frontend Library
**Related**: web-root, jobnimbus-frontend

### web-router
**Purpose**: Routing and navigation for web applications
**Tech Stack**: Node.js, AWS Lambda
**Key Features**: Dynamic routing, URL rewriting, legacy URL handling
**Type**: Backend Service (Lambda)
**Related**: web-root

---

## Specialty Services

### conversations-backend
**Purpose**: Conversation thread management (combines calls, texts, emails)
**Tech Stack**: .NET 8, C#, PostgreSQL
**API Endpoints**: /api/conversations, /api/conversations/{id}, /api/conversations/threads
**Key Features**: Unified conversation view, thread aggregation, contact history
**Type**: Backend Service (Microservice)
**Related**: engage, text-messaging, notification-center-backend

### sunlight-financial
**Purpose**: Sunlight Financial lending integration
**Tech Stack**: Node.js, TypeScript
**API Endpoints**: /api/sunlight/applications, /api/sunlight/credit-check
**Key Features**: Financing application, credit checks, loan processing
**Type**: Backend Service (Integration)
**Related**: financials-api

### jn-to-sq-sync
**Purpose**: JobNimbus to SumoQuote data synchronization
**Tech Stack**: .NET 8, C#, AWS Lambda
**API Endpoints**: Event-driven (Lambda), no direct HTTP endpoints
**Key Features**: Estimate sync, contact sync, job sync between platforms
**Type**: Backend Service (Sync Lambda)
**Related**: sumoquote, jncore-monolith-api

### jn-srs-integration-backend
**Purpose**: JobNimbus to SRS (roofing supplier) integration
**Tech Stack**: .NET 8, C#
**API Endpoints**: /api/srs/orders, /api/srs/pricing, /api/srs/tracking
**Key Features**: Material ordering, price sync, order tracking
**Type**: Backend Service (Integration)
**Related**: suppliers

---

## Data & Analytics

### lakehouse
**Purpose**: Data lake/warehouse infrastructure
**Tech Stack**: Terraform, AWS Glue, Athena, S3
**Key Features**: Data ingestion, ETL pipelines, analytics storage
**Type**: Infrastructure + Data Engineering
**Related**: raw-data-infra, datalake-normalization

### raw-data-infra
**Purpose**: Raw data ingestion infrastructure
**Tech Stack**: Python (Lambda), AWS services, Docker images for ingestion
**Key Features**: HubSpot, Stripe, Payrix, Chargebee data ingestion, webhook validation
**Type**: Infrastructure + Data Pipeline
**Related**: lakehouse

---

## Design & Development Tools

### design-system
**Purpose**: Design system documentation and assets
**Tech Stack**: Storybook, React, CSS
**Key Features**: Component library, design tokens, style guide
**Type**: Documentation + Library
**Related**: jobnimbus-frontend, styles

### styles
**Purpose**: Shared CSS/SCSS styles and design tokens
**Tech Stack**: SCSS, CSS variables
**Key Features**: Color palettes, typography, spacing
**Type**: Frontend Library
**Related**: design-system, jobnimbus-frontend

### jobnimbus-claude-plugin-marketplace
**Purpose**: Claude AI plugins for JobNimbus engineering workflows
**Tech Stack**: Markdown (instructions), various tools
**Key Features**: Engineering standards, design patterns, Terraform helpers, jnlocal plugins
**Type**: AI Assistant Extensions
**Related**: jnlocal, engineering-standards

### engineering-standards
**Purpose**: Engineering best practices and guidelines documentation
**Tech Stack**: Markdown
**Key Features**: Coding standards, architecture patterns, review checklists
**Type**: Documentation
**Related**: jobnimbus-claude-plugin-marketplace

### JobNimbus.Templates
**Purpose**: .NET project templates for microservices
**Tech Stack**: .NET templates
**Key Features**: Lambda templates, API templates, test templates
**Type**: Development Templates
**Related**: All .NET microservices

---

## Testing Infrastructure

### lionAutomation
**Purpose**: E2E testing automation framework
**Tech Stack**: Playwright, TypeScript, Node.js
**Key Features**: Browser automation, test suites, CI/CD integration
**Type**: Testing Infrastructure
**Related**: gazelleAutomation, android-e2e-automation

### gazelleAutomation
**Purpose**: Python-based E2E testing framework
**Tech Stack**: Python, Selenium
**Key Features**: Web automation, test scenarios, reporting
**Type**: Testing Infrastructure
**Related**: lionAutomation

---

## AI & Innovation

### jobnimbus-mcp
**Purpose**: Model Context Protocol (MCP) server providing Claude AI access to JobNimbus data
**Tech Stack**: TypeScript, Node.js, MCP SDK
**Key Features**: Job data access, contact lookup, activity retrieval for AI assistants
**Type**: Integration Service (MCP Server)
**Related**: jobnimbus-frontend

### ai-platform-spike
**Purpose**: AI/ML platform experimentation and POCs
**Tech Stack**: Python, AWS services (Lambda, Bedrock), Portkey.ai
**Key Features**: AI assistant chat, model routing, prompt management
**Type**: Backend Service (Experimental)
**Related**: hack-* repos

---

## Summary Statistics

- **Total Repositories**: 205
- **Primary Languages**: TypeScript/JavaScript (80+), C#/.NET (40+), Python (20+), Go (5+), PHP (2)
- **Frontend Frameworks**: React (primary), Angular (legacy mobile), Single-SPA (architecture)
- **Backend Frameworks**: .NET 8, NestJS, Node.js/Express, PHP/CodeIgniter
- **Databases**: PostgreSQL, DynamoDB, Couchbase, MySQL, CosmosDB/DocumentDB, MongoDB, Elasticsearch/OpenSearch
- **Infrastructure**: Terraform/OpenTofu, AWS services (Lambda, ECS, S3, API Gateway, etc.)
- **Key Architectural Patterns**: Microservices, Microfrontends (Single-SPA), Event-Driven (MSK/Kafka), Lambda Functions
