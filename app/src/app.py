# app.py
import logging
import os

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for
from models import Base, Expense
from sqlalchemy import MetaData, Table, create_engine, func
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# Global engine and logger instances
engine = None
logger = None

def init_env() -> dict:
    # Load environment variables from .env file
    load_dotenv()
    # Get values from environment variables
    logger_name: str = os.getenv('LOGGER_NAME', 'split_expense')  # Default logger name if not found in .env
    debug_mode: str = os.getenv('LOG_LEVEL_DEBUG', 'False').lower() == 'true'  # Convert string to bool
    configuration: dict = {
        'logger_name': logger_name,
        'debug_mode': debug_mode
    }
    return configuration

def init_logger(configuration: dict) -> logging.Logger:
    global logger
    # Set up logger
    logger = logging.getLogger(configuration['logger_name'])
    # Create console handler
    console_handler = logging.StreamHandler()
    # Create formatter and add it to the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(fmt=formatter)
    # Add the handler to the logger
    logger.addHandler(console_handler)
    # Configure logging based on Flask debug mode
    if configuration['debug_mode']:
        logger.setLevel(logging.DEBUG)  # Enable debug logs when Flask is in debug mode
        console_handler.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)  # Otherwise, only log info and above
        console_handler.setLevel(logging.INFO)
    logger.propagate = True
    logger.info(f"Logger initialized successfully at level {logger.getEffectiveLevel()}! Debug mode: {configuration['debug_mode']}")
    return logger

# Database setup function
def init_db(database_uri: str = 'sqlite:///expenses.db'):
    global engine
    try:
        logger.info(f"Initializing database '{database_uri}'")
        engine = create_engine(database_uri)
        Base.metadata.create_all(engine)
        logger.info(f"Database '{database_uri}' initialized successfully!")
    except Exception as expt:
        # Log the exception with traceback
        if hasattr(expt, 'message'):
            error_message = f"Exception occurred during database initialization: {expt.message}"
        else:
            error_message = f"Exception occurred during database initialization: {expt}"
        logger.exception(error_message)
        return error_message, 500

# Refactored execute_query function
# def insert_object( birthday: str or datetime = None) -> None:
def insert_expense(expense:Expense) -> None:
    try:
        logger.debug(f"Opening DB session...")
        Session = sessionmaker(bind=engine)
        session = Session()
        session.add(expense)
        session.commit()
        logger.debug(f"Added new expense to the database!")
        session.close()
        logger.debug(f"Closed DB session!")
    except Exception as expt:
        # Log the exception with traceback
        if hasattr(expt, 'message'):
            error_message = f"Exception occurred during query execution: {expt.message}"
        else:
            error_message = f"Exception occurred during query execution: {expt}"
        logger.exception(error_message)

# Refactored execute_query function
def get_all_ojbects(table:str, limit:int=0) -> list:
    try:
        logger.debug(f"Opening DB session...")
        Session = sessionmaker(bind=engine)
        session = Session()
        metadata = MetaData()
        selected_table = Table(table, metadata, autoload_with=engine)
        if(limit > 0):
            logger.debug(f"Executing query: get all from {selected_table.name} limit {limit}")
            elements = session.query(selected_table).limit(limit).all()
        else:
            logger.debug(f"Executing query: get all from {selected_table.name}")
            elements = session.query(selected_table).all()
        logger.debug(f"Obtained '{len(elements)}' elements successfully!")
        session.close()
        logger.debug(f"Closed DB session!")
        return elements
    except Exception as expt:
        # Log the exception with traceback
        if hasattr(expt, 'message'):
            error_message = f"Exception occurred during query execution: {expt.message}"
        else:
            error_message = f"Exception occurred during query execution: {expt}"
        logger.exception(error_message)
        return []

# Refactored execute_query function
def get_all_expenses_grouped_by_player(table:str) -> list:
    try:
        logger.debug(f"Opening DB session...")
        Session = sessionmaker(bind=engine)
        session = Session()
        metadata = MetaData()
        selected_table = Table(table, metadata, autoload_with=engine)
        result = session.query( selected_table.c.payer, selected_table.c.split_with, func.sum(selected_table.c.amount).label('total_amount') ).group_by(selected_table.c.payer).all()
        logger.debug(f"Obtained '{len(result)}' elements successfully!")
        session.close()
        logger.debug(f"Closed DB session!")
        return result
    except Exception as expt:
        # Log the exception with traceback
        if hasattr(expt, 'message'):
            error_message = f"Exception occurred during query execution: {expt.message}"
        else:
            error_message = f"Exception occurred during query execution: {expt}"
        logger.exception(error_message)
        return []


# Home route
@app.route('/')
def index():
    expenses = get_all_ojbects(Expense.__tablename__)
    column_amount = 2
    total_expense = sum([amount_import[column_amount] for amount_import in expenses])
    return render_template('index.html', expenses=expenses, total=round(total_expense, 2))

# Add new expense
@app.route(rule='/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        description = request.form['description']
        amount = request.form['amount']
        payer = request.form['payer']
        split_with = request.form['split_with']
        new_expense = Expense(description=description, amount=amount, payer=payer, split_with=split_with)
        logger.debug(f"Adding new expense: {new_expense}")
        insert_expense(new_expense)
        return redirect(url_for('index'))
    
    return render_template('add_expense.html')

# Split logic route
@app.route('/split')
def split_expense():
    expenses = get_all_expenses_grouped_by_player(Expense.__tablename__)
    split_data = {}
    for expense in expenses:
        payer, split_with, total_amount = expense
        if payer not in split_data:
            split_data[payer] = 0
        split_data[payer] += total_amount / len(split_with.split(','))
    return render_template('view_expenses.html', split_data=split_data)

configuration: dict = init_env()  # Initialize the environment variables when the app starts
logger = init_logger(configuration)  # Initialize the logger when the app starts
if __name__ == '__main__':
    init_db()  # Initialize the database when the app starts
    app.run(debug=configuration['debug_mode'])  # Run the app in debug mode based on the environment variable
