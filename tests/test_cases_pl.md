# Zarządzanie jakością - przypadki testowe

Ninejszy dokument ma na celu zdefiniowanie przypadków testowych dla aplikacji **llm_app**.

## Moduł `routes.documents`

### ✔ Test case 1 `upload_document_route` - API zwraca 200, gdy PDF zostaje przesłany i pomyślnie zapisany

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

---

### ✔ Test case 2 `upload_document_route` - API zwraca 400, gdy PDF nie zostaje przesłany

**Stan wejściowy (GIVEN):**

Brak pliku PDF w żądaniu.

**Akcje/Operacje (WHEN):**

Wysłanie żądania `POST` na endpoint `/documents/` bez pliku PDF.

**Oczekiwany rezultat (THEN):**

- Odpowiedź HTTP z kodem `400`.
- Treść odpowiedzi zawiera komunikat z frazą `Invalid file`.

**Otrzymany rezultat:**

Test zakończony sukcesem.

---

### ✔ Test case 3 `upload_document_route` - API zwraca 409, gdy plik z tą samą sumą kontrolną już został zapisany

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

---

### ✔ Test case 4 `upload_document_route` - API zwraca 500, gdy baza danych nie jest dostępna

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

---

### ✔ Test case 5 `get_documents_route` - API zwraca 200, gdy lista dokumentów zostanie zwrócona z bazy

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

---

### ✔ Test case 6 `get_documents_route` - API zwraca 500, gdy baza danych nie jest dostępna

**Stan wejściowy (GIVEN):**

- Mock funkcji `fetch_documents` rzuca wyjątek `DB is down`:

**Akcje/Operacje (WHEN):**

Wysłanie żądania `GET` na endpoint `/documents/`.

**Oczekiwany rezultat (THEN):**

- Funkcja `fetch_documents` została wywołana.
- Odpowiedź HTTP z kodem `500`.
- Treść odpowiedzi zawiera komunikat z frazą `DB error`.

**Otrzymany rezultat:**

Test zakończony sukcesem.

---

### ✔ Test case 7 `delete_document_route` - API zwraca 200, gdy PDF podany PDF istnieje w bazie

**Stan wejściowy (GIVEN):**

- Mock `delete_document` wykonuje się bez błędów (zwracaja `None`)

**Akcje/Operacje (WHEN):**

Wysłanie żądania `DELETE` na endpoint `/documents/test.pdf`.

**Oczekiwany rezultat (THEN):**

- Funkcja `delete_document` została wywołana z argumentem `test.pdf`.
- Odpowiedź HTTP z kodem `200`.
- Treść odpowiedzi zawiera komunikat z frazą `Deleted document test.pdf`.

**Otrzymany rezultat:**

Test zakończony sukcesem.

---

### ✔ Test case 8 `delete_document_route` - API zwraca 500, gdy baza danych nie jest dostępna

**Stan wejściowy (GIVEN):**

- Mock funkcji `delete_document` rzuca wyjątek `DB is down`:

**Akcje/Operacje (WHEN):**

Wysłanie żądania `DELETE` na endpoint `/documents/test.pdf`.

**Oczekiwany rezultat (THEN):**

- Odpowiedź HTTP z kodem `500`.
- Treść odpowiedzi zawiera komunikat z frazą `DB error`.

**Otrzymany rezultat:**

Test zakończony sukcesem.

---

### ✔ Test case 9 `delete_document_route` - API zwraca 404, gdy PDF podany PDF nie istnieje w bazie

**Stan wejściowy (GIVEN):**

- Mock `delete_document` zwraca `0` (Usuwany pdf nie istnieje w bazie).

**Akcje/Operacje (WHEN):**

Wysłanie żądania `DELETE` na endpoint `/documents/test.pdf`.

**Oczekiwany rezultat (THEN):**

- Odpowiedź HTTP z kodem `404`.
- Treść odpowiedzi zawiera komunikat z frazą `Document not found`.

**Otrzymany rezultat:**

Test zakończony sukcesem.

---

<br>

## Moduł `llm.rag`

### ✔ Test case 10 `perform_rag` - Sprawdzenie, czy metoda poprawnie integruje proces RAG

**Stan wejściowy (GIVEN):**

- Mock `fetch_documents` zwraca `[{'filename': 'doc1.pdf'}]` (Istnieją dokumenty w bazie)
- Mock `load_all_documents` zwraca `['doc content']` (Wyciągnięcie zawartości z dokumentu na dysku)
- Mock `chunk_data` zwraca `['chunk1', 'chunk2']` (Zawartość dokumentu zostaje podzielona na części)
- Mock `vectorize_documents` zwraca `vectorsotre` (Przekonwertowanie zawartości dokumentu na embeddingi)
- Mock `build_qa_chain` zwraca `qa_chain` (Stworzenie łańcucha: Pytanie → Wyszukiwanie w wektorowej bazie wiedzy → Kontekst + pytanie → LLM → Odpowiedź)
- Mock `run_chain` zwraca `final_answer` (Zwrócenie ostatecznej odpowiedzi)

**Akcje/Operacje (WHEN):**

Wywołanie funkcji `perform_rag` z parametrem `What is AI?`

**Oczekiwany rezultat (THEN):**

- `perform_rag` zwróci `final_answer`.

**Otrzymany rezultat:**

Test zakończony sukcesem.

---

### ✔ Test case 11 `perform_rag` - Sprawdzenie, czy metoda rzuca wyjątek, gdy nie ma ustawionej zmiennej środowiskowej wskazującej używany model językowy

**Stan wejściowy (GIVEN):**

- Zmienna środowiskowa `MODEL` nie jest ustawiona (`os.environ` jest puste)
- Wszystkie zależności (`fetch_documents`, `load_all_documents`, `chunk_data`, `vectorize_documents`, `build_qa_chain`) zostały zamockowane i zwracają atrapowe obiekty
- Zmienna `prompt` zawiera zapytanie: `"What is AI?"`

**Akcje/Operacje (WHEN):**

Wywołanie funkcji `perform_rag` z parametrem `What is AI?`

**Oczekiwany rezultat (THEN):**

- `perform_rag` rzuca wyjątkiem `ValueError` o treści `MODEL environment variable is not set`.

**Otrzymany rezultat:**

Test zakończony sukcesem.

---

### ✔ Test case 12 `load_all_documents` - Sprawdzenie wczytywania i parsowania treści dokumentów

**Stan wejściowy (GIVEN):**

- Zmienna `input_rows` o z danymi dotyczącymi dwóch dokumentów: 

    ```
        input_rows = [
            {"filename": "doc1.pdf"},
            {"filename": "doc2.pdf"}
        ]
    ```

- Mock `load_pdf` zwraca treść tych dokumentów:

    ```
        [Document(page_content="Content from doc1 page 1")],
        [Document(page_content="Content from doc2 page 1"), Document(page_content="Content from doc2 page 2")]

    ```

**Akcje/Operacje (WHEN):**

Wywołanie funkcji `load_all_documents` z parametrem `input_rows`

**Oczekiwany rezultat (THEN):**

Zwrócone zostaje
- lista obiektów o rozmiarze `3`
- 1\. element listy `"page_content": "Content from doc1 page 1"`
- 2\. element listy `"page_content": "Content from doc2 page 1"`
- 3\. element listy `"page_content": "Content from doc2 page 2"`

**Otrzymany rezultat:**

Test zakończony sukcesem.

---

### ✔ Test case 13 `load_pdf` - Sprawdzenie załadowania pliku z file systemu

**Stan wejściowy (GIVEN):**

- Zmienna środowiskowa `"DOCUMENT_STORAGE_PATH"` ma wartość `tests/resources/pdf`
- Na dysku w ścieżce `tests/resources/pdf` w głównym katalogu projektu znajduje się plik `Profile.pdf`
- Nazwa pliku `Profile.pdf`

**Akcje/Operacje (WHEN):**

Wywołanie funkcji `load_pdf` z parametrem `Profile.pdf`

**Oczekiwany rezultat (THEN):**

- Zwrócony obiekt `documents` jest typu `list`
- Wszyskie elementy listy to obiekty `Document`
- Lista nie jest pusta

**Otrzymany rezultat:**

Test zakończony sukcesem.

---

### ✔ Test case 14 `load_pdf` - Sprawdzenie, czy metoda rzuca wyjątek, gdy nie ma ustawionej zmiennej środowiskowej wskazującej ścieżkę do katalogu z dokumentami na dysku

**Stan wejściowy (GIVEN):**

- Zmienna środowiskowa `"DOCUMENT_STORAGE_PATH"` nie jest ustawiona (`os.environ` jest puste)
- Nazwa pliku `Profile.pdf`

**Akcje/Operacje (WHEN):**

Wywołanie funkcji `load_pdf` z parametrem `Profile.pdf`

**Oczekiwany rezultat (THEN):**

- `load_pdf` rzuca wyjątkiem `ValueError` o treści `DOCUMENT_STORAGE_PATH environment variable is not set`.

**Otrzymany rezultat:**

Test zakończony sukcesem.

---

### ✔ Test case 15 `chunk_data` - Sprawdzenie poprawności dzielenia treści dokumentów na części

**Stan wejściowy (GIVEN):**

- Zmienna `doc` typu `Document` z długim tekstem = `"This is a test sentence. " * 100`

**Akcje/Operacje (WHEN):**

Wywołanie funkcji `chunk_data` z parametrem `doc`

**Oczekiwany rezultat (THEN):**

- Zwrócony obiekt typu `list`
- Lista ma rozmiar większy niż `1`
- Wszyskie elementy listy to obiekty `Document`
- Każdy `Dcoument` w liście zawiera tekst o długości nie większej niż `500` znaków.

**Otrzymany rezultat:**

Test zakończony sukcesem.

---

### ✔ Test case 16 `chunk_data` - Sprawdzenie czy części dokumentów "na siebie nachodzą"

**Stan wejściowy (GIVEN):**

- Zmienna `doc` typu `Document` z wystarczająco długim tekstem = `text = "a" * 450 + "bc" * 50 + "c" * 100`

**Akcje/Operacje (WHEN):**

Wywołanie funkcji `chunk_data` z parametrem `doc`

**Oczekiwany rezultat (THEN):**

- Zwrócona lista ma roziar `2`
- Ostatnie **50** znaków pierwszej części jest, takie samo jak pierwsze **50** znaków drugiej.

**Otrzymany rezultat:**

Test zakończony sukcesem.

---

### ✔ Test case 17 `vectorize_documents` - Sprawdzenie, czy w metodzie jest wywoływane `faiss` z poprawnymi argumentami

**Stan wejściowy (GIVEN):**

- Zmienna środowiskowa `EMBEDDING_MODEL` ma wartość `mock-embed-model`
- Mock `OllamaEmbeddings` zwraca obiekt atrapę `mock_embed_instance`
- Mock `FAISS` zwraca obiekt atrapę `mock_vectorstore`
- Zmienna `chunks` z listą dokumentów:
    ```
        chunks = [
            Document(page_content="Chunk 1"),
            Document(page_content="Chunk 2")
        ]
    ```

**Akcje/Operacje (WHEN):**

Wywołanie funkcji `vectorize_documents` z parametrem `chunks`

**Oczekiwany rezultat (THEN):**

- `OllamaEmbeddings` jest wywołane raz z parametrem `model="mock-embed-model"`
- `FAISS` jest wywołane raz z parametrami `chunks` i  `mock_embed_instance`
- Funkcja zwraca ten sam obiekt co `mock_vectorstore`

**Otrzymany rezultat:**

Test zakończony sukcesem.

---

### ✔ Test case 18 `vectorize_documents` - Sprawdzenie, czy metoda rzuca wyjątek, gdy nie ma ustawionej zmiennej środowiskowej wskazującej model do embeddingów

**Stan wejściowy (GIVEN):**

- Zmienna środowiskowa `EMBEDDING_MODEL` nie jest ustawiona (`os.environ` jest puste)
- Zmienna `chunks` z listą dokumentów:
    ```
        chunks = [Document(page_content="Chunk 1")]
    ```

**Akcje/Operacje (WHEN):**

Wywołanie funkcji `vectorize_documents` z parametrem `chunks`

**Oczekiwany rezultat (THEN):**

- `vectorize_documents` rzuca wyjątkiem `ValueError` o treści `EMBEDDING_MODEL environment variable is not set`.

**Otrzymany rezultat:**

Test zakończony sukcesem.

---

### ✔ Test case 19 `build_qa_chain` - Poprawne skonstruowanie RetrievalQA z modelu LLM i retrievera

**Stan wejściowy (GIVEN):**

- Mock `mock_vectorstore` (obiekt atrapa) po wywołaniu funkcji `as_retriever`  zwraca obiekt atrapę `mock_retriever`
- Mock `mock_retrieval_qa` (obiekt atrapa) po wywołaniu funkcji `from_chain_type` zwraca obiekt atrapę `mock_chain`
- Tworzony jest mock `mock_model` (obiekt atrapa)

**Akcje/Operacje (WHEN):**

Wywołanie funkcji `build_qa_chain` z parametrami `mock_model` i `mock_vectorstore`

**Oczekiwany rezultat (THEN):**

- Funkcja `as_retriever` z `mock_vectorstore` jest wywołana raz.
- Funkcja `from_chain_type` jest wywołana raz z parametrami `llm=mock_model`, `retriever=mock_retriever`, `return_source_documents=False`
- Zwrócona wartość to taki sam obiekt jak `mock_chain`

**Otrzymany rezultat:**

Test zakończony sukcesem.

---

### ✔ Test case 20 `run_chain` - Sprawdzenie, czy metoda wywołuje obiekt `chain` i zwraca odpowiedź

**Stan wejściowy (GIVEN):**

- Tworzony jest mock `mock_chain` zwracający ciąg znaków `Final answer`
- Zmienna `prompt` o wartości `What is AI?`

**Akcje/Operacje (WHEN):**

Wywołanie funkcji `run_chain` z parametrami `mock_chain` i `prompt`

**Oczekiwany rezultat (THEN):**

- Obiekt `mock_chain` jest wywoływany raz z parametrem `prompt`
- Zwrócona wartość to `Final answer`

**Otrzymany rezultat:**

Test zakończony sukcesem.

---
