CREATE TABLE menus (
        id SERIAL NOT NULL,
        title VARCHAR(128) NOT NULL,
        description VARCHAR(128) NOT NULL,
        PRIMARY KEY (id),
        UNIQUE (title)
);

CREATE TABLE submenus (
        id SERIAL NOT NULL,
        title VARCHAR(128) NOT NULL,
        description VARCHAR(128) NOT NULL,
        menu_id INTEGER NOT NULL,
        PRIMARY KEY (id),
        UNIQUE (title),
        FOREIGN KEY(menu_id) REFERENCES menus (id)
);

CREATE TABLE dishes (
        id SERIAL NOT NULL,
        title VARCHAR(128) NOT NULL,
        description VARCHAR(128) NOT NULL,
        price FLOAT(4) NOT NULL,
        submenu_id INTEGER NOT NULL,
        PRIMARY KEY (id),
        UNIQUE (title),
        FOREIGN KEY(submenu_id) REFERENCES submenus (id) ON DELETE CASCADE
);

