INSERT INTO users (username, role, token) VALUES
    ('tyler', 'user',  'tyler-token'),
    ('truong', 'user',  'truong-token'),
    ('admin', 'admin', 'admin-token');

INSERT INTO orders (owner_id, item, amount) VALUES
    (1, 'GPU',           1200),
    (1, 'Mouse',           25),
    (2, 'Monitor',        300),
    (2, 'Keyboard',        80);

INSERT INTO documents (owner_id, title, content) VALUES
    (1, 'Tyler Notes',  'tyler private data'),
    (2, 'Truong Notes',  'truong private data'),
    (3, 'Admin Report', 'admin-only data');