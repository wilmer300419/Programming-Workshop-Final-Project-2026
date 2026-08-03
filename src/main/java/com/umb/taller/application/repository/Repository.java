package com.umb.taller.application.repository;

import java.util.List;

/**
 * Contrato base para los repositorios del sistema.
 * Define las operaciones mínimas de persistencia compartidas por los distintos tipos de entidad.
 */
public interface Repository<T> {

    void save(T entity);

    List<T> findAll();

}