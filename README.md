# What is ML-CCD
ML-CCD is a software based on the Random Forest Machine Learning (ML) Model to predict the Concrete Cover Delamination (CCD) premature failure of FRP strengthened RC beams. The model is trained using a database compiled from 70 beams that were tested experimentally and failed in CCD. The database is provided in the project folder and named as (database.xls). The second sheet of the excel file (database.xls) is provided for the user as an alternative method of data entry, the software will give the user the option to either enter the parameters for the tested beam manually or read from the second sheet in the excel file. 
***
# How to use ML-CCD
To run the software. Please follow the following instructions:
1. create an empty folder to at your local machine to host the code.
2. Using visual studio, clone this project to your local machine.
3. create a virtual environment in the created folder that hosts the code on your local machine.
4. Using python 3.11 download the requirements provided in text file (requirements.txt). 
**NOTE: VISUAL STUDIO USUALLY DETECTS THE "requirements.txt" FILE AND GIVES THE OPTION TO CREATE A VIRTUAL ENVIRONMENT AND DOWNLOAD THE REQUIREMENTS.**
5. Run the software and follow the following steps:
 1. Click start to load the database and start the software.
 b. Import the database.xls provided in the project.
 c. Move to the "Unstrengthened Capacity" tab and hit the "Find Unstrengthened Capacity" button to analyze all beams without the presence of the FRP material. This function is used to find the critical strengthening ratio (M_strengthened/M_unstrengthened). 
 d. Conduct failure analysis through the "Failure Analysis" tab, this tab finds the strain profiles of all beams exist in the database and check compliance with basic RC mechanics. 
 e. Obtain the trilinear response of the beams. This function refines the ML model results based on mechanics formulations for the beams that will be subject to prediction. 
 f. The ML-Training tab is where the model is trained, and the required input is provided. the user may visualize the error in the predictions after the model is trained. The user may vary the error percentage and an error bar is plotted to show the accuracy of the prediction for that error percentage. 
 g. Hit the "Run Predictions" button to explore the parameters used in the ML model then move to the "Calibration" tab to calibrate the correlation function that obtains the "Strengthened Capacity" through the strengthening ratio. The user can do this by changing the slope and intercept of the linear curve to exclude the noisy points that do not comply with mechanics of RC beams. 
 h. Fill in the parameters of the beam to be tested, an alternative approach is to fill in the beam information using the second sheet of the database.xls file.
 i. After calibration is achieved and the beam parameters are input, run the results using the "Run Results"

  ***
# Additional Notes
## Expanding the database
The user has the ability to enlarge the database by adding additional rows to the database, however, the model is equipped to with functions that will filter out any additional data points that do not comply with the fundamentals of RC beam mechanics.
## Supported units
PLEASE NOTE THAT THIS SOFTWARE USES SI SYSTEM OF UNITS. 

