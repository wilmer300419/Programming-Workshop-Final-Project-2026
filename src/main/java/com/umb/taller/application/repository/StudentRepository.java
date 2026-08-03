package com.umb.taller.application.repository;

import java.util.ArrayList;
import java.util.List;

import com.umb.taller.domain.Student;

/**
 * Repositorio en memoria para gestionar los estudiantes del sistema.
 */
public class StudentRepository implements Repository<Student>{

    private final List<Student> students;

    public StudentRepository(){

        students = new ArrayList<>();

    }

    @Override
    public void save(Student student){

        students.add(student);

    }

    @Override
    public List<Student> findAll(){

        return students;

    }

    public Student findById(String id){

        for(Student student : students){

            if(student.getId().equals(id)){

                return student;

            }

        }

        return null;

    }

}