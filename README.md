라즈베리파이
============
### 데이터베이스(Mysql Workbench) 
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

###hand_pipe.py

![index](https://user-images.githubusercontent.com/73813738/195222095-400f1ef7-5415-48ae-a652-9b61a8a145e2.jpg)
+ space: 중지만 접기, clear: 중지 약지 접기
