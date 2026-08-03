package com.umb.taller.application.repository;

import java.util.ArrayList;
import java.util.List;

import com.umb.taller.domain.Loan;

public class LoanRepository implements Repository<Loan> {

    private final List<Loan> loans;

    public LoanRepository() {

        loans = new ArrayList<>();

    }

    @Override
    public void save(Loan loan) {

        loans.add(loan);

    }

    @Override
    public List<Loan> findAll() {

        return new ArrayList<>(loans);

    }

    public Loan findActiveLoanByBookId(String bookId) {

        for (Loan loan : loans) {

            if (loan.isActive()
                    && loan.getBook().getId().equals(bookId)) {

                return loan;

            }

        }

        return null;

    }

}