### Question 1: FastAPI and Asynchronous Requests

FastAPI utilizes asynchronous programming to manage multiple requests simultaneously, significantly improving performance compared to synchronous code in Python.

#### Benefits:

1. **Concurrency:** Asynchronous handling allows multiple operations to progress concurrently, enhancing efficiency.
   
2. **Improved Responsiveness:** Applications remain responsive, providing a seamless user experience, especially when dealing with I/O-bound tasks.

3. **Scalability:** FastAPI's asynchronous model is beneficial for applications dealing with a large number of simultaneous connections, ensuring optimal scalability.

### Question 2: Dependency Injection in FastAPI

FastAPI employs dependency injection to manage and provide shared resources seamlessly across different parts of an application.

#### Practical Use:

For example, managing access to a database can be simplified using dependency injection:

```python
from fastapi import Depends, FastAPI, HTTPException

app = FastAPI()

def get_db():
    db = DBConnection()
    try:
        yield db
    finally:
        db.close()


@app.get("/items/")
async def read_item(db: DBConnection = Depends(get_db)):
    return {"message": "Item read successfully"}

```
### Question 3: Code Walkthrough

1. **Imports:**
   ```python
   from fastapi import APIRouter, BackgroundTasks, Depends
   from fastapi.exceptions import HTTPException
   from sqlalchemy.orm import Session
   ```

   - Import necessary modules.

2. **Additional Imports:**
   ```python
   from ...core.response_handlers import success_response
   from ...models import Book, Review
   from ...schemas import BookCreate, ReviewCreate
   from ...utils.email_sender import send_email
   from ..dependencies import get_db
   ```

   - Import project-specific modules.

3. **Router Instance:**
   ```python
   router = APIRouter()
   ```

   - Create an API router instance.

4. **Create Book Endpoint:**
   ```python
   @router.post("/books", response_model=None)
   def create_book(book: BookCreate, db: Session = Depends(get_db)):
       # ... (creates and adds a new book to the database)
   ```

   - POST endpoint to create a new book.

5. **Create Review Endpoint:**
   ```python
   @router.post("/books/{book_id}/reviews", response_model=None)
   def create_review(
       book_id: int,
       background_tasks: BackgroundTasks,
       review: ReviewCreate,
       db: Session = Depends(get_db),
   ):
       # ... (creates and adds a new review, triggers an email background task)
   ```

   - POST endpoint to create a new review, triggers email task.

6. **Get Books and Reviews Endpoints:**
   ```python
   @router.get("/books", response_model=None)
   def get_books(author: str = None, publication_year: int = None, db: Session = Depends(get_db)):
       # ... (retrieve books based on optional parameters)
   
   @router.get("/books/{book_id}/reviews", response_model=None)
   def get_reviews(book_id: int, db: Session = Depends(get_db)):
       # ... (retrieve reviews for a specific book)
   ```

   - GET endpoints to retrieve books and reviews.

