package com.umb.taller.domain;

public class Librarian extends Person {

    private String employeeCode;

    public Librarian(String id, String fullName, String employeeCode) {

        super(id, fullName);
        this.employeeCode = employeeCode;

    }

    public String getEmployeeCode() {

        return employeeCode;

    }

    @Override
    public void displayInformation() {

        super.displayInformation();
        System.out.println("Employee Code: " + employeeCode);

    }

}