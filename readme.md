# Task Pipeline Project

This project simulates a task pipeline with multiple stages, where tasks are processed through different stages with specific headcounts, lead times, and QA rates. The progress is saved to an Excel file.

## Features

- Simulate task processing through multiple stages.
- Calculate remaining time and total time taken.
- Save daily progress to an Excel file.

## Requirements

- Python 3.x
- `openpyxl` library

## Installation

1. Extract the project:

    ```sh
    Extract the project to your working directory.
    ```
2. Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the main script:

    ```sh
    python3 main.py
    ```

2. Follow the prompts to input the number of stages, details for each stage, and the initial number of tasks for the first stage.

3. The script will simulate the task pipeline and print the daily progress to the terminal.

4. Once all tasks are completed, the total time taken and total work time will be displayed, and the progress will be saved to an Excel file named `project_progress.xlsx`.

## Example

```sh
Enter the number of stages: 3
Enter the name for stage 1: L0
Enter the headcount for stage 1: 40
Enter the lead time (minutes per task) for stage 1: 30
Enter the QA rate for stage 1 (default is 1.0): 0.8
Enter the name for stage 2: L1
Enter the headcount for stage 2: 10
Enter the lead time (minutes per task) for stage 2: 45
Enter the QA rate for stage 2 (default is 1.0): 1.0
Enter the name for stage 3: L2
Enter the headcount for stage 3: 5
Enter the lead time (minutes per task) for stage 3: 60
Enter the QA rate for stage 3 (default is 1.0): 1.0
Enter the initial number of tasks for the first stage: 100
```

## Testing
the tests folder is only for testing purposes, feel free to take a look at it and use it as well. As it remains, the final production ready code is in the src directory and is the one used in the final build.


## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing
Contributions are welcome! Please contact me if you want to add or improve existing features in the code

## Contact
For any questions or inquiries, please contact mohamedifqir99@gmail.com

