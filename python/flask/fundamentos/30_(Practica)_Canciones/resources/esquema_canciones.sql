CREATE DATABASE IF NOT EXISTS esquema_canciones;

USE esquema_canciones;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(45) NOT NULL,
    email VARCHAR(45) NOT NULL,
    contrasena VARCHAR(45) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE canciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(45) NOT NULL,
    artista VARCHAR(45) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE favoritos (
    usuario_id INT NOT NULL,
    cancion_id INT NOT NULL,

    PRIMARY KEY (usuario_id, cancion_id),

    CONSTRAINT fk_favoritos_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_favoritos_cancion
        FOREIGN KEY (cancion_id)
        REFERENCES canciones(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
