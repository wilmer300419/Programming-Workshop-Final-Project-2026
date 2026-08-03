package com.umb.taller.infrastructure;

import com.umb.taller.application.service.LibraryService;
import com.umb.taller.domain.Book;
import com.umb.taller.domain.Student;

/**
 * Carga datos iniciales de ejemplo para poner el sistema en un estado usable al arrancar.
 */
public class DataSeeder {

    private final LibraryService libraryService;

    public DataSeeder(LibraryService libraryService) {
        this.libraryService = libraryService;
    }

    /**
     * Inserta estudiantes y libros base para la demo inicial de la biblioteca.
     */
    public void loadSampleData() {

        libraryService.registerStudent(
                new Student("S001",
                        "Wilmer Andres Capera Hernandez",
                        "Software Engineering"));

        libraryService.registerStudent(
                new Student("S002",
                        "Esteban Salvador Guzman",
                        "Software Engineering"));

        libraryService.registerStudent(
                new Student("S003",
                        "Santiago Santana Nieto",
                        "Software Engineering"));

        libraryService.registerBook(
                new Book("B001",
                        "Clean Code",
                        "Robert C. Martin"));

        libraryService.registerBook(
                new Book("B002",
                        "Effective Java",
                        "Joshua Bloch"));

        libraryService.registerBook(
                new Book("B003",
                        "Design Patterns",
                        "GoF"));

    }

}