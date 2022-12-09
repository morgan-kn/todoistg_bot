CREATE TABLE tasks (
     task_id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
     name varchar(255) NOT NULL,
     user_id varchar(255),
     priority int,
     status int,
     created_at TIMESTAMP NOT NULL,
     updated_at TIMESTAMP NOT NULL,
     comment text
);