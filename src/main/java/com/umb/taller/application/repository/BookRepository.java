package com.umb.taller.application.repository;

import java.util.ArrayList;
import java.util.List;

import com.umb.taller.domain.Book;

/**
 * Repositorio en memoria para gestionar los libros del sistema.
 */
public class BookRepository implements Repository<Book> {

    private final List<Book> books;

    public BookRepository() {

        books = new ArrayList<>();

    }

    @Override
    public void save(Book book) {

        books.add(book);

    }

    @Override
    public List<Book> findAll() {

        return books;

    }

    public Book findById(String id) {

        for (Book book : books) {

            if (book.getId().equals(id)) {

                return book;

            }

        }

        return null;

    }

}