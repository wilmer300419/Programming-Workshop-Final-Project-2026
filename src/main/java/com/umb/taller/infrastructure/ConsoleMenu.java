package com.umb.taller.infrastructure;

import java.util.Scanner;

import com.umb.taller.application.exception.LibraryException;
import com.umb.taller.application.service.LibraryService;
import com.umb.taller.application.service.LoanService;
import com.umb.taller.domain.Book;
import com.umb.taller.domain.Loan;
import com.umb.taller.domain.Student;

public class ConsoleMenu {

    private final LibraryService libraryService;
    private final LoanService loanService;

    private final Scanner scanner;

    public ConsoleMenu(
            LibraryService libraryService,
            LoanService loanService) {

        this.libraryService = libraryService;
        this.loanService = loanService;

        this.scanner =
                new Scanner(System.in);

    }

    public void start() {

        int option = -1;

        do {

            showMenu();

            option = readInteger(
                    "Option: ");

            try {

                switch (option) {

                    case 1 -> showBooks();

                    case 2 -> showStudents();

                    case 3 -> borrowBook();

                    case 4 -> returnBook();

                    case 5 -> registerBook();

                    case 6 -> registerStudent();

                    case 7 -> searchBook();

                    case 8 -> searchStudent();

                    case 9 -> showLoans();

                    case 0 ->
                            System.out.println(
                                    "Good bye!");

                    default ->
                            System.out.println(
                                    "Invalid option.");

                }

            } catch (LibraryException e) {

                System.out.println(
                        "\nERROR: "
                                + e.getMessage());

            }

        } while (option != 0);

    }

    private void showMenu() {

        System.out.println();

        System.out.println(
                "================================");

        System.out.println(
                "       UMB SMART LIBRARY");

        System.out.println(
                "================================");

        System.out.println(
                "1. Show Books");

        System.out.println(
                "2. Show Students");

        System.out.println(
                "3. Borrow Book");

        System.out.println(
                "4. Return Book");

        System.out.println(
                "5. Register Book");

        System.out.println(
                "6. Register Student");

        System.out.println(
                "7. Search Book");

        System.out.println(
                "8. Search Student");

        System.out.println(
                "9. Show Loans");

        System.out.println(
                "0. Exit");

        System.out.println(
                "================================");

    }

    private void showBooks() {

        System.out.println(
                "\n--- BOOKS ---");

        for (Book book :
                libraryService.getBooks()) {

            System.out.println(
                    "ID: "
                            + book.getId());

            System.out.println(
                    "Title: "
                            + book.getTitle());

            System.out.println(
                    "Author: "
                            + book.getAuthor());

            System.out.println(
                    "Available: "
                            + book.isAvailable());

            System.out.println(
                    "----------------");

        }

    }

    private void showStudents() {

        System.out.println(
                "\n--- STUDENTS ---");

        for (Student student :
                libraryService
                        .getStudents()) {

            student.displayInformation();

            System.out.println(
                    "----------------");

        }

    }

    private void borrowBook() {

        System.out.println(
                "\n--- BORROW BOOK ---");

        String studentId =
                readText(
                        "Student ID: ");

        String bookId =
                readText(
                        "Book ID: ");

        loanService.createLoan(
                studentId,
                bookId);

        System.out.println(
                "Book borrowed successfully.");

    }

    private void returnBook() {

        System.out.println(
                "\n--- RETURN BOOK ---");

        String bookId =
                readText(
                        "Book ID: ");

        loanService.returnBook(
                bookId);

        System.out.println(
                "Book returned successfully.");

    }

    private void registerBook() {

        System.out.println(
                "\n--- REGISTER BOOK ---");

        String id =
                readText(
                        "Book ID: ");

        String title =
                readText(
                        "Title: ");

        String author =
                readText(
                        "Author: ");

        Book book =
                new Book(
                        id,
                        title,
                        author);

        libraryService.registerBook(
                book);

        System.out.println(
                "Book registered successfully.");

    }

    private void registerStudent() {

        System.out.println(
                "\n--- REGISTER STUDENT ---");

        String id =
                readText(
                        "Student ID: ");

        String name =
                readText(
                        "Full name: ");

        String career =
                readText(
                        "Career: ");

        Student student =
                new Student(
                        id,
                        name,
                        career);

        libraryService.registerStudent(
                student);

        System.out.println(
                "Student registered successfully.");

    }

    private void searchBook() {

        System.out.println(
                "\n--- SEARCH BOOK ---");

        String id =
                readText(
                        "Book ID: ");

        Book book =
                libraryService
                        .findBookById(id);

        if (book == null) {

            System.out.println(
                    "Book not found.");

            return;

        }

        System.out.println(
                "Book found:");

        System.out.println(
                "ID: "
                        + book.getId());

        System.out.println(
                "Title: "
                        + book.getTitle());

        System.out.println(
                "Author: "
                        + book.getAuthor());

        System.out.println(
                "Available: "
                        + book.isAvailable());

    }

    private void searchStudent() {

        System.out.println(
                "\n--- SEARCH STUDENT ---");

        String id =
                readText(
                        "Student ID: ");

        Student student =
                libraryService
                        .findStudentById(id);

        if (student == null) {

            System.out.println(
                    "Student not found.");

            return;

        }

        student.displayInformation();

    }

    private void showLoans() {

        System.out.println(
                "\n--- LOANS ---");

        for (Loan loan :
                loanService.getLoans()) {

            System.out.println(
                    "Student: "
                            + loan
                            .getStudent()
                            .getFullName());

            System.out.println(
                    "Book: "
                            + loan
                            .getBook()
                            .getTitle());

            System.out.println(
                    "Loan date: "
                            + loan
                            .getLoanDate());

            System.out.println(
                    "Status: "
                            + loan
                            .getStatus());

            System.out.println(
                    "----------------");

        }

    }

    private int readInteger(
            String message) {

        while (true) {

            try {

                return Integer.parseInt(
                        readText(message));

            } catch (
                    NumberFormatException e) {

                System.out.println(
                        "Please enter a valid number.");

            }

        }

    }

    private String readText(
            String message) {

        System.out.print(message);

        if (!scanner.hasNextLine()) {

            throw new LibraryException(
                    "Input stream closed.");

        }

        return scanner.nextLine()
                .trim();

    }

}