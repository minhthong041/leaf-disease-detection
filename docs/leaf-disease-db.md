# Schema: leaf_disease_db
Database: pgsql
Tables: 4
Columns are NOT NULL unless marked nullable.

## users
id: bigserial PK
username: varchar(50) unique nullable
fullname: varchar(255)
email: varchar(255) unique nullable
password_hash: varchar(255)
created_at: timestamptz indexed
is_staff: boolean default:false
is_superuser: boolean default:false
updated_at: timestamptz
is_active: boolean default:true
last_login: timestamptz nullable
deleted_at: timestamptz nullable
terms_accepted_at: timestamptz
terms_version: varchar(20)

## diagnosis_histories
id: bigserial PK
user_id: bigint FK
original_image: varchar(500)
processed_image: varchar(500) nullable
status: varchar(20) indexed default:pending
error_message: text nullable
severity: varchar(20) indexed nullable
created_at: timestamptz
updated_at: timestamptz
is_bookmarked: boolean default:false
leaf_area_px: int nullable
lesion_area_px: int nullable
infected_ratio: decimal(5,4) nullable
lesion_count: int nullable
lesions: jsonb nullable

## feedbacks
id: bigserial PK
history_id: bigint FK indexed
title: varchar(255)
description: text
created_at: timestamptz indexed
status: varchar(20) indexed default:pending
updated_at: timestamptz

## error_reports
id: bigserial PK
user_id: bigint FK indexed
title: varchar(255)
description: text
created_at: timestamptz indexed
is_resolved: boolean default:false
updated_at: timestamptz

## Relationships
users.id → diagnosis_histories.user_id (one-to-many)
diagnosis_histories.id → feedbacks.history_id (one-to-many)
users.id → error_reports.user_id (one-to-many)

## Indexes
diagnosis_histories.6f88c2ed-f6b2-43c6-abeb-6d63dc711e94 (index): user_id, created_at
diagnosis_histories.86f07853-c307-48a3-85a9-e32a8b61a78e (index): user_id, is_bookmarked

---
If you suggest changes to this schema, ALSO return them as a DrawSQL patch: one fenced ```json code block, so I can apply them to my diagram. If you are only answering a question, skip the patch.

Patch rules:
- One JSON object with "strategy": "merge"; combine every change into that single patch.
- Reference tables and columns by name. Only include what changes — omit unchanged columns and unused optional fields.
- Column: {"name","type","length","is_primary_key","is_auto_increment","is_nullable","is_unique_key","is_index","is_unsigned","default","enum_values"} — use exact type names for pgsql as shown in the schema above.
- Relationship: {"type":"one-to-many","source_table":"users","source_column":"id","target_table":"posts","target_column":"user_id"} — for "one-to-many" the source is the "one" side; for "many-to-one" the source is the "many" (foreign-key) side. Prefer "one-to-many".
- Add "default_type" ("string" | "function" | "number" | "boolean") when a default could be misread — a literal string "CURRENT_TIMESTAMP" or "0" needs "default_type":"string".
- SET columns (MySQL) list their members in "set_values", not "enum_values".
- Index: {"indexes":[{"name":"idx_posts_user_created","type":"index","columns":["user_id","created_at"]}]} on its table — "type" is "index" or "unique"; delete via "deletions".
- Group: {"name":"Billing"}. A group never lists its members — put "parent_name":"Billing" on each table that belongs to it.
- Sticky note: {"sticky_notes":[{"content":"..."}]}.
- Delete via "deletions"; rename via "old_name". Do not include left/top coordinates.

Examples:
Add table: `{"strategy":"merge","tables":[{"name":"posts","comment":"Blog posts","columns":[{"name":"id","type":"bigint","is_primary_key":true,"is_auto_increment":true},{"name":"user_id","type":"bigint","is_index":true},{"name":"title","type":"varchar","length":255},{"name":"body","type":"text","is_nullable":true},{"name":"created_at","type":"timestamp","is_nullable":true},{"name":"updated_at","type":"timestamp","is_nullable":true}]}]}`
Rename table and column (use old_name only when renaming): `{"strategy":"merge","tables":[{"name":"articles","old_name":"posts","columns":[{"name":"content","old_name":"body"}]}]}`
Delete: `{"strategy":"merge","deletions":{"tables":["tmp"],"columns":[{"table":"users","columns":["legacy"]}],"relationships":[{"source_table":"users","source_column":"id","target_table":"posts","target_column":"user_id"}]}}`
Multiple groups with nested tables (every table sets parent_name): `{"strategy":"merge","groups":[{"name":"Auth"},{"name":"Content"}],"tables":[{"name":"users","parent_name":"Auth","columns":[{"name":"id","type":"bigint","is_primary_key":true,"is_auto_increment":true}]},{"name":"roles","parent_name":"Auth","columns":[{"name":"id","type":"bigint","is_primary_key":true,"is_auto_increment":true}]},{"name":"posts","parent_name":"Content","columns":[{"name":"id","type":"bigint","is_primary_key":true,"is_auto_increment":true}]}]}`
