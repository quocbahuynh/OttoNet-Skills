# Task name: Certificate Management APIs

## Overview

The Certificate Management module provides a centralized master list of professional certificates used across the ERP system.

The module allows administrators to maintain certificate master data, which can later be assigned to Technicians and Engineers through the User module and referenced by other ERP modules.

## Scope

- Create Certificate.
- View Certificate List.
- Edit Certificate.
- Delete Certificate.

## Endpoints

GET /api/certificates

POST /api/certificates

PUT /api/certificates/{id}

DELETE /api/certificates/{id}

## Field Rules

| Field | Type | Required | Rule |
| --- | --- | --- | --- |
| Certificate Name | Text | Yes | Must be unique. Maximum 255 characters. |

## Business Rules

1. The system shall maintain a centralized Certificate Master.
2. Certificate Name must be unique.
3. Authorized users can create, edit and delete Certificates.
4. Certificates assigned to one or more Users cannot be deleted.
5. Deleted Certificates shall no longer be available for new assignments.

## Permission Matrix

| Function | Admin | HR |
| --- | --- | --- |
| View Certificate List | Yes | Yes |
| Create Certificate | Yes | Yes |
| Edit Certificate | Yes | Yes |
| Delete Certificate | Yes | Yes |

## Test Cases

| ID | Test Case | Expected Result |
| --- | --- | --- |
| CERT-001 | Create a new Certificate | Certificate is created successfully. |
| CERT-002 | Edit an existing Certificate | Certificate is updated successfully. |
| CERT-003 | Delete an unused Certificate | Certificate is deleted successfully. |
| CERT-004 | Delete a Certificate assigned to Users | System prevents deletion and displays a validation message. |
| CERT-005 | Create a Certificate with a duplicate name | System prevents creation and displays a validation message. |
| CERT-006 | View Certificate List | Certificate list is displayed correctly. |

## Acceptance Criteria

- Users can create, edit and delete Certificate master data.
- Certificate Name is unique across the system.
- Certificates assigned to Users cannot be deleted.
- Deleted Certificates are unavailable for future assignments.
- Certificate List is available for selection in the User module.
- Role-based permissions are enforced for all Certificate Management functions.
