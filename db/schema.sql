-- SkillBridge Prototype Schema (Day 3)
-- Scope: prototype-level subset of the full ERD (Jobs + DataSources + Countries).
-- Full ERD entities (Employers, Locations, Skills, Occupations, JobSkills, Users,
-- UserSkills, AnalysisResults, Recommendations) are deferred to later sprints.

CREATE DATABASE IF NOT EXISTS skillbridge
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE skillbridge;

DROP TABLE IF EXISTS jobs;
DROP TABLE IF EXISTS data_sources;
DROP TABLE IF EXISTS countries;

CREATE TABLE countries (
    country_id      INT AUTO_INCREMENT PRIMARY KEY,
    country_name    VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE data_sources (
    source_id       INT AUTO_INCREMENT PRIMARY KEY,
    source_name     VARCHAR(255) NOT NULL,
    reliability     VARCHAR(255),
    limitation      TEXT,
    UNIQUE KEY uq_source_name (source_name(191))
);

CREATE TABLE jobs (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    job_id          VARCHAR(50) NOT NULL,       -- original ID from raw dataset
    country_id      INT NOT NULL,
    original_title  VARCHAR(255) NOT NULL,
    normalized_title VARCHAR(255),              -- placeholder for G1-B's NLP normalization
    company         VARCHAR(255),
    location        VARCHAR(255),
    category        VARCHAR(100),
    sub_category    VARCHAR(150),
    role_type       VARCHAR(50)     NULL,       -- NULL: not provided in either source dataset
    salary_raw      VARCHAR(255),               -- original free-text salary string
    salary_min      DECIMAL(12,2)   NULL,
    salary_max      DECIMAL(12,2)   NULL,
    currency        VARCHAR(10)     NULL,       -- INR / MYR
    salary_period   VARCHAR(10)     NULL,       -- 'annual' / 'monthly'
    posting_date    DATE            NULL,       -- NULL: not provided in either source dataset
    source_id       INT,

    CONSTRAINT fk_jobs_country FOREIGN KEY (country_id) REFERENCES countries(country_id),
    CONSTRAINT fk_jobs_source  FOREIGN KEY (source_id)  REFERENCES data_sources(source_id),
    UNIQUE KEY uq_job_country (job_id, country_id)
);

CREATE INDEX idx_jobs_country ON jobs(country_id);
CREATE INDEX idx_jobs_category ON jobs(category);
CREATE INDEX idx_jobs_title ON jobs(original_title);
