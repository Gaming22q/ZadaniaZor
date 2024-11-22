-- Создание базы данных
CREATE DATABASE UserTesting;

-- Использование базы данных
USE UserTesting;

-- Таблица пользователей
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,  -- Уникальный идентификатор пользователя
    email VARCHAR(255) NOT NULL UNIQUE,      -- Электронная почта пользователя (должна быть уникальной)
    password VARCHAR(255) NOT NULL            -- Пароль пользователя (хранить в зашифрованном виде)
);

-- Таблица тестов
CREATE TABLE Tests (
    test_id INT AUTO_INCREMENT PRIMARY KEY,   -- Уникальный идентификатор теста
    title VARCHAR(255) NOT NULL,              -- Название теста
    description TEXT,                          -- Описание теста
    created_by INT,                           -- Идентификатор администратора, который создал тест
    FOREIGN KEY (created_by) REFERENCES Users(user_id)  -- Связь с таблицей пользователей
);

-- Таблица результатов тестов
CREATE TABLE Results (
    result_id INT AUTO_INCREMENT PRIMARY KEY,  -- Уникальный идентификатор результата теста
    user_id INT,                               -- Идентификатор пользователя, который прошел тест
    test_id INT,                               -- Идентификатор теста
    score FLOAT,                               -- Результат теста
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,  -- Дата и время завершения теста
    FOREIGN KEY (user_id) REFERENCES Users(user_id),  -- Связь с таблицей пользователей
    FOREIGN KEY (test_id) REFERENCES Tests(test_id)   -- Связь с таблицей тестов
);

-- Таблица для совместного использования результатов
CREATE TABLE SharedResults (
    shared_id INT AUTO_INCREMENT PRIMARY KEY,  -- Уникальный идентификатор записи о совместном использовании
    result_id INT,                              -- Идентификатор результата, который был поделён
    shared_with_user_id INT,                   -- Идентификатор пользователя, с которым был поделён результат
    FOREIGN KEY (result_id) REFERENCES Results(result_id),  -- Связь с таблицей результатов
    FOREIGN KEY (shared_with_user_id) REFERENCES Users(user_id)  -- Связь с таблицей пользователей
);
