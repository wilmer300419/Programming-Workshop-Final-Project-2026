package com.umb.taller.application.service;

import java.util.List;

import com.umb.taller.application.repository.BookRepository;
import com.umb.taller.application.repository.StudentRepository;
import com.umb.taller.domain.Book;
import com.umb.taller.domain.Student;

/**
 * Servicio de aplicación para gestionar libros y estudiantes de la biblioteca.
 * Actúa como punto de entrada para las operaciones básicas de registro y consulta.
 */
public class LibraryService {

    private final BookRepository bookRepository;
    private final StudentRepository studentRepository;

    public LibraryService(
            BookRepository bookRepository,
            StudentRepository studentRepository) {

        this.bookRepository = bookRepository;
        this.studentRepository = studentRepository;

    }

    /**
     * Registra un nuevo libro en el sistema.
     */
    public void registerBook(Book book) {

        bookRepository.save(book);

    }

    /**
     * Registra un nuevo estudiante en el sistema.
     */
    public void registerStudent(Student student) {

        studentRepository.save(student);

    }

    public List<Book> getBooks() {

        return bookRepository.findAll();

    }

    public List<Student> getStudents() {

        return studentRepository.findAll();

    }

    public Book findBookById(String id) {

        return bookRepository.findById(id);

    }

    public Student findStudentById(String id) {

        return studentRepository.findById(id);

    }

}