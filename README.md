# DailyExpensesManager
A CLI-based app to help users manage expenses based on their monthly salary.
Users can add their monthly salary and create simulation how they should spend it

## Features
1. Salary DATA
    - Show current salary simulation
    - Change current salary simulation
    - Add new salary
    - Edit salary
    - Delete salary

2. Expenses DATA
    - Show monthly expenses
    - Set monthly expenses
    - Edit monthly expenses

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

## Planned Feature
- Show daily expenses simulation
- Add new expenses category and value
- Edit or delete expenses category and value

## TODO
- add priority level for each monthly expenses value
- create documentation or help menu for each feature
- use `data/daily_expenses.yaml` as placeholder for feature show daily expenses simulation
- select which expenses from `data/monthly_expenses.yaml` will be used for daily expenses simulation and save the configuration in `data/config.yaml`