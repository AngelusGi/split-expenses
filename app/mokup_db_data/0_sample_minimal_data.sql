INSERT INTO Users (name, email, phone_number) VALUES ('John Doe', 'john@example.com', '123-456-7890');
INSERT INTO Groups (group_name) VALUES ('Vacation Trip');
INSERT INTO GroupMembers (group_id, user_id) VALUES (1, 1);
INSERT INTO Expenses (group_id, amount, description, date) VALUES (1, 100.00, 'Hotel Booking', '2024-10-01');
INSERT INTO ExpenseShares (expense_id, user_id, amount) VALUES (1, 1, 100.00);
