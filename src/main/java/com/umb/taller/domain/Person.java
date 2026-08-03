package com.umb.taller.domain;

/**
 * Abstract base class for people in the library.
 */
public abstract class Person implements Identifiable, Displayable {

    private final String id;
    private String fullName;

    protected Person(String id, String fullName) {

        this.id = id;
        this.fullName = fullName;

    }

    @Override
    public String getId() {

        return id;

    }

    public String getFullName() {

        return fullName;

    }

    public void setFullName(String fullName) {

        this.fullName = fullName;

    }

    @Override
    public void displayInformation() {

        System.out.println("ID: " + id);
        System.out.println("Name: " + fullName);

    }

}