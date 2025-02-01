from books.models import Book
from django.core.cache import cache
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


CACHE_TIMEOUT = 3600


def get_vectorizer_and_matrix():
    vectorizer = cache.get("book_vectorizer")
    tfidf_matrix = cache.get("book_tdidf_matrix")
    book_ids = cache.get("book_ids")

    if vectorizer is None or tfidf_matrix is None or book_ids is None:
        books = Book.objects.all()
        documents = []
        book_ids = []

        for book in books:
            text_parts = []
            if book.title:
                text_parts.append(book.title)
            if book.description:
                text_parts.append(book.description)
            if hasattr(book, "categories") and book.categories:
                text_parts.append(book.categories)

            combined_text = " ".join(text_parts)
            documents.append(combined_text)
            book_ids.append(book.id)

        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = vectorizer.fit_transform(documents)

        cache.set("book_vectorizer", vectorizer, CACHE_TIMEOUT)
        cache.set("book_tdidf_matrix", tfidf_matrix, CACHE_TIMEOUT)
        cache.set("book_ids", book_ids, CACHE_TIMEOUT)

    return vectorizer, tfidf_matrix, book_ids


def get_recommendations(favorite_books, limit=5):
    if not favorite_books:
        return Book.objects.none()

    combined_docs = []
    for book in favorite_books:
        text_parts = []
        if book.title:
            text_parts.append(book.title)
        if book.description:
            text_parts.append(book.description)
        if hasattr(book, "categories") and book.categories:
            text_parts.append(book.categories)

        combined_doc = " ".join(text_parts)
        combined_docs.append(combined_doc)

    combined_text = " ".join(combined_docs)

    vectorizer, tfidf_matrix, book_ids = get_vectorizer_and_matrix()

    fav_vector = vectorizer.transform([combined_text])
    similarities = cosine_similarity(fav_vector, tfidf_matrix).flatten()

    favorite_ids = set(book.id for book in favorite_books)
    candidate_similarities = [
        (i, sim)
        for i, (book_id, sim) in enumerate(zip(book_ids, similarities))
        if book_id not in favorite_ids
    ]
    candidate_similarities.sort(key=lambda x: x[1], reverse=True)

    top_indices = [i for i, sim in candidate_similarities[:limit]]
    recommended_book_ids = [book_ids[i] for i in top_indices]

    recommended_books = Book.objects.filter(id__in=recommended_book_ids)
    return recommended_books
