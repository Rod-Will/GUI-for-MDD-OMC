# OMC & MDD Prediction Application

![Presentation2](https://github.com/user-attachments/assets/697712cf-c358-474a-8b00-f948ae57230b)


## Overview
This application predicts the Optimum Moisture Content (OMC) and Maximum Dry Density (MDD) for soil compaction based on the soil's physical properties such as Gravel, Sand, Silt, Liquid Limit, Plastic Limit, and Compaction Energy. The models used for prediction are pre-trained Gradient Boosting models.

The application also calculates the Clay content and Plasticity Index dynamically based on the input values for Gravel, Sand, and Silt percentages, and displays the results for OMC and MDD.

## Features
- Input fields for Gravel, Sand, Silt, Liquid Limit, Plastic Limit, and Compaction Energy.
- Dynamic calculation of Clay percentage and Plasticity Index.
- Prediction of OMC and MDD based on pre-trained Gradient Boosting models.
- Option to copy all inputs and results to the clipboard for easy sharing or saving.
- User-friendly interface with error handling for invalid inputs.

## Requirements
- Python 3.x
- Tkinter (for the GUI)
- Pillow (for image handling)
- NumPy (for numerical operations)
- Scikit-learn (for model prediction)
- joblib (for model loading)

To install the required libraries, use the following:

```bash
pip install tkinter pillow numpy scikit-learn joblib
```

## Usage
1. **Enter the soil properties:**
   - Gravel, Sand, and Silt percentages.
   - Liquid Limit, Plastic Limit, and Compaction Energy values.

2. **The application will automatically calculate:**
   - Clay percentage.
   - Plasticity Index.

3. **Click "Predict OMC & MDD" to see the results for:**
   - Predicted Optimum Moisture Content (OMC).
   - Predicted Maximum Dry Density (MDD).

4. **Click "Copy All" to copy all the entered values and results to the clipboard for easy sharing.**

## License
This project is licensed under the Creative Commons Zero v1.0 License.

## Acknowledgements
- The pre-trained Gradient Boosting models were developed and trained for soil compaction prediction.
- Thanks to [scikit-learn](https://scikit-learn.org/stable/) and [Tkinter](https://wiki.python.org/moin/TkInter) for providing the necessary tools and libraries for this project.

## Contact
For questions or suggestions, please contact:
- **Developed and Designed by:** Rod Will
- **Email:** [rhudwill@gmail.com]

## References
- Soil Mechanics and Foundations (for understanding the theoretical background of soil compaction).
- Gradient Boosting Model for Predictive Analytics (for insights into using Gradient Boosting for prediction).

## How to Contribute
Contributions to improve this application are welcome! Feel free to fork this repository, create a branch, and submit a pull request with your suggestions or improvements.

## Screenshots
![GUI](https://github.com/user-attachments/assets/4888cdf7-d7a9-4974-a437-9c396fb502f3)
```
