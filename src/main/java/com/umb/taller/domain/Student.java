package com.umb.taller.domain;

public class Student extends Person {

    private String career;

    public Student(String id, String fullName, String career) {

        super(id, fullName);
        this.career = career;

    }

    public String getCareer() {

        return career;

    }

    public void setCareer(String career) {

        this.career = career;

    }

    @Override
    public void displayInformation() {

        super.displayInformation();
        System.out.println("Career: " + career);

    }

}