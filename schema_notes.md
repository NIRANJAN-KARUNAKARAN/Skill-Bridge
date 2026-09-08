## Unified Job Schema Mapping
## Unified Job Schema Mapping

| Unified Field      | India source column | Malaysia source column | Notes |
|---------------------|---------------------|-------------------------|-------|
| job_id              | Job ID              | Job ID                  |       |
| original_title      | Job Title           | Job Title                |       |
| normalized_title    |                     |                          | needs NLP team |
| country              | Country            | Country                  |       |
| salary_min          | Salary              | Salary                   | parse from Salary text (e.g. "2-4 Lacs PA") |
| salary_max          | Salary              | Salary                   | parse from Salary text |
| currency            |                     |                          | not its own column — infer per country (India=INR, Malaysia=MYR) |
| job_description     |                     |                          | check if it exists — not seen in columns so far; may need to use Category/Sub-category/Role Type instead |
| posting_date        | Listing Date         | Listing Date              |       |
| source              | Data Source          | Data Source               |       |