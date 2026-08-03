package com.umb.taller.domain;

import java.time.LocalDate;

/**
 * Represents a book loan made by a student.
 */
public class Loan {

    private final Student student;
    private final Book book;
    private final LocalDate loanDate;

    private LocalDate returnDate;
    private LoanStatus status;

    public Loan(Student student, Book book) {

        this.student = student;
        this.book = book;
        this.loanDate = LocalDate.now();
        this.status = LoanStatus.ACTIVE;

    }

    /**
     * Finishes the current loan.
     */
    public void finishLoan() {

        if (status == LoanStatus.RETURNED) {
            return;
        }

        status = LoanStatus.RETURNED;
        returnDate = LocalDate.now();

        book.giveBack();

    }

    public Student getStudent() {
        return student;
    }

    public Book getBook() {
        return book;
    }

    public LocalDate getLoanDate() {
        return loanDate;
    }

    public LocalDate getReturnDate() {
        return returnDate;
    }

    public LoanStatus getStatus() {
        return status;
    }

    public boolean isActive() {
        return status == LoanStatus.ACTIVE;
    }

}