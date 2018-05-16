# monitoring

서버 배포 후 모니터링 시스템

# 주제선정배경

- 서비스에 코드를 일부 시스템에 부분 배포한 직 후 시스템의 상태가 기존과 유의미하게 차이가 있는지 application의 log 와 system resource를 모니터링 해 주면 전체 장애를 막을 수 있습니다. 따라서 이런 시스템을 만들어 보고자 합니다.

# 요구사항 (필수)

- DB 에 평상시에 배포 system 상태를 기록
- 각 여러 시스템의 log를 읽고 이상 status 파악
- 각 서버의 resource usage를 얻어와서 이를 DB에 기록하고 비교

# 요구사항 (선택)

- 평상 시 resource 사용량 대비 delta를 어디까지 허용할지에 대한 통계적 구현.

# 평가 기준

- 각 기능별 모듈화
- 서버 resource에 대한 이해
- Log parser의 구현 정도

# 개발 언어

- Java
- Python

# 플랫폼

- linux

---

#### 멘토 라인 / email

ksmail13 / minkyu.kim13@navercorp.com


기타 문의 사항은 issue에 등록해주세요.
