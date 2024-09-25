<<<<<<< HEAD
@echo off

echo Checking if "Processed data.json" already exists...
IF EXIST "Processed data.json" (
    echo "Processed data.json" already exists. Skipping the DataProcessor script.
) ELSE (
    echo "Processed data.json" not found. Running the DataProcessor script...
    python DataProcessor.py
    echo DataProcessor script finished.
)

echo Checking if "Processed data.json" exists after the DataProcessor script...
IF EXIST "Processed data.json" (
    echo "Processed data.json" found. Running the Dashboard script...
    python Dashboard.py
    echo Dashboard script finished.
    
    echo Launching the dashboard using Streamlit...
    streamlit run Dashboard.py
) ELSE (
    echo "Processed data.json" not found. Skipping the Dashboard script.
    pause
)

pause
=======
@echo off

echo Checking if "Processed data.json" already exists...
IF EXIST "Processed data.json" (
    echo "Processed data.json" already exists. Skipping the DataProcessor script.
) ELSE (
    echo "Processed data.json" not found. Running the DataProcessor script...
    python DataProcessor.py
    echo DataProcessor script finished.
)

echo Checking if "Processed data.json" exists after the DataProcessor script...
IF EXIST "Processed data.json" (
    echo "Processed data.json" found. Running the Dashboard script...
    python Dashboard.py
    echo Dashboard script finished.
    
    echo Launching the dashboard using Streamlit...
    streamlit run Dashboard.py
) ELSE (
    echo "Processed data.json" not found. Skipping the Dashboard script.
    pause
)

pause
>>>>>>> 222f1dee3f04cf95e7eb12c66294b2f7efee6525
