admin으로만 등록가능하게만듬

1.위에 주소쳐서 들어가는걸 막아야함
## 🔧 API Endpoint 정리

| 기능 | HTTP | URL |
| --- | --- | --- |
| 책 목록 조회 | GET | `/api/books/` |
| 책 등록 | POST | `/api/books/` |
| 책 상세 조회 | GET | `/api/books/{id}/` |
| 책 수정 | PUT/PATCH | `/api/books/{id}/` |
| 책 삭제 | DELETE | `/api/books/{id}/` |
| 리뷰 등록 | POST | `/api/reviews/` |
| 리뷰 목록 조회 (도서 기준) | GET | `/api/books/{book_id}/reviews/` |
| 리뷰 상세 조회 | GET | `/api/reviews/{id}/` |
| 리뷰 수정 | PUT/PATCH | `/api/reviews/{id}/` |
| 리뷰 삭제 | DELETE | `/api/reviews/{id}/` |
| 저자 목록 조회 | GET | `/api/authors/` |
| 저자 등록/수정/삭제 | POST/PUT/DELETE | `/api/authors/`, `/api/authors/{id}/` |
| 저자별 도서 수 통계 | GET | `/api/dashboard/authors/` |