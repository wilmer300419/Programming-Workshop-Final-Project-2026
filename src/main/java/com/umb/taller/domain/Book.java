package com.umb.taller.domain;

public class Book implements Identifiable, Displayable {

    private final String id;
    private String title;
    private String author;
    private boolean available;

    public Book(String id, String title, String author) {

        this.id = id;
        this.title = title;
        this.author = author;
        this.available = true;

    }

    @Override
    public String getId() {

        return id;

    }

    public String getTitle() {

        return title;

    }

    public String getAuthor() {

        return author;

    }

    public boolean isAvailable() {

        return available;

    }

    public void borrow() {

        available = false;

    }

    public void giveBack() {

        available = true;

    }

    @Override
    public void displayInformation() {

        System.out.println(id + " - "+title + " - " + author);

    }

}