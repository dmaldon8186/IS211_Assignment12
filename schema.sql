CREATE TABLE students (
  id INTEGER PRIMARY KEY AUTOINCREMENT, 
  first_name TEXT,
  last_name TEXT
);

CREATE TABLE quizzes (
  id INTEGER PRIMARY KEY AUTOINCREMENT, 
  subject TEXT,
  num_questions INTEGER,
  date_given TEXT
);

CREATE TABLE results (
  student_id INTEGER,
  quiz_id INTEGER,
  score INTEGER,
  FOREIGN KEY (student_id) REFERENCES students(id),
  FOREIGN KEY (quiz_id) REFERENCES quizzes(id),
  PRIMARY KEY (student_id, quiz_id)
);