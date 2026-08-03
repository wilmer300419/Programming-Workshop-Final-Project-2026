package com.umb.taller;

import com.umb.taller.application.repository.BookRepository;
import com.umb.taller.application.repository.LoanRepository;
import com.umb.taller.application.repository.StudentRepository;
import com.umb.taller.application.service.LibraryService;
import com.umb.taller.application.service.LoanService;
import com.umb.taller.infrastructure.ConsoleMenu;
import com.umb.taller.infrastructure.DataSeeder;

/**
 * Punto de entrada de la aplicación.
 * Se encarga de inicializar los repositorios, servicios y la interfaz de consola.
 */
public class Main {

    /**
     * Inicia la aplicación y conecta los componentes principales del sistema.
     */
    public static void main(String[] args) {

        BookRepository bookRepository = new BookRepository();

        StudentRepository studentRepository = new StudentRepository();

        LoanRepository loanRepository = new LoanRepository();

        LibraryService libraryService =
                new LibraryService(
                        bookRepository,
                        studentRepository);

        LoanService loanService =
                new LoanService(
                        loanRepository,
                        bookRepository,
                        studentRepository);

        DataSeeder dataSeeder =
                new DataSeeder(libraryService);

        dataSeeder.loadSampleData();

        ConsoleMenu menu =
                new ConsoleMenu(
                        libraryService,
                        loanService);

        menu.start();

    }

}