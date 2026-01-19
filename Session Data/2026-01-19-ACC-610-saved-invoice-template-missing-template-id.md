# Analyze-Bug Session: ACC-610

**Date:** 2026-01-19
**Command Version (Hash):** ba88163
**Linear Issue:** ACC-610
**Classification:** Frontend
**Outcome:** Ticket Created

---

## Session Summary

Customer reported that editing a saved invoice template shows "An invoice design template is required to manage line items for this invoice" error, despite having multiple invoice templates configured. Investigation revealed older saved invoice templates lack `template_id` field, causing the frontend to fail finding a matching design template. Proposed frontend fix adds fallback to use first active design template.

---

## User Inputs

**Input 1: Initial Report**
> When navigating to a Job and selecting "Create Invoice" then selecting the drop-down on the saved invoice templates and editing one, it will take you to a page that should allow you to modify the line items for that saved invoice, but the page just says "An invoice design template is required to manage line items for this invoice. Please go to your template settings and create an invoice template." The account has multiple invoice templates and one is selected (typically by default) upon the creation of the invoice. This does not happen in my test account.

**Input 2: Confirmation**
> I did just confirm that creating a new saved invoice template works correctly, so this sounds likely. Here's the information needed on the Linear: JN ID 3gf08c, Comp ID: 3gf08c

**Input 3: Format Request**
> Can you update it to follow the linear ticket hybrid format markdown file in my local files?

---

## Claude's Analysis & Thinking

### Classification
- **Decision:** Frontend
- **Confidence:** High
- **Reasoning:** Error appears despite valid templates being selected - UI isn't receiving/reading the template ID correctly. Works in test account (new templates have `template_id`), fails for older templates (missing `template_id`). API data structure issue manifesting in frontend rendering.

### Investigation Steps
1. Searched for error message in `jobnimbus-frontend` - not found
2. Found related Linear issue ACC-526 (template state issue, fixed in `invoices-frontend`)
3. Cloned `invoices-frontend` repository
4. Located error message in `add-line-items-container.component.tsx:106-117`
5. Traced data flow: `watchDesignTemplateId` from form → `useMemo` lookup → `designTemplate` undefined when no match
6. Found form initialization in `use-edit-invoice-form.ts:98`: `templateId: invoice.template_id || ''`
7. Confirmed `template_id` is optional in `BaseInvoice` model (line 68)
8. Root cause: older saved invoice templates created before `template_id` field was used/required

### Code Analysis
- **Repository:** `invoices-frontend`
- **Files Examined:**
  - `src/app/pages/create-edit-invoice-page/add-line-items/add-line-items-container.component.tsx:51-57, 106-117` - error rendering and template lookup
  - `src/app/pages/create-edit-invoice-page/form/use-edit-invoice-form.ts:98` - form initialization with `template_id`
  - `src/app/pages/create-edit-invoice-page/invoice-details/item-template-input/item-template-input.component.tsx:91-101` - navigation to edit template page
  - `src/models/invoices/invoice.ts:68` - `template_id` field is optional
  - `src/apis/invoices.api.ts:142-153` - `getTemplateDetail` API call
- **Root Cause:** Older saved invoice templates (item templates) lack `template_id` field. When editing, form initializes with empty string, `AddLineItemsContainer.useMemo` finds no matching design template, renders error message.

### Fix Proposal
- **Approach:** Add fallback in `AddLineItemsContainer` to use first active design template when `watchDesignTemplateId` is empty
- **Files to Change:** `src/app/pages/create-edit-invoice-page/add-line-items/add-line-items-container.component.tsx:51-57`
- **Risks:** Low - fallback only triggers when `template_id` is missing, existing behavior unchanged for templates with valid IDs

---

## Outputs

- **Linear Ticket:** [ACC-610](https://linear.app/jobnimbus/issue/ACC-610/invoices-or-invoice-design-template-required-error-when-editing-saved)
- **PR Created:** Not created
- **Branch:** brandykinsman/acc-610

---

## Key Learnings

- Invoice templates have two types: "design templates" (appearance/formatting) and "item templates" (saved invoice templates with line items). The `template_id` field links item templates to design templates.
- Legacy data issues can manifest as frontend errors when required fields were added later - fallback handling is important
- Related issue ACC-526 had similar template state problems - this codebase has a pattern of template field issues
- The `invoices-frontend` repo is separate from `jobnimbus-frontend` - invoice-specific functionality lives there

---

*Session captured: 2026-01-19 11:30*
*Command Version: ba88163*
*Saved by /save-session*
