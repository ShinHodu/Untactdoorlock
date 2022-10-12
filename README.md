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
- 여기서 일부 손동작만 사용(코드 참고) + space: 중지만 접기, clear: 중지 약지 접기
- answer.txt에 정답 저장 (ex. CY I)
- 스크립트 실행 후 손동작 실행: a누르면 실행한 손동작 test.txt에 저장, b누르면 종료
- answer.txt와 test.txt 내용이 같으면 서보모터 동작, 다르면 hand 테이블에 인덱스 
