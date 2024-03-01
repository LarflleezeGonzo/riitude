from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from ...core.response_handlers import success_response
from ...models import Book, Review
from ...schemas import BookCreate, ReviewCreate
from ...utils.email_sender import send_email
from ..dependencies import get_db

router = APIRouter()


@router.post("/books", response_model=None)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return success_response(message="Book created", code=201, data=db_book)


@router.post("/books/{book_id}/reviews", response_model=None)
def create_review(
    book_id: int,
    background_tasks: BackgroundTasks,
    review: ReviewCreate,
    db: Session = Depends(get_db),
):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    db_review = Review(**review.dict(), book_id=book_id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    background_tasks.add_task(
        send_email,
        to="example@email.com",
        subject="New Review Added",
        content="A new review has been added.",
    )
    return success_response(message="Review created", code=201, data=db_review)


@router.get("/books", response_model=None)
def get_books(
    author: str = None, publication_year: int = None, db: Session = Depends(get_db)
):
    query = db.query(Book)
    if author:
        query = query.filter(Book.author == author)
    if publication_year:
        query = query.filter(Book.publication_year == publication_year)
    return success_response(message="Retrieved all books", code=200, data=query.all())


@router.get("/books/{book_id}/reviews", response_model=None)
def get_reviews(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    reviews = db.query(Review).filter(Review.book_id == book_id).all()

    return success_response(message="Retrieved reviews", code=200, data=reviews)
