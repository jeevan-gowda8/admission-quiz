-- College Admission Quiz System — Database Schema
-- Run this once to create the database and tables

CREATE DATABASE IF NOT EXISTS admission_quiz
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE admission_quiz;

-- Students table: tracks who has logged in and attempted the quiz
CREATE TABLE IF NOT EXISTS students (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(255)  NOT NULL,
    reg_no     VARCHAR(100)  UNIQUE NOT NULL,
    attempted  BOOLEAN       DEFAULT FALSE,
    created_at TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
);

-- Results table: stores scores (hidden from students)
CREATE TABLE IF NOT EXISTS results (
    id        INT AUTO_INCREMENT PRIMARY KEY,
    reg_no    VARCHAR(100)               NOT NULL,
    score     INT                        NOT NULL,
    total     INT                        DEFAULT 30,
    status    ENUM('Selected','Rejected') NOT NULL,
    timestamp TIMESTAMP                  DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (reg_no) REFERENCES students(reg_no)
        ON DELETE CASCADE ON UPDATE CASCADE
);

USE admission_quiz;
CREATE INDEX idx_results_score ON results(score DESC);
