This project is a Naive Bayes classification system designed to work with categorical data. 
It includes a full pipeline starting from loading data from various sources such as CSV files, APIs, and MySQL databases, 
followed by thorough data cleaning to handle missing and inconsistent values. 
The cleaned data is then used to train a Naive Bayes model with Laplace smoothing to handle unseen categories.

The system supports prediction on new input data by calculating class probabilities using log computations for numerical stability. 
It also provides tools to evaluate model accuracy on the entire dataset as well as on train-test splits, ensuring reliable performance measurement.

User interaction is currently supported through a command-line interface that guides the user to input feature values and displays prediction 
results both numerically and visually via bar and pie charts. A graphical user interface using Streamlit is planned to offer a more user-friendly experience.

The codebase follows modular design principles, separating data loading, cleaning, modeling, prediction, evaluation, 
and user interface logic into distinct components. This structure facilitates maintenance, testing, and future enhancements.

Security best practices are followed by externalizing sensitive configuration such as database credentials into separate configuration files 
excluded from version control. Overall, the project demonstrates a solid foundation for building and experimenting with Naive Bayes classifiers in real-world scenarios.
