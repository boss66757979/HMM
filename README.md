#HMM Weather Predict
**Usage:**
-
**1. Install the software:**
-
![Image text](img_set/install.png)<br>
-
**2. Click the lnk file to open main window:**
-
![Image text](img_set/ico.png)<br>
-
**3. Copy training data into train window, like this:**
-
![Image text](img_set/copydatas.png)<br>
-
**4. Click Train button to training model, try different training epoch to find best acc**
-
![Image text](img_set/epoch-50-train.png)![Image text](img_set/epoch-60-train.png)<br>
-
**5. Choose a weather like Rain, then press Predict Button, then:**
-
![Image text](img_set/Predict.png)<br>
-
**The Future weather comes out ^_^**
---
Code Structure:
---
**1. Model Segment:**<br>
hmm_model.py: main HMM functions, like Baum-Welch alg, Forward & Backword alg, Viterbi alg<br>
main_model.py: source text operate and build data model, utility tools, other math functions, move all functions in hmm_model into the Class HMM<br>
**2. Data Plot Segment:**<br>
data_plot.py: display the data in dataset, like this:
![Image text](img_set/plot_data_overview.png)<br>
**3. Spyder Segment:**<br>
data_spyder.py: Crawl some test data from China Meteorological Administration, not a essential part<br>
**4. UI Segment:**<br>
newUI.py: all QT UI structure and functions<br>
mainwindow.py: entrance for UI and QT<br>
---
File & Dir Structure:
---
img_set: dir for train & test & readme images <br>
qtUI: UI design file dir <br>
dataset: weather train & test dataset <br>
*.py: python3 file <br>
*.exe: windows install file <br>
---