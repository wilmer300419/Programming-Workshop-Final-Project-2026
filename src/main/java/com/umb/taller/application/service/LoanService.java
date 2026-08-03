package com.umb.taller.application.service;

import java.util.List;

import com.umb.taller.application.exception.LibraryException;
import com.umb.taller.application.repository.BookRepository;
import com.umb.taller.application.repository.LoanRepository;
import com.umb.taller.application.repository.StudentRepository;
import com.umb.taller.domain.Book;
import com.umb.taller.domain.Loan;
import com.umb.taller.domain.Student;

/**
 * Servicio de aplicación encargado de controlar el ciclo de vida de los préstamos.
 * Coordina la validación del estudiante, del libro y el cambio de estado del préstamo.
 */
public class LoanService {

    private final LoanRepository loanRepository;
    private final BookRepository bookRepository;
    private final StudentRepository studentRepository;

    public LoanService(
            LoanRepository loanRepository,
            BookRepository bookRepository,
            StudentRepository studentRepository) {

        this.loanRepository = loanRepository;
        this.bookRepository = bookRepository;
        this.studentRepository = studentRepository;

    }

    /**
     * Creates a new loan.
     */
    /**
     * Crea un préstamo cuando el estudiante existe, el libro existe y está disponible.
     */
    public void createLoan(
            String studentId,
            String bookId) {

        Student student =
                studentRepository.findById(studentId);

        if (student == null) {

            throw new LibraryException(
                    "Student not found.");

        }

        Book book =
                bookRepository.findById(bookId);

        if (book == null) {

            throw new LibraryException(
                    "Book not found.");

        }

        if (!book.isAvailable()) {

            throw new LibraryException(
                    "Book is already borrowed.");

        }

        book.borrow();

        Loan loan =
                new Loan(student, book);

        loanRepository.save(loan);

    }

    /**
     * Returns a borrowed book.
     */
    /**
     * Finaliza un préstamo activo asociado a un libro.
     */
    public void returnBook(String bookId) {

        Loan loan =
                loanRepository
                        .findActiveLoanByBookId(bookId);

        if (loan == null) {

            throw new LibraryException(
                    "No active loan found for this book.");

        }

        loan.finishLoan();

    }

    /**
     * Returns all registered loans.
     */
    public List<Loan> getLoans() {

        return loanRepository.findAll();

    }

}