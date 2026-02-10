# DailyExpensesManager
A CLI-based app to help users manage expenses based on their monthly salary.
Users can add their monthly salary and create simulation how they should spend it

## Features
1. Simulation Menu
    - Show daily expenses simulation
    - Show daily expenses

2. Salary Management
    - Show current salary simulation
    - Change current salary simulation
    - Add new salary
    - Edit salary
    - Delete salary

3. Expenses Management
    - Show monthly expenses
    - Update all monthly expense
    - Add new monthly expense
    - Edit monthly expense
    - Delete monthly expense

## Requirements
- Python 3.10+
- Libraries listed in 'requirements.txt'

## Installation
1. Clone the repository: `git clone https://github.com/Rifki-NQ/DailyExpensesManager`
2. Navigate into the project directory: `cd DailyExpensesManager`
3. Install dependencies: `pip install -r requirements.txt`

## Usage
```bash
python main.py
```

## Planned Features
- Edit or delete daily expense

## TODO
- use data from `data/daily_expenses.yaml` for daily expenses simulation features
- create documentation or help menu for each feature
- use `data/daily_expenses.yaml` as placeholder for feature show daily expenses simulation
- select which expenses from `data/monthly_expenses.yaml` will be used for daily expenses simulation and save the configuration in `data/config.yaml`
- find out why adding out of range index to the paremeter of method get_keys_by_index from expenses_logic sometime does not return error