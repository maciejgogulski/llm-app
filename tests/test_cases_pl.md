# Zarządzanie jakością - przypadki testowe

Ninejszy dokument ma na celu definicje przypadków testowych dla aplikacji **llm_app**.

## Moduł routes.documents

### Test case 1 (upload_document_route) - API zwraca 200, gdy PDF zostaje przesłany i pomyślnie zapisany

**Stan wejściowy (GIVEN):**

- Mock funkcji `compute_checksum` zwraca sumę kontrolną:
`6c99f39e9003a9f6ee089c472790def8f87e5f05fbd0c248e5a7b4aca5aecbb3`
- Mock `document_exists_by_checksum` zwraca `False` (plik nie istnieje w bazie)
- Mock `insert_document` i `FileStorage.save` wykonują się bez błędów (zwracają `None`)
- Przesłany plik to `test.pdf` o zawartości `b"%PDF-1.4 some pdf content"`

**Akcje/Operacje (WHEN):**

Wysłanie żądania `POST` na endpoint `/documents/` z plikiem PDF jako `multipart/form-data`.

**Oczekiwany rezultat (THEN):**

- Odpowiedź HTTP z kodem `200`.
- Treść odpowiedzi zawiera komunikat z frazą `Saved to`.

**Otrzymany rezultat:**

Test zakończony sukcesem.


### Test case 2 (upload_document_route) - API zwraca 400, gdy PDF nie zostaje przesłany

**Stan wejściowy (GIVEN):**

Brak pliku PDF w żądaniu.

**Akcje/Operacje (WHEN):**

Wysłanie żądania `POST` na endpoint `/documents/` bez pliku PDF.

**Oczekiwany rezultat (THEN):**

- Odpowiedź HTTP z kodem `400`.
- Treść odpowiedzi zawiera komunikat z frazą `Invalid file`.

**Otrzymany rezultat:**

Test zakończony sukcesem.


### Test case 3 (upload_document_route) - API zwraca 409, gdy plik z tą samą sumą kontrolną już został zapisany

**Stan wejściowy (GIVEN):**

- Mock funkcji `compute_checksum` zwraca sumę kontrolną:
`6c99f39e9003a9f6ee089c472790def8f87e5f05fbd0c248e5a7b4aca5aecbb3`
- Mock `document_exists_by_checksum` zwraca `True` (plik istnieje w bazie)
- Przesłany plik to `test.pdf` o zawartości `b"fake pdf content""`

**Akcje/Operacje (WHEN):**

Wysłanie żądania `POST` na endpoint `/documents/` z plikiem PDF jako `multipart/form-data`.

**Oczekiwany rezultat (THEN):**

- Odpowiedź HTTP z kodem `409`.
- Treść odpowiedzi zawiera komunikat z frazą `Duplicate document`.

**Otrzymany rezultat:**

Test zakończony sukcesem.


### Test case 4 (upload_document_route) - API zwraca 500, gdy baza danych nie jest dostępna

**Stan wejściowy (GIVEN):**

- Mock funkcji `compute_checksum` zwraca sumę kontrolną:
`6c99f39e9003a9f6ee089c472790def8f87e5f05fbd0c248e5a7b4aca5aecbb3`
- Mock `document_exists_by_checksum` zwraca `False` (plik nie istnieje w bazie)
- Przesłany plik to `test.pdf` o zawartości `b"valid pdf content""`
- Mock `insert_document` rzuca wyjątkiem `DB is down`

**Akcje/Operacje (WHEN):**

Wysłanie żądania `POST` na endpoint `/documents/` z plikiem PDF jako `multipart/form-data`.

**Oczekiwany rezultat (THEN):**

- Odpowiedź HTTP z kodem `500`.
- Treść odpowiedzi zawiera komunikat z frazą `DB error`.

**Otrzymany rezultat:**

Test zakończony sukcesem.


### Test case 5 (get_documents_route) - API zwraca 200, z listą dokumentów

**Stan wejściowy (GIVEN):**

- Mock funkcji `fetch_documents` zwraca listę obiektów:
```
    mock_docs = [
        {"id": 1, "filename": "test1.pdf", "filepath": "/uploads/test1.pdf", "added_at": "2025-06-25 12:00:00", "updated_at": "2025-06-25 12:00:00"},
        {"id": 2, "filename": "test2.pdf", "filepath": "/uploads/test2.pdf", "added_at": "2025-06-25 12:00:00", "updated_at": "2025-06-25 12:00:00"}
    ]
```

**Akcje/Operacje (WHEN):**

Wysłanie żądania `GET` na endpoint `/documents/`.

**Oczekiwany rezultat (THEN):**

- Funkcja `fetch_documents` została wywołana.
- Odpowiedź HTTP z kodem `200`.
- Treść odpowiedzi zawiera ten sam json, co zwrócony przez mock `fetch_documents`.

**Otrzymany rezultat:**

Test zakończony sukcesem.

