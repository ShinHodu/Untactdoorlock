라즈베리파이
============
## 데이터베이스 
sql 설정


```
CREATE DATABASE doorlock;

USE doorlock;

CREATE TABLE doorlock_video(
    id INT AUTO_INCREMENT PRIMARY KEY, 
    name VARCHAR(100), 
    date_created DATETIME DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE switch (
    id TINYINT(1) PRIMARY KEY,
    switch TINYINT(1) NOT NULL
);

CREATE TABLE hand (
    id INT AUTO_INCREMENT PRIMARY KEY,
   name VARCHAR(100)
);
```

##
