CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone_number TEXT
);

CREATE TABLE Groups (
    group_id INTEGER PRIMARY KEY,
    group_name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE GroupMembers (
    group_member_id INTEGER PRIMARY KEY,
    group_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (group_id) REFERENCES Groups(group_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Expenses (
    expense_id INTEGER PRIMARY KEY,
    group_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    description TEXT,
    date DATE NOT NULL,
    FOREIGN KEY (group_id) REFERENCES Groups(group_id)
);

CREATE TABLE ExpenseShares (
    expense_share_id INTEGER PRIMARY KEY,
    expense_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    FOREIGN KEY (expense_id) REFERENCES Expenses(expense_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);
